"""
CodeGen: traduce la NetworkIR a un script Python ejecutable con Mininet.

Mapeo de tipos:
  router → net.addHost()  +  sysctl ip_forward=1
  switch → net.addSwitch()
  host   → net.addHost()

Para conexiones TCLink:
  bw_kbps  → bw en Mbps (TCLink espera Mbps como float)
  lat_us   → delay como cadena, ej. '2000us'
"""

from IRGenerator import NetworkIR


def _mask_a_cidr(mask: str) -> int:
    """Convierte una máscara de red (p.ej. '255.255.255.0') a prefijo CIDR."""
    partes = list(map(int, mask.split('.')))
    bits = sum(bin(p).count('1') for p in partes)
    return bits


def _kbps_a_mbps(kbps: int) -> float:
    return kbps / 1_000


def _us_a_str(us: int) -> str:
    if us % 1_000 == 0:
        return f'{us // 1_000}ms'
    return f'{us}us'


class CodeGen:
    def __init__(self, ir: NetworkIR):
        self.ir = ir
        self._tipo = {d['name']: d['tipo'] for d in ir.devices}

        # Map (device, declared_iface_name) → Mininet ethN index.
        # Mininet numbers interfaces in the order addLink() is called, so we
        # replicate that order here to get the correct ethN for each declared
        # interface name.
        self._mininet_eth: dict[tuple, int] = {}
        dev_eth_count: dict[str, int] = {}
        for conn in ir.connections:
            for dev, iface in [(conn['src_dev'], conn['src_iface']),
                               (conn['dst_dev'], conn['dst_iface'])]:
                if (dev, iface) not in self._mininet_eth:
                    n = dev_eth_count.get(dev, 0)
                    self._mininet_eth[(dev, iface)] = n
                    dev_eth_count[dev] = n + 1

        # IP/mask for the interface that will be eth0 (first connection) per device.
        self._eth0_ip:   dict[str, str] = {}
        self._eth0_mask: dict[str, str] = {}
        for iface in ir.interfaces:
            dev, ifn = iface['device'], iface['iface']
            if self._mininet_eth.get((dev, ifn)) == 0:
                self._eth0_ip[dev]   = iface['ip']
                self._eth0_mask[dev] = iface['mask']

    def generar(self) -> str:
        ir = self.ir
        lines = []
        a = lines.append

        a('#!/usr/bin/env python3')
        a(f'"""')
        a(f'Topologia Mininet generada por NetLang CodeGen')
        a(f'Red: {ir.name}')
        a(f'"""')
        a('from mininet.net import Mininet')
        a('from mininet.node import Host, OVSSwitch, Controller')
        a('from mininet.link import TCLink')
        a('from mininet.log import setLogLevel, info')
        a('from mininet.cli import CLI')
        a('')

        a(f'def crear_topologia_{ir.name}():')
        a(f'    net = Mininet(controller=Controller, link=TCLink, switch=OVSSwitch)')
        a('')

        # Dispositivos
        a('    info("*** Agregando dispositivos\\n")')
        routers = []
        for d in ir.devices:
            nombre = d['name']
            tipo = d['tipo']
            if tipo == 1:  # switch — failMode standalone: aprende MACs sin controlador
                a(f'    {nombre} = net.addSwitch("{nombre}", failMode="standalone")')
            else:          # router o host
                # Use the IP that belongs to eth0 (first connection in addLink order)
                ip = self._eth0_ip.get(nombre)
                if ip:
                    mask = self._eth0_mask.get(nombre, '255.255.255.0')
                    cidr = _mask_a_cidr(mask)
                    a(f'    {nombre} = net.addHost("{nombre}", ip="{ip}/{cidr}")')
                else:
                    a(f'    {nombre} = net.addHost("{nombre}")')
                if tipo == 0:
                    routers.append(nombre)
        a('')

        # Conexiones
        a('    info("*** Agregando enlaces\\n")')
        for conn in ir.connections:
            sd, dd = conn['src_dev'], conn['dst_dev']
            bw = conn['bw_kbps']
            lat = conn['lat_us']
            if bw > 0 and lat > 0:
                bw_mbps = _kbps_a_mbps(bw)
                delay_str = _us_a_str(lat)
                a(f'    net.addLink({sd}, {dd}, bw={bw_mbps:.3f}, delay="{delay_str}")')
            elif bw > 0:
                bw_mbps = _kbps_a_mbps(bw)
                a(f'    net.addLink({sd}, {dd}, bw={bw_mbps:.3f})')
            elif lat > 0:
                delay_str = _us_a_str(lat)
                a(f'    net.addLink({sd}, {dd}, delay="{delay_str}")')
            else:
                a(f'    net.addLink({sd}, {dd})')
        a('')

        # Arranque
        a('    info("*** Iniciando red\\n")')
        a('    net.start()')
        a('')

        # Configurar interfaces adicionales (eth1, eth2, …) con la IP correcta.
        # eth0 ya quedó configurado en addHost(); solo procesamos ethN con N > 0.
        ifaces_adicionales = [
            iface for iface in ir.interfaces
            if self._mininet_eth.get((iface['device'], iface['iface']), 0) > 0
        ]
        if ifaces_adicionales:
            a('    info("*** Configurando interfaces\\n")')
            for iface in ifaces_adicionales:
                dev, ifn = iface['device'], iface['iface']
                ip, mask = iface['ip'], iface['mask']
                cidr = _mask_a_cidr(mask)
                eth_n = self._mininet_eth[(dev, ifn)]
                a(f'    {dev}.cmd("ip addr add {ip}/{cidr} dev {dev}-eth{eth_n}")')
            a('')

        if routers:
            a('    info("*** Habilitando IP forwarding en routers\\n")')
            for r in routers:
                a(f'    {r}.cmd("sysctl -w net.ipv4.ip_forward=1")')
            a('')

        # Rutas por defecto para hosts que no son routers.
        # Para cada host, busca un router directamente conectado y lo usa como gateway.
        self._agregar_rutas(ir, routers, a)

        a('    info("*** Ejecutando CLI\\n")')
        a('    CLI(net)')
        a('')
        a('    info("*** Deteniendo red\\n")')
        a('    net.stop()')
        a('')

        a('')
        a('if __name__ == "__main__":')
        a('    setLogLevel("info")')
        a(f'    crear_topologia_{ir.name}()')

        return '\n'.join(lines)

    def _agregar_rutas(self, ir: NetworkIR, routers: list, a) -> None:
        """Genera rutas ip route add default via <gw> para hosts no-router."""
        router_set = set(routers)

        # Build adjacency: for each (device, iface) find the peer device and its IP.
        # We need the IP of the router's interface that faces this host/switch.
        iface_ip: dict[tuple, str] = {
            (iface['device'], iface['iface']): iface['ip']
            for iface in ir.interfaces
        }

        # For each non-router host, look for a directly connected router.
        # If connected via a switch, also check the switch's neighbours.
        host_devices = {d['name'] for d in ir.devices if d['tipo'] == 2}
        switch_devices = {d['name'] for d in ir.devices if d['tipo'] == 1}

        # Build neighbour map: device → [(peer_dev, peer_iface)]
        neighbours: dict[str, list] = {}
        for conn in ir.connections:
            sd, si = conn['src_dev'], conn['src_iface']
            dd, di = conn['dst_dev'], conn['dst_iface']
            neighbours.setdefault(sd, []).append((dd, di))
            neighbours.setdefault(dd, []).append((sd, si))

        def find_router_gateway(host: str) -> str | None:
            """Return the IP of the best router gateway for host, or None."""
            for peer, peer_iface in neighbours.get(host, []):
                if peer in router_set:
                    gw = iface_ip.get((peer, peer_iface))
                    if gw:
                        return gw
                # Host connected via a switch — one hop further
                if peer in switch_devices:
                    for peer2, peer2_iface in neighbours.get(peer, []):
                        if peer2 in router_set and peer2 != host:
                            gw = iface_ip.get((peer2, peer2_iface))
                            if gw:
                                return gw
            return None

        routes_added = False
        for dev_name in host_devices:
            gw = find_router_gateway(dev_name)
            if gw:
                if not routes_added:
                    a('    info("*** Configurando rutas\\n")')
                    routes_added = True
                a(f'    {dev_name}.cmd("ip route add default via {gw}")')
        if routes_added:
            a('')

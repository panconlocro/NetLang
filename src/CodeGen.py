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
        # Mapas auxiliares para acceso rápido
        self._tipo = {d['name']: d['tipo'] for d in ir.devices}
        # primera IP declarada por dispositivo → para addHost(ip=...)
        self._primera_ip: dict[str, str] = {}
        self._primera_mask: dict[str, str] = {}
        for iface in ir.interfaces:
            dev = iface['device']
            if dev not in self._primera_ip:
                self._primera_ip[dev] = iface['ip']
                self._primera_mask[dev] = iface['mask']

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
        a('from mininet.node import Host, OVSSwitch, OVSController')
        a('from mininet.link import TCLink')
        a('from mininet.log import setLogLevel, info')
        a('from mininet.cli import CLI')
        a('')

        a(f'def crear_topologia_{ir.name}():')
        a(f'    net = Mininet(controller=OVSController, link=TCLink, switch=OVSSwitch)')
        a('')

        # Dispositivos
        a('    info("*** Agregando dispositivos\\n")')
        routers = []
        for d in ir.devices:
            nombre = d['name']
            tipo = d['tipo']
            if tipo == 1:  # switch
                a(f'    {nombre} = net.addSwitch("{nombre}")')
            else:          # router o host
                ip = self._primera_ip.get(nombre)
                if ip:
                    mask = self._primera_mask.get(nombre, '255.255.255.0')
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

        # Interfaces adicionales e IP forwarding para routers
        if len(ir.interfaces) > 0:
            a('    info("*** Configurando interfaces\\n")')
            # Interfaces ya asignadas (primera de cada dispositivo va en addHost)
            ya_asignadas = set(self._primera_ip.keys())
            for iface in ir.interfaces:
                dev, ifn = iface['device'], iface['iface']
                ip, mask = iface['ip'], iface['mask']
                cidr = _mask_a_cidr(mask)
                # La primera interfaz ya fue configurada en addHost;
                # Las adicionales se configuran via comando
                clave = f"{dev}.{ifn}"
                if dev in ya_asignadas and ip == self._primera_ip[dev]:
                    continue  # ya configurada
                # nombre de interfaz en mininet: <dev>-eth<n>
                a(f'    {dev}.cmd("ip addr add {ip}/{cidr} dev {dev}-eth0")')
            a('')

        if routers:
            a('    info("*** Habilitando IP forwarding en routers\\n")')
            for r in routers:
                a(f'    {r}.cmd("sysctl -w net.ipv4.ip_forward=1")')
            a('')

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

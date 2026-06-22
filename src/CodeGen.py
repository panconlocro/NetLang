import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from grammar.NetLangVisitor import NetLangVisitor
from grammar.NetLangParser import NetLangParser

DEVICE_TIPOS = {'router': 0, 'switch': 1, 'host': 2}
BW_FACTOR    = {'Kbps': 1, 'Mbps': 1_000, 'Gbps': 1_000_000}
LAT_FACTOR   = {'ms': 1_000, 'us': 1}


def _mask_a_cidr(mask: str) -> int:
    partes = list(map(int, mask.split('.')))
    return sum(bin(p).count('1') for p in partes)


def _kbps_a_mbps(kbps: int) -> float:
    return kbps / 1_000


def _us_a_str(us: int) -> str:
    if us % 1_000 == 0:
        return f'{us // 1_000}ms'
    return f'{us}us'


class CodeGenVisitor(NetLangVisitor):
    """Visitor que recorre el AST y genera directamente un script Mininet."""

    def __init__(self):
        self._network_name = ''
        self._devices    = []   # [{'name': str, 'tipo': int}]
        self._interfaces = []   # [{'device', 'iface', 'ip', 'mask'}]
        self._connections = []  # [{'src_dev','src_iface','dst_dev','dst_iface','bw_kbps','lat_us'}]

    # ── Recolección de datos desde el AST ────────────────────────────

    def visitProgram(self, ctx):
        return self.visitChildren(ctx)

    def visitNetworkBlock(self, ctx):
        self._network_name = ctx.ID().getText()
        return self.visitChildren(ctx)

    def visitNetworkBody(self, ctx):
        return self.visitChildren(ctx)

    def visitStatement(self, ctx):
        return self.visitChildren(ctx)

    def visitDeviceDecl(self, ctx):
        nombre = ctx.ID().getText()
        tipo   = DEVICE_TIPOS[ctx.deviceType().getText()]
        self._devices.append({'name': nombre, 'tipo': tipo})
        return self.visitChildren(ctx)

    def visitSubnetDecl(self, ctx):
        return None  # no se necesita para generar Mininet

    def visitInterfaceDecl(self, ctx):
        self._interfaces.append({
            'device': ctx.ID(0).getText(),
            'iface':  ctx.ID(1).getText(),
            'ip':     self._ip_text(ctx.ipAddress(0)),
            'mask':   self._ip_text(ctx.ipAddress(1)),
        })
        return None

    def visitConnectDecl(self, ctx):
        refs = ctx.portRef()
        bw_kbps = 0
        lat_us  = 0
        if ctx.linkProps():
            for prop in ctx.linkProps().linkProp():
                valor = int(prop.INT().getText())
                if prop.speedUnit():
                    bw_kbps = valor * BW_FACTOR[prop.speedUnit().getText()]
                elif prop.timeUnit():
                    lat_us  = valor * LAT_FACTOR[prop.timeUnit().getText()]
        self._connections.append({
            'src_dev':   refs[0].ID(0).getText(),
            'src_iface': refs[0].ID(1).getText(),
            'dst_dev':   refs[1].ID(0).getText(),
            'dst_iface': refs[1].ID(1).getText(),
            'bw_kbps':   bw_kbps,
            'lat_us':    lat_us,
        })
        return None

    def visitDeviceBody(self, ctx):  return self.visitChildren(ctx)
    def visitDeviceProp(self, ctx):  return None
    def visitDeviceType(self, ctx):  return None
    def visitLinkProps(self, ctx):   return None
    def visitLinkProp(self, ctx):    return None
    def visitPortRef(self, ctx):     return None
    def visitSpeedUnit(self, ctx):   return None
    def visitTimeUnit(self, ctx):    return None
    def visitIpAddress(self, ctx):   return None

    # ── Emisión del script Mininet ────────────────────────────────────

    def generar(self) -> str:
        # Determinar índice ethN que Mininet asigna a cada (device, iface)
        # según el orden en que se llaman addLink()
        mininet_eth: dict[tuple, int] = {}
        dev_eth_count: dict[str, int] = {}
        for conn in self._connections:
            for dev, iface in [(conn['src_dev'], conn['src_iface']),
                               (conn['dst_dev'], conn['dst_iface'])]:
                if (dev, iface) not in mininet_eth:
                    n = dev_eth_count.get(dev, 0)
                    mininet_eth[(dev, iface)] = n
                    dev_eth_count[dev] = n + 1

        # IP de la interfaz que será eth0 (primera conexión) por dispositivo
        eth0_ip:   dict[str, str] = {}
        eth0_mask: dict[str, str] = {}
        for iface in self._interfaces:
            dev, ifn = iface['device'], iface['iface']
            if mininet_eth.get((dev, ifn)) == 0:
                eth0_ip[dev]   = iface['ip']
                eth0_mask[dev] = iface['mask']

        tipo_map   = {d['name']: d['tipo'] for d in self._devices}
        router_set = {d['name'] for d in self._devices if d['tipo'] == 0}
        switch_set = {d['name'] for d in self._devices if d['tipo'] == 1}
        host_set   = {d['name'] for d in self._devices if d['tipo'] == 2}

        lines = []
        a = lines.append

        a('#!/usr/bin/env python3')
        a(f'"""')
        a(f'Topologia Mininet generada por NetLang CodeGenVisitor')
        a(f'Red: {self._network_name}')
        a(f'"""')
        a('from mininet.net import Mininet')
        a('from mininet.node import Host, OVSSwitch, OVSController')
        a('from mininet.link import TCLink')
        a('from mininet.log import setLogLevel, info')
        a('from mininet.cli import CLI')
        a('')

        a(f'def crear_topologia_{self._network_name}():')
        a(f'    net = Mininet(controller=OVSController, link=TCLink, switch=OVSSwitch)')
        a('')

        a('    info("*** Agregando dispositivos\\n")')
        for d in self._devices:
            nombre, tipo = d['name'], d['tipo']
            if tipo == 1:  # switch
                a(f'    {nombre} = net.addSwitch("{nombre}")')
            else:
                ip = eth0_ip.get(nombre)
                if ip:
                    cidr = _mask_a_cidr(eth0_mask.get(nombre, '255.255.255.0'))
                    a(f'    {nombre} = net.addHost("{nombre}", ip="{ip}/{cidr}")')
                else:
                    a(f'    {nombre} = net.addHost("{nombre}")')
        a('')

        a('    info("*** Agregando enlaces\\n")')
        for conn in self._connections:
            sd, dd = conn['src_dev'], conn['dst_dev']
            bw, lat = conn['bw_kbps'], conn['lat_us']
            if bw > 0 and lat > 0:
                a(f'    net.addLink({sd}, {dd}, bw={_kbps_a_mbps(bw):.3f}, delay="{_us_a_str(lat)}")')
            elif bw > 0:
                a(f'    net.addLink({sd}, {dd}, bw={_kbps_a_mbps(bw):.3f})')
            elif lat > 0:
                a(f'    net.addLink({sd}, {dd}, delay="{_us_a_str(lat)}")')
            else:
                a(f'    net.addLink({sd}, {dd})')
        a('')

        a('    info("*** Iniciando red\\n")')
        a('    net.start()')
        a('')

        # Interfaces adicionales (eth1, eth2, …)
        ifaces_extra = [
            iface for iface in self._interfaces
            if mininet_eth.get((iface['device'], iface['iface']), 0) > 0
        ]
        if ifaces_extra:
            a('    info("*** Configurando interfaces\\n")')
            for iface in ifaces_extra:
                dev, ifn = iface['device'], iface['iface']
                cidr  = _mask_a_cidr(iface['mask'])
                eth_n = mininet_eth[(dev, ifn)]
                a(f'    {dev}.cmd("ip addr add {iface["ip"]}/{cidr} dev {dev}-eth{eth_n}")')
            a('')

        if router_set:
            a('    info("*** Habilitando IP forwarding en routers\\n")')
            for r in router_set:
                a(f'    {r}.cmd("sysctl -w net.ipv4.ip_forward=1")')
            a('')

        self._agregar_rutas(router_set, switch_set, host_set,
                            mininet_eth, a)

        a('    info("*** Ejecutando CLI\\n")')
        a('    CLI(net)')
        a('')
        a('    info("*** Deteniendo red\\n")')
        a('    net.stop()')
        a('')
        a('')
        a('if __name__ == "__main__":')
        a('    setLogLevel("info")')
        a(f'    crear_topologia_{self._network_name}()')

        return '\n'.join(lines)

    def _agregar_rutas(self, router_set, switch_set, host_set,
                       mininet_eth, a) -> None:
        iface_ip: dict[tuple, str] = {
            (iface['device'], iface['iface']): iface['ip']
            for iface in self._interfaces
        }

        neighbours: dict[str, list] = {}
        for conn in self._connections:
            sd, si = conn['src_dev'], conn['src_iface']
            dd, di = conn['dst_dev'], conn['dst_iface']
            neighbours.setdefault(sd, []).append((dd, di))
            neighbours.setdefault(dd, []).append((sd, si))

        def find_gateway(host: str) -> str | None:
            for peer, peer_iface in neighbours.get(host, []):
                if peer in router_set:
                    return iface_ip.get((peer, peer_iface))
                if peer in switch_set:
                    for peer2, peer2_iface in neighbours.get(peer, []):
                        if peer2 in router_set and peer2 != host:
                            return iface_ip.get((peer2, peer2_iface))
            return None

        routes_added = False
        for dev in host_set:
            gw = find_gateway(dev)
            if gw:
                if not routes_added:
                    a('    info("*** Configurando rutas\\n")')
                    routes_added = True
                a(f'    {dev}.cmd("ip route add default via {gw}")')
        if routes_added:
            a('')

    @staticmethod
    def _ip_text(ctx) -> str:
        return '.'.join(t.getText() for t in ctx.INT())

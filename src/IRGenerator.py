import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from grammar.NetLangVisitor import NetLangVisitor
from grammar.NetLangParser import NetLangParser


DEVICE_TIPOS = {'router': 0, 'switch': 1, 'host': 2}

BW_FACTOR = {'Kbps': 1, 'Mbps': 1_000, 'Gbps': 1_000_000}
LAT_FACTOR = {'ms': 1_000, 'us': 1}


class NetworkIR:
    """Representación intermedia de dominio para una red NetLang."""

    def __init__(self, name):
        self.name        = name
        self.devices     = []   # [{'name': str, 'tipo': int}]
        self.subnets     = []   # [{'name': str, 'address': str, 'prefix': int}]
        self.interfaces  = []   # [{'device', 'iface', 'ip', 'mask'}]
        self.connections = []   # [{'src_dev','src_iface','dst_dev','dst_iface','bw_kbps','lat_us'}]

    def __repr__(self):
        return (f"NetworkIR({self.name!r}, "
                f"{len(self.devices)}d, {len(self.subnets)}s, "
                f"{len(self.interfaces)}i, {len(self.connections)}c)")


class IRGenerator(NetLangVisitor):
    """Visitor que recorre el AST y construye una NetworkIR."""

    def __init__(self):
        self.ir = None

    def visitProgram(self, ctx):
        return self.visitChildren(ctx)

    def visitNetworkBlock(self, ctx):
        self.ir = NetworkIR(ctx.ID().getText())
        self.visitChildren(ctx)
        return self.ir

    def visitNetworkBody(self, ctx):
        return self.visitChildren(ctx)

    def visitStatement(self, ctx):
        return self.visitChildren(ctx)

    def visitDeviceDecl(self, ctx):
        self.ir.devices.append({
            'name': ctx.ID().getText(),
            'tipo': DEVICE_TIPOS[ctx.deviceType().getText()],
        })
        return self.visitChildren(ctx)

    def visitSubnetDecl(self, ctx):
        self.ir.subnets.append({
            'name':    ctx.ID().getText(),
            'address': self._ip_text(ctx.ipAddress()),
            'prefix':  int(ctx.INT().getText()),
        })
        return None

    def visitInterfaceDecl(self, ctx):
        self.ir.interfaces.append({
            'device': ctx.ID(0).getText(),
            'iface':  ctx.ID(1).getText(),
            'ip':     self._ip_text(ctx.ipAddress(0)),
            'mask':   self._ip_text(ctx.ipAddress(1)),
        })
        return None

    def visitConnectDecl(self, ctx):
        refs    = ctx.portRef()
        bw_kbps = 0
        lat_us  = 0
        if ctx.linkProps():
            for prop in ctx.linkProps().linkProp():
                valor = int(prop.INT().getText())
                if prop.speedUnit():
                    bw_kbps = valor * BW_FACTOR[prop.speedUnit().getText()]
                elif prop.timeUnit():
                    lat_us  = valor * LAT_FACTOR[prop.timeUnit().getText()]
        self.ir.connections.append({
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

    @staticmethod
    def _ip_text(ctx) -> str:
        return '.'.join(t.getText() for t in ctx.INT())

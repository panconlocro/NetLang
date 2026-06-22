import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from grammar.NetLangVisitor import NetLangVisitor
from grammar.NetLangParser import NetLangParser


DEVICE_TIPOS = {'router': 0, 'switch': 1, 'host': 2}

BW_FACTOR = {'Kbps': 1, 'Mbps': 1_000, 'Gbps': 1_000_000}
LAT_FACTOR = {'ms': 1_000, 'us': 1}


class NetworkIR:
    """Representación intermedia de la red antes de emitir LLVM IR."""

    def __init__(self, name):
        self.name = name
        self.devices = []      # [{'name': str, 'tipo': int}]
        self.subnets = []      # [{'name': str, 'address': str, 'prefix': int}]
        self.interfaces = []   # [{'device': str, 'iface': str, 'ip': str, 'mask': str}]
        self.connections = []  # [{'src_dev', 'src_iface', 'dst_dev', 'dst_iface', 'bw_kbps', 'lat_us'}]


class IRGenerator(NetLangVisitor):
    """Recorre el AST y produce una NetworkIR + texto LLVM IR."""

    def __init__(self):
        self.ir = None

    # ──────────────────────────────────────────────────────────────
    # Visitors
    # ──────────────────────────────────────────────────────────────

    def visitProgram(self, ctx):
        return self.visitChildren(ctx)

    def visitNetworkBlock(self, ctx):
        nombre = ctx.ID().getText()
        self.ir = NetworkIR(nombre)
        self.visitChildren(ctx)
        return self.ir

    def visitNetworkBody(self, ctx):
        return self.visitChildren(ctx)

    def visitStatement(self, ctx):
        return self.visitChildren(ctx)

    def visitDeviceDecl(self, ctx):
        nombre = ctx.ID().getText()
        tipo_texto = ctx.deviceType().getText()
        self.ir.devices.append({
            'name': nombre,
            'tipo': DEVICE_TIPOS[tipo_texto],
        })
        return self.visitChildren(ctx)

    def visitSubnetDecl(self, ctx):
        nombre = ctx.ID().getText()
        ip = self._ip_text(ctx.ipAddress())
        prefix = int(ctx.INT().getText())
        self.ir.subnets.append({'name': nombre, 'address': ip, 'prefix': prefix})
        return None  # no seguir visitando hijos (ipAddress ya procesada)

    def visitInterfaceDecl(self, ctx):
        device = ctx.ID(0).getText()
        iface = ctx.ID(1).getText()
        ip = self._ip_text(ctx.ipAddress(0))
        mask = self._ip_text(ctx.ipAddress(1))
        self.ir.interfaces.append({
            'device': device,
            'iface': iface,
            'ip': ip,
            'mask': mask,
        })
        return None

    def visitConnectDecl(self, ctx):
        refs = ctx.portRef()
        src_dev = refs[0].ID(0).getText()
        src_iface = refs[0].ID(1).getText()
        dst_dev = refs[1].ID(0).getText()
        dst_iface = refs[1].ID(1).getText()

        bw_kbps = 0
        lat_us = 0

        if ctx.linkProps():
            for prop in ctx.linkProps().linkProp():
                valor = int(prop.INT().getText())
                if prop.speedUnit():
                    unidad = prop.speedUnit().getText()
                    bw_kbps = valor * BW_FACTOR[unidad]
                elif prop.timeUnit():
                    unidad = prop.timeUnit().getText()
                    lat_us = valor * LAT_FACTOR[unidad]

        self.ir.connections.append({
            'src_dev': src_dev,
            'src_iface': src_iface,
            'dst_dev': dst_dev,
            'dst_iface': dst_iface,
            'bw_kbps': bw_kbps,
            'lat_us': lat_us,
        })
        return None

    # Nodos hoja — no hacer nada
    def visitDeviceBody(self, ctx):   return self.visitChildren(ctx)
    def visitDeviceProp(self, ctx):   return None
    def visitDeviceType(self, ctx):   return None
    def visitLinkProps(self, ctx):    return None
    def visitLinkProp(self, ctx):     return None
    def visitPortRef(self, ctx):      return None
    def visitSpeedUnit(self, ctx):    return None
    def visitTimeUnit(self, ctx):     return None
    def visitIpAddress(self, ctx):    return None

    # ──────────────────────────────────────────────────────────────
    # Emisión de LLVM IR
    # ──────────────────────────────────────────────────────────────

    def emit_llvm_ir(self) -> str:
        ir = self.ir

        # ── Pasada 1: recolectar TODOS los strings necesarios ─────────
        strings: dict[str, str] = {}  # tag → valor

        def reg(tag, value):
            if tag not in strings:
                strings[tag] = value

        reg('network', ir.name)
        for d in ir.devices:
            reg(d['name'], d['name'])
        for s in ir.subnets:
            reg(s['name'], s['name'])
            reg(f"addr.{s['name']}", f"{s['address']}/{s['prefix']}")
        for iface in ir.interfaces:
            reg(f"iface.{iface['device']}.{iface['iface']}", iface['iface'])
            reg(f"ip.{iface['device']}.{iface['iface']}", iface['ip'])
            reg(f"mask.{iface['device']}.{iface['iface']}", iface['mask'])
        for conn in ir.connections:
            for dev, iface in [(conn['src_dev'], conn['src_iface']),
                               (conn['dst_dev'], conn['dst_iface'])]:
                reg(f'iface.{dev}.{iface}', iface)

        def n(tag):
            return len(strings[tag]) + 1

        def ref(tag):
            size = n(tag)
            return f'getelementptr inbounds ([{size} x i8], [{size} x i8]* @str.{tag}, i32 0, i32 0)'

        # ── Pasada 2: emitir IR ────────────────────────────────────────
        lines = []
        a = lines.append

        a('; ============================================================')
        a(f'; NetLang Intermediate Representation')
        a(f'; Red: {ir.name}')
        a('; Generado automaticamente por NetLang IRGenerator')
        a('; ============================================================')
        a('')

        a('; tipo: 0=router  1=switch  2=host')
        a('%device_t    = type { i8*, i32 }')
        a('%subnet_t    = type { i8*, i8*, i32 }')
        a('%interface_t = type { i8*, i8*, i8*, i8* }')
        a('; bw_kbps: i32  lat_us: i32  (0 = sin restriccion)')
        a('%connect_t   = type { i8*, i8*, i8*, i8*, i32, i32 }')
        a('')

        a('; ── Constantes de cadena ────────────────────────────────────')
        for tag, value in strings.items():
            size = len(value) + 1
            a(f'@str.{tag} = private unnamed_addr constant [{size} x i8] c"{value}\\00", align 1')
        a('')

        a('; ── Dispositivos ─────────────────────────────────────────────')
        for i, d in enumerate(ir.devices):
            a(f'@device.{i} = global %device_t {{ i8* {ref(d["name"])}, i32 {d["tipo"]} }}')
        a(f'@device_count = global i32 {len(ir.devices)}')
        a('')

        a('; ── Subredes ─────────────────────────────────────────────────')
        for i, s in enumerate(ir.subnets):
            tag_addr = f"addr.{s['name']}"
            a(f'@subnet.{i} = global %subnet_t {{ i8* {ref(s["name"])}, i8* {ref(tag_addr)}, i32 {s["prefix"]} }}')
        a(f'@subnet_count = global i32 {len(ir.subnets)}')
        a('')

        a('; ── Interfaces ───────────────────────────────────────────────')
        for i, iface in enumerate(ir.interfaces):
            dev, ifn = iface['device'], iface['iface']
            tag_if   = f'iface.{dev}.{ifn}'
            tag_ip   = f'ip.{dev}.{ifn}'
            tag_mask = f'mask.{dev}.{ifn}'
            a(f'@interface.{i} = global %interface_t {{ i8* {ref(dev)}, i8* {ref(tag_if)}, i8* {ref(tag_ip)}, i8* {ref(tag_mask)} }}')
        a(f'@interface_count = global i32 {len(ir.interfaces)}')
        a('')

        a('; ── Conexiones ───────────────────────────────────────────────')
        for i, conn in enumerate(ir.connections):
            sd, si = conn['src_dev'], conn['src_iface']
            dd, di = conn['dst_dev'], conn['dst_iface']
            tag_si = f'iface.{sd}.{si}'
            tag_di = f'iface.{dd}.{di}'
            a(f'@connect.{i} = global %connect_t {{ i8* {ref(sd)}, i8* {ref(tag_si)}, i8* {ref(dd)}, i8* {ref(tag_di)}, i32 {conn["bw_kbps"]}, i32 {conn["lat_us"]} }}')
        a(f'@connect_count = global i32 {len(ir.connections)}')
        a('')

        a('; ── Punto de entrada ─────────────────────────────────────────')
        a('define i32 @main() {')
        a('entry:')
        a(f'  ; Red: {ir.name} — {len(ir.devices)} dispositivo(s), {len(ir.subnets)} subred(es),')
        a(f'  ;                  {len(ir.interfaces)} interfaz(ces), {len(ir.connections)} conexion(es)')
        a('  ret i32 0')
        a('}')

        return '\n'.join(lines)

    # ──────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def _ip_text(ctx) -> str:
        nums = [t.getText() for t in ctx.INT()]
        return '.'.join(nums)

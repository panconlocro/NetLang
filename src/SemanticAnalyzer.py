from grammar.NetLangVisitor import NetLangVisitor
from grammar.NetLangParser import NetLangParser

class SemanticAnalyzer(NetLangVisitor):

    def __init__(self):
        self.devices = {}       # nombre -> tipo
        self.subnets = set()    # nombres de subredes declaradas
        self.interfaces = set() # "dispositivo.interfaz"
        self.ips = {}           # "ip" -> interfaz que la usa
        self.errors = []

    def visitNetworkBlock(self, ctx):
        return self.visitChildren(ctx)

    def visitNetworkBody(self, ctx):
        return self.visitChildren(ctx)

    def visitStatement(self, ctx):
        return self.visitChildren(ctx)

    # Registra dispositivos declarados
    def visitDeviceDecl(self, ctx):
        name = ctx.ID().getText()
        tipo = ctx.deviceType().getText()
        if name in self.devices:
            self.errors.append(f"Error semantico: dispositivo '{name}' declarado mas de una vez")
        else:
            self.devices[name] = tipo
        return self.visitChildren(ctx)

    # Valida propiedades del dispositivo
    def visitDeviceProp(self, ctx):
        if ctx.SUBNET():
            subnet_name = ctx.ID().getText()
            if subnet_name not in self.subnets:
                self.errors.append(f"Error semantico: subred '{subnet_name}' referenciada pero no declarada")
        return self.visitChildren(ctx)

    # Registra subredes declaradas
    def visitSubnetDecl(self, ctx):
        name = ctx.ID().getText()
        if name in self.subnets:
            self.errors.append(f"Error semantico: subred '{name}' declarada mas de una vez")
        else:
            self.subnets.add(name)
        return self.visitChildren(ctx)

    # Valida interfaces
    def visitInterfaceDecl(self, ctx):
        device = ctx.ID(0).getText()
        iface = ctx.ID(1).getText()
        key = f"{device}.{iface}"

        # Dispositivo existe?
        if device not in self.devices:
            self.errors.append(f"Error semantico: dispositivo '{device}' no declarado en interfaz '{key}'")

        # Interfaz repetida?
        if key in self.interfaces:
            self.errors.append(f"Error semantico: interfaz '{key}' declarada mas de una vez")
        else:
            self.interfaces.add(key)

        # IP duplicada?
        ip = ctx.ipAddress(0).getText()
        if ip in self.ips:
            self.errors.append(f"Error semantico: IP '{ip}' ya esta en uso en '{self.ips[ip]}'")
        else:
            self.ips[ip] = key

        return self.visitChildren(ctx)

    # Valida conexiones
    def visitConnectDecl(self, ctx):
        refs = ctx.portRef()
        for ref in refs:
            device = ref.ID(0).getText()
            iface = ref.ID(1).getText()
            key = f"{device}.{iface}"
            if device not in self.devices:
                self.errors.append(f"Error semantico: dispositivo '{device}' no declarado en conexion '{key}'")
        return self.visitChildren(ctx)
# Generated from NetLang.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .NetLangParser import NetLangParser
else:
    from NetLangParser import NetLangParser

class NetLangVisitor(ParseTreeVisitor):
    def visitProgram(self, ctx:NetLangParser.ProgramContext): return self.visitChildren(ctx)
    def visitNetworkBlock(self, ctx:NetLangParser.NetworkBlockContext): return self.visitChildren(ctx)
    def visitNetworkBody(self, ctx:NetLangParser.NetworkBodyContext): return self.visitChildren(ctx)
    def visitStatement(self, ctx:NetLangParser.StatementContext): return self.visitChildren(ctx)
    def visitDeviceDecl(self, ctx:NetLangParser.DeviceDeclContext): return self.visitChildren(ctx)
    def visitDeviceBody(self, ctx:NetLangParser.DeviceBodyContext): return self.visitChildren(ctx)
    def visitDeviceProp(self, ctx:NetLangParser.DevicePropContext): return self.visitChildren(ctx)
    def visitDeviceType(self, ctx:NetLangParser.DeviceTypeContext): return self.visitChildren(ctx)
    def visitSubnetDecl(self, ctx:NetLangParser.SubnetDeclContext): return self.visitChildren(ctx)
    def visitInterfaceDecl(self, ctx:NetLangParser.InterfaceDeclContext): return self.visitChildren(ctx)
    def visitConnectDecl(self, ctx:NetLangParser.ConnectDeclContext): return self.visitChildren(ctx)
    def visitPortRef(self, ctx:NetLangParser.PortRefContext): return self.visitChildren(ctx)
    def visitLinkProps(self, ctx:NetLangParser.LinkPropsContext): return self.visitChildren(ctx)
    def visitLinkProp(self, ctx:NetLangParser.LinkPropContext): return self.visitChildren(ctx)
    def visitSpeedUnit(self, ctx:NetLangParser.SpeedUnitContext): return self.visitChildren(ctx)
    def visitTimeUnit(self, ctx:NetLangParser.TimeUnitContext): return self.visitChildren(ctx)
    def visitIpAddress(self, ctx:NetLangParser.IpAddressContext): return self.visitChildren(ctx)

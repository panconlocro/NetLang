# Generated from NetLang.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .NetLangParser import NetLangParser
else:
    from NetLangParser import NetLangParser

class NetLangListener(ParseTreeListener):
    def enterProgram(self, ctx:NetLangParser.ProgramContext): pass
    def exitProgram(self, ctx:NetLangParser.ProgramContext): pass
    def enterNetworkBlock(self, ctx:NetLangParser.NetworkBlockContext): pass
    def exitNetworkBlock(self, ctx:NetLangParser.NetworkBlockContext): pass
    def enterNetworkBody(self, ctx:NetLangParser.NetworkBodyContext): pass
    def exitNetworkBody(self, ctx:NetLangParser.NetworkBodyContext): pass
    def enterStatement(self, ctx:NetLangParser.StatementContext): pass
    def exitStatement(self, ctx:NetLangParser.StatementContext): pass
    def enterDeviceDecl(self, ctx:NetLangParser.DeviceDeclContext): pass
    def exitDeviceDecl(self, ctx:NetLangParser.DeviceDeclContext): pass
    def enterDeviceBody(self, ctx:NetLangParser.DeviceBodyContext): pass
    def exitDeviceBody(self, ctx:NetLangParser.DeviceBodyContext): pass
    def enterDeviceProp(self, ctx:NetLangParser.DevicePropContext): pass
    def exitDeviceProp(self, ctx:NetLangParser.DevicePropContext): pass
    def enterDeviceType(self, ctx:NetLangParser.DeviceTypeContext): pass
    def exitDeviceType(self, ctx:NetLangParser.DeviceTypeContext): pass
    def enterSubnetDecl(self, ctx:NetLangParser.SubnetDeclContext): pass
    def exitSubnetDecl(self, ctx:NetLangParser.SubnetDeclContext): pass
    def enterInterfaceDecl(self, ctx:NetLangParser.InterfaceDeclContext): pass
    def exitInterfaceDecl(self, ctx:NetLangParser.InterfaceDeclContext): pass
    def enterConnectDecl(self, ctx:NetLangParser.ConnectDeclContext): pass
    def exitConnectDecl(self, ctx:NetLangParser.ConnectDeclContext): pass
    def enterPortRef(self, ctx:NetLangParser.PortRefContext): pass
    def exitPortRef(self, ctx:NetLangParser.PortRefContext): pass
    def enterLinkProps(self, ctx:NetLangParser.LinkPropsContext): pass
    def exitLinkProps(self, ctx:NetLangParser.LinkPropsContext): pass
    def enterLinkProp(self, ctx:NetLangParser.LinkPropContext): pass
    def exitLinkProp(self, ctx:NetLangParser.LinkPropContext): pass
    def enterSpeedUnit(self, ctx:NetLangParser.SpeedUnitContext): pass
    def exitSpeedUnit(self, ctx:NetLangParser.SpeedUnitContext): pass
    def enterTimeUnit(self, ctx:NetLangParser.TimeUnitContext): pass
    def exitTimeUnit(self, ctx:NetLangParser.TimeUnitContext): pass
    def enterIpAddress(self, ctx:NetLangParser.IpAddressContext): pass
    def exitIpAddress(self, ctx:NetLangParser.IpAddressContext): pass

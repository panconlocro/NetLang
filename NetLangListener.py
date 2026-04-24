# Generated from NetLang.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .NetLangParser import NetLangParser
else:
    from NetLangParser import NetLangParser

# This class defines a complete listener for a parse tree produced by NetLangParser.
class NetLangListener(ParseTreeListener):

    # Enter a parse tree produced by NetLangParser#program.
    def enterProgram(self, ctx:NetLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by NetLangParser#program.
    def exitProgram(self, ctx:NetLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by NetLangParser#networkBlock.
    def enterNetworkBlock(self, ctx:NetLangParser.NetworkBlockContext):
        pass

    # Exit a parse tree produced by NetLangParser#networkBlock.
    def exitNetworkBlock(self, ctx:NetLangParser.NetworkBlockContext):
        pass


    # Enter a parse tree produced by NetLangParser#networkBody.
    def enterNetworkBody(self, ctx:NetLangParser.NetworkBodyContext):
        pass

    # Exit a parse tree produced by NetLangParser#networkBody.
    def exitNetworkBody(self, ctx:NetLangParser.NetworkBodyContext):
        pass


    # Enter a parse tree produced by NetLangParser#statement.
    def enterStatement(self, ctx:NetLangParser.StatementContext):
        pass

    # Exit a parse tree produced by NetLangParser#statement.
    def exitStatement(self, ctx:NetLangParser.StatementContext):
        pass


    # Enter a parse tree produced by NetLangParser#deviceDecl.
    def enterDeviceDecl(self, ctx:NetLangParser.DeviceDeclContext):
        pass

    # Exit a parse tree produced by NetLangParser#deviceDecl.
    def exitDeviceDecl(self, ctx:NetLangParser.DeviceDeclContext):
        pass


    # Enter a parse tree produced by NetLangParser#deviceBody.
    def enterDeviceBody(self, ctx:NetLangParser.DeviceBodyContext):
        pass

    # Exit a parse tree produced by NetLangParser#deviceBody.
    def exitDeviceBody(self, ctx:NetLangParser.DeviceBodyContext):
        pass


    # Enter a parse tree produced by NetLangParser#deviceProp.
    def enterDeviceProp(self, ctx:NetLangParser.DevicePropContext):
        pass

    # Exit a parse tree produced by NetLangParser#deviceProp.
    def exitDeviceProp(self, ctx:NetLangParser.DevicePropContext):
        pass


    # Enter a parse tree produced by NetLangParser#deviceType.
    def enterDeviceType(self, ctx:NetLangParser.DeviceTypeContext):
        pass

    # Exit a parse tree produced by NetLangParser#deviceType.
    def exitDeviceType(self, ctx:NetLangParser.DeviceTypeContext):
        pass


    # Enter a parse tree produced by NetLangParser#subnetDecl.
    def enterSubnetDecl(self, ctx:NetLangParser.SubnetDeclContext):
        pass

    # Exit a parse tree produced by NetLangParser#subnetDecl.
    def exitSubnetDecl(self, ctx:NetLangParser.SubnetDeclContext):
        pass


    # Enter a parse tree produced by NetLangParser#interfaceDecl.
    def enterInterfaceDecl(self, ctx:NetLangParser.InterfaceDeclContext):
        pass

    # Exit a parse tree produced by NetLangParser#interfaceDecl.
    def exitInterfaceDecl(self, ctx:NetLangParser.InterfaceDeclContext):
        pass


    # Enter a parse tree produced by NetLangParser#connectDecl.
    def enterConnectDecl(self, ctx:NetLangParser.ConnectDeclContext):
        pass

    # Exit a parse tree produced by NetLangParser#connectDecl.
    def exitConnectDecl(self, ctx:NetLangParser.ConnectDeclContext):
        pass


    # Enter a parse tree produced by NetLangParser#portRef.
    def enterPortRef(self, ctx:NetLangParser.PortRefContext):
        pass

    # Exit a parse tree produced by NetLangParser#portRef.
    def exitPortRef(self, ctx:NetLangParser.PortRefContext):
        pass


    # Enter a parse tree produced by NetLangParser#linkProps.
    def enterLinkProps(self, ctx:NetLangParser.LinkPropsContext):
        pass

    # Exit a parse tree produced by NetLangParser#linkProps.
    def exitLinkProps(self, ctx:NetLangParser.LinkPropsContext):
        pass


    # Enter a parse tree produced by NetLangParser#linkProp.
    def enterLinkProp(self, ctx:NetLangParser.LinkPropContext):
        pass

    # Exit a parse tree produced by NetLangParser#linkProp.
    def exitLinkProp(self, ctx:NetLangParser.LinkPropContext):
        pass


    # Enter a parse tree produced by NetLangParser#speedUnit.
    def enterSpeedUnit(self, ctx:NetLangParser.SpeedUnitContext):
        pass

    # Exit a parse tree produced by NetLangParser#speedUnit.
    def exitSpeedUnit(self, ctx:NetLangParser.SpeedUnitContext):
        pass


    # Enter a parse tree produced by NetLangParser#timeUnit.
    def enterTimeUnit(self, ctx:NetLangParser.TimeUnitContext):
        pass

    # Exit a parse tree produced by NetLangParser#timeUnit.
    def exitTimeUnit(self, ctx:NetLangParser.TimeUnitContext):
        pass


    # Enter a parse tree produced by NetLangParser#ipAddress.
    def enterIpAddress(self, ctx:NetLangParser.IpAddressContext):
        pass

    # Exit a parse tree produced by NetLangParser#ipAddress.
    def exitIpAddress(self, ctx:NetLangParser.IpAddressContext):
        pass



del NetLangParser
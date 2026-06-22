#!/usr/bin/env python3
"""
Topologia Mininet generada por NetLang CodeGen
Red: LabRed
"""
from mininet.net import Mininet
from mininet.node import Host, OVSSwitch, Controller
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI

def crear_topologia_LabRed():
    net = Mininet(controller=Controller, link=TCLink, switch=OVSSwitch)

    info("*** Agregando dispositivos\n")
    Router1 = net.addHost("Router1", ip="192.168.1.1/24")
    Switch1 = net.addSwitch("Switch1", failMode="standalone")
    Switch2 = net.addSwitch("Switch2", failMode="standalone")
    PC1 = net.addHost("PC1", ip="192.168.1.10/24")
    PC2 = net.addHost("PC2", ip="192.168.1.20/24")
    Server1 = net.addHost("Server1", ip="10.0.0.10/24")

    info("*** Agregando enlaces\n")
    net.addLink(Router1, Switch1, bw=1000.000, delay="1ms")
    net.addLink(PC1, Switch1, bw=100.000, delay="2ms")
    net.addLink(PC2, Switch1, bw=100.000, delay="2ms")
    net.addLink(Router1, Switch2, bw=1000.000, delay="1ms")
    net.addLink(Server1, Switch2, bw=100.000, delay="5ms")

    info("*** Iniciando red\n")
    net.start()

    info("*** Configurando interfaces\n")
    Router1.cmd("ip addr add 10.0.0.1/24 dev Router1-eth1")

    info("*** Habilitando IP forwarding en routers\n")
    Router1.cmd("sysctl -w net.ipv4.ip_forward=1")

    info("*** Configurando rutas\n")
    Server1.cmd("ip route add default via 10.0.0.1")
    PC2.cmd("ip route add default via 192.168.1.1")
    PC1.cmd("ip route add default via 192.168.1.1")

    info("*** Ejecutando CLI\n")
    CLI(net)

    info("*** Deteniendo red\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    crear_topologia_LabRed()
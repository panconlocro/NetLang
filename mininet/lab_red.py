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
    R1 = net.addHost("R1", ip="10.0.1.1/24")
    SW1 = net.addSwitch("SW1", failMode="standalone")
    PC1 = net.addHost("PC1", ip="10.0.1.10/24")
    PC2 = net.addHost("PC2", ip="10.0.1.20/24")

    info("*** Agregando enlaces\n")
    net.addLink(R1, SW1, bw=1000.000, delay="1ms")
    net.addLink(PC1, SW1, bw=100.000)
    net.addLink(PC2, SW1, bw=100.000)

    info("*** Iniciando red\n")
    net.start()

    info("*** Habilitando IP forwarding en routers\n")
    R1.cmd("sysctl -w net.ipv4.ip_forward=1")

    info("*** Configurando rutas\n")
    PC2.cmd("ip route add default via 10.0.1.1")
    PC1.cmd("ip route add default via 10.0.1.1")

    info("*** Ejecutando CLI\n")
    CLI(net)

    info("*** Deteniendo red\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    crear_topologia_LabRed()
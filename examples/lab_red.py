#!/usr/bin/env python3
"""
Topologia Mininet — Red: lab_red
  R1 (router)  —1000Mbps/1ms—  SW1  —100Mbps—  PC1
                                      —100Mbps—  PC2
Subredes:
  LAN: 192.168.1.0/24  →  R1 (.1), PC1 (.2), PC2 (.3)
"""
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI


def crear_topologia():
    net = Mininet(controller=Controller, link=TCLink, switch=OVSSwitch)

    info('*** Agregando dispositivos\n')
    R1  = net.addHost('R1',  ip='192.168.1.1/24')
    # failMode=standalone: el switch aprende MACs solo, sin depender del controlador
    SW1 = net.addSwitch('SW1', failMode='standalone')
    PC1 = net.addHost('PC1', ip='192.168.1.2/24')
    PC2 = net.addHost('PC2', ip='192.168.1.3/24')

    info('*** Agregando enlaces\n')
    # Orden de addLink determina ethN en cada dispositivo:
    #   R1-eth0  ↔  SW1-eth1   (1000 Mbps, 1 ms)
    #   PC1-eth0 ↔  SW1-eth2   (100 Mbps)
    #   PC2-eth0 ↔  SW1-eth3   (100 Mbps)
    net.addLink(R1,  SW1, bw=1000.000, delay='1ms')
    net.addLink(PC1, SW1, bw=100.000)
    net.addLink(PC2, SW1, bw=100.000)

    info('*** Iniciando red\n')
    net.start()

    info('*** Habilitando IP forwarding en R1\n')
    R1.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Ejecutando CLI\n')
    CLI(net)

    info('*** Deteniendo red\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    crear_topologia()

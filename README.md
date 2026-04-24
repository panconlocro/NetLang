# NetLang

NetLang es un lenguaje declarativo de dominio especifico (DSL) para el modelado
de topologias de redes de telecomunicaciones. Permite describir dispositivos,
subredes, interfaces y conexiones de forma simple, portable y verificable.

## Requisitos

- Python 3.10+
- Java (para correr ANTLR4)
- ANTLR4 jar en /usr/local/lib/antlr-4.13.1-complete.jar
- Runtime de ANTLR4 para Python:

    pip install antlr4-python3-runtime==4.13.1

## Estructura del proyecto

NetLang/
├── grammar/          # Gramatica ANTLR4 y archivos generados
│   └── NetLang.g4
├── examples/         # Ejemplos de programas en NetLang
│   ├── Ejemplo1.txt
│   └── EjemploError1.txt
├── src/
│   └── main.py       # Driver principal
└── Makefile

## Uso

1. Generar el parser a partir de la gramatica:
    make

2. Parsear un archivo:
    python3 src/main.py examples/Ejemplo1.txt

3. Limpiar archivos generados:
    make clean

## Ejemplo de programa valido

network EmpresaDemo {

    subnet LAN_Oficina 192.168.1.0/24
    subnet LAN_Servidores 10.0.0.0/24

    device Router1 router {
        gateway 192.168.1.1
    }

    device Switch1 switch

    device PC1 host {
        subnet LAN_Oficina
    }

    interface Router1 eth0 ip 192.168.1.1 mask 255.255.255.0
    interface PC1 eth0 ip 192.168.1.10 mask 255.255.255.0

    connect Router1.eth0 to Switch1.port1 bandwidth 100 Mbps latency 2 ms
    connect PC1.eth0 to Switch1.port2
}

## Integrantes

- Rosa Rodriguez
- Braulio Bartra
- David
- Luis
# NetLang

NetLang es un lenguaje declarativo de dominio específico (DSL) para el modelado de topologías de redes de telecomunicaciones. Permite describir dispositivos, subredes, interfaces y conexiones de forma simple, portable y verificable, separando la descripción lógica de la red de su implementación técnica.

## Pipeline del compilador

```
archivo.netlang
      │
      ▼
  Lexer / Parser (ANTLR4)
      │  error sintáctico → para aquí
      ▼
  Analizador Semántico
      │  error semántico → reporta y para
      ▼
  IRGenerator  →  archivo.ll  (LLVM IR)
      │
      ▼
  CodeGen  →  topologia.py  (script Mininet ejecutable)
```

## Estructura del proyecto

```
NetLang/
├── grammar/
│   ├── NetLang.g4            # Gramática ANTLR4
│   ├── NetLangLexer.py       # Lexer generado
│   ├── NetLangParser.py      # Parser generado
│   ├── NetLangListener.py    # Listener generado
│   └── NetLangVisitor.py     # Visitor generado
├── src/
│   ├── main.py               # Driver principal (pipeline completo)
│   ├── SemanticAnalyzer.py   # Analizador semántico (Visitor)
│   ├── IRGenerator.py        # Generador de LLVM IR
│   └── CodeGen.py            # Generador de script Mininet
├── examples/
│   ├── Ejemplo1.txt          # Topología válida de demostración
│   ├── Ejemplo1.ll           # LLVM IR generado del ejemplo anterior
│   ├── EjemploError1.txt     # Error sintáctico
│   ├── EjemploError2.txt
│   ├── EjemploError3.txt
│   ├── EjemploErrorSemantico1.txt  # IP duplicada
│   ├── EjemploErrorSemantico2.txt  # Dispositivo duplicado
│   ├── EjemploErrorSemantico3.txt  # Interfaz duplicada
│   ├── EjemploErrorSemantico4.txt  # Dispositivo no declarado en conexión
│   └── EjemploErrorSemantico5.txt  # Subred no declarada
└── Makefile
```

## Requisitos

```bash
pip install antlr4-python3-runtime==4.13.1
```

Para regenerar los archivos de la gramática (opcional, ya están incluidos):

```bash
# Requiere Java y el jar de ANTLR4
make
```

Para ejecutar el script Mininet generado se necesita Mininet instalado:

```bash
# Ubuntu / Debian
sudo apt-get install mininet
```

Para la interfaz grafica se necesita intalar tkinter en: 

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install python3-tk
```

## Ejecución

### Solo análisis léxico y semántico

```bash
python3 src/main.py examples/Ejemplo1.txt
```

Salida esperada:

```
✓ Analisis sintactico correcto.
✓ Analisis semantico correcto.
```

### Generar LLVM IR

```bash
python3 src/main.py examples/Ejemplo1.txt --ir
```

Genera `examples/Ejemplo1.ll` con la representación intermedia en formato LLVM IR. El archivo contiene tipos estructurales para cada elemento de la red y una función `@main` de entrada.

### Generar script Mininet

```bash
python3 src/main.py examples/Ejemplo1.txt --codegen topologia.py
```

### Pipeline completo (IR + script Mininet)

```bash
python3 src/main.py examples/Ejemplo1.txt --ir --codegen topologia.py
```

Salida esperada:

```
✓ Analisis sintactico correcto.
✓ Analisis semantico correcto.
✓ LLVM IR generado en: examples/Ejemplo1.ll
✓ Script Mininet generado en: topologia.py
```

### Probar con archivos de error

```bash
# Error sintáctico
python3 src/main.py examples/EjemploError1.txt

# Error semántico (IP duplicada)
python3 src/main.py examples/EjemploErrorSemantico1.txt
```

## Integración con Mininet

### Ejecutar la topología generada

Una vez generado el script, se ejecuta con privilegios de administrador (Mininet los requiere):

```bash
sudo python3 mininet/topologia.py
```

Esto levanta la red virtual y abre la CLI de Mininet:

```
*** Agregando dispositivos
*** Agregando enlaces
*** Iniciando red
*** Habilitando IP forwarding en routers
*** Ejecutando CLI
mininet>
```

### Comandos de demostración en la CLI de Mininet

Desde la CLI se puede verificar que la topología funciona correctamente:

```bash
# Ver todos los nodos
mininet> nodes

# Ver los enlaces
mininet> links

# Verificar conectividad entre todos los nodos
mininet> pingall

# Ping puntual entre dos nodos
mininet> Router1 ping -c 3 PC1

# Ver interfaces y direcciones IP de un nodo
mininet> Router1 ip addr

# Ejecutar un comando en un nodo específico
mininet> PC1 ip route

# Ver la tabla de forwarding del switch
mininet> sh ovs-vsctl show

# Salir
mininet> exit
```

### Demostración completa paso a paso

1. Escribir la topología en un archivo `.txt`:

```
network LabRed {

    subnet LAN_Oficina 192.168.1.0/24
    subnet LAN_Servidores 10.0.0.0/24

    device Router1 router

    device Switch1 switch
    device Switch2 switch

    device PC1 host {
        subnet LAN_Oficina
        gateway 192.168.1.1
    }

    device PC2 host {
        subnet LAN_Oficina
        gateway 192.168.1.1
    }

    device Server1 host {
        subnet LAN_Servidores
        gateway 10.0.0.1
    }

    // Interfaces del router, una por cada subred
    interface Router1 eth0 ip 192.168.1.1 mask 255.255.255.0
    interface Router1 eth1 ip 10.0.0.1 mask 255.255.255.0

    // Interfaces de los hosts
    interface PC1 eth0 ip 192.168.1.10 mask 255.255.255.0
    interface PC2 eth0 ip 192.168.1.20 mask 255.255.255.0
    interface Server1 eth0 ip 10.0.0.10 mask 255.255.255.0

    // Conexiones lado LAN_Oficina
    connect Router1.eth0 to Switch1.port1 bandwidth 1 Gbps latency 1 ms
    connect PC1.eth0 to Switch1.port2 bandwidth 100 Mbps latency 2 ms
    connect PC2.eth0 to Switch1.port3 bandwidth 100 Mbps latency 2 ms

    // Conexiones lado LAN_Servidores
    connect Router1.eth1 to Switch2.port1 bandwidth 1 Gbps latency 1 ms
    connect Server1.eth0 to Switch2.port2 bandwidth 100 Mbps latency 5 ms
}
```

2. Compilar y generar la topología:

```bash
python3 src/main.py examples/lab_red.txt --ir --codegen lab_red.py
```

3. Levantar la red en Mininet:

```bash
sudo python3 mininet/lab_red.py
```

4. Pruebas completas:

Conectividad Intra-sured

```
mininet> pingall
*** Ping: testing ping reachability
R1 -> PC1 PC2
PC1 -> R1 PC2
PC2 -> R1 PC1
*** Results: 0% dropped (6/6 received)
```
Cruza de una subred a otra via Router1

```
mininet> PC1 ping -c 5 Server1
```

Confirma las dos interfaces (eth0, eth1)

```
mininet> Router1 ip addr 
```
Confirmar que usa 192.168.1.1 como gateway

```
mininet> PC1 ip route
```

Verificación de propiedades de enlace (bandwidth/latency) a nivel del kernel

```
mininet> PC1 tc qdisc show dev PC1-eth0
```

5. Limpiar la red después de terminar:

```bash
sudo mn -c
```

## Lenguaje NetLang — referencia rápida

### Estructura general

```
network <NombreRed> {
    <declaraciones>
}
```

### Tipos de declaración

| Declaración | Sintaxis | Ejemplo |
|---|---|---|
| Subred | `subnet <nombre> <ip>/<prefijo>` | `subnet LAN 192.168.1.0/24` |
| Dispositivo | `device <nombre> <tipo> [{ ... }]` | `device R1 router` |
| Interfaz | `interface <disp> <iface> ip <ip> mask <mask>` | `interface R1 eth0 ip 192.168.1.1 mask 255.255.255.0` |
| Conexión | `connect <disp>.<iface> to <disp>.<iface> [props]` | `connect R1.eth0 to SW1.port1 bandwidth 100 Mbps latency 2 ms` |

### Tipos de dispositivo

| Tipo | Mapeo en Mininet |
|---|---|
| `router` | `addHost()` + `ip_forward=1` |
| `switch` | `addSwitch()` |
| `host` | `addHost()` |

### Propiedades de enlace

| Propiedad | Unidades | Ejemplo |
|---|---|---|
| `bandwidth` | `Kbps`, `Mbps`, `Gbps` | `bandwidth 1 Gbps` |
| `latency` | `ms`, `us` | `latency 5 ms` |

### Propiedades de dispositivo

```
device Router1 router {
    gateway 192.168.1.1    # IP del gateway
    subnet LAN_Oficina     # Subred a la que pertenece
}
```

### Validaciones semánticas

El analizador detecta y reporta:

- Dispositivo declarado más de una vez
- Subred declarada más de una vez
- Interfaz declarada más de una vez (`dispositivo.interfaz`)
- Dirección IP duplicada entre interfaces
- Dispositivo referenciado en `interface` o `connect` sin haber sido declarado
- Subred referenciada en `device { subnet ... }` sin haber sido declarada

## Integrantes

| Nombre | Código |
|---|---|
| Bartra Sandoval, Braulio Alonso | U202214069 |
| Rodriguez Valencia, Rosa Maria | U202212675 |
| Ballón Villar, Diego Eduardo | U201520327 |
| Flores Centeno, Luis Alberto | U20201a626 |

Curso: 1ACC0218 - Teoría de Compiladores · NRC 17829 · 2026-01

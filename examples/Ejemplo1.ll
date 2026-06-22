; ============================================================
; NetLang Intermediate Representation
; Red: EmpresaDemo
; Generado automaticamente por NetLang IRGenerator
; ============================================================

; tipo: 0=router  1=switch  2=host
%device_t    = type { i8*, i32 }
%subnet_t    = type { i8*, i8*, i32 }
%interface_t = type { i8*, i8*, i8*, i8* }
; bw_kbps: i32  lat_us: i32  (0 = sin restriccion)
%connect_t   = type { i8*, i8*, i8*, i8*, i32, i32 }

; ── Constantes de cadena ────────────────────────────────────
@str.network = private unnamed_addr constant [12 x i8] c"EmpresaDemo\00", align 1
@str.Router1 = private unnamed_addr constant [8 x i8] c"Router1\00", align 1
@str.Switch1 = private unnamed_addr constant [8 x i8] c"Switch1\00", align 1
@str.PC1 = private unnamed_addr constant [4 x i8] c"PC1\00", align 1
@str.LAN_Oficina = private unnamed_addr constant [12 x i8] c"LAN_Oficina\00", align 1
@str.addr.LAN_Oficina = private unnamed_addr constant [15 x i8] c"192.168.1.0/24\00", align 1
@str.LAN_Servidores = private unnamed_addr constant [15 x i8] c"LAN_Servidores\00", align 1
@str.addr.LAN_Servidores = private unnamed_addr constant [12 x i8] c"10.0.0.0/24\00", align 1
@str.iface.Router1.eth0 = private unnamed_addr constant [5 x i8] c"eth0\00", align 1
@str.ip.Router1.eth0 = private unnamed_addr constant [12 x i8] c"192.168.1.1\00", align 1
@str.mask.Router1.eth0 = private unnamed_addr constant [14 x i8] c"255.255.255.0\00", align 1
@str.iface.PC1.eth0 = private unnamed_addr constant [5 x i8] c"eth0\00", align 1
@str.ip.PC1.eth0 = private unnamed_addr constant [13 x i8] c"192.168.1.10\00", align 1
@str.mask.PC1.eth0 = private unnamed_addr constant [14 x i8] c"255.255.255.0\00", align 1
@str.iface.Switch1.port1 = private unnamed_addr constant [6 x i8] c"port1\00", align 1
@str.iface.Switch1.port2 = private unnamed_addr constant [6 x i8] c"port2\00", align 1

; ── Dispositivos ─────────────────────────────────────────────
@device.0 = global %device_t { i8* getelementptr inbounds ([8 x i8], [8 x i8]* @str.Router1, i32 0, i32 0), i32 0 }
@device.1 = global %device_t { i8* getelementptr inbounds ([8 x i8], [8 x i8]* @str.Switch1, i32 0, i32 0), i32 1 }
@device.2 = global %device_t { i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.PC1, i32 0, i32 0), i32 2 }
@device_count = global i32 3

; ── Subredes ─────────────────────────────────────────────────
@subnet.0 = global %subnet_t { i8* getelementptr inbounds ([12 x i8], [12 x i8]* @str.LAN_Oficina, i32 0, i32 0), i8* getelementptr inbounds ([15 x i8], [15 x i8]* @str.addr.LAN_Oficina, i32 0, i32 0), i32 24 }
@subnet.1 = global %subnet_t { i8* getelementptr inbounds ([15 x i8], [15 x i8]* @str.LAN_Servidores, i32 0, i32 0), i8* getelementptr inbounds ([12 x i8], [12 x i8]* @str.addr.LAN_Servidores, i32 0, i32 0), i32 24 }
@subnet_count = global i32 2

; ── Interfaces ───────────────────────────────────────────────
@interface.0 = global %interface_t { i8* getelementptr inbounds ([8 x i8], [8 x i8]* @str.Router1, i32 0, i32 0), i8* getelementptr inbounds ([5 x i8], [5 x i8]* @str.iface.Router1.eth0, i32 0, i32 0), i8* getelementptr inbounds ([12 x i8], [12 x i8]* @str.ip.Router1.eth0, i32 0, i32 0), i8* getelementptr inbounds ([14 x i8], [14 x i8]* @str.mask.Router1.eth0, i32 0, i32 0) }
@interface.1 = global %interface_t { i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.PC1, i32 0, i32 0), i8* getelementptr inbounds ([5 x i8], [5 x i8]* @str.iface.PC1.eth0, i32 0, i32 0), i8* getelementptr inbounds ([13 x i8], [13 x i8]* @str.ip.PC1.eth0, i32 0, i32 0), i8* getelementptr inbounds ([14 x i8], [14 x i8]* @str.mask.PC1.eth0, i32 0, i32 0) }
@interface_count = global i32 2

; ── Conexiones ───────────────────────────────────────────────
@connect.0 = global %connect_t { i8* getelementptr inbounds ([8 x i8], [8 x i8]* @str.Router1, i32 0, i32 0), i8* getelementptr inbounds ([5 x i8], [5 x i8]* @str.iface.Router1.eth0, i32 0, i32 0), i8* getelementptr inbounds ([8 x i8], [8 x i8]* @str.Switch1, i32 0, i32 0), i8* getelementptr inbounds ([6 x i8], [6 x i8]* @str.iface.Switch1.port1, i32 0, i32 0), i32 100000, i32 2000 }
@connect.1 = global %connect_t { i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.PC1, i32 0, i32 0), i8* getelementptr inbounds ([5 x i8], [5 x i8]* @str.iface.PC1.eth0, i32 0, i32 0), i8* getelementptr inbounds ([8 x i8], [8 x i8]* @str.Switch1, i32 0, i32 0), i8* getelementptr inbounds ([6 x i8], [6 x i8]* @str.iface.Switch1.port2, i32 0, i32 0), i32 0, i32 0 }
@connect_count = global i32 2

; ── Punto de entrada ─────────────────────────────────────────
define i32 @main() {
entry:
  ; Red: EmpresaDemo — 3 dispositivo(s), 2 subred(es),
  ;                  2 interfaz(ces), 2 conexion(es)
  ret i32 0
}
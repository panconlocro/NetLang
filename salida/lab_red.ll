; ============================================================
; NetLang Intermediate Representation
; Red: LabRed
; Generado automaticamente por NetLang IRGenerator
; ============================================================

; tipo: 0=router  1=switch  2=host
%device_t    = type { i8*, i32 }
%subnet_t    = type { i8*, i8*, i32 }
%interface_t = type { i8*, i8*, i8*, i8* }
; bw_kbps: i32  lat_us: i32  (0 = sin restriccion)
%connect_t   = type { i8*, i8*, i8*, i8*, i32, i32 }

; ── Constantes de cadena ────────────────────────────────────
@str.network = private unnamed_addr constant [7 x i8] c"LabRed\00", align 1
@str.R1 = private unnamed_addr constant [3 x i8] c"R1\00", align 1
@str.SW1 = private unnamed_addr constant [4 x i8] c"SW1\00", align 1
@str.PC1 = private unnamed_addr constant [4 x i8] c"PC1\00", align 1
@str.PC2 = private unnamed_addr constant [4 x i8] c"PC2\00", align 1
@str.LAN_Alumnos = private unnamed_addr constant [12 x i8] c"LAN_Alumnos\00", align 1
@str.addr.LAN_Alumnos = private unnamed_addr constant [12 x i8] c"10.0.1.0/24\00", align 1
@str.iface.R1.eth0 = private unnamed_addr constant [5 x i8] c"eth0\00", align 1
@str.ip.R1.eth0 = private unnamed_addr constant [9 x i8] c"10.0.1.1\00", align 1
@str.mask.R1.eth0 = private unnamed_addr constant [14 x i8] c"255.255.255.0\00", align 1
@str.iface.PC1.eth0 = private unnamed_addr constant [5 x i8] c"eth0\00", align 1
@str.ip.PC1.eth0 = private unnamed_addr constant [10 x i8] c"10.0.1.10\00", align 1
@str.mask.PC1.eth0 = private unnamed_addr constant [14 x i8] c"255.255.255.0\00", align 1
@str.iface.PC2.eth0 = private unnamed_addr constant [5 x i8] c"eth0\00", align 1
@str.ip.PC2.eth0 = private unnamed_addr constant [10 x i8] c"10.0.1.20\00", align 1
@str.mask.PC2.eth0 = private unnamed_addr constant [14 x i8] c"255.255.255.0\00", align 1
@str.iface.SW1.port1 = private unnamed_addr constant [6 x i8] c"port1\00", align 1
@str.iface.SW1.port2 = private unnamed_addr constant [6 x i8] c"port2\00", align 1
@str.iface.SW1.port3 = private unnamed_addr constant [6 x i8] c"port3\00", align 1

; ── Dispositivos ─────────────────────────────────────────────
@device.0 = global %device_t { i8* getelementptr inbounds ([3 x i8], [3 x i8]* @str.R1, i32 0, i32 0), i32 0 }
@device.1 = global %device_t { i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.SW1, i32 0, i32 0), i32 1 }
@device.2 = global %device_t { i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.PC1, i32 0, i32 0), i32 2 }
@device.3 = global %device_t { i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.PC2, i32 0, i32 0), i32 2 }
@device_count = global i32 4

; ── Subredes ─────────────────────────────────────────────────
@subnet.0 = global %subnet_t { i8* getelementptr inbounds ([12 x i8], [12 x i8]* @str.LAN_Alumnos, i32 0, i32 0), i8* getelementptr inbounds ([12 x i8], [12 x i8]* @str.addr.LAN_Alumnos, i32 0, i32 0), i32 24 }
@subnet_count = global i32 1

; ── Interfaces ───────────────────────────────────────────────
@interface.0 = global %interface_t { i8* getelementptr inbounds ([3 x i8], [3 x i8]* @str.R1, i32 0, i32 0), i8* getelementptr inbounds ([5 x i8], [5 x i8]* @str.iface.R1.eth0, i32 0, i32 0), i8* getelementptr inbounds ([9 x i8], [9 x i8]* @str.ip.R1.eth0, i32 0, i32 0), i8* getelementptr inbounds ([14 x i8], [14 x i8]* @str.mask.R1.eth0, i32 0, i32 0) }
@interface.1 = global %interface_t { i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.PC1, i32 0, i32 0), i8* getelementptr inbounds ([5 x i8], [5 x i8]* @str.iface.PC1.eth0, i32 0, i32 0), i8* getelementptr inbounds ([10 x i8], [10 x i8]* @str.ip.PC1.eth0, i32 0, i32 0), i8* getelementptr inbounds ([14 x i8], [14 x i8]* @str.mask.PC1.eth0, i32 0, i32 0) }
@interface.2 = global %interface_t { i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.PC2, i32 0, i32 0), i8* getelementptr inbounds ([5 x i8], [5 x i8]* @str.iface.PC2.eth0, i32 0, i32 0), i8* getelementptr inbounds ([10 x i8], [10 x i8]* @str.ip.PC2.eth0, i32 0, i32 0), i8* getelementptr inbounds ([14 x i8], [14 x i8]* @str.mask.PC2.eth0, i32 0, i32 0) }
@interface_count = global i32 3

; ── Conexiones ───────────────────────────────────────────────
@connect.0 = global %connect_t { i8* getelementptr inbounds ([3 x i8], [3 x i8]* @str.R1, i32 0, i32 0), i8* getelementptr inbounds ([5 x i8], [5 x i8]* @str.iface.R1.eth0, i32 0, i32 0), i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.SW1, i32 0, i32 0), i8* getelementptr inbounds ([6 x i8], [6 x i8]* @str.iface.SW1.port1, i32 0, i32 0), i32 1000000, i32 1000 }
@connect.1 = global %connect_t { i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.PC1, i32 0, i32 0), i8* getelementptr inbounds ([5 x i8], [5 x i8]* @str.iface.PC1.eth0, i32 0, i32 0), i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.SW1, i32 0, i32 0), i8* getelementptr inbounds ([6 x i8], [6 x i8]* @str.iface.SW1.port2, i32 0, i32 0), i32 100000, i32 0 }
@connect.2 = global %connect_t { i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.PC2, i32 0, i32 0), i8* getelementptr inbounds ([5 x i8], [5 x i8]* @str.iface.PC2.eth0, i32 0, i32 0), i8* getelementptr inbounds ([4 x i8], [4 x i8]* @str.SW1, i32 0, i32 0), i8* getelementptr inbounds ([6 x i8], [6 x i8]* @str.iface.SW1.port3, i32 0, i32 0), i32 100000, i32 0 }
@connect_count = global i32 3

; ── Punto de entrada ─────────────────────────────────────────
define i32 @main() {
entry:
  ; Red: LabRed — 4 dispositivo(s), 1 subred(es),
  ;                  3 interfaz(ces), 3 conexion(es)
  ret i32 0
}
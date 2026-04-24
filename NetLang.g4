// NetLang.g4
grammar NetLang;

// ─── PARSER RULES ───────────────────────────────────────────

program
    : networkBlock EOF
    ;

networkBlock
    : NETWORK ID LBRACE networkBody RBRACE
    ;

networkBody
    : statement*
    ;

statement
    : deviceDecl
    | subnetDecl
    | interfaceDecl
    | connectDecl
    ;

// device Router1 router { ... }
deviceDecl
    : DEVICE ID deviceType LBRACE deviceBody RBRACE
    | DEVICE ID deviceType
    ;

deviceBody
    : deviceProp*
    ;

deviceProp
    : SUBNET ID           // subnet LAN_Oficina
    | GATEWAY ipAddress   // gateway 192.168.1.1
    ;

deviceType
    : ROUTER
    | SWITCH
    | HOST
    ;

// subnet LAN_Oficina 192.168.1.0/24
subnetDecl
    : SUBNET ID ipAddress SLASH INT
    ;

// interface Router1 eth0 ip 192.168.1.1 mask 255.255.255.0
interfaceDecl
    : INTERFACE ID ID IP ipAddress MASK ipAddress
    ;

// connect Router1.eth0 to Switch1.port1 bandwidth 100 Mbps latency 2 ms
connectDecl
    : CONNECT portRef TO portRef linkProps?
    ;

portRef
    : ID DOT ID
    ;

linkProps
    : linkProp+
    ;

linkProp
    : BANDWIDTH INT speedUnit
    | LATENCY INT timeUnit
    ;

speedUnit
    : KBPS
    | MBPS
    | GBPS
    ;

timeUnit
    : MS
    | US
    ;

ipAddress
    : INT DOT INT DOT INT DOT INT
    ;


// ─── LEXER RULES ────────────────────────────────────────────

// Keywords
NETWORK     : 'network'     ;
DEVICE      : 'device'      ;
SUBNET      : 'subnet'      ;
INTERFACE   : 'interface'   ;
CONNECT     : 'connect'     ;
TO          : 'to'          ;
IP          : 'ip'          ;
MASK        : 'mask'        ;
GATEWAY     : 'gateway'     ;
BANDWIDTH   : 'bandwidth'   ;
LATENCY     : 'latency'     ;

// Device types
ROUTER      : 'router'      ;
SWITCH      : 'switch'      ;
HOST        : 'host'        ;

// Units
KBPS        : 'Kbps'        ;
MBPS        : 'Mbps'        ;
GBPS        : 'Gbps'        ;
MS          : 'ms'          ;
US          : 'us'          ;

// Symbols
LBRACE      : '{'           ;
RBRACE      : '}'           ;
DOT         : '.'           ;
SLASH       : '/'           ;

// Primitives
ID          : [a-zA-Z][a-zA-Z0-9_]* ;
INT         : [0-9]+                 ;

// Ignored
WS          : [ \t\r\n]+ -> skip    ;
COMMENT     : '//' ~[\r\n]* -> skip ;
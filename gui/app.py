#!/usr/bin/env python3
"""
NetLang Designer — Interfaz gráfica de escritorio.

Permite diseñar topologías de red visualmente y compilarlas con
el pipeline NetLang (léxico → sintáctico → semántico → LLVM IR → Mininet).
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import tempfile
import traceback

# ── Path setup ────────────────────────────────────────────────────────────
GUI_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(GUI_DIR)
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'src'))
sys.path.insert(0, os.path.join(ROOT_DIR, 'grammar'))

# ── Constantes visuales ───────────────────────────────────────────────────
C = {
    'router':   '#3A7BD5',
    'switch':   '#E8973A',
    'host':     '#4CAF7D',
    'bg':       '#F5F5F5',
    'grid':     '#E8E8E8',
    'sel':      '#FF5722',
    'line':     '#607D8B',
    'text':     '#212121',
    'text_dim': '#757575',
}

NODE_R   = 28   # radio del nodo circular
SW_W     = 56   # ancho del rectángulo de switch
SW_H     = 22   # alto del rectángulo de switch
GRID     = 40   # tamaño de celda del grid


# ═════════════════════════════════════════════════════════════════════════
# Modelos de datos
# ═════════════════════════════════════════════════════════════════════════

class DeviceModel:
    _seq = 0
    LABELS = {'router': 'Router', 'switch': 'Switch', 'host': 'Host'}
    ABBREV = {'router': 'RTR',    'switch': 'SW',     'host': 'PC'}

    def __init__(self, dtype: str, x: float, y: float):
        DeviceModel._seq += 1
        self.id    = DeviceModel._seq
        self.dtype = dtype
        self.x, self.y = x, y
        # Propiedades NetLang
        self.name       = f'{self.ABBREV[dtype]}{self.id}'
        self.ip         = ''
        self.mask       = '255.255.255.0'
        self.gateway    = ''
        self.subnet_ref = ''
        # Contador de interfaces (para asignar nombres automáticamente)
        self._iface_seq = 0

    def next_iface(self) -> str:
        if self.dtype == 'switch':
            self._iface_seq += 1
            return f'port{self._iface_seq}'
        name = f'eth{self._iface_seq}'
        self._iface_seq += 1
        return name

    @property
    def color(self) -> str:
        return C[self.dtype]


class ConnectionModel:
    _seq = 0

    def __init__(self, dev_a: DeviceModel, iface_a: str,
                 dev_b: DeviceModel, iface_b: str):
        ConnectionModel._seq += 1
        self.id      = ConnectionModel._seq
        self.dev_a   = dev_a
        self.iface_a = iface_a
        self.dev_b   = dev_b
        self.iface_b = iface_b
        self.bw      = 0
        self.bw_unit = 'Mbps'
        self.lat     = 0
        self.lat_unit= 'ms'
        # IDs de elementos en el canvas
        self.line_id  = None
        self.label_id = None


class SubnetModel:
    _seq = 0

    def __init__(self, name='', address='192.168.1.0', prefix=24):
        SubnetModel._seq += 1
        self.id      = SubnetModel._seq
        self.name    = name or f'Subnet{self.id}'
        self.address = address
        self.prefix  = prefix


# ═════════════════════════════════════════════════════════════════════════
# Diálogos
# ═════════════════════════════════════════════════════════════════════════

class _BaseDialog(tk.Toplevel):
    def _center(self, parent):
        self.update_idletasks()
        pw, ph = parent.winfo_width(), parent.winfo_height()
        px, py = parent.winfo_rootx(), parent.winfo_rooty()
        dw, dh = self.winfo_width(), self.winfo_height()
        self.geometry(f'+{px + (pw - dw)//2}+{py + (ph - dh)//2}')


class DeviceDialog(_BaseDialog):
    """Diálogo para crear / editar un dispositivo."""

    def __init__(self, parent, device: DeviceModel, subnets: list):
        super().__init__(parent)
        self.device  = device
        self.result  = False
        self.title(f'Configurar {DeviceModel.LABELS[device.dtype]}')
        self.resizable(False, False)
        self.grab_set()

        frm = ttk.Frame(self, padding=14)
        frm.pack(fill='both', expand=True)
        pad = dict(padx=6, pady=3)
        row = 0

        def field(label, var, r):
            ttk.Label(frm, text=label).grid(row=r, column=0, sticky='w', **pad)
            ttk.Entry(frm, textvariable=var, width=22).grid(row=r, column=1, sticky='ew', **pad)

        self.v_name = tk.StringVar(value=device.name)
        field('Nombre:', self.v_name, row); row += 1

        self.v_ip = self.v_mask = self.v_gw = self.v_sub = None

        if device.dtype != 'switch':
            self.v_ip = tk.StringVar(value=device.ip)
            field('Dirección IP:', self.v_ip, row); row += 1
            self.v_mask = tk.StringVar(value=device.mask)
            field('Máscara:', self.v_mask, row); row += 1

        if device.dtype == 'router':
            self.v_gw = tk.StringVar(value=device.gateway)
            field('Gateway:', self.v_gw, row); row += 1

        if device.dtype == 'host' and subnets:
            self.v_sub = tk.StringVar(value=device.subnet_ref or '(ninguna)')
            ttk.Label(frm, text='Subred:').grid(row=row, column=0, sticky='w', **pad)
            vals = ['(ninguna)'] + [s.name for s in subnets]
            ttk.Combobox(frm, textvariable=self.v_sub, values=vals,
                         state='readonly', width=20).grid(row=row, column=1, **pad)
            row += 1

        btn = ttk.Frame(frm)
        btn.grid(row=row, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btn, text='Aceptar',  command=self._ok).pack(side='left', padx=4)
        ttk.Button(btn, text='Cancelar', command=self.destroy).pack(side='left', padx=4)

        self.bind('<Return>', lambda _: self._ok())
        self.bind('<Escape>', lambda _: self.destroy())
        self._center(parent)

    def _ok(self):
        name = self.v_name.get().strip()
        if not name:
            messagebox.showwarning('Nombre requerido', 'El nombre no puede estar vacío.', parent=self)
            return
        self.device.name = name
        if self.v_ip:   self.device.ip      = self.v_ip.get().strip()
        if self.v_mask: self.device.mask    = self.v_mask.get().strip() or '255.255.255.0'
        if self.v_gw:   self.device.gateway = self.v_gw.get().strip()
        if self.v_sub:
            val = self.v_sub.get()
            self.device.subnet_ref = '' if val == '(ninguna)' else val
        self.result = True
        self.destroy()


class ConnectionDialog(_BaseDialog):
    """Diálogo para configurar propiedades de enlace."""

    def __init__(self, parent, conn: ConnectionModel):
        super().__init__(parent)
        self.conn   = conn
        self.result = False
        self.title('Propiedades del enlace')
        self.resizable(False, False)
        self.grab_set()

        frm = ttk.Frame(self, padding=14)
        frm.pack(fill='both', expand=True)
        pad = dict(padx=6, pady=3)

        ttk.Label(frm,
                  text=f'{conn.dev_a.name}.{conn.iface_a}  ←→  {conn.dev_b.name}.{conn.iface_b}',
                  font=('', 9, 'bold')).grid(row=0, column=0, columnspan=3,
                                             sticky='w', pady=(0, 8))

        ttk.Label(frm, text='Ancho de banda:').grid(row=1, column=0, sticky='w', **pad)
        self.v_bw = tk.StringVar(value=str(conn.bw) if conn.bw else '')
        ttk.Entry(frm, textvariable=self.v_bw, width=10).grid(row=1, column=1, **pad)
        self.v_bw_u = tk.StringVar(value=conn.bw_unit)
        ttk.Combobox(frm, textvariable=self.v_bw_u,
                     values=['Kbps', 'Mbps', 'Gbps'],
                     state='readonly', width=7).grid(row=1, column=2, **pad)

        ttk.Label(frm, text='Latencia:').grid(row=2, column=0, sticky='w', **pad)
        self.v_lat = tk.StringVar(value=str(conn.lat) if conn.lat else '')
        ttk.Entry(frm, textvariable=self.v_lat, width=10).grid(row=2, column=1, **pad)
        self.v_lat_u = tk.StringVar(value=conn.lat_unit)
        ttk.Combobox(frm, textvariable=self.v_lat_u,
                     values=['ms', 'us'],
                     state='readonly', width=7).grid(row=2, column=2, **pad)

        btn = ttk.Frame(frm)
        btn.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        ttk.Button(btn, text='Aceptar',  command=self._ok).pack(side='left', padx=4)
        ttk.Button(btn, text='Sin props', command=self._skip).pack(side='left', padx=4)
        ttk.Button(btn, text='Cancelar', command=self.destroy).pack(side='left', padx=4)

        self.bind('<Return>', lambda _: self._ok())
        self.bind('<Escape>', lambda _: self.destroy())
        self._center(parent)

    def _ok(self):
        try:
            self.conn.bw  = int(self.v_bw.get())  if self.v_bw.get().strip()  else 0
        except ValueError:
            self.conn.bw  = 0
        try:
            self.conn.lat = int(self.v_lat.get()) if self.v_lat.get().strip() else 0
        except ValueError:
            self.conn.lat = 0
        self.conn.bw_unit  = self.v_bw_u.get()
        self.conn.lat_unit = self.v_lat_u.get()
        self.result = True
        self.destroy()

    def _skip(self):
        self.conn.bw = self.conn.lat = 0
        self.result  = True
        self.destroy()


class SubnetManagerDialog(_BaseDialog):
    """Diálogo para gestionar subredes."""

    def __init__(self, parent, subnets: list):
        super().__init__(parent)
        self.subnets = subnets
        self.title('Gestionar subredes')
        self.resizable(False, False)
        self.grab_set()

        frm = ttk.Frame(self, padding=14)
        frm.pack(fill='both', expand=True)
        pad = dict(padx=5, pady=3)

        ttk.Label(frm, text='Subredes declaradas:', font=('', 9, 'bold')).pack(anchor='w')

        lf = ttk.Frame(frm)
        lf.pack(fill='x', pady=4)
        self.lb = tk.Listbox(lf, height=6, width=44, selectmode='single')
        sb = ttk.Scrollbar(lf, command=self.lb.yview)
        self.lb.config(yscrollcommand=sb.set)
        self.lb.pack(side='left')
        sb.pack(side='left', fill='y')
        self._refresh()

        add = ttk.LabelFrame(frm, text='Nueva subred', padding=8)
        add.pack(fill='x', pady=4)

        ttk.Label(add, text='Nombre:').grid(row=0, column=0, sticky='w', **pad)
        self.v_name = tk.StringVar()
        ttk.Entry(add, textvariable=self.v_name, width=16).grid(row=0, column=1, **pad)

        ttk.Label(add, text='Dirección:').grid(row=1, column=0, sticky='w', **pad)
        self.v_addr = tk.StringVar(value='192.168.1.0')
        ttk.Entry(add, textvariable=self.v_addr, width=16).grid(row=1, column=1, **pad)

        ttk.Label(add, text='Prefijo CIDR:').grid(row=2, column=0, sticky='w', **pad)
        self.v_pfx = tk.StringVar(value='24')
        ttk.Entry(add, textvariable=self.v_pfx, width=6).grid(row=2, column=1, sticky='w', **pad)

        btn = ttk.Frame(frm)
        btn.pack(fill='x', pady=(4, 0))
        ttk.Button(btn, text='Agregar',           command=self._add).pack(side='left', padx=3)
        ttk.Button(btn, text='Eliminar',          command=self._del).pack(side='left', padx=3)
        ttk.Button(btn, text='Cerrar',            command=self.destroy).pack(side='right', padx=3)

        self._center(parent)

    def _refresh(self):
        self.lb.delete(0, tk.END)
        for s in self.subnets:
            self.lb.insert(tk.END, f'  {s.name:<18} {s.address}/{s.prefix}')

    def _add(self):
        name = self.v_name.get().strip()
        addr = self.v_addr.get().strip()
        try:
            pfx = int(self.v_pfx.get().strip())
        except ValueError:
            pfx = 24
        if not name or not addr:
            messagebox.showwarning('Incompleto', 'Nombre y dirección son obligatorios.', parent=self)
            return
        self.subnets.append(SubnetModel(name=name, address=addr, prefix=pfx))
        self._refresh()
        self.v_name.set('')

    def _del(self):
        sel = self.lb.curselection()
        if sel:
            self.subnets.pop(sel[0])
            self._refresh()


# ═════════════════════════════════════════════════════════════════════════
# Aplicación principal
# ═════════════════════════════════════════════════════════════════════════

class NetLangApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('NetLang Designer')
        self.geometry('1150x780')
        self.minsize(900, 650)

        # Estado
        self.devices:     list[DeviceModel]     = []
        self.connections: list[ConnectionModel] = []
        self.subnets:     list[SubnetModel]     = []
        self.selected     = None
        self._tool        = 'select'
        self._connect_src: DeviceModel | None   = None
        self._drag_state  = None   # (start_cx, start_cy, dev_x0, dev_y0)

        self._build_ui()
        self._bind_canvas_events()

    # ── Construcción de la UI ─────────────────────────────────────────────

    def _build_ui(self):
        self._build_toolbar()

        # Divisor vertical: canvas+props arriba, output abajo
        vpane = ttk.PanedWindow(self, orient='vertical')
        vpane.pack(fill='both', expand=True, padx=4, pady=(0, 4))

        # Mitad superior: divisor horizontal canvas | props
        hpane = ttk.PanedWindow(vpane, orient='horizontal')
        vpane.add(hpane, weight=3)

        canvas_frame = ttk.Frame(hpane)
        hpane.add(canvas_frame, weight=4)
        self._build_canvas(canvas_frame)

        props_outer = ttk.Frame(hpane, width=210)
        hpane.add(props_outer, weight=1)
        self._build_props(props_outer)

        # Mitad inferior: output
        out_frame = ttk.Frame(vpane)
        vpane.add(out_frame, weight=1)
        self._build_output(out_frame)

    # ── Toolbar ───────────────────────────────────────────────────────────

    def _build_toolbar(self):
        tb = ttk.Frame(self, padding=(6, 5))
        tb.pack(fill='x', side='top')

        self._tool_btns: dict[str, ttk.Button] = {}

        tools = [
            ('select',  'Seleccionar', '↖'),
            ('router',  'Router',      '[R]'),
            ('switch',  'Switch',      '[SW]'),
            ('host',    'Host',        '[H]'),
            ('connect', 'Conectar',    '<->'),
            ('delete',  'Borrar',      '[X]'),
        ]
        for key, label, icon in tools:
            b = ttk.Button(tb, text=f'{icon}  {label}',
                           command=lambda k=key: self._set_tool(k))
            b.pack(side='left', padx=2)
            self._tool_btns[key] = b

        ttk.Separator(tb, orient='vertical').pack(side='left', fill='y', padx=8)
        ttk.Button(tb, text='Subredes', command=self._manage_subnets).pack(side='left', padx=2)

        ttk.Separator(tb, orient='vertical').pack(side='left', fill='y', padx=8)
        ttk.Label(tb, text='Red:').pack(side='left')
        self.v_net_name = tk.StringVar(value='MiRed')
        ttk.Entry(tb, textvariable=self.v_net_name, width=14).pack(side='left', padx=4)

        ttk.Separator(tb, orient='vertical').pack(side='left', fill='y', padx=8)
        ttk.Button(tb, text='Generar NetLang', command=self._generate).pack(side='left', padx=2)
        ttk.Button(tb, text='Compilar',        command=self._compile).pack(side='left', padx=2)
        ttk.Button(tb, text='Guardar .txt',    command=self._save).pack(side='left', padx=2)
        ttk.Button(tb, text='Limpiar todo',    command=self._clear_all).pack(side='left', padx=2)

        # Indicador de herramienta activa
        self.v_tool_label = tk.StringVar(value='Modo: Seleccionar')
        ttk.Label(tb, textvariable=self.v_tool_label,
                  foreground='gray').pack(side='right', padx=8)

    # ── Canvas ────────────────────────────────────────────────────────────

    def _build_canvas(self, parent):
        self.canvas = tk.Canvas(parent, bg=C['bg'], highlightthickness=0)
        vsb = ttk.Scrollbar(parent, orient='vertical',   command=self.canvas.yview)
        hsb = ttk.Scrollbar(parent, orient='horizontal', command=self.canvas.xview)
        self.canvas.config(yscrollcommand=vsb.set, xscrollcommand=hsb.set,
                           scrollregion=(-400, -400, 1800, 1800))
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.canvas.pack(fill='both', expand=True)
        self._draw_grid()

    def _draw_grid(self):
        self.canvas.delete('grid')
        for x in range(-400, 1800, GRID):
            self.canvas.create_line(x, -400, x, 1800, fill=C['grid'], tags='grid')
        for y in range(-400, 1800, GRID):
            self.canvas.create_line(-400, y, 1800, y, fill=C['grid'], tags='grid')
        self.canvas.tag_lower('grid')

    # ── Panel de propiedades ──────────────────────────────────────────────

    def _build_props(self, parent):
        ttk.Label(parent, text='Propiedades',
                  font=('', 10, 'bold'), padding=(8, 6)).pack(anchor='w')
        ttk.Separator(parent, orient='h').pack(fill='x')
        self.props_inner = ttk.Frame(parent, padding=10)
        self.props_inner.pack(fill='both', expand=True)
        self._show_props(None)

    def _show_props(self, element):
        for w in self.props_inner.winfo_children():
            w.destroy()
        f = self.props_inner

        if element is None:
            ttk.Label(f, text='Ningún elemento\nseleccionado.',
                      foreground='gray', justify='left').pack(anchor='nw')
            return

        if isinstance(element, DeviceModel):
            color = element.color
            ttk.Label(f, text=DeviceModel.LABELS[element.dtype],
                      font=('', 10, 'bold'),
                      foreground=color).pack(anchor='w')
            ttk.Separator(f, orient='h').pack(fill='x', pady=6)

            rows = [('Nombre', element.name)]
            if element.dtype != 'switch':
                rows += [('IP', element.ip or '—'), ('Máscara', element.mask)]
            if element.dtype == 'router' and element.gateway:
                rows.append(('Gateway', element.gateway))
            if element.dtype == 'host' and element.subnet_ref:
                rows.append(('Subred', element.subnet_ref))
            self._prop_rows(f, rows)

        elif isinstance(element, ConnectionModel):
            ttk.Label(f, text='Enlace', font=('', 10, 'bold')).pack(anchor='w')
            ttk.Separator(f, orient='h').pack(fill='x', pady=6)
            rows = [
                ('Origen',  f'{element.dev_a.name}.{element.iface_a}'),
                ('Destino', f'{element.dev_b.name}.{element.iface_b}'),
            ]
            if element.bw:
                rows.append(('Ancho BW', f'{element.bw} {element.bw_unit}'))
            if element.lat:
                rows.append(('Latencia', f'{element.lat} {element.lat_unit}'))
            self._prop_rows(f, rows)

        ttk.Button(f, text='Editar',
                   command=lambda: self._edit(element)).pack(fill='x', pady=(10, 0))

    def _prop_rows(self, parent, rows):
        for label, val in rows:
            row = ttk.Frame(parent)
            row.pack(fill='x', pady=1)
            ttk.Label(row, text=f'{label}:', width=9, anchor='w',
                      foreground=C['text_dim']).pack(side='left')
            ttk.Label(row, text=val, anchor='w').pack(side='left')

    # ── Panel de salida ───────────────────────────────────────────────────

    def _build_output(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True)
        self.txt_netlang = self._make_tab('NetLang (.txt)')
        self.txt_ir      = self._make_tab('LLVM IR (.ll)')
        self.txt_mininet = self._make_tab('Mininet Script (.py)')
        self.txt_log     = self._make_tab('Log')

    def _make_tab(self, label: str) -> tk.Text:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=label)
        txt = tk.Text(frame, height=10, wrap='none',
                      font=('Courier', 9), bg='#1E1E1E', fg='#D4D4D4',
                      insertbackground='white', selectbackground='#264F78')
        vsb = ttk.Scrollbar(frame, command=txt.yview)
        hsb = ttk.Scrollbar(frame, orient='horizontal', command=txt.xview)
        txt.config(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        txt.pack(fill='both', expand=True)
        return txt

    # ── Herramientas ──────────────────────────────────────────────────────

    def _set_tool(self, tool: str):
        self._tool = tool
        self._connect_src = None
        # Deseleccionar elemento actual al cambiar herramienta
        if tool != 'select':
            self._select(None)
        cursors = {
            'select':  'arrow',
            'router':  'crosshair',
            'switch':  'crosshair',
            'host':    'crosshair',
            'connect': 'tcross',
            'delete':  'X_cursor',
        }
        self.canvas.config(cursor=cursors.get(tool, 'arrow'))
        labels = {
            'select': 'Seleccionar', 'router': 'Agregar Router',
            'switch': 'Agregar Switch', 'host': 'Agregar Host',
            'connect': 'Conectar (clic en dos nodos)', 'delete': 'Borrar',
        }
        self.v_tool_label.set(f'Modo: {labels[tool]}')

    # ── Eventos del canvas ────────────────────────────────────────────────

    def _bind_canvas_events(self):
        c = self.canvas
        c.bind('<Button-1>',        self._on_click)
        c.bind('<B1-Motion>',       self._on_drag)
        c.bind('<ButtonRelease-1>', self._on_release)
        c.bind('<Double-Button-1>', self._on_dblclick)
        c.bind('<Button-3>',        self._on_rightclick)

    def _cxy(self, event):
        return self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

    def _on_click(self, event):
        x, y   = self._cxy(event)
        tool   = self._tool
        dev    = self._hit_device(x, y)
        conn   = self._hit_connection(x, y) if not dev else None

        if tool in ('router', 'switch', 'host'):
            self._place_device(tool, x, y)

        elif tool == 'select':
            hit = dev or conn
            self._select(hit)
            if isinstance(hit, DeviceModel):
                self._drag_state = (x, y, hit.x, hit.y)

        elif tool == 'connect':
            if dev:
                if self._connect_src is None:
                    self._connect_src = dev
                    self._highlight(dev, C['sel'])
                    self.v_tool_label.set(f'Conectar: selecciona el segundo nodo desde {dev.name}')
                elif dev is not self._connect_src:
                    self._highlight(self._connect_src, self._connect_src.color)
                    self._make_connection(self._connect_src, dev)
                    self._connect_src = None
                    self.v_tool_label.set('Modo: Conectar (clic en dos nodos)')

        elif tool == 'delete':
            hit = dev or conn
            if hit:
                self._delete(hit)

    def _on_drag(self, event):
        if self._tool != 'select' or not self._drag_state:
            return
        if not isinstance(self.selected, DeviceModel):
            return
        cx, cy = self._cxy(event)
        x0, y0, dx0, dy0 = self._drag_state
        dev = self.selected
        dev.x = dx0 + (cx - x0)
        dev.y = dy0 + (cy - y0)
        self._redraw_device(dev)
        self._redraw_conn_of(dev)

    def _on_release(self, event):
        self._drag_state = None

    def _on_dblclick(self, event):
        x, y = self._cxy(event)
        hit  = self._hit_device(x, y) or self._hit_connection(x, y)
        if hit:
            self._edit(hit)

    def _on_rightclick(self, event):
        x, y = self._cxy(event)
        hit  = self._hit_device(x, y) or self._hit_connection(x, y)
        if not hit:
            return
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label='Editar',   command=lambda: self._edit(hit))
        menu.add_separator()
        menu.add_command(label='Eliminar', command=lambda: self._delete(hit))
        menu.tk_popup(event.x_root, event.y_root)

    # ── Hit testing ───────────────────────────────────────────────────────

    def _hit_device(self, x, y) -> DeviceModel | None:
        for d in self.devices:
            if d.dtype == 'switch':
                if abs(x - d.x) <= SW_W / 2 + 4 and abs(y - d.y) <= SW_H / 2 + 4:
                    return d
            else:
                if (x - d.x)**2 + (y - d.y)**2 <= (NODE_R + 4)**2:
                    return d
        return None

    def _hit_connection(self, x, y) -> ConnectionModel | None:
        THRESH = 7
        for conn in self.connections:
            ax, ay = conn.dev_a.x, conn.dev_a.y
            bx, by = conn.dev_b.x, conn.dev_b.y
            dx, dy = bx - ax, by - ay
            if dx == dy == 0:
                continue
            t  = max(0, min(1, ((x-ax)*dx + (y-ay)*dy) / (dx*dx + dy*dy)))
            px = ax + t*dx
            py = ay + t*dy
            if (x-px)**2 + (y-py)**2 <= THRESH**2:
                return conn
        return None

    # ── Selección ─────────────────────────────────────────────────────────

    def _select(self, element):
        # Quitar resaltado anterior
        if isinstance(self.selected, DeviceModel):
            self._highlight(self.selected, self.selected.color)
        elif isinstance(self.selected, ConnectionModel):
            self.canvas.itemconfig(self.selected.line_id, fill=C['line'], width=2)

        self.selected = element

        if isinstance(element, DeviceModel):
            self._highlight(element, C['sel'])
        elif isinstance(element, ConnectionModel):
            self.canvas.itemconfig(element.line_id, fill=C['sel'], width=3)

        self._show_props(element)

    def _highlight(self, dev: DeviceModel, color: str):
        if dev.shape_id:
            self.canvas.itemconfig(dev.shape_id, fill=color)

    # ── Operaciones con elementos ─────────────────────────────────────────

    def _place_device(self, dtype: str, x: float, y: float):
        dev = DeviceModel(dtype, x, y)
        dlg = DeviceDialog(self, dev, self.subnets)
        self.wait_window(dlg)
        if dlg.result:
            self.devices.append(dev)
            self._draw_device(dev)
            self._set_tool('select')
            self._select(dev)

    def _make_connection(self, a: DeviceModel, b: DeviceModel):
        conn = ConnectionModel(a, a.next_iface(), b, b.next_iface())
        dlg  = ConnectionDialog(self, conn)
        self.wait_window(dlg)
        if dlg.result:
            self.connections.append(conn)
            self._draw_conn(conn)
            self._select(conn)

    def _edit(self, element):
        if isinstance(element, DeviceModel):
            dlg = DeviceDialog(self, element, self.subnets)
            self.wait_window(dlg)
            if dlg.result:
                self._redraw_device(element)
                self._show_props(element)
        elif isinstance(element, ConnectionModel):
            dlg = ConnectionDialog(self, element)
            self.wait_window(dlg)
            if dlg.result:
                self._update_conn_label(element)
                self._show_props(element)

    def _delete(self, element):
        if isinstance(element, DeviceModel):
            for conn in [c for c in self.connections
                         if c.dev_a is element or c.dev_b is element]:
                self.canvas.delete(f'conn_{conn.id}')
                self.connections.remove(conn)
            self.canvas.delete(f'dev_{element.id}')
            self.devices.remove(element)
        elif isinstance(element, ConnectionModel):
            self.canvas.delete(f'conn_{element.id}')
            self.connections.remove(element)

        if self.selected is element:
            self.selected = None
            self._show_props(None)

    # ── Dibujo en canvas ──────────────────────────────────────────────────

    def _draw_device(self, dev: DeviceModel):
        tag = f'dev_{dev.id}'
        x, y = dev.x, dev.y
        col  = dev.color

        if dev.dtype == 'switch':
            dev.shape_id = self.canvas.create_rectangle(
                x - SW_W//2, y - SW_H//2, x + SW_W//2, y + SW_H//2,
                fill=col, outline='white', width=2, tags=tag)
        else:
            dev.shape_id = self.canvas.create_oval(
                x - NODE_R, y - NODE_R, x + NODE_R, y + NODE_R,
                fill=col, outline='white', width=2, tags=tag)

        # Abreviatura dentro del nodo
        self.canvas.create_text(
            x, y, text=DeviceModel.ABBREV[dev.dtype],
            fill='white', font=('Courier', 8, 'bold'), tags=tag)

        # Nombre debajo del nodo
        offset = SW_H // 2 + 12 if dev.dtype == 'switch' else NODE_R + 12
        self.canvas.create_text(
            x, y + offset, text=dev.name,
            font=('', 9, 'bold'), fill=C['text'], tags=tag)

        # IP debajo del nombre (si tiene)
        if dev.ip:
            self.canvas.create_text(
                x, y + offset + 13, text=dev.ip,
                font=('Courier', 8), fill=C['text_dim'], tags=tag)

    def _redraw_device(self, dev: DeviceModel):
        was_selected = self.selected is dev
        self.canvas.delete(f'dev_{dev.id}')
        self._draw_device(dev)
        if was_selected:
            self._highlight(dev, C['sel'])

    def _draw_conn(self, conn: ConnectionModel):
        tag = f'conn_{conn.id}'
        ax, ay = conn.dev_a.x, conn.dev_a.y
        bx, by = conn.dev_b.x, conn.dev_b.y

        conn.line_id = self.canvas.create_line(
            ax, ay, bx, by, fill=C['line'], width=2, tags=tag)
        self.canvas.tag_lower(tag)
        self.canvas.tag_lower('grid')

        mx, my = (ax + bx) / 2, (ay + by) / 2
        label  = self._conn_label_text(conn)
        conn.label_id = self.canvas.create_text(
            mx, my - 12, text=label,
            font=('Courier', 8), fill='#37474F', tags=tag)

    def _conn_label_text(self, conn: ConnectionModel) -> str:
        parts = []
        if conn.bw:  parts.append(f'{conn.bw}{conn.bw_unit}')
        if conn.lat: parts.append(f'{conn.lat}{conn.lat_unit}')
        return '  '.join(parts)

    def _update_conn_label(self, conn: ConnectionModel):
        if conn.label_id:
            self.canvas.itemconfig(conn.label_id, text=self._conn_label_text(conn))

    def _redraw_conn_of(self, dev: DeviceModel):
        for conn in self.connections:
            if conn.dev_a is dev or conn.dev_b is dev:
                ax, ay = conn.dev_a.x, conn.dev_a.y
                bx, by = conn.dev_b.x, conn.dev_b.y
                self.canvas.coords(conn.line_id, ax, ay, bx, by)
                if conn.label_id:
                    self.canvas.coords(conn.label_id,
                                       (ax+bx)/2, (ay+by)/2 - 12)

    # ── Gestión de subredes ───────────────────────────────────────────────

    def _manage_subnets(self):
        dlg = SubnetManagerDialog(self, self.subnets)
        self.wait_window(dlg)

    # ── Generación de código NetLang ──────────────────────────────────────

    def _build_netlang(self) -> str:
        net_name = self.v_net_name.get().strip() or 'MiRed'
        lines = [f'network {net_name} {{', '']

        if self.subnets:
            for s in self.subnets:
                lines.append(f'    subnet {s.name} {s.address}/{s.prefix}')
            lines.append('')

        for dev in self.devices:
            props = []
            if dev.dtype == 'router' and dev.gateway:
                props.append(f'        gateway {dev.gateway}')
            if dev.dtype == 'host' and dev.subnet_ref:
                props.append(f'        subnet {dev.subnet_ref}')
            if props:
                lines.append(f'    device {dev.name} {dev.dtype} {{')
                lines.extend(props)
                lines.append('    }')
            else:
                lines.append(f'    device {dev.name} {dev.dtype}')
        lines.append('')

        # Interfaces: una por dispositivo no-switch con IP
        seen_ifaces: set[str] = set()
        for dev in self.devices:
            if dev.dtype == 'switch' or not dev.ip:
                continue
            iface = self._first_iface(dev)
            if iface:
                key = f'{dev.name}.{iface}'
                if key not in seen_ifaces:
                    seen_ifaces.add(key)
                    lines.append(
                        f'    interface {dev.name} {iface} ip {dev.ip} mask {dev.mask}')
        if seen_ifaces:
            lines.append('')

        for conn in self.connections:
            line = (f'    connect {conn.dev_a.name}.{conn.iface_a}'
                    f' to {conn.dev_b.name}.{conn.iface_b}')
            if conn.bw:
                line += f' bandwidth {conn.bw} {conn.bw_unit}'
            if conn.lat:
                line += f' latency {conn.lat} {conn.lat_unit}'
            lines.append(line)

        lines.append('}')
        return '\n'.join(lines)

    def _first_iface(self, dev: DeviceModel) -> str | None:
        for conn in self.connections:
            if conn.dev_a is dev: return conn.iface_a
            if conn.dev_b is dev: return conn.iface_b
        return None

    # ── Acciones de la toolbar ────────────────────────────────────────────

    def _generate(self):
        code = self._build_netlang()
        self._set_text(self.txt_netlang, code)
        self.notebook.select(0)
        self._log('NetLang generado.')

    def _compile(self):
        if not self.devices:
            messagebox.showwarning('Sin dispositivos',
                                   'Agrega al menos un dispositivo antes de compilar.')
            return

        code = self._build_netlang()
        self._set_text(self.txt_netlang, code)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                         delete=False, encoding='utf-8') as f:
            f.write(code)
            tmp = f.name

        try:
            from antlr4 import FileStream, CommonTokenStream
            from NetLangLexer    import NetLangLexer
            from NetLangParser   import NetLangParser
            from SemanticAnalyzer import SemanticAnalyzer
            from IRGenerator     import IRGenerator
            from CodeGen         import CodeGen

            stream = FileStream(tmp, encoding='utf-8')
            lexer  = NetLangLexer(stream)
            tokens = CommonTokenStream(lexer)
            parser = NetLangParser(tokens)
            tree   = parser.program()

            if parser.getNumberOfSyntaxErrors():
                self._log(f'✗ {parser.getNumberOfSyntaxErrors()} error(es) sintáctico(s).',
                          error=True)
                self.notebook.select(3)
                return

            sem = SemanticAnalyzer()
            sem.visit(tree)
            if sem.errors:
                self._log('✗ Errores semánticos:\n' +
                           '\n'.join(f'  • {e}' for e in sem.errors), error=True)
                self.notebook.select(3)
                return

            ir_gen = IRGenerator()
            ir_gen.visit(tree)
            network_ir = ir_gen.ir

            self._set_text(self.txt_ir,      ir_gen.emit_llvm_ir())
            self._set_text(self.txt_mininet, CodeGen(network_ir).generar())

            self._log('✓ Compilación exitosa. IR y script Mininet listos.')
            self.notebook.select(1)

        except Exception:
            self._log(f'✗ Error inesperado:\n{traceback.format_exc()}', error=True)
            self.notebook.select(3)

        finally:
            try:
                os.unlink(tmp)
            except OSError:
                pass

    def _save(self):
        code = self._build_netlang()
        path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('NetLang', '*.txt'), ('Todos', '*.*')],
            initialfile=f'{self.v_net_name.get().strip() or "red"}.txt',
            title='Guardar topología NetLang')
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(code)
            self._log(f'Guardado en: {path}')

    def _clear_all(self):
        if not messagebox.askyesno('Confirmar', '¿Borrar toda la topología y subredes?'):
            return
        for d in self.devices:
            self.canvas.delete(f'dev_{d.id}')
        for c in self.connections:
            self.canvas.delete(f'conn_{c.id}')
        self.devices.clear()
        self.connections.clear()
        self.subnets.clear()
        DeviceModel._seq = ConnectionModel._seq = SubnetModel._seq = 0
        self.selected = None
        self._show_props(None)
        for txt in (self.txt_netlang, self.txt_ir, self.txt_mininet, self.txt_log):
            self._set_text(txt, '')

    # ── Helpers ───────────────────────────────────────────────────────────

    def _log(self, msg: str, error: bool = False):
        self.txt_log.config(state='normal')
        tag = 'err' if error else 'ok'
        self.txt_log.tag_config('err', foreground='#F44747')
        self.txt_log.tag_config('ok',  foreground='#4EC9B0')
        self.txt_log.insert(tk.END, msg + '\n', tag)
        self.txt_log.see(tk.END)
        self.txt_log.config(state='normal')

    @staticmethod
    def _set_text(widget: tk.Text, text: str):
        widget.config(state='normal')
        widget.delete('1.0', tk.END)
        widget.insert('1.0', text)


# ─────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app = NetLangApp()
    app.mainloop()

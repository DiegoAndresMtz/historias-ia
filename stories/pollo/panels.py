import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect_path, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp, text_w
from povlib import *
from scenes import popin, tag2, bust_back, sepia
import leyendas as L
import guion as G

YOU = dict(hat="beanie", skin="#c48a5c", shirt="#3c6a9a", cap_col="#e8702a")
VALE = dict(hat="bun", freckles=True, skin="#c48a5c", shirt="#f0a8c8", hair_col="#2a1a10", pants="#f0a8c8")
ABUELA = dict(hat="bun", glasses="#8a6a4a", skin="#b88a64", shirt="#5a3a6a", hair_col="#d8d8d0")
TIO = dict(hat="none", skin="#a8704a", shirt="#d8c8a0", hair_col="#1a120e", mustache=True, mole=True)
AMIGO1 = dict(hat="cap", skin="#8a5a3a", shirt="#5a7a3a", hair_col="#1a120e", cap_col="#2a4a7a")
AMIGO2 = dict(hat="hair", skin="#c08a60", shirt="#8a3a2a", hair_col="#2a1a10", mustache=True)
VALE_GRANDE = dict(hat="bun", freckles=True, skin="#c48a5c", shirt="#3a7a6a", hair_col="#2a1a10")
NIETO = dict(hat="hair", freckles=True, skin="#c48a5c", shirt="#e8b83a", hair_col="#2a1a10")
FOCUS = {}; CAM = {}

def big(c, s_, x, y, col="#ffffff", size=120):
    ui(c, size); w_ = text_w(c, s_); c.new_path(); c.move_to(x - w_ / 2, y); c.text_path(s_)
    c.set_line_width(16); c.set_line_join(cairo.LINE_JOIN_ROUND); src(c, "#000"); c.stroke_preserve(); src(c, col); c.fill()

# ---------------- escenarios ----------------
def noche(c, t, y0=640, moon=True, cafe=True, sky=("#070a14", "#1a2030")):
    vgrad(c, 0, 0, P, y0, *sky)
    r = random.Random(3)
    for k in range(40): circ(c, r.uniform(0, P), r.uniform(0, y0 - 200), r.uniform(1, 2.5), hx("#ffffff", r.uniform(0.2, 0.6)))
    if moon: circ(c, 860, 160, 46, "#eef0f4"); glow(c, 860, 160, 280, "#dfe8ff", 0.2)
    poly(c, [(0, y0 - 120), (160, y0 - 260), (330, y0 - 170), (560, y0 - 300), (760, y0 - 180), (940, y0 - 260), (P, y0 - 200), (P, y0), (0, y0)], "#0c1420")
    poly(c, [(0, y0 - 40), (220, y0 - 140), (480, y0 - 70), (700, y0 - 150), (P, y0 - 60), (P, y0), (0, y0)], "#0a140e")
    vgrad(c, 0, y0, P, P - y0, "#0c1a10", "#040806")
    if cafe:
        for row in range(5):
            yy = y0 + 30 + row * 90
            for k in range(9):
                x = (k * 140 + row * 70) % 1200 - 60
                ell(c, x, yy, 70 + row * 10, 34 + row * 6, "#0a2412" if row % 2 else "#0e2a16")
                for j in range(3): circ(c, x - 30 + j * 30, yy - 10, 5, hx("#a01a1a", 0.6))   # granos de café

def guamo(c, x, y, s, col="#060c08"):
    def f():
        line(c, [(0, 0), (10, -300), (-20, -520)], col, 46)
        line(c, [(10, -300), (140, -440)], col, 24); line(c, [(-10, -380), (-160, -470)], col, 22)
        for dx_, dy_, rx in ((-180, -520, 170), (60, -580, 200), (220, -470, 150), (-40, -640, 160)): ell(c, dx_, dy_, rx, rx * 0.45, col)
    scaled(c, x, y, s, f)

def casa(c, x, y, s, t, light=1.0):
    """Casa de finca: bahareque blanco, zócalo rojo, techo de zinc y corredor con bombillo."""
    def f():
        rect(c, -420, -330, 840, 330, "#d8d0c0"); rect(c, -420, -90, 840, 90, "#9a2a22")       # pared y zócalo
        for k in range(4): rect(c, -400 + k * 270, -330, 26, 330, "#5a3a22")                     # pilares del corredor
        poly(c, [(-480, -320), (480, -320), (420, -470), (-420, -470)], "#7a8088")                 # zinc
        for k in range(22): line(c, [(-470 + k * 43, -322), (-412 + k * 39, -468)], hx("#4a5058", 0.8), 4)
        rect(c, -480, -330, 960, 16, "#5a6068")
        rect(c, -80, -260, 140, 260, "#4a2a18"); rect(c, 200, -250, 150, 110, "#2a1a10")
        rect(c, 210, -240, 130, 90, hx("#ffc070", 0.9 * light))
        if light:
            line(c, [(-200, -320), (-200, -270)], "#222", 3); circ(c, -200, -262, 12, "#fff2c0")
            glow(c, -200, -262, 360, "#ffc070", 0.35 * light)
    scaled(c, x, y, s, f)

def carta(c, x, y, s, rot, up, seed=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rrect(c, -34, -50, 68, 100, 8, "#000"); rrect(c, -31, -47, 62, 94, 7, "#f4f0e4" if up else "#a01a22")
    if up:
        r = random.Random(seed); kind = seed % 4
        col = "#c01a1a" if kind in (1, 3) else "#11131a"
        if kind == 0:   # espada
            line(c, [(0, -30), (0, 26)], col, 6); line(c, [(-12, 14), (12, 14)], col, 6)
        elif kind == 1: circ(c, 0, 0, 18, col); circ(c, 0, 0, 9, "#f4f0e4")      # oro
        elif kind == 2: line(c, [(-14, 26), (14, -26)], col, 9)                    # basto
        else: poly(c, [(-14, -16), (14, -16), (8, 22), (-8, 22)], col)            # copa
    else:
        for k in range(4): line(c, [(-24, -38 + k * 24), (24, -26 + k * 24)], hx("#f0c0c0", 0.5), 3)
    c.restore()

def mesa(c, x, y, s, t, up=0.0, regadas=False):
    """Mesa del corredor con cartas, botella y copitas. up = cuántas cartas se han volteado (0..1)."""
    def f():
        rect(c, -300, -20, 600, 30, "#5a3a1e"); rect(c, -280, 10, 24, 200, "#3a2410"); rect(c, 256, 10, 24, 200, "#3a2410")
        rect(c, 150, -150, 46, 130, hx("#e8f0f4", 0.7)); rect(c, 158, -190, 30, 40, hx("#e8f0f4", 0.7)); rect(c, 150, -110, 46, 50, "#2a5aa8")
        for k, cx_ in enumerate((-220, 100, 230)): rect(c, cx_, -54, 24, 34, hx("#e8f0f0", 0.6))
        n = 8
        for k in range(n):
            u = up * n > k
            carta(c, -200 + k * 42, -40 + (k % 2) * 6, 0.6, -0.2 + k * 0.05, u, k)
    scaled(c, x, y, s, f)

def ondas(c, x, y, t, col="#ffd21a", n=3, r=260, a=1.0, sy=1.0, speed=0.6):
    """El canto: ondas que salen de un punto."""
    for k in range(n):
        p = (t * speed + k / n) % 1
        c.new_path(); c.save(); c.translate(x, y); c.scale(1, sy); c.arc(0, 0, 20 + r * p, 0, 2 * math.pi); c.restore()
        c.set_line_width(6 - 3 * p); src(c, hx(col, 0.55 * a * (1 - p))); c.stroke()
    glow(c, x, y, 60, col, 0.35 * a)

def plumas(c, t, n=12, seed=4, a=1.0, x0=0, x1=P):
    r = random.Random(seed)
    for k in range(n):
        sp = r.uniform(60, 140); ph = r.uniform(0, P)
        y = (ph + t * sp) % (P + 100) - 50; x = r.uniform(x0, x1) + math.sin(t * 2 + k) * 40
        c.save(); c.translate(x, y); c.rotate(math.sin(t * 3 + k) * 0.8)
        ell(c, 0, 0, 10, 34, hx("#0a0604", a)); line(c, [(0, -34), (0, 40)], hx("#4a3a2a", a * 0.8), 2); c.restore()

def techo(c, t, y=380):
    """Borde del techo de zinc visto desde abajo, de noche."""
    vgrad(c, 0, 0, P, y, "#05070c", "#101622")
    poly(c, [(0, y), (P, y - 60), (P, y + 80), (0, y + 140)], "#6a7078")
    for k in range(26): line(c, [(k * 44, y + 140 - k * 5.5), (k * 44 + 10, y - k * 2.3)], hx("#3a4048", 0.9), 5)
    rect(c, 0, y + 120, P, P, "#1a1410")

def cuarto(c, t, lamp=1.0, bed=True, escaparate=True, open_esc=0.0):
    vgrad(c, 0, 0, P, P, "#4a4038", "#18140f")
    for k in range(5): line(c, [(60 + k * 220, 60), (80 + k * 220, 300), (64 + k * 220, 420)], hx("#000", 0.18), 4)
    rect(c, 0, 860, P, 220, "#3a2a1a")
    for k in range(10): rect(c, k * 110, 860, 6, 220, hx("#000", 0.5))
    if escaparate:
        rect(c, 690, 260, 300, 600, "#4a2a16"); rect(c, 700, 270, 280, 580, "#5a3620")
        if open_esc <= 0: line(c, [(840, 280), (840, 840)], "#2a160a", 6); circ(c, 820, 560, 8, "#c8a040"); circ(c, 860, 560, 8, "#c8a040")
    if bed:
        rrect(c, 60, 720, 520, 140, 16, "#6a4a2a"); rrect(c, 70, 680, 500, 70, 20, "#d8d0c0"); rect(c, 60, 560, 30, 300, "#5a3a1e")
        rrect(c, 90, 650, 140, 50, 20, "#f4f0e8"); rect(c, 60, 860, 520, 20, "#000")
    if lamp: rrect(c, 600, 640, 40, 60, 10, hx("#ffd890", 0.9 * lamp)); glow(c, 620, 650, 380, "#ffb060", 0.3 * lamp)

def camandula(c, x, y, s, t, lit=0, cross=True):
    """Rosario de cuentas; lit = cuántas cuentas se iluminan (las oraciones)."""
    def f():
        for k in range(9):
            a = math.pi * (0.1 + 0.8 * k / 8)
            bx, by = math.cos(a) * 220, math.sin(a) * 160
            if k: line(c, [(px, py), (bx, by)], hx("#c8b08a", 0.8), 3)
            px, py = bx, by
            on = k < lit
            if on: glow(c, bx, by, 60, "#ffd890", 0.6)
            circ(c, bx, by, 22, "#000"); circ(c, bx, by, 18, "#f0e0b0" if on else "#5a3a2a")
        if cross:
            line(c, [(0, 160), (0, 290)], "#c8a040", 12); line(c, [(-40, 200), (40, 200)], "#c8a040", 12)
    scaled(c, x, y, s, f)

def vela(c, x, y, s, t, lit=1.0):
    def f():
        rect(c, -18, -120, 36, 120, "#f0ead8"); rect(c, -40, 0, 80, 14, "#8a6a3a")
        if lit > 0:
            fl = 1 + 0.12 * math.sin(t * 13) + 0.06 * math.sin(t * 29)
            glow(c, 0, -150, 260, "#ffb060", 0.4 * lit)
            ell(c, 0, -146 - 6 * fl, 13 * fl * lit, 30 * fl * lit, "#ffc24a"); ell(c, 0, -140, 6 * lit, 14 * lit, "#fff2c0")
    scaled(c, x, y, s, f)

def machete(c, x, y, s, rot):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rect(c, -16, 0, 32, 90, "#2a1a0e")
    poly(c, [(-20, 0), (20, 0), (34, -360), (0, -420), (-14, -360)], "#b8c0c8"); line(c, [(6, -10), (18, -380)], hx("#ffffff", 0.6), 4)
    c.restore()

def linterna(c, x0, y0, x1, y1, w_=260, a=0.16):
    dx_, dy_ = x1 - x0, y1 - y0; d = math.hypot(dx_, dy_); nx, ny = -dy_ / d, dx_ / d
    poly(c, [(x0, y0), (x1 + nx * w_, y1 + ny * w_), (x1 - nx * w_, y1 - ny * w_)], hx("#fff8d0", a))
    glow(c, x1, y1, w_ * 1.3, "#fff8d0", a * 1.6)

def garra(c, x, y, s, ang, t=0.0):
    """Pata de pollo con garras negras (se clava)."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    line(c, [(0, -220), (0, 0)], "#7a6a4a", 40)
    for k in range(6): line(c, [(-18, -200 + k * 30), (18, -196 + k * 30)], hx("#3a2e1a", 0.8), 3)
    for a in (-0.6, 0.0, 0.6):
        ex, ey = math.sin(a) * 110, math.cos(a) * 110
        line(c, [(0, 0), (ex, ey)], "#7a6a4a", 22)
        poly(c, [(ex - 10, ey - 6), (ex + 10, ey - 6), (ex + math.sin(a) * 50, ey + 50)], "#050302")
    c.restore()

def trocha(c, t, curve=True, y0=560):
    noche(c, t, y0=y0, cafe=False)
    vgrad(c, 0, y0, P, P - y0, "#0c1a10", "#030604")
    poly(c, [(300, P), (780, P), (620, y0 + 40), (560, y0 + 20)], "#3a2e20")
    if curve: poly(c, [(560, y0 + 20), (620, y0 + 40), (820, y0 + 10), (760, y0)], "#3a2e20")
    for k in range(6):
        guamo(c, 60 + k * 50 if k < 3 else 860 + (k - 3) * 80, y0 + 300 - (k % 3) * 120, 0.9 - (k % 3) * 0.25)
    r = random.Random(5)
    for k in range(18): ell(c, r.choice([r.uniform(0, 280), r.uniform(800, P)]), r.uniform(y0 + 40, P), 70, 36, "#081a0c")

def ojos_blanco(c, x, y, s, t, talk=0.0, **kw):
    bust(c, x, y, s, t, "creepy", look=(0, -5.2), talk=talk, **kw)

# ---------------- PARTE 1 ----------------
R = G.RULETA
def t00(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#140c06", "#030202")
    tt = t - R["start"]
    L.ruleta(c, 540, 600, 410, max(0, tt), R["dur"], R["target"], win=clamp((tt - R["dur"]) / 0.3))
FOCUS["t00"] = (540, 560)
CAM["t00"] = [(0.0, 1.0, 540, 560)]

def t01(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#140a04", "#020101")
    glow(c, 540, 460, 540, "#ffb21a", 0.2)
    plumas(c, t, 10, 7)
    sc = 0.4 + 0.75 * ease(clamp(t / 0.5))
    L.icono("El Pollo Maligno", c, 540, 430, sc, t)
    big(c, "EL POLLO MALIGNO", 540, 1010, "#ffd21a", 92)
FOCUS["t01"] = (540, 500)
CAM["t01"] = [(0.0, 1.0, 540, 540)]

def t02(c, t, T, w):
    noche(c, t, y0=600)
    casa(c, 540, 880, 0.95, t)
    mesa(c, 380, 960, 0.55, t)
    if t > w("aurelio") - 0.3:
        bust(c, 260, 950, 0.32, t, "happy", look=(0.6, 0), **TIO)
        bust(c, 500, 950, 0.3, t + 1, "smile", look=(-0.6, 0), **AMIGO1)
        bust(c, 380, 940, 0.28, t + 2, "happy", look=(0, 0.3), **AMIGO2)
    mesa(c, 380, 1000, 0.55, t)
FOCUS["t02"] = (420, 820)

def t03(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#3a2a20", "#100a06")
    glow(c, 700, 600, 500, "#ffb060", 0.2)
    vela(c, 860, 900, 1.2, t)
    bust(c, 440, 1110, 1.05, t, "worry", look=(0.4, 0), arms="hold", **ABUELA)
    camandula(c, 440, 920, 0.6, t, lit=9 if t > w("miguel") - 0.2 else 0)
FOCUS["t03"] = (480, 620)

def t04(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#2a1e18", "#0a0604")
    glow(c, 540, 560, 500, "#ffb060", 0.18)
    bust(c, 540, 1110, 1.15, t, "angry", look=(0, 0), talk="auto", **ABUELA)
FOCUS["t04"] = (540, 600)

def t05(c, t, T, w):
    noche(c, t, y0=560)
    guamo(c, 860, 760, 0.7)
    casa(c, 180, 1080, 0.6, t)
    if t > w("pío") - 0.2:
        ondas(c, 780, 640, t, "#ffd21a", 3, 160, 0.9, 0.6, 0.9)
FOCUS["t05"] = (700, 620)

def t06(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#2a1e18", "#0a0604")
    bust(c, 540, 1110, 1.15, t, "shock" if t > w("pálida") - 0.2 else "worry", look=(0.6, -0.2), shake=0.6, gray=True, **ABUELA)
    if t > w("cerca") - 0.2:
        overlay(c, "#000", 0.35)
        ondas(c, 900, 260, t, "#ffd21a", 3, 200, 1.0, 1.0, 1.2)
FOCUS["t06"] = (540, 600)

def t07(c, t, T, w):
    noche(c, t, y0=500, cafe=False); overlay(c, "#000", 0.2)
    glow(c, 300, 300, 460, "#ffc070", 0.3)
    bust(c, 540, 1110, 1.1, t, "happy", look=(-0.3, -0.2), talk="auto", **TIO)
    c.save(); c.translate(820, 760); c.rotate(0.2 + 0.1 * math.sin(t * 4)); rect(c, -24, -60, 48, 60, hx("#e8f0f0", 0.7)); c.restore()
FOCUS["t07"] = (540, 600)

def t08(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#1a1410", "#060402")
    glow(c, 540, 300, 600, "#ffc070", 0.28 if t < w("silencio") else 0.12)
    sil = t > w("silencio") - 0.1
    bust(c, 200, 760, 0.55, t, "shock" if sil else "happy", look=(0.6, 0.4), **AMIGO1)
    bust(c, 880, 760, 0.55, t + 1, "shock" if sil else "happy", look=(-0.6, 0.4), **AMIGO2)
    up = clamp((t - w("voltean") + 0.1) / 2.0) if t > w("voltean") - 0.1 else 0.0
    mesa(c, 540, 860, 1.4, t, up=up)
FOCUS["t08"] = (540, 760)
CAM["t08"] = [(0.0, 1.0, 540, 540), ("voltean", 1.35, 540, 760)]

def t09(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#1e1812", "#080604")
    rect(c, 330, 120, 420, 860, "#0a0806"); rect(c, 310, 100, 460, 20, "#4a2a18"); rect(c, 310, 100, 20, 880, "#4a2a18"); rect(c, 750, 100, 20, 880, "#4a2a18")
    glow(c, 540, 600, 300, "#ffc070", 0.12)
    bust(c, 540, 1000, 0.6, t, "worry", look=(0, -1.2), **VALE)
FOCUS["t09"] = (540, 640)

def t10(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#1e1812", "#080604")
    bust(c, 540, 1110, 1.05, t, "scared", look=(0, -1.0), talk="auto", tears=0.4, **VALE)
    if t > w("mí") - 0.2: overlay(c, "#200000", 0.25)
FOCUS["t10"] = (540, 600)

def t11(c, t, T, w):
    y = 520
    techo(c, t, y)
    rise = ease(clamp((t - w("cresta") + 0.3) / 1.6))
    eyes = t > w("amarillos") - 0.3
    c.save(); c.rectangle(0, 0, P, y - 40 + 60); c.clip()
    L.icono("El Pollo Maligno", c, 560, y + 320 - 380 * rise, 1.25, t)
    c.restore()
    techo_front = [(0, y), (P, y - 60), (P, y + 80), (0, y + 140)]
    poly(c, techo_front, "#6a7078")
    for k in range(26): line(c, [(k * 44, y + 140 - k * 5.5), (k * 44 + 10, y - k * 2.3)], hx("#3a4048", 0.9), 5)
    if t > w("garras") - 0.2:
        sc = math.sin(t * 9) * 12
        garra(c, 320 + sc, y + 60, 0.7, math.pi * 0.95); garra(c, 760 - sc, y + 20, 0.7, math.pi * 1.05)
        for k in range(4): line(c, [(260 + k * 30, y + 90 - k * 4), (330 + k * 30 + sc, y + 100 - k * 4)], hx("#e8e8f0", 0.7), 3)
    linterna(c, 540, 1200, 560, y - 60, 300, 0.16 if t > w("alumbras") - 0.1 else 0)
    if not eyes: overlay(c, "#000", 0.15)
FOCUS["t11"] = (540, 480)
CAM["t11"] = [(0.0, 1.0, 540, 540), ("amarillos", 1.35, 560, 420)]

def t12(c, t, T, w):
    techo(c, t, 520)
    c.save(); c.rectangle(0, 0, P, 520); c.clip(); L.icono("El Pollo Maligno", c, 560, 140, 1.25, t); c.restore()
    poly(c, [(0, 520), (P, 460), (P, 600), (0, 660)], "#6a7078")
    overlay(c, "#000", 0.45)

# ---------------- PARTE 2 ----------------
def u01(c, t, T, w):
    cuarto(c, t, lamp=0.5)
    sh = 0
    if t > w("rasguña") - 0.2:
        x = 100 + ((t - w("rasguña")) * 260) % 900
        for k in range(4): line(c, [(x + k * 18, 20), (x + k * 18 + 40, 70)], hx("#d8d0c0", 0.7), 4)
        for k in range(6): circ(c, x + 30 + math.sin(t * 7 + k) * 30, 80 + ((t * 300 + k * 90) % 500), 4, hx("#c8b8a0", 0.6))   # polvo
    for sx in (-1, 1): glow(c, 280 + sx * 26, 800, 22, "#ffffff", 0.3); circ(c, 280 + sx * 26, 800, 7, "#f4f4f4"); circ(c, 280 + sx * 26, 801, 4, "#2a1a10")
    bust(c, 560, 1110, 0.8, t, "worry", look=(0, -1.0), **YOU)
FOCUS["u01"] = (480, 640)

def u02(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#140c08", "#050302")
    lit = clamp((t - w("vela") + 0.2) / 0.3)
    vela(c, 820, 960, 1.2, t, lit)
    bust(c, 420, 1120, 1.05, t, "worry", look=(0.4, -0.2), arms="hold", **ABUELA)
    if t > w("camándula") - 0.3: camandula(c, 420, 930, 0.6, t, lit=0)
FOCUS["u02"] = (480, 600)

def u03(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#1a100a", "#050302")
    glow(c, 760, 600, 400, "#ffb060", 0.25)
    bust(c, 540, 1110, 1.15, t, "angry", look=(0, 0), talk="auto", **ABUELA)
FOCUS["u03"] = (540, 600)

def u04(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#140c08", "#050302")
    glow(c, 540, 560, 500, "#ffb060", 0.2)
    lit = sum(1 for k in ("una", "dos", "tres", "cuatro", "cinco") if t > w(k) - 0.1)
    camandula(c, 540, 380, 1.5, t, lit=lit)
    a = 1 - 0.18 * lit
    ondas(c, 540 + 60 * lit, 860, t, "#ffd21a", 3, 280 - 40 * lit, a, 0.4)
    if t > w("significa") - 0.2: overlay(c, "#200000", 0.3)
FOCUS["u04"] = (540, 520)

def u05(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#2a2018", "#0a0604")
    rect(c, 330, 140, 420, 840, "#4a2a18"); rect(c, 350, 160, 380, 820, "#5a3620"); circ(c, 690, 580, 12, "#c8a040")
    ad = t > w("adentro") - 0.2
    if ad:
        rect(c, 350, 960, 380, 20, hx("#ffd21a", 0.6)); glow(c, 540, 975, 300, "#ffd21a", 0.35)
        ondas(c, 540, 560, t, "#ffd21a", 4, 420, 0.8, 1.0, 0.8)
    camandula(c, 160, 160, 0.45, t, lit=6)
FOCUS["u05"] = (540, 600)
CAM["u05"] = [(0.0, 1.0, 540, 540), ("cuarto", 1.3, 540, 760)]

def u06(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#2a2018", "#0a0604")
    kick = t > w("patada") - 0.1
    if not kick:
        rect(c, 600, 140, 400, 840, "#5a3620"); circ(c, 640, 580, 12, "#c8a040")
    else:
        rect(c, 600, 140, 400, 840, "#020101")
        poly(c, [(1000, 140), (1060, 100), (1060, 1020), (1000, 980)], "#5a3620")
        glow(c, 800, 560, 320, "#ffd21a", 0.15)
    bust(c, 360, 1110, 1.0, t, "angry", look=(0.7, 0), shake=0.5 if kick else 0, **TIO)
    if t > w("machete") - 0.3: machete(c, 200, 900, 1.1, -0.3 + (0.5 if kick else 0))
FOCUS["u06"] = (520, 600)

def u07(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#100806", "#020101")
    glow(c, 540, 560, 500, "#ffd21a", 0.1)
    bust(c, 540, 1110, 1.15, t, "angry", look=(0, -0.2), talk="auto", shake=0.4, **TIO)
    machete(c, 860, 1000, 1.4, 0.25 + 0.1 * math.sin(t * 8))
FOCUS["u07"] = (540, 600)

def u08(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#140c08", "#050302")
    vela(c, 820, 960, 1.2, t)
    bust(c, 420, 1120, 1.05, t, "shock" if t > w("deja") - 0.2 else "worry", look=(-0.8, 0), arms="up" if t > w("gritarle") - 0.2 else "hold", **ABUELA)
    camandula(c, 420, 930, 0.6, t, lit=7)
FOCUS["u08"] = (480, 600)

def u09(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#08060a", "#000")
    rect(c, 240, 100, 600, 900, "#020101")
    gr = t > w("grueso") - 0.2
    L.pollo_cuerpo(c, 540, 1040, 0.66, t, cara="sombra", alas="plegadas", glow_a=0.5)
    if gr: ondas(c, 540, 380, t * 0.6, "#c0121a", 3, 520, 0.9, 1.0, 0.5)
    else: ondas(c, 540, 380, t, "#ffd21a", 3, 300, 0.7, 1.0, 1.0)
    bust_back(c, 540, 1240, 0.75, t, shirt=TIO["shirt"], hair=TIO["hair_col"], skin=TIO["skin"], hood=False)
FOCUS["u09"] = (540, 520)
CAM["u09"] = [(0.0, 1.0, 540, 540), ("ronco", 1.3, 540, 440)]

def u10(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#020203", "#000")
    off = t > w("luz") - 0.1
    if not off:
        cuarto(c, t, lamp=0.3)
    else:
        al = t > w("alas") - 0.2
        if al:
            ph = (t - w("alas")) * 2.2
            for k in range(3):
                x = 540 + math.sin(ph + k * 2.1) * 380; y = 520 + math.cos(ph * 1.3 + k) * 200
                c.save(); c.translate(x, y); c.rotate(math.sin(ph + k) * 0.6)
                for j in range(9): L._pluma(c, 0, 0, -math.pi / 2 - 1.2 + j * 0.3, 300, 30, "#0e0a08", "#2a2018")
                c.restore()
            flick = abs(math.sin(t * 23)) > 0.85
            if flick: overlay(c, "#ffffff", 0.08)
            plumas(c, t, 16, 9, 0.9)
        if t > w("grita") - 0.2 and t < w("nada") - 0.1:
            c.save(); c.translate(540, 980); c.scale(0.9, 0.9)
            bust(c, 0, 0, 0.9, t, "shock", look=(0, -1), arms="up", shake=1.0, gray=True, **TIO); c.restore()
            overlay(c, "#000", 0.55)
FOCUS["u10"] = (540, 560)

def u11(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#020203", "#000")
    on = t > w("linterna") - 0.2
    if on:
        c.save(); c.new_path(); c.arc(540, 760, 380, 0, 2 * math.pi); c.clip()
        rect(c, 0, 0, P, P, "#3a2a1a")
        for k in range(10): rect(c, k * 110, 0, 6, P, hx("#000", 0.5))
        if t > w("machete") - 0.2: machete(c, 380, 900, 0.9, 1.3)
        r = random.Random(12)
        if t > w("plumas") - 0.2:
            for k in range(14):
                c.save(); c.translate(r.uniform(220, 860), r.uniform(500, 1040)); c.rotate(r.uniform(0, 6.3))
                ell(c, 0, 0, 12, 40, "#0a0604"); line(c, [(0, -40), (0, 46)], "#4a3a2a", 2); c.restore()
        if t > w("cartas") - 0.2:
            for k in range(9): carta(c, r.uniform(260, 820), r.uniform(560, 1000), 1.1, r.uniform(-1, 1), True, k)
        c.restore()
        glow(c, 540, 760, 420, "#fff8d0", 0.18)
FOCUS["u11"] = (540, 760)

def u12(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#050403", "#000")
    rect(c, 0, 0, P, 300, "#3a2a1a"); rect(c, 0, 290, P, 18, "#000")     # tabla de la cama encima
    glow(c, 540, 640, 420, "#fff8d0", 0.12)
    c.save(); c.translate(540, 700); c.rotate(-1.5708 * 0.0)
    if t > w("blanco") - 0.2: ojos_blanco(c, 0, 420, 0.95, t, talk=0.25 * abs(math.sin(t * 8)) if t > w("piar") - 0.1 else 0, **VALE)
    else: bust(c, 0, 420, 0.95, t, "scared", look=(0, -0.5), shake=0.8, **VALE)
    c.restore()
    if t > w("piar") - 0.2: ondas(c, 540, 700, t, "#ffd21a", 3, 360, 0.8)
FOCUS["u12"] = (540, 600)
CAM["u12"] = [(0.0, 1.0, 540, 540), ("blanco", 1.3, 540, 560)]

def u13(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#050403", "#000"); rect(c, 0, 0, P, 300, "#3a2a1a")
    ojos_blanco(c, 540, 1120, 0.95, t, **VALE); overlay(c, "#000", 0.5)

# ---------------- PARTE 3 ----------------
def carga(c, x, y, s, t, mood="worry", vale_mood="creepy", look=(0, 0), talk=0.0):
    """Tú con Valentina abrazada a la espalda (su carita asoma por tu hombro)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    bust(c, 150, -330, 0.5, t + 3, vale_mood, look=(0, -5.2) if vale_mood == "creepy" else (-0.5, 0), **VALE)
    c.restore()
    bust(c, x, y, s, t, mood, look=look, arms="hold", talk=talk, **YOU)
    c.save(); c.translate(x, y); c.scale(s, s)
    for sx in (-1, 1): line(c, [(sx * 120 + 150 * 0, -300), (sx * 60, -230)], VALE["shirt"], 30)   # bracitos al cuello
    c.restore()

def v01(c, t, T, w):
    trocha(c, t, curve=False)
    casa(c, 900, 600, 0.22, t)
    p = ease(clamp(t / T))
    carga(c, 540 - 40 * p, 1140 - 20 * p, 0.85, t, "shock", vale_mood="creepy", look=(0, 0))
FOCUS["v01"] = (540, 640)

def v02(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0a0f14", "#000")
    bust(c, 420, 1150, 1.15, t, "scared", look=(0.7, 0), **YOU)
    c.save(); c.translate(760, 820)
    ojos_blanco(c, 0, 240, 0.85, t, talk=0.2 * abs(math.sin(t * 7)), **VALE); c.restore()
    if t > w("piando") - 0.2: ondas(c, 620, 620, t, "#ffd21a", 3, 120, 0.7, 1.0, 1.4)
FOCUS["v02"] = (560, 600)

def v03(c, t, T, w):
    trocha(c, t, curve=True)
    dl = t > w("delante") - 0.2
    if dl:
        ondas(c, 780, 590, t, "#ffd21a", 3, 220, 1.0, 0.7)
        for sx in (-1, 1): glow(c, 780 + sx * 14, 560, 30, "#ffd21a", 0.8); circ(c, 780 + sx * 14, 560, 4, "#fff2a0")
    carga(c, 360, 1110, 0.7, t, "shock" if dl else "worry", look=(0.8, -0.3))
FOCUS["v03"] = (640, 620)
CAM["v03"] = [(0.0, 1.0, 540, 540), ("delante", 1.4, 720, 560)]

def v04(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#d8b890", "#8a6a4a")
    bust(c, 540, 1110, 1.1, t, "angry", look=(0, 0), **ABUELA)
    line(c, [(760, 900), (800, 700)], ABUELA["skin"], 34); circ(c, 800, 690, 24, ABUELA["skin"]); line(c, [(800, 680), (806, 600)], ABUELA["skin"], 18)   # dedo
    sepia(c, 0.6)
    if t > w("desgracia") - 0.2: overlay(c, "#3a0000", 0.25)
FOCUS["v04"] = (540, 600)

def v05(c, t, T, w):
    op = ease(clamp((t - w("escaparate") + 0.1) / 0.8))
    cuarto(c, t, lamp=0.4, bed=False, open_esc=op)
    if op > 0:
        rect(c, 700, 270, 280, 580, "#100804")
        poly(c, [(700, 270), (700 - 240 * op, 230), (700 - 240 * op, 890), (700, 850)], "#5a3620")
        bust(c, 840, 980, 0.6, t, "sad", look=(-0.6, 0.3), tears=1.0, shake=0.5, **VALE)
    carga(c, 300, 1100, 0.7, t, "shock" if t > w("verdad") - 0.2 else "worry", look=(1, 0))
FOCUS["v05"] = (600, 640)
CAM["v05"] = [(0.0, 1.0, 540, 540), ("verdad", 1.3, 760, 600)]

def v06(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0e0a08", "#000")
    glow(c, 540, 560, 500, "#ffb060", 0.1)
    c.save(); c.translate(540, 1120); c.scale(1.05, 1.05)
    circ(c, 160, -560, 120, "#050304"); poly(c, [(80, -620), (110, -760), (150, -640)], "#050304"); poly(c, [(170, -640), (230, -760), (240, -610)], "#050304")
    for sx in (-1, 1): glow(c, 160 + sx * 40, -580, 40, "#ffd21a", 0.7); circ(c, 160 + sx * 40, -580, 6, "#fff2a0")
    c.restore()
    bust(c, 540, 1120, 1.05, t, "shock", look=(0.9, -0.3), shake=0.5, **YOU)
FOCUS["v06"] = (560, 560)
CAM["v06"] = [(0.0, 1.0, 540, 540), ("espalda", 1.3, 680, 460)]

def v07(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0a0806", "#000")
    glow(c, 540, 400, 600, "#ffb21a", 0.12)
    L.pollo_cuerpo(c, 600, 1500, 0.9, t, alas="envuelve" if t > w("alas") - 0.2 else "plegadas")
    bust(c, 480, 1140, 0.95, t, "shock", look=(0, -0.3), shake=1.0, **YOU)
    if t > w("garras") - 0.2:
        garra(c, 330, 800, 0.75, 0.25); garra(c, 630, 800, 0.75, -0.25)
        for k in range(3): line(c, [(300 + k * 26, 880), (296 + k * 26, 930)], "#a01010", 6); line(c, [(610 + k * 26, 880), (606 + k * 26, 930)], "#a01010", 6)
FOCUS["v07"] = (540, 520)
CAM["v07"] = [(0.0, 1.0, 540, 540), ("murciélago", 1.3, 600, 380)]

def v08(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0a0604", "#000")
    glow(c, 540, 520, 600, "#ffb21a", 0.2)
    plumas(c, t, 8, 3)
    sh = 8 * math.sin(t * 30) if t > w("cuál") - 0.1 else 0
    L.icono("El Pollo Maligno", c, 540 + sh, 540, 1.75, t)
FOCUS["v08"] = (540, 520)
CAM["v08"] = [(0.0, 1.0, 540, 540), ("cuál", 1.2, 540, 560)]

def v09(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0e0a08", "#000")
    bust(c, 540, 1110, 1.15, t, "sad", look=(0, 0.2), tears=1.0, **YOU)
    c.save(); c.translate(540, 1110); c.scale(1.15, 1.15)
    for sx in (-1, 1):
        for k in range(6): L._pluma(c, sx * 180, -260, math.pi / 2 + sx * (0.2 + k * 0.08), 300, 34, "#0a0604", "#3a2a1a")
    c.restore()
FOCUS["v09"] = (540, 600)

def v10(c, t, T, w):
    noche(c, t, y0=640, cafe=False)
    casa(c, 540, 1060, 1.1, t, light=0.5)
    ab = t > w("abren") - 0.1
    if not ab:
        L.pollo_cuerpo(c, 620, 1060, 0.42, t, alas="envuelve")
    else:
        p = ease(clamp((t - w("abren")) / 2.5))
        L.pollo_cuerpo(c, 620 + 240 * p, 1060 - 900 * p, 0.42 - 0.3 * p, t, alas="abiertas")
        plumas(c, t, 8, 5, 0.8, 400, 900)
    bust(c, 260, 1060, 0.4, t, "sad" if ab else "worry", look=(0.8, -0.3), tears=1.0 if ab else 0, arms="hold", **ABUELA)
    vela(c, 380, 1060, 0.5, t)
FOCUS["v10"] = (540, 760)

def amanecer(c, t):
    vgrad(c, 0, 0, P, 600, "#e8a070", "#8a9ab0")
    circ(c, 200, 560, 90, "#ffd0a0"); glow(c, 200, 560, 300, "#ffd0a0", 0.3)
    poly(c, [(0, 520), (200, 420), (420, 500), (680, 400), (P, 480), (P, 600), (0, 600)], "#6a7a7a")
    vgrad(c, 0, 600, P, 480, "#3a5a3a", "#1a2a1a")
    for row in range(5):
        yy = 640 + row * 90
        for k in range(9):
            x = (k * 140 + row * 70) % 1200 - 60
            ell(c, x, yy, 70 + row * 10, 34 + row * 6, "#2a4a2a" if row % 2 else "#335a33")
            for j in range(3): circ(c, x - 30 + j * 30, yy - 10, 6, "#c02020")

def v11(c, t, T, w):
    amanecer(c, t)
    guamo(c, 620, 1000, 1.2, "#2a2a1a")
    r = random.Random(8)
    if t > w("guamo") - 0.3:
        for k in range(12):
            c.save(); c.translate(r.uniform(360, 900), r.uniform(940, 1040)); c.rotate(r.uniform(0, 6.3))
            ell(c, 0, 0, 10, 34, "#0a0604"); c.restore()
        c.save(); c.translate(520, 1000)   # tu gorro naranja en el suelo
        c.new_path(); c.arc(0, 0, 70, math.pi, 2 * math.pi); c.close_path(); fill(c, YOU["cap_col"])
        rect(c, -72, -6, 144, 24, "#c85a1a"); circ(c, 0, -74, 18, YOU["cap_col"]); c.restore()
        machete(c, 760, 1020, 0.6, 1.4)
    if t > w("sangre") - 0.2: overlay(c, "#3a0000", 0.15)
FOCUS["v11"] = (600, 900)
CAM["v11"] = [(0.0, 1.0, 540, 540), ("plumas", 1.4, 560, 900)]

def v12(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#e8d0a8", "#a88a60")
    casa(c, 540, 1040, 1.0, t, light=0.0)
    gr = t > w("valentina") - 0.3
    if not gr:
        mesa(c, 540, 980, 0.8, t, up=0.0)
        overlay(c, "#000", 0.2)
    else:
        bust(c, 380, 1110, 0.8, t, "worry", look=(0.6, 0.3), **VALE_GRANDE)
        bust(c, 720, 1110, 0.55, t, "shock" if t > w("tapa") - 0.2 else "happy", look=(-0.6, 0), **NIETO)
        if t > w("tapa") - 0.2:
            line(c, [(500, 900), (690, 870)], VALE_GRANDE["shirt"], 40); ell(c, 712, 900, 40, 30, VALE_GRANDE["skin"])
        if t > w("reza") - 0.2: camandula(c, 380, 840, 0.4, t, lit=9)
FOCUS["v12"] = (540, 760)

def v13(c, t, T, w):
    noche(c, t, y0=640)
    guamo(c, 700, 1080, 1.3)
    L.pollo_cuerpo(c, 640, 440, 0.2, t, cara="sombra")
    overlay(c, "#000", 0.4)

PANELS = {k: v for k, v in globals().items() if len(k) == 3 and k[0] in "tuv" and k[1:].isdigit() and callable(v)}

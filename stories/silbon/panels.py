import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect_path, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp, text_w, tranquera
from povlib import *
from scenes import popin, tag2, bust_back, sepia
import leyendas as L
import guion as G

YOU = dict(hat="beanie", skin="#c48a5c", shirt="#3c6a9a", cap_col="#e8702a")
PRIMO = dict(hat="hair", skin="#a8704a", shirt="#b83a2a", hair_col="#1a120e", mole=True, pants="#3a4a6a")
ABUELA = dict(hat="bun", glasses="#8a6a4a", skin="#a87a54", shirt="#3a6a5a", hair_col="#d8d8d0")
PAPA = dict(hat="none", skin="#a8704a", shirt="#3a5a8a", hair_col="#1a120e", mustache=True)
FOCUS = {}; CAM = {}

def big(c, s_, x, y, col="#ffffff", size=120):
    ui(c, size); w_ = text_w(c, s_); c.new_path(); c.move_to(x - w_ / 2, y); c.text_path(s_)
    c.set_line_width(16); c.set_line_join(cairo.LINE_JOIN_ROUND); src(c, "#000"); c.stroke_preserve(); src(c, col); c.fill()

# ---------------- utilería ----------------
def palma(c, x, y, s, col="#060a08", t=0.0):
    """Palma de moriche: tronco recto altísimo y abanico de hojas en punta."""
    def f():
        line(c, [(0, 0), (6, -380), (0, -760)], col, 30)
        for k in range(15):
            a = -math.pi * (0.05 + 0.9 * k / 14) + math.sin(t * 0.8 + k) * 0.02
            L_ = 220 + 60 * math.sin(k * 1.7) ** 2
            poly(c, [(0, -760), (math.cos(a - 0.05) * L_, -760 + math.sin(a - 0.05) * L_ * 0.8), (math.cos(a) * (L_ + 50), -760 + math.sin(a) * (L_ + 50) * 0.8 + 40),
                     (math.cos(a + 0.05) * L_, -760 + math.sin(a + 0.05) * L_ * 0.8)], col)
        for k in range(5): ell(c, -20 + k * 10, -730, 14, 22, col)
    scaled(c, x, y, s, f)

def llano(c, t, y0=640, luna=True, palmas=True, sky=("#05070f", "#1a2232"), grass=("#0e1a10", "#030604")):
    vgrad(c, 0, 0, P, y0, *sky)
    r = random.Random(3)
    for k in range(50): circ(c, r.uniform(0, P), r.uniform(0, y0 - 80), r.uniform(1, 2.5), hx("#ffffff", r.uniform(0.2, 0.6) * (0.7 + 0.3 * math.sin(t + k))))
    if luna: circ(c, 820, 170, 44, "#eef0f4"); glow(c, 820, 170, 300, "#dfe8ff", 0.2)
    vgrad(c, 0, y0, P, P - y0, *grass)
    if palmas:
        for px, ps in ((90, 0.32), (180, 0.26), (930, 0.3), (1010, 0.22), (640, 0.16)): palma(c, px, y0 + 6, ps, "#05080a", t)
    for k in range(60):   # paja de sabana
        gx = r.uniform(0, P); gy = r.uniform(y0 + 10, P); hgt = 8 + (gy - y0) * 0.06
        line(c, [(gx, gy), (gx + math.sin(t * 1.2 + k) * 3, gy - hgt)], hx("#1e3020", 0.8), 3)

def hamaca(c, x0, y0, x1, y1, t, swing=0.0, col="#c8302a", sag=140, primo=False):
    sw = math.sin(t * 1.6) * swing
    mx = (x0 + x1) / 2 + sw; my = max(y0, y1) + sag
    line(c, [(x0, y0), (x0 + 50, y0 + 30)], "#5a4a3a", 4); line(c, [(x1, y1), (x1 - 50, y1 + 30)], "#5a4a3a", 4)
    c.new_path(); c.move_to(x0 + 50, y0 + 30); c.curve_to(mx - 120, my + 30, mx + 120, my + 30, x1 - 50, y1 + 30)
    c.curve_to(mx + 100, my - 40, mx - 100, my - 40, x0 + 50, y0 + 30); c.close_path(); fill(c, col)
    for k in range(6): line(c, [(x0 + 70 + k * (x1 - x0 - 140) / 5, y0 + 40 + sag * 0.3), (x0 + 70 + k * (x1 - x0 - 140) / 5 + sw * 0.3, my + 10)], hx("#f0c040", 0.5), 3)
    return mx, my

def hato(c, x, y, s, t, light=1.0, hamacas=True, hueso_colgado=False):
    """Casa de hato llanero: bahareque blanco, techo de palma, corredor con horcones, hamaca y mechero."""
    def f():
        rect(c, -440, -330, 880, 330, "#cfc6b2"); rect(c, -440, -60, 880, 60, "#8a6a4a")
        for k in range(6): line(c, [(-420 + k * 160, -320), (-400 + k * 160, -60)], hx("#000", 0.07), 6)
        rect(c, -60, -250, 130, 250, "#3a2414"); rect(c, 180, -240, 140, 110, "#241608")
        rect(c, 190, -230, 120, 90, hx("#ffb860", 0.85 * light))
        poly(c, [(-520, -310), (520, -310), (420, -500), (-420, -500)], "#6a5230")                   # techo de palma
        r = random.Random(4)
        for k in range(40): line(c, [(-510 + k * 26, -310 + r.uniform(0, 18)), (-410 + k * 21, -500)], hx("#3a2a14", 0.8), 4)
        for k in (-480, -240, 300, 480): rect(c, k - 12, -320, 24, 320, "#3a2410")                   # horcones
        if hamacas:
            hamaca(c, -470, -260, -250, -260, t, 0.3, "#c8302a", 90)
            if hueso_colgado:
                line(c, [(-360, -180), (-360, -130)], "#3a2a1a", 3); c.save(); c.translate(-360, -112); c.rotate(math.sin(t * 2) * 0.2); hueso(c, 0, 0, 0.35, 1.5708); c.restore()
        if light:
            line(c, [(120, -310), (120, -280)], "#222", 3); poly(c, [(108, -280), (132, -280), (126, -250), (114, -250)], "#5a5a5a")
            ell(c, 120, -262, 6, 14, "#ffd070"); glow(c, 120, -262, 320, "#ffb060", 0.3 * light)
    scaled(c, x, y, s, f)

def hueso(c, x, y, s, rot=0.0, col="#e2d6b4", glow_a=0.0):
    """Hueso largo (canilla) con nudos en las puntas."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if glow_a: glow(c, 0, 0, 260, "#ffffff", 0.35 * glow_a)
    line(c, [(-150, 0), (150, 0)], "#2a2010", 40); line(c, [(-150, 0), (150, 0)], col, 30)
    for sx in (-1, 1):
        circ(c, sx * 160, -16, 26, "#2a2010"); circ(c, sx * 160, 16, 26, "#2a2010")
        circ(c, sx * 160, -16, 21, col); circ(c, sx * 160, 16, 21, col)
    line(c, [(-120, -6), (120, -6)], hx("#ffffff", 0.35), 5); line(c, [(-100, 8), (90, 9)], hx("#8a7a5a", 0.4), 3)
    c.restore()

def notas(c, x0, y0, t, t0, col="#ffffff", dx=70, dy=-46, s=1.0, a=1.0, n=7, gap=0.3):
    """La escala que sube: do, re, mi, fa, sol, la, si (notas musicales que aparecen una a una)."""
    for k in range(n):
        tk = t - t0 - k * gap
        if tk < 0: continue
        al = a * clamp(tk / 0.15) * clamp(1.6 - tk * 0.25)
        if al <= 0: continue
        x = x0 + k * dx * s + math.sin(t * 3 + k) * 6 * s; y = y0 + k * dy * s - tk * 10 * s
        glow(c, x, y, 60 * s, col, 0.35 * al)
        c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-0.35)
        ell(c, 0, 0, 20, 14, hx(col, al)); c.restore()
        line(c, [(x + 17 * s, y - 4 * s), (x + 17 * s, y - 70 * s)], hx(col, al), 5 * s)
        line(c, [(x + 17 * s, y - 70 * s), (x + 40 * s, y - 50 * s)], hx(col, al), 5 * s)

def perra(c, x, y, s, t, modo="parada", flip=False):
    """Lucero, perra criolla caramelo. modo: parada | ladra | esconde | aulla | corre | muerde"""
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    if modo == "esconde": c.translate(math.sin(t * 50) * 3, 0)
    body, dark = "#b8844a", "#6a4a2a"
    low = 50 if modo == "esconde" else 0
    ph = t * 14 if modo == "corre" else 0
    for k, lx in enumerate((-80, -50, 60, 90)):   # patas
        sw = math.sin(ph + k * 1.6) * 30 if modo == "corre" else 0
        line(c, [(lx, -110 + low), (lx + sw, -4)], dark if k % 2 else body, 18)
        ell(c, lx + sw + 6, -4, 14, 7, dark)
    ell(c, 0, -125 + low, 120, 50 - low * 0.2, body); ell(c, -10, -105 + low, 90, 26, hx("#e8c890", 0.5))
    tail = [(-110, -140 + low), (-170, -200 + low)] if modo not in ("esconde",) else [(-110, -120 + low), (-90, -60 + low)]
    line(c, tail, body, 14)
    if modo == "aulla": hxp, hyp, ang = 120, -230, -1.1
    elif modo == "muerde": hxp, hyp, ang = 140, -110, 0.35
    elif modo == "esconde": hxp, hyp, ang = 120, -120, 0.2
    else: hxp, hyp, ang = 120, -180 + (math.sin(t * 18) * 5 if modo == "ladra" else 0), 0.0
    line(c, [(80, -140 + low), (hxp, hyp)], body, 50)
    c.save(); c.translate(hxp, hyp); c.rotate(ang)
    circ(c, 0, 0, 44, body)
    poly(c, [(-30, -20), (-10, -78 if modo != "esconde" else -30), (14, -30)], dark)       # oreja
    op = (0.6 + 0.4 * abs(math.sin(t * 16))) if modo in ("ladra", "muerde") else (0.8 if modo == "aulla" else 0.0)
    ell(c, 48, 6, 36, 20, body); circ(c, 82, 0, 9, "#120a06")
    if op: poly(c, [(20, 14), (84, 10 + 26 * op), (30, 30)], "#5a1a1a"); line(c, [(30, 18 + 6 * op), (82, 16 + 24 * op)], "#f4f0e0", 3)
    circ(c, 10, -12, 8, "#120a06"); circ(c, 12, -14, 3, "#ffffff")
    if modo == "esconde": line(c, [(0, -24), (20, -18)], "#120a06", 3)
    c.restore(); c.restore()

def totuma(c, x, y, s, t):
    """Totuma (media calabaza) llena de ají pique."""
    def f():
        c.new_path(); c.arc(0, 0, 110, 0, math.pi); c.close_path(); fill(c, "#6a4a1a")
        c.new_path(); c.arc(0, 0, 100, 0, math.pi); c.close_path(); fill(c, "#8a6a2a")
        ell(c, 0, 0, 110, 22, "#3a2a10"); ell(c, 0, -2, 100, 18, "#b01a0a")
        r = random.Random(2)
        for k in range(9):
            c.save(); c.translate(-80 + k * 20, -8 - (k % 3) * 8); c.rotate(r.uniform(-0.8, 0.8))
            poly(c, [(-8, 0), (8, 0), (0, 40)], "#e0200a"); line(c, [(0, 0), (0, -12)], "#2a6a1a", 4); c.restore()
    scaled(c, x, y, s, f)

def mandador(c, x, y, s, rot, t, crack=0.0, tip=None):
    """Mandador llanero: cabo de madera y rejo trenzado. crack>0: el rejo se estira y revienta."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rrect(c, -16, -10, 160, 26, 10, "#5a3a1a"); line(c, [(0, 3), (140, 3)], hx("#2a1a0a", 0.6), 3)
    if crack > 0:
        pts = [(140, 3)]
        for k in range(1, 9):
            f = k / 8; pts.append((140 + 620 * f * crack, 3 - math.sin(f * math.pi) * 120 * (1 - crack) + math.sin(f * 9 + t * 20) * 14))
        line(c, pts, "#3a2410", 10); glow(c, pts[-1][0], pts[-1][1], 90, "#fff4c0", 0.6 * crack)
    else:
        pts = [(140, 3), (200, 60), (170, 130), (110, 150), (60, 120)]
        line(c, pts, "#3a2410", 9)
    c.restore()

def ventana(c, x, y, s, t, open_=0.0, lit=0.0):
    """Ventana de madera vista desde adentro; open_ = cuánto se abre el postigo."""
    def f():
        rect(c, -160, -220, 320, 440, "#2a1a0e"); rect(c, -150, -210, 300, 420, "#05070c")
        if lit: glow(c, 0, 0, 260, "#dfe8ff", 0.2 * lit)
        w_ = 150 * (1 - 0.85 * open_)
        rect(c, -150, -210, 150, 420, "#5a3a1e"); rect(c, 0 + (150 - w_), -210, w_, 420, "#6a4424")
        for yy in (-150, -50, 50, 150): line(c, [(-140, yy), (-10, yy)], hx("#2a1a0e", 0.6), 4)
        line(c, [(-4, -210), (-4, 210)], "#1a0e06", 8)
    scaled(c, x, y, s, f)

def adentro(c, t, lamp=1.0):
    vgrad(c, 0, 0, P, P, "#3e3428", "#14100c")
    for k in range(6): line(c, [(40 + k * 190, 40), (60 + k * 190, 400), (44 + k * 190, 760)], hx("#000", 0.15), 5)
    rect(c, 0, 860, P, 220, "#3a2a18")
    if lamp: glow(c, 200, 300, 520, "#ffb060", 0.28 * lamp)

def piso_huesos(c, t, n, t_last=None, nuevo=False, mano=True, luz=("#1a1c24", "#07080c"), x0=150):
    """El conteo: huesos puestos en fila en el piso, uno por uno, por una mano de raíces."""
    vgrad(c, 0, 0, P, P, *luz)
    rect(c, 0, 0, P, 330, "#2a1a0e"); rect(c, 0, 320, P, 18, "#000")                       # la puerta, arriba
    for k in range(6): rect(c, k * 190, 0, 8, 320, hx("#000", 0.4))
    rect(c, 0, 338, P, 18, hx("#dfe8ff", 0.25))                                                 # luz por debajo de la puerta
    for k in range(12): line(c, [(0, 420 + k * 60), (P, 400 + k * 62)], hx("#000", 0.18), 3)   # tablas del piso
    pos = []
    for k in range(n):
        row = k // 6; col = k % 6
        pos.append((x0 + col * 165 + (row % 2) * 40, 470 + row * 78))
    for k, (bx, by) in enumerate(pos):
        last = nuevo and k == n - 1
        hueso(c, bx, by, 0.4, math.sin(k * 2.3) * 0.08, "#f8f6ee" if last else "#cfc3a0", glow_a=(0.8 + 0.2 * math.sin(t * 6)) if last else 0.0)
    if mano and pos:
        hx_, hy_ = pos[-1]
        reach = 1.0 if t_last is None else clamp(1 - (t - t_last) / 0.5) * 0.6 + 0.4
        tx, ty = hx_ + 10, hy_ - 10 - 240 * (1 - reach)
        line(c, [(tx + 160, -40), (tx + 100, ty - 260), (tx + 20, ty - 60)], "#2a2014", 34); line(c, [(tx + 160, -40), (tx + 100, ty - 260), (tx + 20, ty - 60)], "#8a7a58", 26)
        L._raices(c, tx + 20, ty - 60, math.pi / 2 + 0.3, t, 150, 5, "#8a7a58", 3)

def conteo(t, words_t):
    """Cuántos huesos van según las palabras ya dichas."""
    return sum(1 for wt in words_t if t > wt)

def mecedora(c, x, y, s, front=False):
    def f():
        if not front:
            rect(c, -190, -560, 380, 420, "#5a3a1a"); rect(c, -170, -540, 340, 380, "#7a5a2a")
            for k in range(8): line(c, [(-170 + k * 48, -540), (-170 + k * 48, -160)], hx("#3a2410", 0.6), 4)
        else:
            for sx in (-1, 1): rect(c, sx * 230 - 20, -240, 40, 200, "#5a3a1a"); rect(c, sx * 230 - 40, -260, 80, 30, "#6a4a22")
            c.new_path(); c.arc(0, -900, 960, math.pi * 0.42, math.pi * 0.58); c.set_line_width(26); src(c, "#4a2e14"); c.stroke()
    scaled(c, x, y, s, f)

def abuela_mecedora(c, x, y, s, t, mood="tired", gray=False, mandador_=True, tears=0.0):
    mecedora(c, x, y + 120 * s, s)
    bust(c, x, y, s, t, mood, look=(0, 0.4), arms="hold", gray=gray, tears=tears, **ABUELA)
    if mandador_: mandador(c, x - 160 * s, y - 50 * s, s * 0.9, 0.05, t)
    mecedora(c, x, y + 120 * s, s, front=True)

# ---------------- PARTE 1 ----------------
R = G.RULETA
def t00(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#140c06", "#030202")
    tt = t - R["start"]
    L.ruleta(c, 540, 600, 410, max(0, tt), R["dur"], R["target"], win=clamp((tt - R["dur"]) / 0.3))
FOCUS["t00"] = (540, 560)
CAM["t00"] = [(0.0, 1.0, 540, 560)]

def t01(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#160806", "#020101")
    glow(c, 540, 460, 540, "#ff2a0a", 0.2)
    notas(c, 120, 900, t, 0.0, "#ff3a1a", 60, -70, 0.8, 0.5)
    sc = 0.4 + 0.75 * ease(clamp(t / 0.5))
    L.icono("El Silbón", c, 540, 470, sc, t)
    big(c, "EL SILBÓN", 540, 1010, "#ff4a2a", 110)
FOCUS["t01"] = (540, 500)
CAM["t01"] = [(0.0, 1.0, 540, 540)]

def t02(c, t, T, w):
    llano(c, t, y0=600)
    hato(c, 640, 900, 0.9, t)
    p = clamp((t - w("jhon") + 0.3) / 3.0)
    if t > w("jhon") - 0.3:
        x = 120 + 300 * p
        bust(c, x, 920, 0.3, t, "happy", look=(0.6, 0), **PRIMO)
        c.save(); c.translate(x + 70, 880); c.rotate(0.5 + 0.2 * math.sin(t * 3)); rect(c, -12, -60, 24, 70, hx("#e8f0f0", 0.7)); c.restore()   # la botella
FOCUS["t02"] = (500, 760)

def t03(c, t, T, w):
    llano(c, t, y0=520, palmas=True)
    overlay(c, "#000", 0.25)
    bust(c, 540, 1110, 1.05, t, "smile" if t < w("humana") - 0.2 else "happy", look=(0, 0.6), arms="hold", **PRIMO)
    if t > w("camisa") - 0.3:
        hueso(c, 540, 1060, 0.95, 0.15 * math.sin(t * 2), glow_a=0.6 if t > w("humana") - 0.2 else 0.0)
FOCUS["t03"] = (540, 760)
CAM["t03"] = [(0.0, 1.0, 540, 540), ("canilla", 1.3, 540, 760)]

def t04(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#1a140e", "#080604")
    glow(c, 760, 220, 420, "#ffb060", 0.25)
    rect(c, 40, 0, 40, P, "#3a2410"); rect(c, 1000, 0, 40, P, "#3a2410")
    mx, my = hamaca(c, 60, 300, 1020, 300, t, 0.0, "#c8302a", 220)
    line(c, [(720, 330), (720, 400)], "#3a2a1a", 4)
    c.save(); c.translate(720, 440); c.rotate(1.5708 + math.sin(t * 2) * 0.12); hueso(c, 0, 0, 0.5, 0); c.restore()
    bust(c, 330, 1110, 0.95, t, "happy", look=(0.5, -0.3), talk="auto", **PRIMO)
FOCUS["t04"] = (500, 600)

def t05(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#2a1e16", "#0a0604")
    glow(c, 800, 300, 500, "#ffb060", 0.22)
    bust(c, 540, 1110, 1.15, t, "angry", look=(0, 0), talk="auto", **ABUELA)
    if t > w("costal") - 0.2: L.costal(c, 900, 900, 0.6, t)
FOCUS["t05"] = (540, 600)

def t06(c, t, T, w):
    llano(c, t, y0=560)
    bust(c, 300, 1110, 0.85, t, "smile", look=(0.7, -0.4), talk=0.15 if t > w("silba") - 0.2 and t < w("responde") else 0, **PRIMO)
    if t > w("silba") - 0.2: notas(c, 420, 640, t, w("silba"), "#ffffff", 60, -46, 0.8)
    if t > w("responde") - 0.3:
        notas(c, 640, 560, t, w("responde"), "#ff3a1a", 44, -34, 0.75, 1.0)
        for sx in (-1, 1): glow(c, 700 + sx * 10, 545, 24, "#ff2a0a", 0.7)
FOCUS["t06"] = (560, 560)
CAM["t06"] = [(0.0, 1.0, 540, 540), ("responde", 1.35, 680, 520)]

def t07(c, t, T, w):
    adentro(c, t, 0.7)
    ventana(c, 800, 500, 1.1, t, lit=0.5)
    if t > w("ventana") - 0.3: notas(c, 660, 560, t, w("ventana"), "#ff3a1a", 50, -36, 1.2)
    bust(c, 330, 1120, 1.0, t, "smile" if t > w("respira") - 0.1 else "worry", look=(0.7, 0), **ABUELA)
FOCUS["t07"] = (520, 600)

def t08(c, t, T, w):
    cerca = t > w("cerca") - 0.2
    if t < w("llorar") - 0.2:
        llano(c, t, y0=640)
        notas(c, 500, 630, t, w("suena"), "#ff3a1a", 14, -10, 0.22, 0.8)
    else:
        adentro(c, t, 0.5)
        ventana(c, 760, 460, 1.0, t, lit=0.3)
        if cerca:
            c.save(); c.rectangle(610, 250, 300, 420); c.clip()
            L.silbon_cuerpo(c, 770, 1600, 0.7, t, cara="sombra", con_costal=False); c.restore()
        bust(c, 380, 1120, 1.05, t, "scared" if cerca else "sad", look=(-0.3, 0.2), tears=1.0, **ABUELA)
FOCUS["t08"] = (540, 600)
CAM["t08"] = [(0.0, 1.0, 540, 540), ("cerca", 1.25, 640, 480)]

def t09(c, t, T, w):
    llano(c, t, y0=520, palmas=True); overlay(c, "#000", 0.35)
    rect(c, 0, 0, P, 120, "#3a2a14")
    hamaca(c, -40, 60, 620, 60, t, 0.2, "#c8302a", 200)
    calla = t > w("calla") - 0.2
    if calla: perra(c, 330, 860, 0.9, t, "esconde")
    else: perra(c, 420, 900, 1.1, t, "ladra")
FOCUS["t09"] = (480, 760)

def t10(c, t, T, w):
    toks = [w("tac") - 0.0] + [w("tac") + 0.45, w("tac") + 0.9, w("cuenta") - 0.2, w("cuenta") + 0.3, w("cuenta") + 0.8, w("cuenta") + 1.3]
    n = conteo(t, toks)
    last = max([x for x in toks if x < t], default=None)
    if n: piso_huesos(c, t, n, last)
    else: piso_huesos(c, t, 0, mano=False)
FOCUS["t10"] = (540, 560)

def t11(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#140c08", "#050302")
    glow(c, 800, 600, 400, "#ffb060", 0.2)
    bust(c, 540, 1110, 1.2, t, "worry", look=(0.2, 0.3), talk="auto", **ABUELA)
    if t > w("muere") - 0.2: overlay(c, "#200000", 0.25)
FOCUS["t11"] = (540, 600)

def rendija(c, t, x0=390, x1=690):
    vgrad(c, 0, 0, P, P, "#1a1008", "#0a0604")
    for k in range(14): line(c, [(k * 80, 0), (k * 80 + 10, P)], hx("#000", 0.3), 6)

def t12(c, t, T, w):
    rendija(c, t)
    c.save(); c.rectangle(400, 0, 280, P); c.clip()
    llano(c, t, y0=880, luna=False, palmas=False)
    palma(c, 430, 1000, 0.95, "#05080a", t)
    L.silbon_cuerpo(c, 560, 1060, 0.53, t, cara="sombra" if t < w("palma") - 0.2 else "monstruo", brazos="costal")
    c.restore()
    rect(c, 392, 0, 10, P, "#000"); rect(c, 678, 0, 10, P, "#000")
FOCUS["t12"] = (540, 400)
CAM["t12"] = [(0.0, 1.0, 540, 540), ("palma", 1.25, 540, 420)]

def t13(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#100404", "#000")
    glow(c, 540, 520, 600, "#ff2a0a", 0.2)
    sh = 8 * math.sin(t * 30) if t > w("falta") - 0.1 else 0
    L.icono("El Silbón", c, 540 + sh, 560, 1.75, t)
FOCUS["t13"] = (540, 520)
CAM["t13"] = [(0.0, 1.0, 540, 540), ("falta", 1.2, 540, 500)]

def t14(c, t, T, w):
    rendija(c, t)
    c.save(); c.rectangle(400, 0, 280, P); c.clip()
    llano(c, t, y0=880, luna=False, palmas=False)
    L.silbon_cuerpo(c, 560, 1060, 0.53, t, cara="sombra", brazos="costal"); c.restore()
    overlay(c, "#000", 0.45)

# ---------------- PARTE 2 ----------------
def u01(c, t, T, w):
    adentro(c, t, 0.4)
    bust(c, 540, 1120, 1.05, t, "worry", look=(0, 0.6), arms="hold", **YOU)
    vb = 5 * math.sin(t * 60) if t > w("vibra") - 0.2 else 0
    hueso(c, 540 + vb, 1070, 0.95, 0.1, col="#d8ccb0", glow_a=0.4)
    if t > w("vibra") - 0.2: notas(c, 640, 960, t, w("vibra"), "#ff3a1a", 30, -30, 0.5, 0.6)
FOCUS["u01"] = (540, 760)

def u02(c, t, T, w):
    adentro(c, t, 0.3)
    op = ease(clamp((t - w("abres") + 0.2) / 0.6)) * 0.35
    ventana(c, 760, 480, 1.25, t, open_=op, lit=0.3)
    ar = t > w("arranca") - 0.2
    if t > w("larguísima") - 0.3:
        reach = ease(clamp((t - w("larguísima") + 0.3) / 0.9))
        hx_ = 820 - 280 * reach; hy_ = 500 + 140 * reach
        if ar: hx_ += 300 * ease(clamp((t - w("arranca")) / 0.4))
        line(c, [(960, 430), (hx_, hy_)], "#2a2014", 40); line(c, [(960, 430), (hx_, hy_)], "#8a7a58", 30)
        L._raices(c, hx_, hy_, math.pi * 0.92, t, 200, 5, "#8a7a58", 4)
        if ar: hueso(c, hx_ + 30, hy_ + 20, 0.5, 0.4)
    bust(c, 300, 1130, 0.95, t, "shock" if ar else "worry", look=(0.8, -0.2), arms="hold" if not ar else "none", shake=0.6 if ar else 0, **YOU)
    if not ar: hueso(c, 380, 1080, 0.55, -0.3)
FOCUS["u02"] = (560, 600)

def u03(c, t, T, w):
    toks = [w("conteo"), w("tres"), w("cuatro"), w("cinco"), w("seis")]
    n = 25 + conteo(t, toks)
    last = max([x for x in toks if x < t], default=None)
    piso_huesos(c, t, n, last, x0=110)
FOCUS["u03"] = (540, 600)

def u04(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#1e160e", "#060402")
    glow(c, 760, 400, 400, "#ffb060", 0.2)
    bust(c, 540, 1110, 1.15, t, "smile" if t > w("aire") - 0.3 else "worry", look=(0, 0.3), **ABUELA)
FOCUS["u04"] = (540, 600)

def u05(c, t, T, w):
    nuevo = t > w("siete") - 0.2
    piso_huesos(c, t, 30 + (1 if nuevo else 0), w("siete") if nuevo else None, nuevo=nuevo, x0=110)
    if nuevo: overlay(c, "#300000", 0.25)
FOCUS["u05"] = (540, 600)
CAM["u05"] = [(0.0, 1.0, 540, 540), ("siete", 1.35, 700, 900)]

def u06(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#1a100a", "#050302")
    glow(c, 760, 600, 400, "#ffb060", 0.25)
    bust(c, 540, 1110, 1.15, t, "angry", look=(0, 0), talk="auto", **ABUELA)
FOCUS["u06"] = (540, 600)

def u07(c, t, T, w):
    adentro(c, t, 0.8)
    bust(c, 300, 1110, 0.95, t, "angry", look=(0.6, 0.3), **ABUELA)
    rect(c, 420, 880, 640, 30, "#5a3a1e"); rect(c, 440, 910, 24, 200, "#3a2410"); rect(c, 1010, 910, 24, 200, "#3a2410")
    if t > w("totuma") - 0.3: totuma(c, 600, 880, 1.0, t)
    if t > w("mandador") - 0.3: mandador(c, 780, 860, 0.9, -0.05, t)
    if t > w("perros") - 0.3: perra(c, 800, 1080, 0.7, t, "parada")
FOCUS["u07"] = (600, 760)

def u08(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#14100c", "#050302")
    rect(c, 0, 0, 40, P, "#3a2410"); rect(c, 1040, 0, 40, P, "#3a2410")
    hamaca(c, 20, 200, 1060, 200, t, 0.15, "#c8302a", 640)
    c.save(); c.translate(540, 860); c.rotate(-0.12)
    bust(c, 0, 220, 0.95, t, "tired", look=(0, 0.3), **PRIMO)
    poly(c, [(-80, -20), (80, -20), (0, 150)], PRIMO["skin"])                                   # camisa abierta
    mo = t > w("morado") - 0.3
    if mo: glow(c, 0, 110, 120, "#8a2aaa", 0.6); circ(c, 0, 110, 18, "#4a0a5a"); circ(c, 0, 110, 9, "#1a0020")
    c.restore()
FOCUS["u08"] = (540, 900)
CAM["u08"] = [(0.0, 1.0, 540, 540), ("morado", 1.45, 540, 900)]

def u09(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#1a0a0a", "#050101")
    glow(c, 540, 400, 500, "#8a2aaa", 0.12)
    bust(c, 540, 1110, 1.15, t, "angry", look=(0, 0), talk="auto", **ABUELA)
    if t > w("escogió") - 0.2: overlay(c, "#200000", 0.25)
FOCUS["u09"] = (540, 600)

def u10(c, t, T, w):
    adentro(c, t, 0.3)
    ab = t > w("abres") - 0.1
    bust(c, 540, 1110, 1.15, t, "shock" if ab else "tired", look=(0, 0.2), **YOU)
    if not ab:
        d = clamp((t - w("cierran") + 0.2) / 1.2) if t > w("cierran") - 0.2 else 0
        overlay(c, "#000", 0.95 * d)
FOCUS["u10"] = (540, 600)

def u11(c, t, T, w):
    llano(c, t, y0=600)
    p = clamp((t - w("sabana") + 0.3) / 6)
    L.silbon_cuerpo(c, 620 + 260 * p, 640, 0.15, t, cara="sombra", brazos="costal", mueve=1.0 if t > w("patalea") - 0.3 else 0.3)
    tranquera(c, 640, 860, 0.8, "#2a1a0e")
    perra(c, 760, 860, 0.6, t, "aulla", flip=False)
    rect(c, 0, 0, 40, P, "#3a2410")
    hamaca(c, 20, 140, 520, 140, t, 1.0, "#c8302a", 200)
FOCUS["u11"] = (660, 640)
CAM["u11"] = [(0.0, 1.0, 540, 540), ("sabana", 1.35, 760, 600)]

def u12(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#06070c", "#000")
    lej = t > w("lejísimos") - 0.2
    if lej:
        glow(c, 760, 420, 500, "#ff2a0a", 0.2)
        L.icono("El Silbón", c, 760, 430, 1.3, t)
        overlay(c, "#000", 0.15)
    bust(c, 400, 1120, 1.1, t, "scared" if not lej else "shock", look=(-0.4, 0) if not lej else (0.8, -0.3), shake=0.8 if lej else 0, **YOU)
    if t > w("silbido") - 0.2: notas(c, 560, 420, t, w("do"), "#ff3a1a", 26, -18, 0.4, 0.7, n=3)
FOCUS["u12"] = (560, 520)
CAM["u12"] = [(0.0, 1.0, 540, 540), ("lejísimos", 1.25, 680, 420)]

def u13(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#06070c", "#000")
    L.icono("El Silbón", c, 760, 430, 1.3, t)
    bust(c, 400, 1120, 1.1, t, "shock", look=(0.8, -0.3), **YOU)
    overlay(c, "#000", 0.5)

# ---------------- PARTE 3 ----------------
def v01(c, t, T, w):
    llano(c, t, y0=560)
    p = t / T
    x = 160 + 520 * p
    bust(c, x, 900, 0.42, t, "angry", look=(0.8, 0), arms="hold", **YOU)
    totuma(c, x, 880, 0.35, t)
    perra(c, x + 200, 1060, 0.55, t, "corre")
FOCUS["v01"] = (540, 760)

def morichal(c, t):
    llano(c, t, y0=700, palmas=False)
    for px, ps in ((80, 0.75), (230, 0.6), (980, 0.8), (870, 0.55)): palma(c, px, 760, ps, "#05080a", t)
    ell(c, 540, 860, 520, 70, "#0a1420"); ell(c, 540, 860, 480, 56, hx("#3a5a7a", 0.35))
    for k in range(6): line(c, [(200 + k * 120, 850 + (k % 2) * 10), (260 + k * 120, 850 + (k % 2) * 10)], hx("#dfe8ff", 0.25), 3)

def v02(c, t, T, w):
    morichal(c, t)
    L.silbon_cuerpo(c, 700, 1000, 0.48, t, cara="monstruo", brazos="costal", mueve=1.0 if t > w("mueve") - 0.3 else 0.2)
    bust(c, 210, 1110, 0.5, t, "scared", look=(0.8, -0.5), **YOU)
FOCUS["v02"] = (640, 520)
CAM["v02"] = [(0.0, 1.0, 540, 540), ("mueve", 1.3, 620, 560)]

def v03(c, t, T, w):
    morichal(c, t)
    gr = t > w("grita") - 0.2
    ard = clamp((t - w("piernas") + 0.1) / 0.6) if t > w("piernas") - 0.1 else 0
    L.silbon_cuerpo(c, 700, 1000, 0.48, t, cara="grita" if gr else "monstruo", brazos="arriba" if gr else "costal", mueve=1.0, ardor=ard, bend=-0.08 if gr else 0)
    if t > w("tiras") - 0.2:
        q = clamp((t - w("tiras") + 0.2) / 0.5); r = random.Random(4)
        for k in range(22):
            sx, sy = 260, 900; ex, ey = 680 + r.uniform(-60, 60), 760 + r.uniform(-120, 120)
            px = sx + (ex - sx) * q; py = sy + (ey - sy) * q - math.sin(q * math.pi) * 120
            circ(c, px, py, r.uniform(6, 12), "#e0200a")
    bust(c, 210, 1110, 0.5, t, "angry", look=(0.8, -0.3), arms="up" if t < w("piernas") + 0.4 else "none", **YOU)
FOCUS["v03"] = (640, 560)
CAM["v03"] = [(0.0, 1.0, 540, 540), ("grita", 1.3, 680, 380)]

def v04(c, t, T, w):
    morichal(c, t)
    hu = t > w("huye") - 0.2
    if not hu:
        L.silbon_cuerpo(c, 700, 1000, 0.48, t, cara="grita", brazos="costal", mueve=1.0, ardor=1.0, mordidas=1.0 if t > w("talones") - 0.2 else 0, bend=-0.12)
    else:
        p = ease(clamp((t - w("huye")) / 1.6))
        L.costal(c, 640, 960, 0.45, t, mueve=1.0)
        L.silbon_cuerpo(c, 760 + 500 * p, 1000, 0.48, t, cara="grita", brazos="arriba", con_costal=False, ardor=1.0, mordidas=1.0, bend=-0.2)
    crack = 0
    for k in ("revientas", "veces"):
        if w(k) - 0.15 < t < w(k) + 0.35: crack = clamp((t - w(k) + 0.15) / 0.2)
    bust(c, 200, 1110, 0.5, t, "angry", look=(0.8, -0.2), **YOU)
    mandador(c, 280, 960, 0.6, -0.15, t, crack=crack)
    if t > w("lucero") - 0.3: perra(c, 600, 1010, 0.45, t, "muerde")
FOCUS["v04"] = (600, 760)
CAM["v04"] = [(0.0, 1.0, 540, 540)]

def v05(c, t, T, w):
    morichal(c, t); overlay(c, "#000", 0.2)
    op = t > w("abres") - 0.2
    L.costal(c, 560, 1000, 0.7, t, mueve=0.0 if op else 0.5, abierto=op)
    if op:
        up = ease(clamp((t - w("jhon") + 0.2) / 0.8))
        c.save(); c.rectangle(0, 0, P, 900); c.clip()
        bust(c, 560, 1260 - 240 * up, 0.55, t, "scared", look=(-0.6, 0), shake=0.8, gray=True, tears=1.0, **PRIMO); c.restore()
    bust(c, 230, 1110, 0.6, t, "sad" if t > w("vivo") - 0.2 else "worry", look=(0.8, 0), tears=0.6 if t > w("vivo") - 0.2 else 0, **YOU)
FOCUS["v05"] = (480, 700)

def v06(c, t, T, w):
    llano(c, t, y0=620)
    hato(c, 860, 640, 0.18, t, light=0.3, hamacas=False)
    notas(c, 760, 560, t, w("lejos"), "#ff3a1a", 12, -9, 0.2, 0.9)
    sig = t > w("significa") - 0.2
    bust(c, 300, 1110, 0.85, t, "shock" if sig else "smile", look=(0.9, -0.3), shake=0.4 if sig else 0, **YOU)
    bust(c, 470, 1150, 0.7, t + 2, "tired", look=(-0.3, 0.4), gray=True, **PRIMO)
FOCUS["v06"] = (620, 600)
CAM["v06"] = [(0.0, 1.0, 540, 540), ("significa", 1.5, 820, 560)]

def v07(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0c1018", "#030406")
    rect(c, 0, 0, P, 90, "#3a2a14"); rect(c, 60, 0, 30, P, "#3a2410"); rect(c, 990, 0, 30, P, "#3a2410")
    abuela_mecedora(c, 600, 900, 0.75, t, "tired")
    if t > w("ronca") - 0.3: glow(c, 150, 400, 200, "#2a3050", 0.3)
    bust(c, 180, 1130, 0.6, t, "worry", look=(0.8, 0), **YOU)
FOCUS["v07"] = (560, 620)

def v08(c, t, T, w):
    piso_huesos(c, t, 31 if t > w("más") - 0.2 else 30, None, nuevo=t > w("más") - 0.2, mano=False, luz=("#28303e", "#0e1016"), x0=110)
FOCUS["v08"] = (540, 700)
CAM["v08"] = [(0.0, 1.0, 540, 540), ("blanco", 1.4, 700, 960)]

def v09(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#100404", "#000")
    glow(c, 540, 520, 600, "#ff2a0a", 0.18)
    sh = 6 * math.sin(t * 30) if t > w("contar") - 0.1 else 0
    L.icono("El Silbón", c, 540 + sh, 560, 1.75, t)
FOCUS["v09"] = (540, 520)
CAM["v09"] = [(0.0, 1.0, 540, 540), ("contar", 1.2, 540, 520)]

def v10(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#1a2030", "#06080c")
    abuela_mecedora(c, 560, 900, 0.8, t, "tired", gray=True)
    if t > w("esperando") - 0.3: bust(c, 200, 1140, 0.6, t, "sad", look=(0.8, -0.2), tears=1.0, **YOU)
FOCUS["v10"] = (540, 620)

def v11(c, t, T, w):
    vgrad(c, 0, 0, P, 600, "#e8a070", "#8a9ab0")
    circ(c, 180, 560, 90, "#ffd0a0"); glow(c, 180, 560, 300, "#ffd0a0", 0.3)
    vgrad(c, 0, 600, P, 480, "#5a6a3a", "#2a3a1a")
    for px, ps in ((80, 0.4), (960, 0.45), (870, 0.3)): palma(c, px, 640, ps, "#2a2a1a", t)
    line(c, [(540, 900), (540, 640)], "#4a3418", 24); line(c, [(450, 720), (630, 720)], "#4a3418", 22)   # la cruz
    ell(c, 540, 920, 160, 30, "#4a3a22")
    totuma(c, 470, 910, 0.35, t); mandador(c, 560, 900, 0.4, 0, t)
    if t > w("vendió") - 0.3: bust(c, 820, 1110, 0.55, t, "sad", look=(-0.7, 0), **PAPA)
    if t > w("jhon") - 0.3: bust(c, 220, 1110, 0.55, t + 1, "sad", look=(0.7, 0), tears=0.6, **PRIMO)
FOCUS["v11"] = (540, 760)

def v12(c, t, T, w):
    llano(c, t, y0=640)
    L.silbon_cuerpo(c, 700, 660, 0.12, t, cara="sombra", brazos="costal")
    rect(c, 0, 0, 260, P, "#2a1a0e"); rect(c, 250, 0, 16, P, "#000")
    glow(c, 160, 700, 300, "#ffb060", 0.18)
    bust(c, 430, 1130, 0.8, t, "worry", look=(-0.8, 0), **YOU)
FOCUS["v12"] = (560, 640)

def v13(c, t, T, w):
    llano(c, t, y0=640)
    L.silbon_cuerpo(c, 640, 660, 0.14, t, cara="sombra", brazos="costal")
    overlay(c, "#000", 0.45)

PANELS = {k: v for k, v in globals().items() if len(k) == 3 and k[0] in "tuv" and k[1:].isdigit() and callable(v)}

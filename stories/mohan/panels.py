import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect_path, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp, text_w
from povlib import *
from scenes import popin, tag2, bust_back, sepia
import leyendas as L
import guion as G

YOU = dict(hat="beanie", skin="#a8704a", shirt="#3c6a9a", cap_col="#e8702a")
ROSA = dict(hat="bun", freckles=True, skin="#a8704a", shirt="#e8c860", hair_col="#1a120c")
PAPA = dict(hat="none", skin="#9a6440", shirt="#7a5a3a", hair_col="#2a2a2a", mustache=True)
TIA = dict(hat="bun", glasses="#5a3a2a", skin="#c8beb4", shirt="#d8d8d0", hair_col="#1a120c")
FOCUS = {}; CAM = {}

def big(c, s_, x, y, col="#ffffff", size=120):
    ui(c, size); w_ = text_w(c, s_); c.new_path(); c.move_to(x - w_ / 2, y); c.text_path(s_)
    c.set_line_width(16); c.set_line_join(cairo.LINE_JOIN_ROUND); src(c, "#000"); c.stroke_preserve(); src(c, col); c.fill()

# ---------------- escenarios ----------------
def rio(c, t, moon=True, y0=560, hills=True, sky=("#070b14", "#14221e")):
    vgrad(c, 0, 0, P, y0, *sky)
    if moon: circ(c, 860, 150, 44, "#eef0f4"); glow(c, 860, 150, 260, "#dfe8ff", 0.2)
    if hills:
        poly(c, [(0, y0 - 60), (180, y0 - 150), (380, y0 - 90), (620, y0 - 170), (860, y0 - 80), (P, y0 - 140), (P, y0), (0, y0)], "#08120c")
        r = random.Random(4)
        for k in range(9):   # palmas y guaduas en la otra orilla
            x = 40 + k * 125 + r.uniform(-20, 20); h = r.uniform(90, 170)
            line(c, [(x, y0 - 10), (x + 8, y0 - h)], "#060c08", 8)
            for a in (-2.6, -2.2, -1.6, -1.0, -0.5): line(c, [(x + 8, y0 - h), (x + 8 + math.cos(a) * 70, y0 - h + math.sin(a) * 40 + 30)], "#060c08", 7)
    vgrad(c, 0, y0, P, P - y0, "#1a2a2a", "#040808")
    for k in range(16):
        y = y0 + 20 + k * 30; w_ = 100 + (k * 41) % 220; x = (k * 197 + t * 40) % 1300 - 150
        rect(c, x, y, w_, 3, hx("#a8c8c0", 0.2))
    if moon:
        for k in range(6): rect(c, 820 + math.sin(t * 2 + k) * 20, y0 + 20 + k * 26, 80 - k * 8, 4, hx("#eef0f4", 0.35))

def piedras(c, y=900, n=7, seed=3):
    r = random.Random(seed)
    for k in range(n):
        x = 60 + k * (P / n) + r.uniform(-30, 30); rx = r.uniform(70, 120)
        ell(c, x, y + r.uniform(-20, 40), rx, rx * 0.45, r.choice(["#2a2c28", "#33362e", "#24261f"]))
        ell(c, x - rx * 0.25, y - rx * 0.12, rx * 0.4, rx * 0.12, hx("#8a9a88", 0.18))

def agua(c, t, level, a=1.0, col="#0a1814"):
    if level >= P: return
    c.new_path(); c.move_to(0, level)
    for k in range(25): c.line_to(k * 45, level + math.sin(t * 3 + k * 0.8) * 8)
    c.line_to(P, P); c.line_to(0, P); c.close_path(); src(c, hx(col, 0.9 * a)); c.fill()
    for k in range(6):
        y = level + 30 + k * 40
        if y < P: rect(c, (k * 170 + t * 50) % 1200 - 100, y, 140, 3, hx("#7aa8a0", 0.25 * a))

def remolino(c, x, y, t, r=300, a=1.0):
    for k in range(9):
        rr = r * (1 - k / 10); ph = t * (2 + k * 0.3)
        c.new_path(); c.save(); c.translate(x, y); c.scale(1, 0.32)
        c.arc(0, 0, rr, ph, ph + math.pi * 1.4); c.restore()
        c.set_line_width(6); src(c, hx("#9ac8c0", 0.35 * a * (1 - k / 10))); c.stroke()
    c.save(); c.translate(x, y); c.scale(1, 0.32); circ(c, 0, 0, r * 0.18, hx("#000", 0.85 * a)); c.restore()

def rancho(c, x, y, s, light=1.0):
    def f():
        rect(c, -260, -300, 520, 300, "#a08a6a")                              # bahareque
        for k in range(6): line(c, [(-240 + k * 90, -280), (-230 + k * 90, -20)], hx("#5a4a3a", 0.5), 4)
        poly(c, [(-320, -280), (0, -470), (320, -280)], "#6a5a2a")             # techo de palma
        for k in range(16): line(c, [(-320 + k * 40, -282), (-300 + k * 40, -250)], "#4a3a1a", 6)
        rect(c, -200, -220, 130, 110, "#2a1a10"); rect(c, -190, -210, 110, 90, hx("#ffc070", light))
        if light: glow(c, -135, -165, 200, "#ffb060", 0.3 * light)
        rect(c, 60, -200, 110, 200, "#4a2a18")
    scaled(c, x, y, s, f)

def canoa(c, x, y, s, t):
    def f():
        c.new_path(); c.move_to(-320, -40); c.curve_to(-200, 40, 200, 40, 320, -40); c.line_to(280, -60); c.line_to(-280, -60); c.close_path(); fill(c, "#4a2a14")
        line(c, [(-280, -60), (280, -60)], "#2a160a", 8)
    scaled(c, x, y + math.sin(t * 2) * 6, s, f)

def red(c, x, y, s, t, pelo=0.0, diente=0.0):
    """Atarraya (red de pesca) colgando; pelo verde enredado; diente de oro."""
    def f():
        pts = [(-200, -260), (200, -260), (300, 200), (-300, 200)]
        for k in range(11):
            fx_ = k / 10
            line(c, [(-200 + 400 * fx_, -260), (-300 + 600 * fx_, 200)], hx("#d8d0b8", 0.7), 3)
        for k in range(10):
            fy = k / 9; yy = -260 + 460 * fy; w_ = 200 + 100 * fy
            line(c, [(-w_, yy), (w_, yy)], hx("#d8d0b8", 0.6), 3)
        for k in range(9): circ(c, -300 + k * 75, 200, 10, "#6a6a6a")         # plomos
        if pelo:
            c.save(); c.translate(0, -60); L._musgo(c, 220 * pelo, -160, 220, int(34 * pelo) + 1, 31, t, 2.5); c.restore()
        if diente:
            glow(c, 40, 40, 140 * diente, "#ffd84a", 0.6 * diente)
            poly(c, [(20, 10), (60, 10), (52, 60), (40, 80), (28, 60)], "#e8c23a"); poly(c, [(26, 14), (40, 14), (34, 50)], "#fff4b0")
    scaled(c, x, y, s, f)

def notas(c, t, x0, y0, n=6, col="#ffd84a", rise=500):
    for k in range(n):
        a = (t * 0.4 + k / n) % 1
        x = x0 + math.sin(t * 1.5 + k * 2) * 120 + (k - n / 2) * 40; y = y0 - rise * a
        al = math.sin(a * math.pi)
        glow(c, x, y, 50, col, 0.3 * al)
        circ(c, x, y, 14, hx(col, al)); line(c, [(x + 12, y), (x + 12, y - 60)], hx(col, al), 5)
        line(c, [(x + 12, y - 60), (x + 36, y - 46)], hx(col, al), 5)

def tabaco_piedra(c, x, y, s, t, lleno=True):
    def f():
        ell(c, 0, 40, 260, 90, "#3a3a32"); ell(c, -40, 10, 200, 60, "#4a4a40"); ell(c, -60, 0, 100, 20, hx("#9aa890", 0.2))
        if lleno:
            line(c, [(-140, -10), (-20, -30)], "#3a220e", 26); line(c, [(-140, -16), (-20, -36)], "#5a3a1a", 8)
            rect(c, 60, -110, 60, 100, hx("#e8f0f0", 0.55)); rect(c, 66, -70, 48, 56, hx("#f0e8c8", 0.7))   # copa de aguardiente
    scaled(c, x, y, s, f)

def cuarto(c, t, lamp=1.0, ventana=True, open_=False):
    vgrad(c, 0, 0, P, P, "#5a4a3a", "#1e1810")
    for k in range(5): line(c, [(60 + k * 220, 60), (80 + k * 220, 300), (64 + k * 220, 420)], hx("#000", 0.2), 4)
    rect(c, 0, 840, P, 240, "#3a2a1a")
    for k in range(10): rect(c, k * 110, 840, 6, 240, hx("#000", 0.55))   # tablas con rendijas
    if ventana:
        rect(c, 640, 160, 320, 320, "#2a1a10")
        c.save(); c.rectangle(660, 180, 280, 280); c.clip(); c.translate(660, 180); c.scale(280 / P, 280 / P); rio(c, t); c.restore()
        if not open_:
            rect(c, 660, 180, 140, 280, "#5a3a22"); rect(c, 800, 180, 140, 280, "#4a2a18")
        else:
            poly(c, [(660, 180), (600, 150), (600, 500), (660, 460)], "#5a3a22")
    if lamp: rrect(c, 120, 600, 50, 80, 12, hx("#ffd890", 0.9 * lamp)); glow(c, 145, 620, 360, "#ffb060", 0.3 * lamp)

def mano(c, x, y, s, ang, t, col="#2a1a0c"):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    line(c, [(-300, 0), (0, 0)], "#0e0a04", 60); line(c, [(-300, 0), (0, 0)], "#1e140a", 50)
    for k in range(6): line(c, [(-280 + k * 50, -10), (-270 + k * 50, 40)], "#3a4a22", 8)
    ell(c, 20, 0, 50, 44, col)
    for k in range(5):
        a = (k - 2) * 0.28 + math.sin(t * 6 + k) * 0.06; L_ = 120 + (k % 3) * 20
        ex, ey = 40 + math.cos(a + 0.3) * L_, math.sin(a + 0.3) * L_
        line(c, [(40, 0), (40 + math.cos(a) * L_ * 0.55, math.sin(a) * L_ * 0.55), (ex, ey)], col, 16)
        poly(c, [(ex - 7, ey - 7), (ex + 7, ey + 7), (ex + math.cos(a + 0.6) * 36, ey + math.sin(a + 0.6) * 36)], "#000")
    c.restore()

def tabaco_boca(c, x, y, s, t):
    def f():
        line(c, [(0, 0), (110, -20)], "#3a220e", 22)
        glow(c, 116, -22, 60, "#ff6a1a", 0.6); circ(c, 116, -22, 11, "#ff8a2a")
        for k in range(4):
            a = (t * 0.4 + k / 4) % 1
            ell(c, 120 + math.sin(t + k) * 20 * a, -60 - 220 * a, 18 + 40 * a, 12 + 20 * a, hx("#d8d8c8", 0.3 * (1 - a)))
    scaled(c, x, y, s, f)

def cueva(c, t, glow_a=1.0):
    vgrad(c, 0, 0, P, P, "#2a1a06", "#0a0602")
    glow(c, 540, 500, 700, "#ffb21a", 0.25 * glow_a)
    r = random.Random(6)
    for k in range(14):   # estalactitas
        x = k * 80 + r.uniform(-20, 20); h = r.uniform(80, 220)
        poly(c, [(x - 40, 0), (x + 40, 0), (x, h)], "#1a1004")
    for k in range(26):   # monedas y oro
        x = r.uniform(40, 1040); y = r.uniform(880, 1060)
        ell(c, x, y, 26, 12, "#e8c23a"); ell(c, x - 6, y - 3, 10, 4, "#fff4b0")
    for x, y in ((120, 860), (960, 880), (860, 820)):   # ollas de barro
        ell(c, x, y, 70, 60, "#7a3a1a"); ell(c, x, y - 56, 46, 12, "#3a1a0a")
    for k in range(10):
        a = (t * 0.15 + k / 10) % 1
        circ(c, (k * 113) % P, P - a * P, 6 + k % 3 * 3, hx("#ffe8a0", 0.25 * (1 - a)))

def abajo(c, t, d=0.0):
    vgrad(c, 0, 0, P, P, "#0a2a28", "#000")
    overlay(c, "#000", 0.5 * d)
    for k in range(14): circ(c, 200 + (k * 61) % 680, (900 - (t * 200 + k * 70) % 900), 5 + k % 3 * 4, hx("#bce0d8", 0.35))

def ojos_blanco(c, x, y, s, t, talk=0.0, **kw):
    bust(c, x, y, s, t, "creepy", look=(0, -5.2), talk=talk, **kw)

# ---------------- PARTE 1 ----------------
R = G.RULETA
def t00(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0c140e", "#030504")
    tt = t - R["start"]
    L.ruleta(c, 540, 600, 410, max(0, tt), R["dur"], R["target"], win=clamp((tt - R["dur"]) / 0.3))
FOCUS["t00"] = (540, 560)
CAM["t00"] = [(0.0, 1.0, 540, 560)]

def t01(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0a140c", "#020302")
    glow(c, 540, 480, 520, "#ff5a1a", 0.22)
    sc = 0.4 + 0.75 * ease(clamp(t / 0.5))
    L.icono("El Mohán", c, 540, 440, sc, t)
    big(c, "EL MOHÁN", 540, 1000, "#ffb87a", 110)
FOCUS["t01"] = (540, 500)
CAM["t01"] = [(0.0, 1.0, 540, 540)]

def t02(c, t, T, w):
    rio(c, t, y0=640)
    rancho(c, 300, 700, 0.7, light=1.0)
    piedras(c, 930)
    if t > w("rosa") - 0.3:
        bust(c, 800, 990, 0.42, t, "smile", look=(-0.6, 0.4), arms="hold", **ROSA)
    tag2(c, 540, 400, "NATAGAIMA · TOLIMA", t, w("natagaima"), "#ffffff")
    if t > w("magdalena") - 0.2: tag2(c, 540, 490, "RÍO MAGDALENA", t, w("magdalena"), "#9ad8c8")
FOCUS["t02"] = (540, 700)

def t03(c, t, T, w):
    rio(c, t, y0=520)
    tabaco_piedra(c, 540, 820, 1.4, t)
    glow(c, 540, 780, 300, "#ffb060", 0.15)
    tag2(c, 300, 420, "1 TABACO", t, w("tabaco"), "#ffc24a", "#11131a", 40)
    tag2(c, 780, 420, "1 TRAGO", t, w("aguardiente"), "#ffc24a", "#11131a", 40)
    if t > w("él") - 0.2: tag2(c, 540, 540, "PARA ÉL", t, w("él"), "#e0303a", "#ffffff", 46)
FOCUS["t03"] = (540, 760)
CAM["t03"] = [(0.0, 1.0, 540, 540), ("él", 1.3, 540, 700)]

def t04(c, t, T, w):
    rio(c, t, y0=700)
    bust(c, 540, 1100, 1.1, t, "worry", look=(0.3, 0), talk="auto", **PAPA)
    tag2(c, 540, 380, "SE COBRA SOLO", t, w("cobra"), "#e0303a", "#ffffff", 44)
FOCUS["t04"] = (540, 600)

def t05(c, t, T, w):
    rio(c, t, y0=700)
    tabaco_piedra(c, 860, 1000, 0.7, t, lleno=False)
    bust(c, 480, 1110, 1.05, t, "smile", look=(0.5, 0), **YOU)
    tabaco_boca(c, 520, 1110 - 1.05 * 300, 1.05, t)
    if t > w("trago") - 0.2:
        c.save(); c.translate(250, 860); c.rotate(-0.5); rect(c, -24, -100, 48, 100, hx("#e8f0f0", 0.6)); c.restore()
    if t > w("viejos") - 0.3: tag2(c, 540, 400, "«CUENTO DE VIEJOS»", t, w("viejos"), "#ffffff", "#11131a", 40)
FOCUS["t05"] = (520, 640)

def t06(c, t, T, w):
    rio(c, t, y0=480)
    p = ease(clamp((t - w("jalas")) / 1.5))
    sh = 6 * math.sin(t * 40) if t > w("demasiado") - 0.1 else 0
    c.save(); c.translate(sh, 0)
    bust(c, 420, 900, 0.75, t, "shock" if t > w("pesa") else "neutral", look=(0.8, 0.4), arms="hold", **YOU)
    canoa(c, 480, 960, 1.0, t)
    line(c, [(560, 760), (760 - 60 * p, 900 + 40 * p), (900, 1080)], hx("#d8d0b8", 0.9), 5)
    c.restore()
    agua(c, t, 980, a=0.8)
FOCUS["t06"] = (520, 760)

def t07(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0c1612", "#020403")
    glow(c, 540, 500, 500, "#9ad8c8", 0.1)
    red(c, 540, 520, 1.5, t, pelo=ease(clamp((t - w("pelo") + 0.2) / 0.8)), diente=1.0 if t > w("diente") - 0.1 else 0.0)
    for k in range(8): line(c, [(260 + k * 80, 860), (262 + k * 80, 900 + math.sin(t * 3 + k) * 20 + (t * 60 + k * 40) % 120)], hx("#6ab0c0", 0.6), 4)   # gotea
FOCUS["t07"] = (560, 560)
CAM["t07"] = [(0.0, 1.0, 540, 540), ("diente", 1.6, 600, 600)]

def t08(c, t, T, w):
    rio(c, t, y0=420, moon=False)
    overlay(c, "#000", 0.2)
    if t > w("tiple") - 0.3:
        notas(c, t, 540, 1000, 7)
        for k in range(3):
            a = (t * 0.5 + k / 3) % 1
            c.new_path(); c.save(); c.translate(540, 900); c.scale(1, 0.3); c.arc(0, 0, 60 + 380 * a, 0, 2 * math.pi); c.restore()
            c.set_line_width(4); src(c, hx("#ffd84a", 0.35 * (1 - a))); c.stroke()
FOCUS["t08"] = (540, 760)

def t09(c, t, T, w):
    rio(c, t, y0=520)
    piedras(c, 900)
    p = ease(clamp((t - w("camina")) / 3.0))
    if t < w("pie"):
        bust(c, 540, 990, 0.55, t, "neutral", look=(0, 0.6), arms="hold", **ROSA)
    else:
        bust_back(c, 540, 1000 - 160 * p, 0.55 - 0.15 * p, t * 2, shirt=ROSA["shirt"], hair=ROSA["hair_col"], skin=ROSA["skin"], hood=False)
        circ(c, 540, 1000 - 160 * p - 380 * (0.55 - 0.15 * p) - 120 * (0.55 - 0.15 * p) / 0.55, 40 * (0.55 - 0.15 * p) / 0.55, ROSA["hair_col"])
    notas(c, t, 540, 700, 4, rise=300)
FOCUS["t09"] = (540, 760)

def t10(c, t, T, w):
    rio(c, t, y0=700, moon=False); overlay(c, "#000", 0.3)
    glow(c, 540, 600, 500, "#ffd84a", 0.12)
    bust(c, 540, 1100, 1.15, t * 0.3, "smile", look=(0.2, -0.4), talk="auto", **ROSA)
    notas(c, t, 540, 600, 4, rise=400)
    if t > w("oro") - 0.3: tag2(c, 540, 390, "UNA CASA DE ORO", t, w("oro"), "#ffd84a", "#11131a", 42)
FOCUS["t10"] = (540, 600)

def t11(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#05080a", "#000")
    on = t > w("linterna") - 0.2 if w("linterna") else True
    if on:
        poly(c, [(1080, 1080), (1080, 900), (300, 200), (200, 900)], hx("#fff8d0", 0.14))
        glow(c, 540, 560, 420, "#fff8d0", 0.25)
    ojos_blanco(c, 540, 1100, 1.15, t * 0.3, **ROSA) if t > w("blanco") - 0.2 else bust(c, 540, 1100, 1.15, t * 0.3, "tired", **ROSA)
    if not on: overlay(c, "#000", 0.7)
FOCUS["t11"] = (540, 560)
CAM["t11"] = [(0.0, 1.0, 540, 540), ("blanco", 1.35, 540, 500)]

def t12(c, t, T, w):
    rio(c, t, y0=480)
    p = ease(clamp((t - w("abre") + 0.2) / 2.0))
    if t > w("abre") - 0.3:
        L.mohan_cuerpo(c, 540, 1500 - 260 * p, 0.95, t, brazos="caidos", tabaco=t > w("fumando") - 0.2)
        for k in range(4):
            a = (t * 0.7 + k / 4) % 1
            c.new_path(); c.save(); c.translate(540, 760); c.scale(1, 0.25); c.arc(0, 0, 200 + 300 * a, 0, 2 * math.pi); c.restore()
            c.set_line_width(5); src(c, hx("#bce0d8", 0.4 * (1 - a))); c.stroke()
    agua(c, t, 760, a=0.85)
    bust_back(c, 540, 1180, 0.5, t, shirt=ROSA["shirt"], hair=ROSA["hair_col"], skin=ROSA["skin"], hood=False)
    circ(c, 540, 1180 - 380 * 0.5 - 110, 36, ROSA["hair_col"])
    if t > w("tu") - 0.1: tag2(c, 780, 420, "TU TABACO", t, w("tu"), "#e0303a", "#ffffff", 42)
FOCUS["t12"] = (540, 520)
CAM["t12"] = [(0.0, 1.0, 540, 540), ("enorme", 1.45, 540, 420)]

def t13(c, t, T, w):
    rio(c, t, y0=480)
    L.mohan_cuerpo(c, 540, 1240, 0.95, t)
    agua(c, t, 760, a=0.85); overlay(c, "#000", 0.45)

# ---------------- PARTE 2 ----------------
def u01(c, t, T, w):
    rio(c, t, y0=640); piedras(c, 980)
    bust(c, 380, 1110, 0.95, t * 2, "angry", look=(-0.6, 0), talk=0.4 * abs(math.sin(t * 9)), **ROSA)
    bust(c, 800, 1120, 0.85, t, "shock" if t > w("araña") else "worry", look=(-1, 0), arms="hold", **YOU)
    if t > w("araña"):
        for k in range(3): line(c, [(760 + k * 26, 780), (800 + k * 26, 860)], "#c0202a", 6)
FOCUS["u01"] = (560, 640)

def u02(c, t, T, w):
    cuarto(c, t, lamp=0.6)
    bust(c, 330, 1100, 0.95, t, "shock" if t > w("ve") else "tired", look=(0.6, 0.3), **PAPA)
    red(c, 790, 620, 0.85, t, pelo=1.0)
FOCUS["u02"] = (540, 620)

def u03(c, t, T, w):
    cuarto(c, t, lamp=0.5)
    bust(c, 540, 1100, 1.15, t, "angry", look=(0, 0), talk="auto", **PAPA)
    if t > w("hermana") - 0.2: tag2(c, 540, 380, "QUIERE A ROSA", t, w("hermana"), "#e0303a", "#ffffff", 44)
FOCUS["u03"] = (540, 600)

def u04(c, t, T, w):
    rio(c, t, y0=640); piedras(c, 960)
    gone = t > w("desapareció") - 0.1
    if not gone: bust(c, 420, 1040, 0.6, t, "smile", look=(0.5, 0.4), arms="hold", **TIA)
    else:
        for k in range(3):
            a = ((t - w("desapareció")) * 0.6 + k / 3) % 1
            c.new_path(); c.save(); c.translate(560, 900); c.scale(1, 0.3); c.arc(0, 0, 40 + 260 * a, 0, 2 * math.pi); c.restore()
            c.set_line_width(4); src(c, hx("#dfe8ff", 0.4 * (1 - a))); c.stroke()
        for k in range(4): ell(c, 360 + k * 50, 940, 30, 10, "#e8e0d0")   # la ropa sola en la piedra
    sepia(c, 0.55)
    if t > w("treinta") - 0.2: tag2(c, 540, 560, "HACE 30 AÑOS", t, w("treinta"), "#e0303a", "#ffffff", 40)
    if t > w("carmen") - 0.2 and not gone: tag2(c, 420, 640, "TÍA CARMEN", t, w("carmen"), "#ffffff", "#11131a", 36)
FOCUS["u04"] = (480, 700)

def u05(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#140c08", "#050302")
    rect(c, 140, 820, 26, 80, "#f0ead8"); ell(c, 153, 810, 11, 20, "#ffc24a"); glow(c, 153, 810, 160, "#ffb060", 0.4)
    for k in range(40): circ(c, 600 + (k * 37) % 400, 980 + (k * 13) % 40, 4, "#f4f4f0")   # sal en la puerta
    for i, (tok, s_) in enumerate((("amarran", "1. ROSA AMARRADA"), ("sal", "2. SAL EN LA PUERTA"), ("nadie", "3. NADIE ABRE"))):
        tag2(c, 560, 380 + i * 170, s_, t, w(tok), "#ffc24a" if i < 2 else "#e0303a", "#11131a" if i < 2 else "#ffffff", 42)
FOCUS["u05"] = (540, 560)

def u06(c, t, T, w):
    cuarto(c, t, lamp=0.25)
    bust(c, 540, 1100, 0.9, t, "shock" if t > w("debajo") - 0.1 else "worry", look=(0, 1), **YOU)
    if t > w("música") - 0.3:
        y0 = 1040 if t > w("debajo") - 0.2 else 700
        notas(c, t, 540, y0, 6, rise=400)
FOCUS["u06"] = (540, 760)

def u07(c, t, T, w):
    cuarto(c, t, lamp=0.2)
    for k in range(10):
        x = k * 110 + 3
        for j in range(3):
            a = (t * 0.4 + j / 3 + k * 0.13) % 1
            ell(c, x + math.sin(t + k + j) * 30 * a, 840 - 400 * a, 20 + 50 * a, 12 + 30 * a, hx("#c8c8b8", 0.3 * (1 - a) * clamp((t - w("huele") + 0.3) / 1.0)))
    glow(c, 540, 900, 500, "#ff6a1a", 0.08)
FOCUS["u07"] = (540, 760)

def u08(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#1a140c", "#050302")
    c.save(); c.translate(0, -40)
    for k in range(10):
        c.save(); c.rectangle(k * 110, 0, 6 + 14 * ease(clamp(t / 1.5)), P); c.clip()
        glow(c, 540, 560, 500, "#bce0d8", 0.35)
        ojos_blanco(c, 540, 1120, 1.2, t, talk="auto", **TIA)
        c.restore()
    c.restore()
    for k in range(10): rect(c, k * 110 + 20, 0, 90, P, hx("#3a2a1a", 0.92))
    c.save(); c.rectangle(0, 0, P, P); c.clip()
    for k in range(10): rect(c, k * 110 + 20, 0, 4, P, hx("#000", 0.4))
    c.restore()
FOCUS["u08"] = (540, 560)

def u09(c, t, T, w):
    cuarto(c, t, lamp=0.2, open_=t > w("ventana") - 0.3)
    rrect(c, 80, 700, 460, 160, 20, "#5a3a22"); rrect(c, 100, 660, 420, 70, 20, "#c8c0a8")   # cama vacía
    if t > w("cuerdas") - 0.3:
        for k in range(3):
            line(c, [(140 + k * 140, 640), (150 + k * 140, 700)], "#c8a860", 8); line(c, [(170 + k * 140, 640), (160 + k * 140, 600)], "#c8a860", 8)
            for j in range(3): line(c, [(150 + k * 140 + j * 6, 640), (146 + k * 140 + j * 8, 626)], "#c8a860", 3)
    if t > w("ventana") - 0.2:
        for k in range(4): line(c, [(700, 300 + k * 40), (500 - k * 60, 240 + k * 70)], hx("#9ad8c8", 0.2), 5)
FOCUS["u09"] = (420, 640)
CAM["u09"] = [(0.0, 1.0, 540, 540), ("mordidas", 1.5, 320, 660), ("ventana", 1.4, 780, 340)]

def u10(c, t, T, w):
    rio(c, t, y0=500)
    remolino(c, 640, 680, t, 280)
    p = ease(clamp(t / T))
    agua(c, t, 760, a=0.0)
    bust_back(c, 540 + 60 * p, 900 - 60 * p, 0.38 - 0.05 * p, t * 2, shirt=ROSA["shirt"], hair=ROSA["hair_col"], skin=ROSA["skin"], hood=False)
    agua(c, t, 800, a=0.85)
    bust_back(c, 260, 1180, 0.55, t * 3, shirt=PAPA["shirt"], hair=PAPA["hair_col"], skin=PAPA["skin"], hood=False)
    bust_back(c, 820, 1200, 0.55, t * 3, shirt=YOU["shirt"], hair="#1a120c", skin=YOU["skin"], hood=False)
    c.new_path(); c.arc(820, 1200 - 380 * 0.55 - 4, 80, math.pi, 2 * math.pi); c.close_path(); fill(c, YOU["cap_col"])
    if t > w("remolino") - 0.2: tag2(c, 640, 420, "EL REMOLINO", t, w("remolino"), "#e0303a", "#ffffff", 40)
FOCUS["u10"] = (580, 700)

def u11(c, t, T, w):
    rio(c, t, y0=440, moon=True)
    remolino(c, 540, 820, t, 420)
    L.mohan_cuerpo(c, 540, 1300, 0.9, t, brazos="abiertos" if t > w("abiertas") - 0.4 else "caidos")
    agua(c, t, 840, a=0.8)
    bust_back(c, 540, 1220, 0.4, t, shirt=ROSA["shirt"], hair=ROSA["hair_col"], skin=ROSA["skin"], hood=False)
    agua(c, t, 1000, a=0.6)
FOCUS["u11"] = (540, 520)
CAM["u11"] = [(0.0, 1.0, 540, 540), ("manos", 1.3, 540, 480)]

def u12(c, t, T, w):
    rio(c, t, y0=440)
    remolino(c, 540, 820, t * 1.6, 460)
    tt = w("traga")
    d = ease(clamp((t - tt + 0.2) / 1.0))
    c.save(); c.rectangle(0, 0, P, 830); c.clip()
    bust(c, 540, 1000 + 400 * d, 0.7, t, "shock", look=(0, -1), arms="up", shake=1.0, **PAPA); c.restore()
    if t > tt: mano(c, 300, 900, 1.0, -0.6, t); mano(c, 780, 900, 1.0, math.pi + 0.6, t)
    agua(c, t, 830, a=0.7)
FOCUS["u12"] = (540, 760)

def u13(c, t, T, w):
    rio(c, t, y0=440); remolino(c, 540, 820, t, 460); agua(c, t, 830, a=0.7); overlay(c, "#000", 0.45)

# ---------------- PARTE 3 ----------------
def v01(c, t, T, w):
    abajo(c, t, clamp(t / T))
    bust(c, 540, 820 + 100 * clamp(t / T), 0.85, t, "shock", look=(0, -1), arms="up", **YOU)
    mano(c, 120, 1040, 0.9, -0.9, t); mano(c, 960, 1060, 0.9, math.pi + 0.9, t)
FOCUS["v01"] = (540, 700)

def v02(c, t, T, w):
    cueva(c, t, glow_a=clamp((t - w("luz") + 0.3) / 1.0) if w("luz") else 1.0)
    red(c, 820, 420, 0.5, t)
    if t > w("oro") - 0.2: tag2(c, 540, 600, "LA CUEVA DEL MOHÁN", t, w("oro"), "#ffd84a", "#11131a", 40)
FOCUS["v02"] = (540, 700)

def v03(c, t, T, w):
    cueva(c, t)
    for i, x in enumerate((160, 920)):
        ojos_blanco(c, x, 1060, 0.55, t + i, **dict(TIA, shirt="#c8c8c0", skin="#c0b8b0"))
    for i, x in enumerate((340, 740)):
        ojos_blanco(c, x, 1020, 0.45, t + i * 2, **dict(TIA, shirt="#b8b8b0", skin="#beb6aa"))
    hi = t > w("tía") - 0.3
    if hi: glow(c, 540, 700, 300, "#bce0d8", 0.3)
    ojos_blanco(c, 540, 1100, 0.75, t, **TIA)
    if hi: tag2(c, 540, 400, "TÍA CARMEN", t, w("tía"), "#ffffff", "#11131a", 40)
    if t > w("envejecido") - 0.2: tag2(c, 540, 500, "NI UN DÍA MÁS VIEJA", t, w("envejecido"), "#e0303a", "#ffffff", 36)
FOCUS["v03"] = (540, 640)
CAM["v03"] = [(0.0, 1.0, 540, 540), ("tía", 1.35, 540, 620)]

def v04(c, t, T, w):
    cueva(c, t)
    L.mohan_cuerpo(c, 600, 1000, 0.62, t, brazos="tiple")
    notas(c, t, 620, 520, 5, rise=300)
    c.save(); c.translate(470, 1010); c.rotate(-1.35); bust(c, 0, 0, 0.36, 0, "tired", **ROSA); c.restore()
    bust(c, 900, 1080, 0.42, 0, "tired", look=(0, 0), **PAPA); red(c, 900, 900, 0.55, t)
FOCUS["v04"] = (600, 640)

def v05(c, t, T, w):
    cueva(c, t); overlay(c, "#000", 0.35)
    L.icono("El Mohán", c, 540, 520, 1.55 + 0.25 * ease(clamp(t / T)), t)
FOCUS["v05"] = (540, 520)
CAM["v05"] = [(0.0, 1.0, 540, 540), ("conmigo", 1.25, 540, 560)]

def v06(c, t, T, w):
    cueva(c, t)
    bust(c, 540, 1100, 1.1, t, "worry", look=(0.3, -0.3), talk="auto" if t > w("quédese") - 0.2 else 0, tears=1.0, **YOU)
FOCUS["v06"] = (540, 600)

def v07(c, t, T, w):
    cueva(c, t); overlay(c, "#000", 0.3)
    sh = 6 * math.sin(t * 30) if t > w("ríe") - 0.1 else 0
    L.icono("El Mohán", c, 540 + sh, 540, 1.7, t)
    if t > w("oro") - 0.3: glow(c, 540, 600, 300, "#ffd84a", 0.4)
    if t > w("acepta") - 0.2: tag2(c, 540, 960, "TRATO HECHO", t, w("acepta"), "#ffd84a", "#11131a", 46)
FOCUS["v07"] = (540, 600)

def v08(c, t, T, w):
    cueva(c, t); overlay(c, "#000", 0.3)
    g = ease(clamp((t - w("pelo") + 0.2) / 2.5))
    bust(c, 540, 1100, 1.1, t, "shock" if g < 0.6 else "tired", look=(0, -0.3), **YOU)
    if g > 0:
        c.save(); c.translate(540, 1100 - 1.1 * 420); L._musgo(c, 220, -120, -120 + 600 * g, 34, 41, t, 3.0); c.restore()
    if t > w("cara") - 0.2: mano(c, -80, 560, 1.2, 0.0, t)
    if t > w("nombre") - 0.2: tag2(c, 540, 400, "¿CÓMO TE LLAMABAS?", t, w("nombre"), "#e0303a", "#ffffff", 40)
FOCUS["v08"] = (540, 560)

def amanecer(c, t):
    vgrad(c, 0, 0, P, 620, "#e8a070", "#8a9ab0")
    circ(c, 200, 600, 90, "#ffd0a0"); glow(c, 200, 600, 300, "#ffd0a0", 0.3)
    vgrad(c, 0, 620, P, 460, "#7a8a90", "#3a4a50")
    for k in range(10): rect(c, (k * 160 + t * 30) % 1200 - 100, 640 + k * 20, 120, 3, hx("#ffffff", 0.3))

def v09(c, t, T, w):
    amanecer(c, t); piedras(c, 960, 6, 9)
    bust(c, 300, 1020, 0.6, t, "sad" if t > w("respira") - 0.2 else "tired", tears=1.0 if t > w("respira") else 0, look=(0.8, 0.5), **ROSA)
    if t > w("papá") - 0.3:
        c.save(); c.translate(720, 960); c.rotate(-1.45); bust(c, 0, 0, 0.42, 0, "tired", **PAPA); c.restore()
FOCUS["v09"] = (520, 860)
CAM["v09"] = [(0.0, 1.0, 540, 540), ("respira", 1.45, 640, 880)]

def v10(c, t, T, w):
    amanecer(c, t); overlay(c, "#000", 0.55)
    tag2(c, 540, 460, "LOS SOLTÓ A LOS DOS…", t, w("soltó"), "#ffffff", "#11131a", 46)
    if t > w("vivos") - 0.3: tag2(c, 540, 620, "NUNCA DIJO QUE VIVOS", t, w("vivos"), "#e0303a", "#ffffff", 50)
FOCUS["v10"] = (540, 540)
CAM["v10"] = [(0.0, 1.0, 540, 540), ("vivos", 1.2, 540, 600)]

def v11(c, t, T, w):
    amanecer(c, t)
    rect(c, 0, 860, P, 220, "#8a7a5a")
    p = ease(clamp((t - w("rosa") + 0.2) / 4.0)) if w("rosa") else 0
    bust_back(c, 540 + 300 * p, 1100 - 60 * p, 0.6 - 0.2 * p, t * 3, shirt=ROSA["shirt"], hair=ROSA["hair_col"], skin=ROSA["skin"], hood=False)
    rrect(c, 540 + 300 * p + 60 * (0.6 - 0.2 * p) / 0.6, 980 - 60 * p, 80, 100, 14, "#6a3a1a")
    if t > w("jamás") - 0.2: tag2(c, 540, 420, "NUNCA VOLVIÓ AL RÍO", t, w("jamás"), "#ffffff", "#11131a", 40)
FOCUS["v11"] = (640, 860)

def v12(c, t, T, w):
    rio(c, t, y0=560)
    L.mohan_cuerpo(c, 860, 760, 0.28, t, cara="sombra")
    agua(c, t, 620, a=0.7)
    p = ease(clamp((t - w("atarraya") + 0.2) / 1.2))
    red(c, 460, 760 - 60 * p, 0.8, t, pelo=0.6)
    if t > w("gorro") - 0.2:
        c.save(); c.translate(470, 800 - 60 * p)
        c.new_path(); c.arc(0, 0, 90, math.pi, 2 * math.pi); c.close_path(); fill(c, YOU["cap_col"])
        rect(c, -92, -6, 184, 30, "#c85a1a"); circ(c, 0, -96, 22, YOU["cap_col"]); c.restore()
        glow(c, 470, 760 - 60 * p, 200, "#e8702a", 0.25)
FOCUS["v12"] = (480, 720)
CAM["v12"] = [(0.0, 1.0, 540, 540), ("gorro", 1.6, 470, 740)]

def v13(c, t, T, w):
    rio(c, t, y0=560)
    L.mohan_cuerpo(c, 860, 760, 0.28, t, cara="sombra")
    agua(c, t, 620, a=0.7)
    overlay(c, "#000", 0.45)

PANELS = {k: v for k, v in globals().items() if len(k) == 3 and k[0] in "tuv" and k[1:].isdigit() and callable(v)}

import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect_path, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp, text_w
from povlib import *
from scenes import popin, tag2, bust_back
import leyendas as L
import guion as G

YOU = dict(hat="beanie", skin="#7a4a2a", shirt="#3c8a5a", cap_col="#e8702a")
JOSUE = dict(hat="none", skin="#6a3e22", shirt="#5fa0e0", hair_col="#140a06")
ABUELA = dict(hat="bun", skin="#5a3420", shirt="#7a3a6a", hair_col="#d8d8d8", gray=True)
MAMA = dict(hat="bun", skin="#6a4028", shirt="#2f8f7a", hair_col="#140a06")
FOCUS = {}; CAM = {}

def big(c, s_, x, y, col="#ffffff", size=120):
    ui(c, size); w_ = text_w(c, s_); c.new_path(); c.move_to(x - w_ / 2, y); c.text_path(s_)
    c.set_line_width(16); c.set_line_join(cairo.LINE_JOIN_ROUND); src(c, "#000"); c.stroke_preserve(); src(c, col); c.fill()

# ---------------- escenarios ----------------
def mangle(c, x, y, s, col="#0e1a10"):
    def f():
        for k in range(6):
            a = -0.9 + k * 0.36
            c.new_path(); c.move_to(0, -120); c.curve_to(math.sin(a) * 80, -60, math.sin(a) * 140, 0, math.sin(a) * 170, 40)
            c.set_line_width(14); src(c, col); c.stroke()
        rect(c, -14, -420, 28, 300, col)
        for k in range(7): ell(c, -120 + k * 40, -440 - (k % 3) * 30, 90, 50, col)
    scaled(c, x, y, s, f)

def rio_noche(c, t, moon=True):
    vgrad(c, 0, 0, P, 620, "#0a1020", "#1a2438")
    if moon: circ(c, 880, 160, 46, "#f4efd0"); glow(c, 880, 160, 260, "#f4efd0", 0.18)
    vgrad(c, 0, 620, P, 460, "#101c24", "#060a0e")
    for k in range(14):
        y = 650 + k * 30; w_ = 120 + (k * 37) % 200; x = (k * 173 + t * 30) % 1200 - 100
        rect(c, x, y, w_, 3, hx("#9ab0d0", 0.25))
    for x in (60, 200, 940): mangle(c, x, 680, 0.9)

def casa_pilotes(c, t, light=1.0, win_fig=None):
    rio_noche(c, t)
    for x in (300, 420, 560, 700, 800): rect(c, x, 560, 22, 260, "#2a1c12")
    rect(c, 260, 300, 580, 270, "#5a3e26")
    for k in range(10): rect(c, 260, 300 + k * 27, 580, 3, hx("#000", 0.25))
    poly(c, [(230, 310), (550, 170), (870, 310)], "#3a2a1c")
    rect(c, 330, 360, 150, 120, "#2a1a10"); rect(c, 342, 372, 126, 96, hx("#ffc070", light))
    rect(c, 600, 360, 110, 200, "#2a1a10"); rect(c, 612, 372, 86, 176, hx("#ffb060", 0.8 * light))
    if light: glow(c, 405, 420, 200, "#ffb060", 0.25 * light)
    if win_fig: c.save(); c.rectangle(342, 372, 126, 96); c.clip(); win_fig(c); c.restore()
    poly(c, [(560, 560), (600, 560), (540, 760), (500, 760)], "#3a2a1c")   # escalera
    for k in range(6): rect(c, 520 + k * -6, 580 + k * 30, 60, 6, "#2a1c12")

def interior(c, t, lamp=1.0, ventana=True):
    vgrad(c, 0, 0, P, P, "#3a2618", "#1a1008")
    for k in range(14): rect(c, k * 80, 0, 4, P, hx("#000", 0.3))
    rect(c, 0, 820, P, 260, "#2a1a0e")
    for k in range(6): rect(c, 0, 840 + k * 40, P, 3, hx("#000", 0.35))
    if ventana:
        rect(c, 640, 160, 320, 300, "#1a0e06"); vgrad(c, 656, 176, 288, 268, "#0a1020", "#101c24")
        for x in (700, 860): mangle(c, x, 470, 0.45)
    if lamp: rrect(c, 120, 520, 70, 110, 14, hx("#ffd890", 0.9)); glow(c, 155, 560, 360, "#ffb060", 0.35 * lamp)

def manglar(c, t, fog=1.0, dark=0.0):
    vgrad(c, 0, 0, P, P, "#0a140e", "#030604")
    for k in range(9):
        x = 60 + k * 130; mangle(c, x, 780 - (k % 3) * 40, 1.0 + (k % 2) * 0.3, "#0c180e" if k % 2 else "#122014")
    vgrad(c, 0, 780, P, 300, "#1a1408", "#0a0804")
    for k in range(5):
        y = 760 + k * 50; x = (t * 20 + k * 230) % 1300 - 200
        ell(c, x, y, 320, 40, hx("#c8d0c8", 0.06 * fog))
    if dark: overlay(c, "#000", dark)

def kid_stairs(c, t):
    rio_noche(c, t, moon=False)
    poly(c, [(300, 300), (420, 300), (340, 900), (220, 900)], "#3a2a1c")
    for k in range(8): rect(c, 240 + k * 12, 360 + k * 70, 120, 10, "#2a1c12")

# ---------------- PARTE 1 ----------------
R = G.RULETA
def t00(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#140c10", "#050304")
    tt = t - R["start"]
    L.ruleta(c, 540, 600, 410, max(0, tt), R["dur"], R["target"], win=clamp((tt - R["dur"]) / 0.3))
FOCUS["t00"] = (540, 560)
CAM["t00"] = [(0.0, 1.0, 540, 560)]

def t01(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#1a0a06", "#050302")
    glow(c, 540, 480, 520, "#ffd21a", 0.25)
    sc = 0.4 + 0.75 * ease(clamp(t / 0.5))
    L.icono("La Tunda", c, 540, 470, sc, t)
    big(c, "LA TUNDA", 540, 960, "#ffd21a", 110)
FOCUS["t01"] = (540, 520)
CAM["t01"] = [(0.0, 1.0, 540, 540)]

def t02(c, t, T, w):
    casa_pilotes(c, t)
    tag2(c, 540, 900, "GUAPI · PACÍFICO", t, w("guapi"), "#ffffff")
    if t > w("josué") - 0.2:
        c.save(); c.rectangle(342, 372, 126, 96); c.clip(); bust(c, 405, 560, 0.3, t, "smile", **JOSUE); c.restore()
FOCUS["t02"] = (500, 420)

def t03(c, t, T, w):
    interior(c, t)
    bust(c, 330, 1060, 0.95, t, "worry", look=(0.6, 0), talk=0.5 * abs(math.sin(t * 12)) if t < T * 0.8 else 0, **ABUELA)
    bust(c, 820, 1110, 0.8, t, "neutral", look=(-0.8, 0), **YOU)
    tag2(c, 540, 380, "MAMÁ SIEMPRE LLEGA EN LANCHA", t, w("lancha"), "#ffc24a", "#11131a", 34)
FOCUS["t03"] = (330, 600)

def t04(c, t, T, w):
    interior(c, t)
    bust(c, 760, 1060, 0.95, t, "happy", look=(0.4, -0.3), talk="auto", **JOSUE)
FOCUS["t04"] = (760, 640)

def tunda_lejos(c, t, x, y, s, step=True):
    lim = math.sin(t * 3.0) * 6 if step else 0
    L.tunda(c, x, y + abs(lim), s, t, cara="sombra")

def t05(c, t, T, w):
    rio_noche(c, t)
    tunda_lejos(c, t, 560, 760, 0.42)
    vgrad(c, 0, 0, 120, P, "#1a0e06", "#1a0e06"); rect(c, 960, 0, 120, P, "#1a0e06"); rect(c, 0, 0, P, 60, "#1a0e06")
FOCUS["t05"] = (560, 520)
CAM["t05"] = [("amarillo", 1.6, 560, 520)]

def t06(c, t, T, w):
    manglar(c, t)
    tunda_lejos(c, t, 540, 960, 0.6)
    if t > w("palo") - 0.2: tag2(c, 700, 860, "TUM", t, w("palo"), "#ffffff")
FOCUS["t06"] = (560, 900)
CAM["t06"] = [("cojea", 1.7, 560, 880)]

def t07(c, t, T, w):
    manglar(c, t, dark=0.3)
    c.save(); c.translate(540, 1000); c.scale(1.6, 1.6); c.translate(-540, -1000)
    L.tunda(c, 540, 1080, 0.6, 0.0, cara="sombra"); c.restore()
    for i, tok in enumerate(("tum", "tum", "tum")):
        tt = 0.25 + i * 0.75
        if t > tt: s_ = 1 + 0.5 * math.exp(-(t - tt) * 6); c.save(); c.translate(540, 300 + i * 150); c.scale(s_, s_); big(c, "TUM", 0, 0, "#ffffff", 120); c.restore()
FOCUS["t07"] = (540, 540)
CAM["t07"] = [(0.0, 1.0, 540, 540)]

def t08(c, t, T, w):
    manglar(c, t, dark=0.2)
    tunda_lejos(c, t, 540, 1100, 0.75, step=False)
    c.save(); c.translate(540, 1100 - 930 * 0.75); glow(c, 0, 0, 180, "#ffd21a", 0.15 + 0.2 * povlib_talk()); c.restore()
FOCUS["t08"] = (540, 420)

def povlib_talk():
    import povlib; return povlib.TALK

def t09(c, t, T, w):
    kid_stairs(c, t)
    bust_back(c, 330, 1120, 0.5, t, shirt=JOSUE["shirt"], hair=JOSUE["hair_col"], skin=JOSUE["skin"], hood=False)
    bust(c, 760, 1100, 0.9, t, "shock" if t > w("muerde") else "worry", look=(-1, 0.3), arms="up" if t > w("agarras") else "none", **YOU)
FOCUS["t09"] = (540, 640)

def t10(c, t, T, w):
    interior(c, t, lamp=0.5)
    bust(c, 540, 1080, 1.15, t * 0.2, "tired", look=(0, -0.2), talk=0.4 * abs(math.sin(t * 8)) if t > w("repite") else 0, **JOSUE)
    for k in range(3):
        a = (t * 0.6 + k / 3) % 1; c.new_path(); c.arc(540, 560, 60 + 200 * a, 0, 2 * math.pi); c.set_line_width(4); src(c, hx("#ffd21a", 0.3 * (1 - a))); c.stroke()
FOCUS["t10"] = (540, 600)

def t11(c, t, T, w):
    manglar(c, t, dark=0.1)
    c.save(); c.translate(540, 1080); c.scale(2.4, 2.4); c.translate(-540, -1080)
    L.tunda(c, 540, 1000, 0.6, t, cara="sombra"); c.restore()
    if t > w("molinillo") - 0.2: glow(c, 600, 900, 240, "#ff3a1a", 0.3)
FOCUS["t11"] = (580, 880)
CAM["t11"] = [("levanta", 1.0, 540, 540), ("palo", 1.4, 600, 820)]

def t12(c, t, T, w):
    manglar(c, t, dark=0.55); tunda_lejos(c, t, 540, 1000, 0.5); overlay(c, "#000", 0.4)

# ---------------- PARTE 2 ----------------
def hamaca(c, t, kid_mood="sad", struggle=1.0, broken=False):
    interior(c, t, lamp=0.8)
    line(c, [(160, 500), (540, 640), (920, 500)], "#c8a870", 8)
    sw = math.sin(t * 9) * 14 * struggle
    c.new_path(); c.move_to(160, 500); c.curve_to(360, 760 + sw, 720, 760 - sw, 920, 500); c.line_to(920, 520); c.curve_to(720, 800 - sw, 360, 800 + sw, 160, 520); c.close_path(); fill(c, "#c84a3a")
    c.save(); c.rectangle(0, 0, P, 700 + sw); c.clip(); bust(c, 540 + sw, 900, 0.6, t * 2, kid_mood, look=(math.sin(t * 5), 0), **JOSUE); c.restore()
    if not broken:
        for k in range(3): line(c, [(380 + k * 160, 640), (420 + k * 160, 760)], "#e8d8a8", 6)

def u01(c, t, T, w):
    hamaca(c, t)
    tag2(c, 820, 380, "¡...!", t, w("nombre"), "#e0303a", "#ffffff")
FOCUS["u01"] = (540, 620)

def u02(c, t, T, w):
    interior(c, t, lamp=0.6)
    bust(c, 400, 1080, 1.0, t, "sad", tears=clamp((t - w("llorar")) / 0.6), arms="hold", **ABUELA)
    glow(c, 520, 780, 140, "#ffd890", 0.5); rect(c, 512, 760, 16, 60, "#f4f0e0"); ell(c, 520, 752, 7, 14, "#ffc24a")
FOCUS["u02"] = (420, 600)

def u03(c, t, T, w):
    interior(c, t, lamp=0.6)
    bust(c, 540, 1080, 1.15, t, "sad", tears=1.0, talk="auto", **ABUELA)
FOCUS["u03"] = (540, 600)

def u04(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#1a0a06", "#050302")
    L.icono("La Tunda", c, 320, 480, 0.85, t)
    if t > w("camarones") - 0.2:
        for k in range(5):
            x = 680 + (k % 3) * 110; y = 420 + (k // 3) * 110
            def cam():
                c.new_path(); c.arc(0, 0, 40, 0.3, math.pi * 1.6); c.set_line_width(26); src(c, "#e8784a"); c.stroke()
                circ(c, 30, -18, 6, "#000")
            scaled(c, x, y, popin(t, w("camarones") + k * 0.12), cam)
    if t > w("manglar") - 0.2: tag2(c, 540, 860, "PARA SIEMPRE", t, w("siempre"), "#e0303a", "#ffffff")
FOCUS["u04"] = (540, 520)

def u05(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#140c10", "#050304")
    for i, (tok, s_) in enumerate((("nombre", "1. SU NOMBRE COMPLETO"), ("tres", "2. TRES VECES"), ("ojos", "3. SIN MIRARLA A LOS OJOS"))):
        tag2(c, 540, 380 + i * 170, s_, t, w(tok), "#ffc24a" if i < 2 else "#e0303a", "#11131a" if i < 2 else "#ffffff", 42)
FOCUS["u05"] = (540, 560)

def u06(c, t, T, w):
    rio_noche(c, t, moon=False); overlay(c, "#000010", 0.3)
    rect(c, 0, 0, P, 180, "#3a2a1c")
    for x in (120, 360, 620, 880): rect(c, x, 180, 40, 700, "#2a1c12")
    c.save(); c.translate(500, 880); L.tunda(c, 0, 0, 0.55, t, cara="sombra"); c.restore()
    for i in range(3):
        tt = w("tum") + i * 0.45
        if t > tt and t < tt + 0.8: big(c, "TUM", 300 + i * 240, 600, hx("#ffffff", 1 - (t - tt) / 0.8), 90)
FOCUS["u06"] = (540, 560)

def u07(c, t, T, w):
    rect(c, 0, 0, P, P, "#3a2618")
    for k in range(9): rect(c, 0, k * 120, P, 112, "#4a321e"); rect(c, 0, k * 120 + 112, P, 8, "#0a0604")
    rect(c, 0, 592, P, 26, "#000")
    if t > w("ojo") - 0.2:
        c.save(); c.rectangle(0, 592, P, 26); c.clip(); ell(c, 540, 605, 70, 40, "#f0e0a0"); circ(c, 540, 605, 16, "#ffd21a"); circ(c, 540, 605, 7, "#000"); c.restore()
        glow(c, 540, 605, 160, "#ffd21a", 0.3)
FOCUS["u07"] = (540, 605)
CAM["u07"] = [("rendija", 1.6, 540, 605), ("ojo", 2.6, 540, 605)]

def u08(c, t, T, w):
    u07(c, t + 5, T, lambda tok: -1)
FOCUS["u08"] = (540, 605)
CAM["u08"] = [(0.0, 2.8, 540, 605)]

def u09(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#2c3350", "#1b2036")
    rrect(c, 330, 120, 420, 860, 50, "#111"); rrect(c, 346, 136, 388, 828, 40, "#0b141a")
    rect(c, 346, 136, 388, 100, "#1f2c34"); txt(c, "Mamá", 420, 200, "#e9edef", 34, False, True)
    if t > w("escribe") - 0.2:
        a = popin(t, w("escribe") - 0.2)
        c.save(); c.translate(360, 300); c.scale(a, a); bubble(c, 0, 0, 340, ["ya salí de", "Buenaventura,", "llego en 3 horas"], "#1f2c34", "#e9edef", 30, "l"); c.restore()
    tag2(c, 540, 900, "3 HORAS", t, w("tres"), "#e0303a", "#ffffff")
FOCUS["u09"] = (540, 420)

def u10(c, t, T, w):
    hamaca(c, t, "angry", struggle=1.6)
FOCUS["u10"] = (540, 640)

def u11(c, t, T, w):
    hamaca(c, t, "angry", struggle=2.2, broken=t > w("rompe") - 0.1)
FOCUS["u11"] = (540, 640)

def u12(c, t, T, w):
    casa_pilotes(c, t, light=0.8)
    p = clamp((t - w("corre")) / 2.0)
    bust_back(c, 520 + 200 * p, 900 - 120 * p, 0.32, t * 3, shirt=JOSUE["shirt"], hair=JOSUE["hair_col"], skin=JOSUE["skin"], hood=False)
    tunda_lejos(c, t, 960, 760, 0.3)
FOCUS["u12"] = (700, 700)

def u13(c, t, T, w):
    manglar(c, t, dark=0.55); tunda_lejos(c, t, 540, 1000, 0.5); overlay(c, "#000", 0.4)

# ---------------- PARTE 3 ----------------
def v01(c, t, T, w):
    manglar(c, t)
    bust(c, 420, 1120, 0.9, t * 2, "worry", look=(0.3, -0.2), **YOU)
    glow(c, 900, 760, 120, "#ffd890", 0.4); c.save(); c.rectangle(820, 0, 260, P); c.clip(); bust(c, 960, 1040, 0.5, t, "shock", talk=0.6 * abs(math.sin(t * 11)), **ABUELA); c.restore()
FOCUS["v01"] = (480, 640)

def v02(c, t, T, w):
    manglar(c, t)
    c.save(); c.translate(600, 1000); L.tunda(c, 0, 0, 0.6, t * 0.3, cara="sombra"); c.restore()
    bust(c, 360, 1110, 0.5, t, "tired", look=(1, 0), talk=0.3 * abs(math.sin(t * 6)), **JOSUE)
    for k in range(3): ell(c, 430 + k * 20, 1010, 14, 8, "#e8784a")
FOCUS["v02"] = (480, 760)

def v03(c, t, T, w):
    manglar(c, t, dark=0.2)
    # de espaldas: solo vestido y pañuelo; la cabeza gira (vemos un ojo)
    c.save(); c.translate(540, 1100)
    L.tunda(c, 0, 0, 0.75, 0.0, cara="sombra"); c.restore()
    p = clamp((t - w("voltear")) / 3.0)
    glow(c, 540 + 60 * p, 420, 80, "#ffd21a", 0.4 * p)
FOCUS["v03"] = (540, 460)
CAM["v03"] = [("voltear", 1.6, 540, 460)]

def eyes_closed(c, t, n, name=True):
    vgrad(c, 0, 0, P, P, "#100608", "#000")
    bust(c, 540, 1100, 1.15, t, "angry", look=(0, 0), talk=0.8 * abs(math.sin(t * 12)) if t < 2.2 else 0, **YOU)
    for sx in (-1, 1):  # ojos apretados
        ex = 540 + sx * 62; ey = 1100 - 380 * 1.15 + 4 * 1.15
        ell(c, ex, ey, 52, 58, YOU["skin"]); line(c, [(ex - 36, ey - 6), (ex, ey + 6), (ex + 36, ey - 6)], "#1a1110", 9)
    big(c, "¡JOSUÉ ANGULO RENTERÍA!", 540, 260, "#ffd21a", 52)
    big(c, f"{n}", 540, 1010, "#e0303a", 120)

def v04(c, t, T, w): eyes_closed(c, t, 1)
FOCUS["v04"] = (540, 560)
CAM["v04"] = [(0.0, 1.0, 540, 540)]
def v05(c, t, T, w): eyes_closed(c, t + 2, 2)
FOCUS["v05"] = (540, 560)
CAM["v05"] = [(0.0, 1.0, 540, 540)]

def v06(c, t, T, w):
    rio_noche(c, t)
    rrect(c, 640, 640, 300, 80, 30, "#3a5a7a"); glow(c, 780, 600, 140, "#ffffff", 0.3)
    bust(c, 790, 700, 0.35, t, "worry", talk=0.5 * abs(math.sin(t * 10)) if t > w("llamándote") else 0, **MAMA)
    for x in (100, 300): mangle(c, x, 760, 1.1)
FOCUS["v06"] = (760, 600)

def v07(c, t, T, w):
    rio_noche(c, t)
    bust(c, 540, 1080, 1.1, t, "worry", look=(0, -0.2), talk="auto", **MAMA)
FOCUS["v07"] = (540, 600)

def v08(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#100608", "#000")
    o = clamp((t - w("abres")) / 0.25)
    bust(c, 540, 1100, 1.15, t, "shock", look=(0, 0), **YOU)
    if o < 1:
        for sx in (-1, 1):
            ex = 540 + sx * 62; ey = 1100 - 380 * 1.15 + 4 * 1.15
            ell(c, ex, ey, 52, 58 * (1 - o), YOU["skin"])
FOCUS["v08"] = (540, 560)

def v09(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0a140e", "#000")
    glow(c, 540, 520, 520, "#ffd21a", 0.12)
    s_ = 1.5 + 0.25 * ease(clamp(t / T))
    L.icono("La Tunda", c, 540, 560, s_, t)
FOCUS["v09"] = (540, 560)

def v10(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0a140e", "#000")
    L.icono("La Tunda", c, 540, 620, 2.1, t)
    overlay(c, "#300000", 0.15 + 0.2 * clamp((t - w("míos")) / 0.4))
FOCUS["v10"] = (540, 700)
CAM["v10"] = [(0.0, 1.0, 540, 540), ("míos", 1.4, 540, 700)]

def v11(c, t, T, w):
    interior(c, t, lamp=0.3)
    rect(c, 300, 760, 480, 24, "#5a3a22"); rect(c, 330, 784, 20, 120, "#3a2614"); rect(c, 730, 784, 20, 120, "#3a2614")
    rrect(c, 440, 660, 200, 110, 20, "#6a6a72"); ell(c, 540, 664, 100, 18, "#3a3a40")
    for k in range(4):
        yy = 640 - ((t * 50 + k * 30) % 120); line(c, [(500 + k * 25, yy + 30), (510 + k * 25, yy), (500 + k * 25, yy - 30)], hx("#ffffff", 0.5), 5)
    c.save(); c.rectangle(0, 0, 260, P); c.clip(); bust(c, 120, 1100, 0.85, t, "shock", look=(1, 0), tears=1.0, **MAMA); c.restore()
FOCUS["v11"] = (540, 680)

def v12(c, t, T, w):
    manglar(c, t, fog=2.0)
    vgrad(c, 0, 820, P, 260, "#2a2414", "#14100a")
    for i, x in enumerate((360, 520)):
        bust_back(c, x + math.sin(t + i) * 30, 1000, 0.22, t * 2 + i, shirt=("#5fa0e0", "#3c8a5a")[i], hair="#140a06", skin="#6a3e22", hood=False)
    tunda_lejos(c, t, 820, 1000, 0.42)
    overlay(c, "#0a140e", 0.25)
FOCUS["v12"] = (600, 820)

def v13(c, t, T, w):
    manglar(c, t, dark=0.4); tunda_lejos(c, t, 540, 1000, 0.5)
    for i in range(3):
        tt = 0.25 + i * 0.75
        if t > tt: s_ = 1 + 0.5 * math.exp(-(t - tt) * 6); c.save(); c.translate(540, 300 + i * 150); c.scale(s_, s_); big(c, "TUM", 0, 0, "#ffffff", 120); c.restore()
FOCUS["v13"] = (540, 540)
CAM["v13"] = [(0.0, 1.0, 540, 540)]

def v14(c, t, T, w):
    manglar(c, t, dark=0.55); tunda_lejos(c, t, 540, 1000, 0.5); overlay(c, "#000", 0.4)

PANELS = {k: v for k, v in globals().items() if len(k) == 3 and k[0] in "tuv" and k[1:].isdigit() and callable(v)}

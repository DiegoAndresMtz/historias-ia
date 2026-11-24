import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect_path, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp, text_w
from povlib import *
from scenes import popin, tag2, bust_back, bedroom
import leyendas as L
import guion as G

YOU = dict(hat="beanie", skin="#a8704a", shirt="#3c6a9a", cap_col="#e8702a")
LUZ = dict(hat="bun", skin="#b07a52", shirt="#f08aa8", hair_col="#1a120c")
ABUELA = dict(hat="bun", skin="#9a6440", shirt="#5a4a7a", hair_col="#d8d8d8", gray=True)
MAMA = dict(hat="bun", skin="#a87048", shirt="#2f8f7a", hair_col="#1a120c")
FOCUS = {}; CAM = {}

def big(c, s_, x, y, col="#ffffff", size=120):
    ui(c, size); w_ = text_w(c, s_); c.new_path(); c.move_to(x - w_ / 2, y); c.text_path(s_)
    c.set_line_width(16); c.set_line_join(cairo.LINE_JOIN_ROUND); src(c, "#000"); c.stroke_preserve(); src(c, col); c.fill()

# ---------------- escenarios ----------------
def puente(c, y=430, col="#0c1222"):
    """Honda, la ciudad de los puentes: silueta de un puente de hierro al fondo."""
    rect(c, 0, y, P, 16, col)
    for k in range(7):
        x = 40 + k * 160
        line(c, [(x, y), (x + 80, y - 70), (x + 160, y)], col, 8)
        line(c, [(x + 80, y - 70), (x + 80, y)], col, 5)
    rect(c, 0, y - 74, P, 8, col)
    for x in (200, 840): rect(c, x - 18, y, 36, 120, col)

def rio(c, t, moon=True, y0=560, hills=True):
    vgrad(c, 0, 0, P, y0, "#070b18", "#18223a")
    if moon: circ(c, 860, 150, 44, "#eef0f4"); glow(c, 860, 150, 260, "#dfe8ff", 0.2)
    if hills:
        poly(c, [(0, y0 - 60), (180, y0 - 150), (380, y0 - 90), (620, y0 - 170), (860, y0 - 80), (P, y0 - 140), (P, y0), (0, y0)], "#0a1020")
        puente(c, y0 - 70)
    vgrad(c, 0, y0, P, P - y0, "#1a2840", "#050810")
    for k in range(16):
        y = y0 + 20 + k * 30; w_ = 100 + (k * 41) % 220; x = (k * 197 + t * 40) % 1300 - 150
        rect(c, x, y, w_, 3, hx("#a8c0e8", 0.22))
    if moon:
        for k in range(6): rect(c, 820 + math.sin(t * 2 + k) * 20, y0 + 20 + k * 26, 80 - k * 8, 4, hx("#eef0f4", 0.35))

def piedras(c, y=900, n=7, seed=3):
    r = random.Random(seed)
    for k in range(n):
        x = 60 + k * (P / n) + r.uniform(-30, 30); rx = r.uniform(70, 120)
        ell(c, x, y + r.uniform(-20, 40), rx, rx * 0.45, r.choice(["#2a2c34", "#33363e", "#24262c"]))
        ell(c, x - rx * 0.25, y - rx * 0.12 + r.uniform(-20, 40) * 0, rx * 0.4, rx * 0.12, hx("#8a94a8", 0.18))

def casa_honda(c, t, light=1.0, win_fig=None):
    rio(c, t, y0=760, hills=False)
    vgrad(c, 0, 0, P, 300, "#070b18", "#0e1426")
    circ(c, 900, 130, 40, "#eef0f4"); glow(c, 900, 130, 220, "#dfe8ff", 0.18)
    rect(c, 180, 330, 720, 430, "#d8d0c0")                                  # pared blanca encalada
    for k in range(5): line(c, [(220 + k * 140, 360), (240 + k * 140, 420), (230 + k * 140, 470)], hx("#7a6a5a", 0.5), 3)
    poly(c, [(140, 340), (540, 190), (940, 340)], "#8a3a22")               # teja de barro
    for k in range(12): line(c, [(160 + k * 66, 335), (540, 195)], hx("#000", 0.18), 4)
    rect(c, 130, 330, 820, 22, "#6a2a18")
    rect(c, 260, 420, 190, 170, "#3a2216"); rect(c, 274, 434, 162, 142, hx("#ffc070", light))
    if light: glow(c, 355, 505, 220, "#ffb060", 0.3 * light)
    if win_fig: c.save(); c.rectangle(274, 434, 162, 142); c.clip(); win_fig(c); c.restore()
    for k in range(5): rect(c, 280 + k * 34, 434, 6, 142, "#3a2216")    # barrotes
    rect(c, 600, 460, 150, 300, "#5a2a1a"); circ(c, 730, 620, 8, "#c9a24a")
    rect(c, 0, 760, P, 20, "#2a2622")
    overlay(c, "#0a1030", 0.25)

def cuarto(c, t, lamp=1.0, ventana=True, wf=None):
    vgrad(c, 0, 0, P, P, "#4a4a58", "#1e1e28")                             # bahareque blanco en la oscuridad
    for k in range(4): line(c, [(80 + k * 260, 80), (110 + k * 260, 260), (90 + k * 260, 380)], hx("#000", 0.25), 4)
    rect(c, 0, 840, P, 240, "#3a2a24")
    for k in range(8): rect(c, k * 140, 840, 4, 240, hx("#000", 0.3))
    if ventana:
        rect(c, 600, 160, 380, 380, "#2a1a12")
        c.save(); c.rectangle(620, 180, 340, 340); c.clip()
        c.translate(620, 180); c.scale(340 / P, 340 / P); rio(c, t)
        if wf: wf(c)
        c.restore()
        for k in range(4): rect(c, 640 + k * 90, 180, 8, 340, "#2a1a12")
    if lamp: rrect(c, 120, 600, 60, 90, 12, hx("#ffd890", 0.9)); glow(c, 150, 630, 360, "#ffb060", 0.3 * lamp)

def agua(c, t, level, a=1.0, hair=True):
    """Agua negra del río que sube desde abajo. level = y de la superficie."""
    if level >= P: return
    c.new_path(); c.move_to(0, level)
    for k in range(25): c.line_to(k * 45, level + math.sin(t * 3 + k * 0.8) * 8)
    c.line_to(P, P); c.line_to(0, P); c.close_path(); src(c, hx("#0a1420", 0.88 * a)); c.fill()
    for k in range(6):
        y = level + 30 + k * 40
        if y < P: rect(c, (k * 170 + t * 50) % 1200 - 100, y, 140, 3, hx("#6a88b0", 0.25 * a))
    if hair:
        r = random.Random(5)
        for k in range(9):
            x = r.uniform(50, 1030); y = level + r.uniform(20, 200)
            if y < P - 10: line(c, [(x + math.sin(t + k) * 20 + j * 30, y + math.sin(t * 2 + j + k) * 14) for j in range(6)], hx("#000", 0.9 * a), 5)

def mano(c, x, y, s, ang, t, col="#b9c2cc"):
    """Mano pálida de dedos largos."""
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    line(c, [(-260, 0), (0, 0)], "#7d8794", 40); line(c, [(-260, 0), (0, 0)], col, 32)
    ell(c, 20, 0, 40, 34, col)
    for k in range(5):
        a = (k - 2) * 0.28 + math.sin(t * 6 + k) * 0.06; L_ = 110 + (k % 3) * 20
        pts = [(40, 0), (40 + math.cos(a) * L_ * 0.55, math.sin(a) * L_ * 0.55), (40 + math.cos(a + 0.3) * L_, math.sin(a + 0.3) * L_)]
        line(c, pts, col, 13); circ(c, *pts[-1], 6, "#20242a")
    c.restore()

def vestidito(c, x, y, s, t):
    def f():
        poly(c, [(-50, -90), (50, -90), (110, 90), (-110, 90)], "#f08aa8")
        rect(c, -50, -110, 100, 30, "#f08aa8"); circ(c, -30, -110, 22, "#e07090"); circ(c, 30, -110, 22, "#e07090")
        for k in range(5): line(c, [(-90 + k * 45, 60), (-80 + k * 45, 90)], hx("#a04060", 0.6), 4)
        ell(c, 0, 20, 24, 14, hx("#2a2030", 0.4))
    scaled(c, x, y, s, f)

def techo(c, t, dark=0.0, water=780):
    vgrad(c, 0, 0, P, P, "#070b18", "#16203a")
    circ(c, 860, 140, 40, "#eef0f4"); glow(c, 860, 140, 240, "#dfe8ff", 0.18)
    for x, w_, h in ((40, 220, 600), (760, 280, 640)):                      # casas vecinas medio hundidas
        rect(c, x, h, w_, 300, "#5a5450"); poly(c, [(x - 20, h), (x + w_ / 2, h - 90), (x + w_ + 20, h)], "#5a2a1a")
    agua(c, t, water, hair=False)
    poly(c, [(0, P), (0, 900), (540, 820), (P, 900), (P, P)], "#7a3420")    # nuestro techo de teja
    for k in range(14): line(c, [(k * 80, P), (540, 822)], hx("#000", 0.22), 5)
    if dark: overlay(c, "#000", dark)

# ---------------- PARTE 1 ----------------
R = G.RULETA
def t00(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#140c10", "#050304")
    tt = t - R["start"]
    L.ruleta(c, 540, 600, 410, max(0, tt), R["dur"], R["target"], win=clamp((tt - R["dur"]) / 0.3))
FOCUS["t00"] = (540, 560)
CAM["t00"] = [(0.0, 1.0, 540, 560)]

def t01(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0a0e1a", "#020306")
    glow(c, 540, 480, 520, "#bcd4ff", 0.25)
    sc = 0.4 + 0.75 * ease(clamp(t / 0.5))
    L.icono("La Llorona", c, 540, 470, sc, t)
    big(c, "LA LLORONA", 540, 980, "#dfe8ff", 110)
FOCUS["t01"] = (540, 520)
CAM["t01"] = [(0.0, 1.0, 540, 540)]

def t02(c, t, T, w):
    def kid(c_):
        if t > w("luz") - 0.2: bust(c, 355, 640, 0.36, t, "smile", look=(0.4, 0), **LUZ)
    casa_honda(c, t, win_fig=kid)
    tag2(c, 540, 880, "HONDA · TOLIMA", t, w("honda"), "#ffffff")
    if t > w("magdalena") - 0.2: tag2(c, 540, 980, "RÍO MAGDALENA", t, w("magdalena"), "#9ac8ff")
FOCUS["t02"] = (420, 500)

def foto_mama(c, x, y, t, candle=True):
    rect(c, x - 70, y - 90, 140, 180, "#3a2416"); rect(c, x - 58, y - 78, 116, 156, "#c8b898")
    c.save(); c.rectangle(x - 58, y - 78, 116, 156); c.clip(); bust(c, x, y + 120, 0.3, 0, "smile", **MAMA); c.restore()
    line(c, [(x - 70, y - 90), (x - 30, y - 120), (x + 70, y - 90)], "#111", 6)
    if candle:
        rect(c, x + 90, y + 40, 22, 60, "#f0ead8"); ell(c, x + 101, y + 30, 9, 16, "#ffc24a"); glow(c, x + 101, y + 30, 120, "#ffb060", 0.35)

def t03(c, t, T, w):
    cuarto(c, t, lamp=0)
    foto_mama(c, 220, 420, t)
    bust_back(c, 790, 1000, 0.62, t, shirt=LUZ["shirt"], hair=LUZ["hair_col"], skin=LUZ["skin"], hood=False)
    circ(c, 790, 1000 - 380 * 0.62 - 120, 40, LUZ["hair_col"])
    if t > w("ahogó") - 0.2: tag2(c, 380, 640, "HACE UN AÑO", t, w("año"), "#e0303a", "#ffffff", 34)
FOCUS["t03"] = (600, 560)

def t04(c, t, T, w):
    cuarto(c, t, lamp=0.8)
    bust(c, 330, 1080, 0.95, t, "worry", look=(0.6, 0), talk="auto", **ABUELA)
    bust(c, 820, 1110, 0.8, t, "neutral", look=(-0.8, 0), **YOU)
    tag2(c, 540, 380, "NO LA MIRES", t, w("mires"), "#ffc24a", "#11131a", 38)
    tag2(c, 540, 470, "NUNCA LE CONTESTES", t, w("contestes"), "#e0303a", "#ffffff", 40)
FOCUS["t04"] = (330, 600)

def t05(c, t, T, w):
    bedroom(c, t, "12:00")
    rrect(c, 380, 840, 700, 260, 40, "#2a3460")
    c.save(); c.rectangle(0, 0, P, 880); c.clip()
    bust(c, 700, 1140, 0.85, t, "shock" if t > w("llanto") - 0.1 else "tired", look=(0.4, -0.6), **YOU); c.restore()
    rrect(c, 360, 880, 720, 220, 40, "#38447a")
    if t > w("llanto"):
        for k in range(3):
            a = ((t - w("llanto")) * 0.7 + k / 3) % 1
            c.new_path(); c.arc(860, 270, 40 + 160 * a, 0, 2 * math.pi); c.set_line_width(4); src(c, hx("#dfe8ff", 0.4 * (1 - a))); c.stroke()
FOCUS["t05"] = (540, 600)
CAM["t05"] = [(0.0, 1.0, 540, 540)]

def t06(c, t, T, w):
    rio(c, t)
    piedras(c, 900)
    L.llorona_cuerpo(c, 560, 880, 0.36, t, cara="sombra", brazos="lavando", rodillas=True)
    for k in range(3):
        a = (t * 0.6 + k / 3) % 1
        c.new_path(); c.arc(560, 700, 60 + 260 * a, 0, 2 * math.pi); c.set_line_width(4); src(c, hx("#dfe8ff", 0.3 * (1 - a))); c.stroke()
FOCUS["t06"] = (560, 760)
CAM["t06"] = [(0.0, 1.0, 540, 540), ("hijos", 1.5, 560, 740)]

def t07(c, t, T, w):
    cuarto(c, t, lamp=0)
    bust_back(c, 790, 1000, 0.62, t, shirt=LUZ["shirt"], hair=LUZ["hair_col"], skin=LUZ["skin"], hood=False)
    circ(c, 790, 1000 - 380 * 0.62 - 120, 40, LUZ["hair_col"])
    bust(c, 300, 1120, 0.8, t, "worry", look=(1, -0.2), **YOU)
FOCUS["t07"] = (560, 600)

def t08(c, t, T, w):
    cuarto(c, t, lamp=0)
    glow(c, 540, 600, 500, "#bcd4ff", 0.12)
    bust(c, 540, 1080, 1.15, t * 0.2, "tired", look=(0, 0), talk="auto", **LUZ)
FOCUS["t08"] = (540, 600)

def t09(c, t, T, w):
    rio(c, t)
    piedras(c, 920)
    L.llorona_cuerpo(c, 520, 900, 0.62, t, cara="pelo", brazos="lavando", rodillas=True)
    vgrad(c, 0, 0, 110, P, "#2a1a12", "#2a1a12"); rect(c, 970, 0, 110, P, "#2a1a12"); rect(c, 0, 0, P, 60, "#2a1a12")
    for x in (330, 560, 790): rect(c, x, 0, 12, P, "#2a1a12")
FOCUS["t09"] = (520, 560)
CAM["t09"] = [("blanco", 1.25, 520, 700), ("cara", 1.8, 530, 430)]

def t10(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0e1626", "#03060c")
    agua(c, t, 760, hair=False)
    wob = math.sin(t * 4) * 20
    vestidito(c, 540 + wob, 640, 1.6, t)
    mano(c, 320 + wob, 560, 1.0, 0.2, t); mano(c, 760 + wob, 560, 1.0, math.pi - 0.2, t)
    if t > w("igualito") - 0.1:
        a = popin(t, w("igualito") - 0.1)
        c.save(); c.translate(870, 300); c.scale(a, a)
        circ(c, 0, 0, 150, "#2a1a12"); c.save(); c.new_path(); c.arc(0, 0, 140, 0, 2 * math.pi); c.clip()
        rect(c, -150, -150, 300, 300, "#3a3a48"); bust(c, 0, 230, 0.55, t, "tired", **LUZ); c.restore(); c.restore()
FOCUS["t10"] = (540, 600)

def t11(c, t, T, w):
    rio(c, t, moon=False); overlay(c, "#000", 0.3)
    rect(c, 140, 140, 800, 940, "#d8d0c0"); rect(c, 240, 260, 600, 820, "#2a1a12"); rect(c, 260, 280, 560, 800, "#3a3440")
    glow(c, 540, 620, 400, "#ffb060", 0.15)
    bust(c, 540, 1120, 1.0, t, "happy", look=(0, 0.3), arms="up", talk="auto", **LUZ)
    for k in range(5): rect(c, 280 + k * 120, 280, 12, 800, hx("#2a1a12", 0.0))
FOCUS["t11"] = (540, 600)

def t12(c, t, T, w):
    rio(c, t)
    piedras(c, 960)
    p = ease(clamp((t - w("pie") + 0.2) / 1.2)); q = ease(clamp((t - w("subiendo")) / 2.0))
    alto = 0.62 + 0.38 * p + 0.45 * q
    L.llorona_cuerpo(c, 540, 960, 0.55, t, cara="pelo", brazos="caidos", rodillas=False, alto=alto / 1.0 if p > 0 else 0.62)
    if t > w("metros") - 0.2: tag2(c, 820, 400, "+3 METROS", t, w("metros"), "#e0303a", "#ffffff", 44)
FOCUS["t12"] = (540, 500)
CAM["t12"] = [(0.0, 1.0, 540, 540), ("subiendo", 1.3, 540, 420)]

def t13(c, t, T, w):
    rio(c, t); piedras(c, 960)
    L.llorona_cuerpo(c, 540, 960, 0.5, t, cara="pelo", alto=1.45); overlay(c, "#000", 0.45)

# ---------------- PARTE 2 ----------------
def u01(c, t, T, w):
    cuarto(c, t, lamp=0.4)
    bust(c, 420, 1100, 1.0, t * 2, "angry", look=(0.5, 0), tears=1.0, talk=0.5 * abs(math.sin(t * 9)) if t > w("llorando") else 0, **LUZ)
    bust(c, 860, 1120, 0.8, t, "shock" if t > w("muerde") else "worry", look=(-1, 0), arms="hold", **YOU)
FOCUS["u01"] = (500, 620)

def rosario(c, x, y, s, t):
    for k in range(18):
        a = k / 18 * 2 * math.pi; circ(c, x + math.cos(a) * 60 * s, y + math.sin(a) * 80 * s, 8 * s, "#c8b8a0")
    line(c, [(x, y + 80 * s), (x, y + 150 * s)], "#c8b8a0", 5 * s)
    rect(c, x - 3 * s, y + 140 * s, 6 * s, 50 * s, "#d8c890"); rect(c, x - 18 * s, y + 152 * s, 36 * s, 6 * s, "#d8c890")

def u02(c, t, T, w):
    cuarto(c, t, lamp=0.6)
    bust(c, 400, 1080, 1.0, t, "shock" if t > w("contestó") else "worry", arms="hold", **ABUELA)
    tc = w("cae")
    if t < tc: rosario(c, 420, 850, 1.0, t)
    else:
        f = clamp((t - tc) / 0.4); rosario(c, 420 + 60 * f, 850 + 160 * ease(f), 1.0, t)
FOCUS["u02"] = (420, 640)

def u03(c, t, T, w):
    cuarto(c, t, lamp=0.6)
    bust(c, 540, 1080, 1.15, t, "sad", tears=1.0, talk="auto", **ABUELA)
FOCUS["u03"] = (540, 600)

def u04(c, t, T, w):
    rio(c, t); overlay(c, "#2a1a08", 0.35)                                  # recuerdo, color viejo
    piedras(c, 940)
    L.llorona_cuerpo(c, 300, 940, 0.5, t, cara="pelo", brazos="caidos")
    if t > w("hijos") - 0.2:
        for i, x in enumerate((650, 790)):
            yy = 700 + math.sin(t * 2 + i) * 8
            ell(c, x, yy, 60, 14, "#c8a860"); ell(c, x, yy - 14, 30, 18, "#c8a860")    # dos sombreritos flotando
    if t > w("niño") - 0.4: tag2(c, 600, 440, "SE LLEVA AL QUE LE CONTESTE", t, w("niño"), "#e0303a", "#ffffff", 34)
FOCUS["u04"] = (500, 600)

def u05(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#140c10", "#050304")
    rect(c, 140, 820, 26, 80, "#f0ead8"); ell(c, 153, 810, 11, 20, "#ffc24a"); glow(c, 153, 810, 160, "#ffb060", 0.4)
    for i, (tok, s_) in enumerate((("gallo", "1. HASTA QUE CANTE EL GALLO"), ("salir", "2. LUZ NO PUEDE SALIR"), ("agua", "3. NI TOCAR EL AGUA"))):
        tag2(c, 560, 380 + i * 170, s_, t, w(tok), "#ffc24a" if i < 2 else "#e0303a", "#11131a" if i < 2 else "#ffffff", 42)
FOCUS["u05"] = (540, 560)

def puerta(c, t, level=P, wet=0.0, knock_t=None):
    door_x = 300
    vgrad(c, 0, 0, P, P, "#2a2a34", "#121218")
    rect(c, door_x, 80, 480, 940, "#3a2416"); rect(c, door_x + 30, 110, 420, 910, "#5a3a22")
    rect(c, door_x + 70, 160, 340, 330, hx("#000", 0.18)); rect(c, door_x + 70, 540, 340, 400, hx("#000", 0.18))
    rect(c, door_x + 390, 600, 22, 60, "#9a7a3a")
    rect(c, 0, 1020, P, 60, "#3a2a24")
    if wet:
        for k in range(5): ell(c, door_x + 140 + k * 50, 460 + (k % 2) * 40, 24, 16, hx("#0a1420", 0.6 * wet))
    rect(c, door_x + 30, 1012, 420, 10, hx("#9ab8e0", 0.5))
    agua(c, t, level)

def u06(c, t, T, w):
    sh = 0
    for i in range(3):
        tt = w("tres") + i * 0.35
        if tt <= t < tt + 0.2: sh = 8
    c.save(); c.translate(sh, 0); puerta(c, t, wet=clamp((t - w("mojados")) / 0.4)); c.restore()
    for i in range(3):
        tt = w("tres") + i * 0.35
        if t > tt: big(c, "TOC", 260 + i * 280, 360 + i * 30, hx("#ffffff", clamp(1 - (t - tt) / 2.5)), 90)
FOCUS["u06"] = (540, 540)

def u07(c, t, T, w):
    puerta(c, t, wet=1.0)
    glow(c, 540, 1010, 260, "#dfe8ff", 0.25 + 0.15 * math.sin(t * 3))
    for k in range(4): line(c, [(380 + k * 100, 1018), (390 + k * 100 + math.sin(t + k) * 20, 1040)], "#000", 5)
FOCUS["u07"] = (540, 800)
CAM["u07"] = [(0.0, 1.0, 540, 540), ("frío", 1.4, 540, 800)]

def u08(c, t, T, w):
    cuarto(c, t, lamp=0.3)
    bust(c, 540, 1100, 1.15, t, "shock", look=(0.3, 0), sweat=1.0, **YOU)
    if t > w("enterrar") - 0.3:
        a = popin(t, w("enterrar") - 0.3)
        c.save(); c.translate(860, 300); c.scale(a, a); foto_mama(c, 0, 0, t, candle=False); c.restore()
FOCUS["u08"] = (540, 600)

def u09(c, t, T, w):
    lv = 1020 - 80 * ease(clamp((t - w("agua")) / 3.0))
    puerta(c, t, level=lv if t > w("agua") - 0.2 else P, wet=1.0)
FOCUS["u09"] = (540, 940)
CAM["u09"] = [(0.0, 1.3, 540, 820), ("pelos", 1.7, 540, 940)]

def u10(c, t, T, w):
    cuarto(c, t, lamp=0.3)
    bust(c, 330, 1120, 0.85, t, "shock", look=(0, 0.6), **YOU)
    bust(c, 780, 1140, 0.7, t, "sad", tears=1.0, look=(0, 0.6), **LUZ)
    lv = 1000 - 260 * ease(clamp((t - w("tobillos")) / (w("casa") - w("tobillos") + 0.5)))
    agua(c, t, lv)
FOCUS["u10"] = (540, 760)

def u11(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0a1828", "#02060c")
    for k in range(12): circ(c, (k * 97) % P, (P - (t * 120 + k * 90) % P), 6 + k % 3 * 3, hx("#9ab8e0", 0.25))
    rrect(c, 640, -40, 180, 1000, 80, "#2a3a5a")                           # tu pierna (pantalón)
    rrect(c, 630, 920, 220, 90, 40, "#1a1a1a")
    p = ease(clamp((t - w("roza") + 0.3) / 1.2))
    mano(c, -120 + 620 * p, 700 - 40 * p, 1.1, -0.15, t)
    r = random.Random(2)
    for k in range(10):
        x = r.uniform(0, 500); y = r.uniform(300, 1000)
        line(c, [(x + j * 30, y + math.sin(t * 2 + j + k) * 16) for j in range(7)], hx("#000", 0.85), 5)
FOCUS["u11"] = (560, 700)

def u12(c, t, T, w):
    cuarto(c, t, lamp=0.2)
    bust(c, 540, 1080, 1.1, t, "shock", look=(0, 0.6), arms="up", tears=1.0, talk="auto" if t < w("tobillo") else 0.8, shake=1.0, **LUZ)
    agua(c, t, 860)
    if t > w("mano") - 0.2: mano(c, 120, 960, 1.0, -0.1, t)
FOCUS["u12"] = (540, 640)

def u13(c, t, T, w):
    puerta(c, t, level=900, wet=1.0); overlay(c, "#000", 0.45)

# ---------------- PARTE 3 ----------------
def v01(c, t, T, w):
    cuarto(c, t, lamp=0, ventana=False)
    rect(c, 300, 0, 480, 200, "#050505")                                    # el hueco del zarzo
    for k in range(5): rect(c, 360, 220 + k * 120, 360, 14, "#5a3a22")
    rect(c, 350, 200, 16, 700, "#5a3a22"); rect(c, 714, 200, 16, 700, "#5a3a22")
    p = ease(clamp((t - w("subes")) / 2.0))
    bust(c, 560, 640 - 260 * p, 0.55, t * 3, "shock", look=(0, -1), arms="up", **LUZ)
    bust(c, 520, 1000 - 200 * p, 0.8, t * 3, "shock", look=(0, -1), arms="up", **YOU)
    agua(c, t, 900)
FOCUS["v01"] = (540, 540)

def v02(c, t, T, w):
    techo(c, t)
    L.llorona_cuerpo(c, 540, 800, 0.42, t, cara="pelo", brazos="abiertos" if t > w("brazos") - 0.3 else "caidos")
    agua(c, t, 800, a=0.6, hair=False)
FOCUS["v02"] = (540, 560)
CAM["v02"] = [(0.0, 1.0, 540, 540), ("mujer", 1.45, 540, 560)]

def v03(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#5a2a1a", "#3a1a10")
    for k in range(10): line(c, [(k * 120, 0), (k * 120 + 40, P)], hx("#000", 0.2), 6)
    rect(c, 300, 300, 480, 480, "#050505")
    c.save(); c.rectangle(300, 300, 480, 480); c.clip(); agua(c, t, 560); c.restore()
    rosario(c, 520 + math.sin(t) * 20, 600 + math.sin(t * 2) * 6, 0.8, t)
FOCUS["v03"] = (540, 560)
CAM["v03"] = [(0.0, 1.0, 540, 540), ("escuchas", 1.4, 540, 600)]

def v04(c, t, T, w):
    techo(c, t, dark=0.2)
    L.llorona_cuerpo(c, 540, 980, 0.75, t, cara="pelo", brazos="abiertos")
    agua(c, t, 950, a=0.6, hair=False)
FOCUS["v04"] = (540, 420)
CAM["v04"] = [(0.0, 1.2, 540, 420)]

def v05(c, t, T, w):
    techo(c, t)
    L.llorona_cuerpo(c, 560, 800, 0.42, t, cara="pelo", brazos="abiertos")
    agua(c, t, 800, a=0.6, hair=False)
    p = ease(clamp((t - w("camina")) / 3.0))
    bust_back(c, 480 + 60 * p, 1120 - 140 * p, 0.42 - 0.08 * p, t * 3, shirt=LUZ["shirt"], hair=LUZ["hair_col"], skin=LUZ["skin"], hood=False)
FOCUS["v05"] = (540, 760)

def v06(c, t, T, w):
    techo(c, t, dark=0.3)
    bust(c, 540, 1100, 1.15, t, "shock", look=(0, -0.3), arms="up", talk="auto", sweat=1.0, **YOU)
FOCUS["v06"] = (540, 600)

def v07(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0a1020", "#000")
    glow(c, 540, 500, 520, "#bcd4ff", 0.15)
    op = t > w("abre") - 0.1
    L.llorona_cuerpo(c, 540, 1500, 1.0, t, cara="calavera" if op else "pelo", brazos="pelo" if t > w("despacio") - 0.2 else "caidos")
FOCUS["v07"] = (540, 420)
CAM["v07"] = [(0.0, 1.0, 540, 540), ("despacio", 1.3, 540, 420)]

def v08(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#0a1020", "#000")
    glow(c, 540, 520, 520, "#bcd4ff", 0.15)
    if t < w("brazos") - 0.2:
        L.icono("La Llorona", c, 540, 540, 1.55 + 0.2 * ease(clamp(t / T)), t)
    else:
        L.llorona_cuerpo(c, 540, 1500, 1.0, t, cara="calavera", brazos="bulto", bulto=True)
FOCUS["v08"] = (540, 540)
CAM["v08"] = [(0.0, 1.0, 540, 540), ("bulto", 1.35, 540, 700)]

def v09(c, t, T, w):
    d = clamp(t / T)
    vgrad(c, 0, 0, P, P, "#0a2038", "#000")
    overlay(c, "#000", 0.5 * d)
    c.save(); c.translate(0, -300 * d)
    c.save(); c.translate(540, 260); c.scale(0.4, 0.4); c.translate(-540, -260)
    L.llorona_cuerpo(c, 540, 260, 1.0, t, cara="pelo", brazos="caidos", glow_a=1.6); c.restore()
    c.restore()
    bust(c, 540, 1060 + 80 * d, 0.85, t, "shock", look=(0, -1), arms="hold", **YOU)
    ell(c, 540, 1000 + 80 * d, 130, 80, "#5a5040")
    for k in range(14): circ(c, 300 + (k * 61) % 480, (900 - (t * 200 + k * 70) % 900), 5 + k % 3 * 4, hx("#bcd4ff", 0.35))
FOCUS["v09"] = (540, 760)

def v10(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#e8a070", "#6a7aa0")
    circ(c, 200, 620, 90, "#ffd0a0"); glow(c, 200, 620, 300, "#ffd0a0", 0.3)
    rect(c, 0, 640, P, 440, "#6a6050")
    agua(c, t, 900, a=0.5, hair=False)
    rect(c, 820, 280, 24, 700, "#3a3028")                                   # el poste
    bust(c, 830, 1060, 0.6, t, "sad", tears=1.0, arms="hold", **ABUELA)
    poly(c, [(80, 900), (380, 760), (680, 900)], "#7a3420")
    c.save(); c.translate(380, 830); c.rotate(-1.35); bust(c, 0, 0, 0.32, 0, "tired", **LUZ); c.restore()
FOCUS["v10"] = (600, 760)

def v11(c, t, T, w):
    vgrad(c, 0, 0, P, 520, "#9ab0c8", "#c8d0d8")
    rect(c, 0, 520, P, 240, "#6a7a88")
    for k in range(10): rect(c, (k * 160 + t * 30) % 1200 - 100, 540 + k * 20, 120, 3, hx("#ffffff", 0.3))
    rect(c, 0, 760, P, 320, "#8a8478"); piedras(c, 860, 6, 9)
    for i, x in enumerate((460, 600)):                                       # los zapatos, uno al lado del otro
        rrect(c, x - 60, 880, 120, 60, 26, "#2a2a32"); rrect(c, x - 60, 920, 130, 24, 10, "#e8e8e8")
        ell(c, x - 10, 890, 30, 12, "#111")
FOCUS["v11"] = (530, 900)
CAM["v11"] = [(0.0, 1.0, 540, 540), ("zapatos", 1.7, 530, 900)]

def v12(c, t, T, w):
    rio(c, t); piedras(c, 960)
    for k in range(5): ell(c, (t * 25 + k * 260) % 1400 - 200, 860 + k * 30, 340, 40, hx("#c8d0e0", 0.08))
    L.llorona_cuerpo(c, 620, 960, 0.45, t, cara="pelo", brazos="caidos")
    bust_back(c, 400, 1000, 0.26, t, shirt=YOU["shirt"], hair="#1a120c", skin=YOU["skin"], hood=False)
    c.new_path(); c.arc(400, 1000 - 380 * 0.26 - 4, 38, math.pi, 2 * math.pi); c.close_path(); fill(c, YOU["cap_col"])
    overlay(c, "#0a1020", 0.25)
FOCUS["v12"] = (540, 760)

def v13(c, t, T, w):
    rio(c, t); piedras(c, 960)
    L.llorona_cuerpo(c, 620, 960, 0.45, t, cara="pelo")
    bust_back(c, 400, 1000, 0.26, t, shirt=YOU["shirt"], hair="#1a120c", skin=YOU["skin"], hood=False)
    overlay(c, "#000", 0.45)

PANELS = {k: v for k, v in globals().items() if len(k) == 3 and k[0] in "tuv" and k[1:].isdigit() and callable(v)}

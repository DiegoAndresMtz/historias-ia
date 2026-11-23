import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect_path, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp, text_w, fog
from povlib import *
from scenes import hw, popin, tag2, paper_note
import monstruos as M

# Estilo clásico («Tu IA te hizo rico»): protagonista de gorro naranja, colores planos
YOU = dict(hat="beanie", skin="#c48a5c", shirt="#2e3f6e", cap_col="#e8702a")
VALE = dict(hat="bun", skin="#d2a27a", shirt="#25336a", hair_col="#2a1a14")
VALE_FANT = dict(hat="bun", skin="#c4ccd2", shirt="#1e2a50", hair_col="#141018")
HERNAN = dict(hat="none", skin="#b07a52", shirt="#6a7686", hair_col="#1a120e", mustache=True)
PATRU = dict(hat="cap", skin="#a8704a", shirt="#3d5a34", cap_col="#2f4a2a")
AMARILLO = "#c9a232"   # el carro de don Hernán
AZUL = "#2f5f9a"       # tu carro
FOCUS = {}; CAM = {}

def TALK():
    import povlib
    return povlib.TALK

# ---------------- escenarios ----------------
def eucalipto(c, x, base, h, s=1.0, col="#07100b", seed=0):
    rr = random.Random(seed)
    line(c, [(x, base), (x + 6 * s, base - h * 0.5), (x - 4 * s, base - h)], col, 16 * s)
    for k in range(7):
        yy = base - h + k * h * 0.09
        ell(c, x + rr.uniform(-50, 50) * s, yy, rr.uniform(50, 80) * s, rr.uniform(26, 40) * s, col)

def noche(c, t, dawn=0.0, cross=True, fog_a=0.12, trees=True):
    if dawn > 0:
        vgrad(c, 0, 0, P, 660, "#3a3a5e", "#d8946a")
    else:
        vgrad(c, 0, 0, P, 660, "#03050c", "#121a30")
        for k in range(50):
            rr = random.Random(k); circ(c, rr.uniform(0, P), rr.uniform(0, 420), rr.uniform(1, 2.4), hx("#ffffff", 0.45 + 0.2 * math.sin(t * 2 + k)))
        glow(c, 880, 150, 140, "#dfe8ff", 0.25); circ(c, 880, 150, 40, "#e8eef8")
    hill = "#1a2030" if not dawn else "#4a4a62"
    poly(c, [(0, 660), (0, 520), (220, 450), (430, 520), (640, 430), (860, 500), (P, 440), (P, 660)], hill)
    rect(c, 0, 640, P, 440, "#101810" if not dawn else "#3a4a2c")
    if trees:
        tc = "#060c08" if not dawn else "#1c2418"
        for i, (x, h) in enumerate(((40, 470), (150, 520), (260, 430), (800, 500), (910, 560), (1030, 450))):
            eucalipto(c, x, 700, h, 1.0, tc, i)
    # postes de cerca
    for k in range(12):
        x = 30 + k * 95
        if 380 < x < 700: continue
        rect(c, x, 690, 8, 50, "#2a2218"); line(c, [(x, 700), (x + 95, 700)], hx("#5a5a5a", 0.5), 2)
    if cross:   # vía que sube al horizonte
        poly(c, [(500, 650), (580, 650), (700, 760), (380, 760)], "#3a2e22" if not dawn else "#6a5440")
    rect(c, 0, 760, P, 160, "#3a2e22" if not dawn else "#6a5440")
    for k in range(2): rect(c, 0, 800 + k * 70, P, 6, hx("#000", 0.25))
    if fog_a: fog(c, 720, t, fog_a, "#9aa4c0" if not dawn else "#e8d0c0")

def carro(c, x, y, s, t, col, lights=1.0, door=0.0, inner=0.0, face=1, rear=None, front=None, smoke=True, patrol=False):
    """Carro de lado. (x, y) = suelo bajo el centro. face=1 mira a la derecha."""
    c.save(); c.translate(x, y); c.scale(face * s, s)
    if lights > 0:   # cono de luz delantero
        g = cairo.LinearGradient(300, 0, 1100, 0)
        g.add_color_stop_rgba(0, 1, 0.96, 0.75, 0.45 * lights); g.add_color_stop_rgba(1, 1, 0.96, 0.75, 0)
        c.new_path(); c.move_to(305, -165); c.line_to(1200, -330); c.line_to(1200, 40); c.line_to(305, -125); c.close_path(); c.set_source(g); c.fill()
    ell(c, 0, -4, 340, 18, hx("#000", 0.5))
    if smoke and lights > 0:
        for k in range(4):
            a = (t * 0.7 + k / 4) % 1
            circ(c, -330 - 120 * a, -70 - 50 * a, 18 + 40 * a, hx("#b0b0b8", 0.35 * (1 - a)))
    poly(c, [(-215, -185), (-150, -300), (140, -300), (225, -185)], col)
    rrect(c, -315, -195, 630, 150, 34, col)
    rect(c, -315, -110, 630, 10, hx("#000", 0.18))
    win = hx("#ffe6a0", 0.85) if inner > 0 else "#141c2c"
    rw = [(-192, -192), (-140, -286), (-14, -286), (-14, -192)]
    fw = [(6, -192), (6, -286), (128, -286), (205, -192)]
    poly(c, rw, win); poly(c, fw, win)
    for pts, cb in ((rw, rear), (fw, front)):
        if cb:
            c.save(); c.new_path(); c.move_to(*pts[0])
            for p in pts[1:]: c.line_to(*p)
            c.close_path(); c.clip(); cb(c); c.restore()
    if inner <= 0:
        for pts in (rw, fw): line(c, [pts[1], (pts[1][0] + 40, pts[1][1] + 50)], hx("#ffffff", 0.12), 10)
    line(c, [(-4, -300), (-4, -60)], hx("#000", 0.3), 5)
    if door > 0:   # puerta del conductor abierta hacia ti
        poly(c, [(6, -192), (205, -192), (225, -60), (6, -60)], "#0c0c10")
        glow(c, 100, -150, 150, "#ffe6a0", 0.35 * max(inner, 0.4))
        dx_ = 70 * door
        poly(c, [(6 + dx_, -300 + 20), (150 + dx_ * 1.6, -300 + 30), (240 + dx_ * 1.6, -40), (6 + dx_, -30)], hx(col, 1.0))
        poly(c, [(6 + dx_, -300 + 20), (150 + dx_ * 1.6, -300 + 30), (190 + dx_ * 1.6, -190), (6 + dx_, -190)], hx("#141c2c", 0.9))
        line(c, [(6 + dx_, -300 + 20), (6 + dx_, -30)], hx("#000", 0.35), 6)
    for wx in (-195, 195):
        circ(c, wx, -50, 60, "#0e0e10"); circ(c, wx, -50, 30, "#6a6a70")
        a = t * 8; line(c, [(wx + math.cos(a) * 24, -50 + math.sin(a) * 24), (wx - math.cos(a) * 24, -50 - math.sin(a) * 24)], "#3a3a40", 6)
    rrect(c, 290, -170, 26, 40, 8, hx("#fff4c0", 0.4 + 0.6 * lights))
    rrect(c, -318, -170, 20, 36, 6, hx("#ff2a2a", 0.4 + 0.6 * lights)); glow(c, -320, -150, 60, "#ff2a2a", 0.4 * lights)
    if patrol:
        rect(c, -315, -140, 630, 26, "#2f7a3a"); rect(c, -60, -320, 120, 22, "#1a1a1a")
        b = (t * 3) % 1
        glow(c, -30, -310, 80, "#ff2a2a", 0.6 * (b < 0.5)); glow(c, 30, -310, 80, "#2a6aff", 0.6 * (b >= 0.5))
        rect(c, -58, -318, 56, 16, hx("#ff2a2a", 0.6 + 0.4 * (b < 0.5))); rect(c, 2, -318, 56, 16, hx("#2a6aff", 0.6 + 0.4 * (b >= 0.5)))
        c.save(); c.scale(face, 1); txt(c, "POLICÍA", -60 * face, -150, "#ffffff", 32, True); c.restore()
    c.restore()

def conductor_tu(c, mood="neutral", t=0.0):
    bust(c, 70, -190, 0.26, t, mood, look=(0.6, 0), **YOU)

def tinto(c, x, y, s, t, steam=1.0):
    def f():
        rrect(c, -90, -40, 180, 120, 20, "#1a1a1e")
        poly(c, [(-60, -170), (60, -170), (48, 40), (-48, 40)], "#f4f0e8"); ell(c, 0, -170, 60, 16, "#5a3a22")
        rect(c, -58, -110, 116, 30, "#c0302a")
        for k in range(3):
            a = (t * 0.5 + k / 3) % 1
            line(c, [(-20 + k * 20, -190), (-30 + k * 20 + 20 * math.sin(t * 3 + k), -260 - 120 * a)], hx("#e8e8f0", 0.6 * (1 - a) * steam), 10)
    scaled(c, x, y, s, f)

def maleta(c, x, y, s, open_=0.0):
    def f():
        rrect(c, -110, -150, 220, 280, 50, "#e86aa0"); rrect(c, -80, 10, 160, 100, 24, "#d24a88")
        line(c, [(-70, -150), (-60, -200), (60, -200), (70, -150)], "#c03a78", 16)
        circ(c, 60, 20, 18, "#ffd23a"); line(c, [(60, 0), (60, -30)], "#999", 4)   # llavero
        if open_ > 0:
            rrect(c, -70, -200 - 60 * open_, 140, 100, 8, "#f4d0e0"); txt(c, "VALE", 0, -140 - 60 * open_, "#a03060", 30, True)
    scaled(c, x, y, s, f)

def silla_nina(c, x, y, s):
    def f():
        rrect(c, -120, -260, 240, 360, 60, "#7a4a9a"); rrect(c, -80, -200, 160, 260, 40, "#9a6aba")
        line(c, [(-60, -120), (0, 40)], "#2a2a2a", 14); line(c, [(60, -120), (0, 40)], "#2a2a2a", 14); circ(c, 0, 40, 18, "#c0c0c0")
    scaled(c, x, y, s, f)

def asiento_atras(c, t, girl=None, backpack=True, child=True, dark=0.0, hand=0.0):
    vgrad(c, 0, 0, P, P, "#1a1c24", "#0c0d12")
    poly(c, [(120, 100), (960, 100), (900, 380), (180, 380)], "#0a1020")      # vidrio de atrás
    for k in range(25):
        rr = random.Random(k); circ(c, rr.uniform(200, 880), rr.uniform(120, 360), 1.5, hx("#ffffff", 0.4))
    eucalipto(c, 300, 380, 200, 0.6, "#04080a"); eucalipto(c, 760, 380, 230, 0.6, "#04080a", 3)
    rrect(c, 60, 380, 960, 330, 60, "#3a3640")                                 # espaldar
    for k in range(3): rrect(c, 90 + k * 310, 410, 280, 280, 40, "#45404c")
    rrect(c, 40, 680, 1000, 200, 40, "#332f38")                                # cojín
    rect(c, 0, 880, P, 200, "#141218")
    if child: silla_nina(c, 230, 640, 1.0)
    if girl: girl(c)
    if backpack: maleta(c, 820, 720, 0.9)
    if hand > 0:   # manito pálida en tu hombro
        c.save(); c.translate(980 - 120 * hand, 1080); ell(c, 0, -40, 70, 50, "#c4ccd2")
        for k in range(4): line(c, [(-40 + k * 26, -60), (-50 + k * 30, -140)], "#c4ccd2", 22)
        c.restore()
    if dark: overlay(c, "#000", dark)

def cabina(c, t, mirror=None, speed=0.0, note=False, keys=True, road=True, outside=None, glowdash=1.0):
    """Adentro del carro, mirando hacia adelante."""
    rect(c, 0, 0, P, P, "#0c0d12")
    c.save(); c.new_path(); c.move_to(110, 90); c.line_to(970, 90); c.line_to(1080, 600); c.line_to(0, 600); c.close_path(); c.clip()
    vgrad(c, 0, 90, P, 520, "#03050c", "#121a30")
    poly(c, [(0, 600), (0, 430), (300, 380), (600, 420), (1080, 390), (1080, 600)], "#0a1410")
    if road:
        g = cairo.LinearGradient(0, 600, 0, 380)
        g.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.55); g.add_color_stop_rgba(1, 1, 0.95, 0.75, 0.05)
        c.new_path(); c.move_to(160, 600); c.line_to(500, 400); c.line_to(580, 400); c.line_to(920, 600); c.close_path(); c.set_source(g); c.fill()
        for k in range(5):
            p = ((t * speed * 0.8 + k / 5) % 1); yy = 400 + p * p * 200; wd = 4 + 20 * p * p
            rect(c, 540 - wd / 2, yy, wd, 10 + 30 * p * p, hx("#3a2e22", 0.8))
        for side in (-1, 1):
            for k in range(3):
                p = ((t * speed * 0.6 + k / 3) % 1)
                eucalipto(c, 540 + side * (80 + 600 * p * p), 420 + 200 * p * p, 60 + 400 * p * p, 0.2 + 0.9 * p * p, "#050a07", k)
    if outside: outside(c)
    c.restore()
    poly(c, [(0, 0), (110, 90), (0, 600)], "#16171c"); poly(c, [(P, 0), (970, 90), (P, 600)], "#16171c")
    rect(c, 0, 0, P, 90, "#16171c")
    # tablero
    poly(c, [(0, 600), (1080, 600), (1080, 1080), (0, 1080)], "#1c1b20")
    poly(c, [(0, 600), (1080, 600), (1080, 660), (0, 640)], "#26252c")
    rrect(c, 200, 650, 300, 120, 30, "#0a0a0e")
    for k, xx in enumerate((280, 420)):
        circ(c, xx, 710, 46, "#101018"); c.new_path(); c.arc(xx, 710, 40, math.pi * 0.8, math.pi * 2.2); c.set_line_width(4); src(c, hx("#5fff9a", 0.6 * glowdash)); c.stroke()
        a = math.pi * (1.0 + 0.5 * (0.3 + 0.2 * k + 0.4 * speed)); line(c, [(xx, 710), (xx + math.cos(a) * 34, 710 + math.sin(a) * 34)], "#ff4a2a", 4)
    # timón
    c.new_path(); c.arc(350, 900, 230, 0, 2 * math.pi); c.set_line_width(46); src(c, "#08080a"); c.stroke()
    line(c, [(130, 900), (570, 900)], "#08080a", 40); circ(c, 350, 900, 80, "#101014")
    if note:
        c.save(); c.translate(350, 830); c.rotate(-0.06); rect(c, -90, -60, 180, 110, "#f6f0dc");
        for k in range(3): rect(c, -70, -30 + k * 26, 140, 5, hx("#1c2a5a", 0.6))
        rect(c, -30, -70, 60, 18, hx("#e8e0a0", 0.8)); c.restore()
    if keys:
        circ(c, 640, 760, 14, "#9a9aa0"); line(c, [(640, 760), (650, 830)], "#c0c0c8", 6); circ(c, 652, 840, 16, "#e0b030")
    # espejo retrovisor
    rrect(c, 360, 110, 360, 130, 22, "#050506"); rrect(c, 372, 122, 336, 106, 16, "#141a26")
    line(c, [(540, 90), (540, 112)], "#050506", 14)
    if mirror:
        c.save(); rrect_path(c, 372, 122, 336, 106, 16); c.clip(); c.translate(372, 122); c.scale(336 / P, 106 / 340); mirror(c); c.restore()
    c.save(); rrect_path(c, 372, 122, 336, 106, 16); c.clip(); line(c, [(420, 230), (480, 120)], hx("#ffffff", 0.1), 20); c.restore()

def espejo(c, t, content, shake_=0.0):
    """Primer plano del retrovisor: content dibuja en un lienzo de 1080 x 340."""
    rect(c, 0, 0, P, P, "#0a0b10")
    vgrad(c, 0, 0, P, 300, "#03050c", "#0e1426")
    rect(c, 0, 700, P, 380, "#1c1b20")
    dx = math.sin(t * 50) * 6 * shake_
    line(c, [(540, 0), (540, 330)], "#050506", 40)
    rrect(c, 40 + dx, 320, 1000, 380, 60, "#050506")
    c.save(); rrect_path(c, 62 + dx, 342, 956, 336, 46); c.clip(); c.translate(62 + dx, 342); c.scale(956 / P, 336 / 340); content(c); c.restore()
    c.save(); rrect_path(c, 62 + dx, 342, 956, 336, 46); c.clip(); line(c, [(200, 700), (360, 330)], hx("#ffffff", 0.07), 60); c.restore()

def vista_atras(c, t, speed=0.0):
    """Lo que se ve por el retrovisor: la vía hacia atrás, de noche (lienzo 1080 x 340)."""
    vgrad(c, 0, 0, P, 340, "#05070e", "#141a2a")
    poly(c, [(0, 170), (300, 130), (600, 160), (P, 120), (P, 190), (0, 190)], "#0a120c")
    g = cairo.LinearGradient(0, 340, 0, 170)
    g.add_color_stop_rgba(0, 1, 0.2, 0.15, 0.35); g.add_color_stop_rgba(1, 1, 0.2, 0.15, 0.0)
    c.new_path(); c.move_to(200, 340); c.line_to(510, 180); c.line_to(570, 180); c.line_to(880, 340); c.close_path(); c.set_source(g); c.fill()
    for side in (-1, 1):
        for k in range(3):
            p = ((t * speed * 0.6 + k / 3) % 1)
            p = 1 - p
            eucalipto(c, 540 + side * (60 + 500 * p * p), 180 + 160 * p * p, 40 + 260 * p * p, 0.15 + 0.6 * p * p, "#030605", k)

def vista_asiento(c, t, girl=False, ghost_a=1.0):
    """Por el retrovisor: el asiento de atrás (lienzo 1080 x 340)."""
    rect(c, 0, 0, P, 340, "#1a1820")
    poly(c, [(160, 0), (920, 0), (880, 110), (200, 110)], "#0a1020")
    rrect(c, 60, 110, 960, 200, 40, "#3a3640")
    silla_nina(c, 260, 290, 0.55); maleta(c, 820, 300, 0.5)
    if girl: bust(c, 540, 470, 0.5, t, "smile", look=(0, 0), **VALE_FANT)

def ventana(c, t, who=None, knock=0.0, side=1, dawn=0.0, fogged=0.0):
    """Mirando hacia la ventana lateral del carro (ventana con la noche afuera)."""
    rect(c, 0, 0, P, P, "#15161c")
    c.save(); c.new_path(); c.move_to(80, 160); c.line_to(1000, 120); c.line_to(1000, 680); c.line_to(80, 680); c.close_path(); c.clip()
    if dawn: vgrad(c, 0, 120, P, 560, "#4a4a6a", "#d8946a")
    else: vgrad(c, 0, 120, P, 560, "#03050c", "#121a30")
    for i, x in enumerate((160, 420, 700, 930)): eucalipto(c, x, 700, 520, 1.0, "#06100a" if not dawn else "#1c2418", i)
    rect(c, 0, 600, P, 100, "#0c140c" if not dawn else "#3a4a2c")
    if who: who(c)
    for k in range(3): line(c, [(160 + k * 300, 200), (300 + k * 300, 640)], hx("#ffffff", 0.05), 30)
    if fogged: rect(c, 0, 0, P, P, hx("#c8d0e0", 0.12 * fogged))
    c.restore()
    k = knock * math.sin(t * 50)
    c.new_path(); c.move_to(80, 160); c.line_to(1000, 120); c.line_to(1000, 680); c.line_to(80, 680); c.close_path(); c.set_line_width(26 + 2 * k); src(c, "#08080a"); c.stroke()
    rect(c, 0, 680, P, 400, "#2a2930"); rect(c, 0, 680, P, 30, "#38363e")
    rrect(c, 120 if side > 0 else 760, 780, 200, 50, 20, "#1a1a1e")   # manija
    rect(c, 900 if side > 0 else 140, 700, 40, 40, "#606068")          # seguro

def estacion(c, t, light=1.0):
    vgrad(c, 0, 0, P, 600, "#05070e", "#1a2036")
    rect(c, 120, 360, 840, 340, "#d8d8cc"); rect(c, 120, 360, 840, 60, "#2f6a3a")
    txt(c, "ESTACIÓN DE POLICÍA", 540, 404, "#ffffff", 40, True)
    for k in range(3): rect(c, 180 + k * 260, 460, 160, 120, hx("#ffe6a0", 0.6 * light) if k != 1 else "#3a2a20")
    rect(c, 440, 460, 200, 240, "#5a3a26"); glow(c, 540, 440, 200, "#ffe6a0", 0.25 * light)
    line(c, [(980, 700), (980, 200)], "#3a3a3a", 8)
    rect(c, 984, 200, 90, 26, "#f4d02a"); rect(c, 984, 226, 90, 14, "#2a4aa0"); rect(c, 984, 240, 90, 14, "#d0241c")
    rect(c, 0, 700, P, 380, "#2a2a2e")

def afiche(c, t, stamp=0.0):
    rect(c, 0, 0, P, P, "#3a3226")
    for k in range(40):
        rr = random.Random(k); rect(c, rr.uniform(0, P), rr.uniform(0, P), rr.uniform(20, 60), 3, hx("#000", 0.15))
    c.save(); c.translate(540, 700); c.scale(0.8, 0.8); c.rotate(-0.02)
    rect(c, -380, -460, 760, 900, hx("#000", 0.3)); rect(c, -390, -470, 760, 900, "#f2ecd8")
    rect(c, -390, -470, 760, 130, "#c0201a"); txt(c, "DESAPARECIDOS", -10, -385, "#ffffff", 64, True)
    for i, (who, x) in enumerate(((HERNAN, -190), (VALE, 170))):
        rect(c, x - 150, -300, 300, 340, "#b8b0a0")
        c.save(); c.rectangle(x - 150, -300, 300, 340); c.clip(); bust(c, x, 160, 0.62, 0.0, "neutral", look=(0, 0), **who); c.restore()
    txt(c, "Hernán Rojas", -190, 100, "#1a1a1a", 40, True); txt(c, "Valentina Rojas (8)", 170, 100, "#1a1a1a", 36, True)
    txt(c, "Vistos en el cruce de la vereda", -10, 190, "#3a3a3a", 34, True)
    txt(c, "Carro amarillo · HRN 482", -10, 250, "#3a3a3a", 34, True)
    txt(c, "Hace 2 años", -10, 330, "#c0201a", 40, True)
    if stamp > 0:
        c.save(); c.translate(0, -100); c.rotate(-0.25); s_ = 1 + 0.6 * (1 - stamp); c.scale(s_, s_)
        c.new_path(); rrect_path(c, -300, -70, 600, 140, 20); c.set_line_width(12); src(c, hx("#c0201a", stamp)); c.stroke()
        txt(c, "SIN RESOLVER", 0, 24, hx("#c0201a", stamp), 70, True); c.restore()
    c.restore()

def cuaderno(c, t, open_=1.0):
    rect(c, 0, 0, P, P, "#2a2a30")
    maleta(c, 860, 900, 0.9, open_=1.0)
    c.save(); c.translate(500, 560); c.rotate(-0.05)
    rrect(c, -340, -300, 680, 600, 20, "#e86aa0")
    if open_ > 0:
        rect(c, -320 * open_, -290, 640 * open_, 580, "#fbf6e6")
        for k in range(10): rect(c, -310 * open_, -230 + k * 50, 620 * open_, 2, hx("#5fb4ff", 0.35))
        rect(c, -2, -290, 4, 580, hx("#000", 0.2))
    c.restore()

def nota_tu(c, t, t0, lines_, col="#1a3a8a"):
    rect(c, 0, 0, P, P, "#1a1b20")
    paper_note(c, 540, 600, 1.4, lines_, t, t0, rot=0.03)

def bosque(c, t, dawn=0.0, who=None):
    if dawn: vgrad(c, 0, 0, P, P, "#4a4a6a", "#9a7a7a")
    else: vgrad(c, 0, 0, P, P, "#03050c", "#0c1220")
    for i, (x, s) in enumerate(((100, 1.6), (330, 1.9), (620, 1.7), (900, 2.0))):
        line(c, [(x, 1080), (x + 10, 0)], "#0a100c" if not dawn else "#2a2a28", 60 * s / 1.6)
    if who: who(c)
    for i, x in enumerate((210, 800)): line(c, [(x, 1080), (x - 10, 0)], "#040806" if not dawn else "#1c1c1a", 110)
    fog(c, 880, t, 0.25, "#9aa4c0" if not dawn else "#e8d0c0", n=8, h=160)

def you_out(c, t, x=540, y=1240, s=0.95, mood="worry", look=(0, -0.3), arms="none", **kw):
    bust(c, x, y, s, t, mood, look=look, arms=arms, **dict(YOU, **kw))

# ---------------- PARTE 1 ----------------
def g01(c, t, T, w):
    noche(c, t)
    carro(c, 600, 880, 0.78, t, AMARILLO, lights=1.0, face=-1)
    tag2(c, 270, 400, "1:00 a. m.", t, w("una"), "#ffffff")
    tag2(c, 600, 460, "NADIE ADENTRO", t, w("nadie"), "#e0303a", "#ffffff")
FOCUS["g01"] = (600, 720)
CAM["g01"] = [("nadie", 1.45, 600, 700)]

def g02(c, t, T, w):
    noche(c, t * 3, cross=False)
    carro(c, 520, 880, 0.75, t, AZUL, lights=1.0, front=lambda c_: conductor_tu(c_, "worry", t))
    rect(c, 800, 520, 12, 200, "#6a6a6a"); rrect(c, 690, 460, 240, 90, 10, "#1c5a2a")
    txt(c, "VENTAQUEMADA", 810, 498, "#ffffff", 26, True); txt(c, "← 12 km", 810, 532, "#ffffff", 24, True)
    tag2(c, 300, 420, "SIN SEÑAL", t, w("señal"), "#e0303a", "#ffffff")
FOCUS["g02"] = (520, 700)

def g03(c, t, T, w):
    noche(c, t)
    carro(c, 210, 900, 0.55, t, AZUL, lights=1.0, front=lambda c_: conductor_tu(c_, "worry", t))
    carro(c, 790, 880, 0.6, t, AMARILLO, lights=1.0, face=-1)
    k = w("callan")
    if t < k:
        for j in range(4):
            a = (t * 0.6 + j / 4) % 1; txt(c, "cri", 120 + j * 260, 640 - 60 * a, hx("#bfe8a0", 0.6 * (1 - a)), 30, True)
    tag2(c, 360, 560, "¡PIII!", t, w("pitas"), "#ffc24a")
    tag2(c, 360, 460, "¡PIII!", t, w("dos"), "#ffc24a")
    tag2(c, 700, 400, "SILENCIO", t, k, "#e0303a", "#ffffff")
FOCUS["g03"] = (500, 720)

def asiento_conductor(c, t, you=True, mood="worry"):
    rect(c, 0, 0, P, P, "#0a0b10")
    poly(c, [(160, 120), (960, 120), (1000, 760), (120, 760)], "#2a2630")
    glow(c, 600, 300, 560, "#ffe6a0", 0.3)        # hueco de la puerta
    rrect(c, 640, 160, 260, 520, 60, "#5a5260"); rrect(c, 690, 90, 160, 110, 40, "#5a5260")   # silla vacía (de lado)
    rrect(c, 380, 560, 520, 150, 40, "#4a4452")
    c.new_path(); c.arc(330, 380, 160, 0, 2 * math.pi); c.set_line_width(34); src(c, "#08080a"); c.stroke()
    rect(c, 160, 520, 260, 60, "#1c1b20")
    tinto(c, 470, 640, 0.45, t)
    # cinturón abrochado sobre nada
    line(c, [(860, 180), (780, 420), (700, 640)], "#1a1a1e", 34); rect(c, 680, 620, 50, 40, "#9a9aa4")
    if you: you_out(c, t, 230, 1180, 0.75, mood, look=(0.7, -0.4))

def g04(c, t, T, w):
    asiento_conductor(c, t)
    tag2(c, 800, 760, "ABROCHADO", t, w("abrochado"), "#ffc24a")
    tag2(c, 640, 860, "SIN NADIE", t, w("amarrado"), "#e0303a", "#ffffff")
FOCUS["g04"] = (640, 500)
CAM["g04"] = [("cinturón", 1.4, 760, 460)]

def g05(c, t, T, w):
    rect(c, 0, 0, P, P, "#141318")
    rrect(c, 140, 560, 800, 520, 60, "#1c1b20")
    tinto(c, 540, 760, 1.6, t, 1.0)
    tag2(c, 540, 380, "TODAVÍA ECHA HUMO", t, w("humo"), "#e0303a", "#ffffff")
FOCUS["g05"] = (540, 560)

def g06(c, t, T, w):
    asiento_atras(c, t)
    tag2(c, 400, 900, "SILLA DE NIÑA", t, w("silla"), "#ffffff")
    tag2(c, 690, 520, "MALETA ROSADA", t, w("rosada"), "#e86aa0", "#ffffff")
FOCUS["g06"] = (540, 620)

def g07(c, t, T, w):
    cabina(c, t, note=True)
    tag2(c, 380, 640, "LETRA TEMBLOROSA", t, w("temblorosa"), "#ffc24a")
FOCUS["g07"] = (380, 800)
CAM["g07"] = [("timón", 1.6, 360, 800)]

def g08(c, t, T, w):
    rect(c, 0, 0, P, P, "#1a1b20")
    paper_note(c, 540, 560, 1.4, ["Si usted paró,", "no se baje del carro.", "Eso imita voces."], t, w("paró") - 0.4)
    tag2(c, 540, 820, "ESO IMITA VOCES", t, w("imita"), "#e0303a", "#ffffff")
FOCUS["g08"] = (540, 540)

def g09(c, t, T, w):
    noche(c, t)
    carro(c, 820, 880, 0.55, t, AMARILLO, lights=1.0, face=-1, door=1.0, inner=0.6)
    you_out(c, t, 420, 1240, 1.05, "shock" if t > w("bajaste") else "worry", look=(0, 0.5), arms="head" if t > w("bajaste") else "none", sweat=1.0)
    tag2(c, 760, 420, "YA TE BAJASTE", t, w("bajaste"), "#e0303a", "#ffffff")
FOCUS["g09"] = (480, 640)

def g10(c, t, T, w):
    bosque(c, t)
    if t > w("niña") - 0.2:
        for k in range(3):
            a = (t * 0.5 + k / 3) % 1; txt(c, "papá...", 560 + k * 40, 620 - 100 * a, hx("#dfe8ff", 0.7 * (1 - a)), 36, True)
FOCUS["g10"] = (540, 560)

def g11(c, t, T, w):
    def girl(c_):
        bust(c_, 520, 1000, 0.55, t, "sad", look=(0.6, 0), talk="auto", tears=0.6, **VALE)
    bosque(c, t, who=girl)
    for k in range(2):
        a = (t * 0.8 + k / 2) % 1; circ(c, 560 + 40 * a, 760 - 60 * a, 14 + 30 * a, hx("#e8eef8", 0.3 * (1 - a)))
    tag2(c, 820, 420, "TENGO FRÍO", t, w("frío"), "#5fb4ff", "#ffffff")
FOCUS["g11"] = (520, 760)

def g12(c, t, T, w):
    noche(c, t)
    k = w("cierra")
    carro(c, 260, 890, 0.55, t, AZUL, lights=1.0, door=1.0 - ease(clamp((t - k) / 0.15)))
    carro(c, 880, 880, 0.5, t, AMARILLO, lights=1.0, face=-1, door=1.0, inner=0.6)
    you_out(c, t, 620 + 20 * clamp(t / 2), 1240, 0.8, "shock" if t > k else "worry", look=(-0.8 if t > k else 0.7, -0.2))
    tag2(c, 260, 440, "¡PUM!", t, k, "#e0303a", "#ffffff", size=56)
FOCUS["g12"] = (440, 720)

def monster_rear(t, open_=0.3, a=1.0):
    def f(c_):
        overlay(c_, "#000", 0.0)
        M.pasajero(c_, -90, -215, 0.3, t, open_=open_, bend=-0.75, body=False)
        poly(c_, [(-200, -150), (-20, -150), (-20, -60), (-200, -60)], "#07070a")
    return f

def g13(c, t, T, w):
    noche(c, t)
    on = 1.0 if t > w("luz") - 0.1 else 0.0
    carro(c, 480, 900, 0.85, t, AZUL, lights=1.0, inner=on)
    you_out(c, t, 900, 1260, 0.75, "shock" if t > w("volteas") else "worry", look=(-0.8, -0.3))
    tag2(c, 380, 420, "LUZ PRENDIDA", t, w("luz"), "#ffc24a")
FOCUS["g13"] = (480, 700)

def g14(c, t, T, w):
    noche(c, t, fog_a=0.06)
    k = w("alguien")
    rear = monster_rear(t, 0.2 + 0.5 * clamp((t - w("techo")) / 0.6)) if t > k - 0.2 else None
    carro(c, 520, 1000, 1.45, t, AZUL, lights=1.0, inner=1.0, rear=rear)
    tag2(c, 540, 900, "CABEZA CONTRA EL TECHO", t, w("techo"), "#e0303a", "#ffffff", size=36)
FOCUS["g14"] = (420, 640)
CAM["g14"] = [("alto", 1.35, 420, 640)]

def g15(c, t, T, w):
    noche(c, 0.0, fog_a=0.06)
    carro(c, 520, 1000, 1.45, 0.0, AZUL, lights=1.0, inner=1.0, rear=monster_rear(0.0, 0.7))
    overlay(c, "#000", 0.55)

# ---------------- PARTE 2 ----------------
def h01(c, t, T, w):
    noche(c, t, fog_a=0.06)
    carro(c, 520, 1000, 1.45, t, AZUL, lights=1.0, inner=1.0, rear=monster_rear(t, 0.5 + 0.3 * clamp((t - w("persona")) / 0.5)))
    tag2(c, 540, 380, "NO ES UNA PERSONA", t, w("persona"), "#e0303a", "#ffffff")
FOCUS["h01"] = (420, 640)
CAM["h01"] = [("persona", 1.5, 330, 600)]

def h02(c, t, T, w):
    cabina(c, t, mirror=lambda c_: vista_atras(c_, t))
    lk = clamp((t - w("seguro")) / 0.25)
    rect(c, 930, 640 + 40 * lk, 40, 60, "#808088")
    tag2(c, 820, 860, "¡CLIC!", t, w("seguro"), "#ffffff")
    tag2(c, 640, 420, "LLAVES PEGADAS", t, w("llaves"), "#ffc24a")
FOCUS["h02"] = (560, 640)

def rise_mirror(t, a):
    def f(c_):
        vista_atras(c_, t)
        carro(c_, 540, 300, 0.32, t, AZUL, lights=0.0, inner=1.0, face=-1, smoke=False)
        sc = 0.08 + 0.17 * a
        M.pasajero(c_, 700, 300 - 1060 * sc, sc, t, open_=0.5, bend=0.5 * (1 - a), look=(-0.5, 0.3))
    return f

def h03(c, t, T, w):
    a = ease(clamp((t - w("bajando")) / max(0.5, w("metros") - w("bajando"))))
    espejo(c, t, rise_mirror(t, a))
    tag2(c, 540, 840, "3 METROS", t, w("metros"), "#e0303a", "#ffffff", size=56)
FOCUS["h03"] = (540, 520)
CAM["h03"] = [("desdoblándose", 1.3, 600, 500)]

def girl_glass(t, x=560, mood="worry", talk=0.0, arms="up", tears=0.8):
    def f(c_):
        bust(c_, x, 820, 0.95, t, mood, look=(-0.3, 0), arms=arms, talk=talk, tears=tears, **VALE)
    return f

def h04(c, t, T, w):
    k = w("golpea")
    kn = 1.0 if k < t < k + 1.2 else 0.0
    ventana(c, t, girl_glass(t), knock=kn)
    tag2(c, 760, 600, "DESCALZA", t, w("descalza"), "#ffffff")
FOCUS["h04"] = (560, 520)

def h05(c, t, T, w):
    ventana(c, t, girl_glass(t, mood="sad", talk="auto", arms="none", tears=1.0), knock=0.4)
FOCUS["h05"] = (560, 480)
CAM["h05"] = [("llevó", 1.35, 560, 460)]

def h06(c, t, T, w):
    ventana(c, t, girl_glass(t, mood="sad", arms="none", tears=0.6))
    paper_note(c, 220, 880, 0.42, ["Eso imita", "voces."], t, -2.0, rot=-0.1)
    tag2(c, 640, 860, "DE CARNE Y HUESO", t, w("carne"), "#ffc24a")
FOCUS["h06"] = (480, 620)

def h07(c, t, T, w):
    k = w("sube")
    def girl(c_):
        if t > k - 0.2: bust(c_, 600, 980, 0.8, t, "sad", look=(0.3, 0.3), arms="hold", tears=0.5, **VALE)
    asiento_atras(c, t, girl=girl)
    tag2(c, 300, 380, "¡CLIC!", t, w("abres"), "#ffffff")
FOCUS["h07"] = (600, 620)

def hernan_glass(t, mood="worry", talk=0.0, rag=1.0, arms="up", creepy=0.0):
    def f(c_):
        bust(c_, 540, 820, 1.0, t, mood, look=(-0.4, 0), arms=arms, talk=talk, sweat=1.0, **HERNAN)
        if rag > 0 and arms == "up":   # trapo con sangre en la mano
            ell(c_, 800, 330, 64, 52, "#d8d0c0"); ell(c_, 800, 330, 38, 28, hx("#9a0010", 0.85))
            M._drip(c_, 800, 370, t, "#8a0010", 3)
    return f

def h08(c, t, T, w):
    ventana(c, t, hernan_glass(t), knock=0.6, side=-1)
    tag2(c, 300, 600, "SANGRE", t, w("sangre"), "#e0303a", "#ffffff")
FOCUS["h08"] = (600, 520)

def h09(c, t, T, w):
    ventana(c, t, hernan_glass(t, "shock", talk="auto"), knock=1.0, side=-1)
FOCUS["h09"] = (540, 460)
CAM["h09"] = [("valentina", 1.3, 540, 460)]

def h10(c, t, T, w):
    def girl(c_): bust(c_, 560, 1000, 0.85, t, "shock", look=(0, 0.2), arms="head", tears=1.0, **VALE)
    asiento_atras(c, t, girl=girl)
FOCUS["h10"] = (560, 600)

def h11(c, t, T, w):
    rect(c, 0, 0, P, P, "#1a1820"); glow(c, 540, 400, 500, "#ffe6a0", 0.08)
    bust(c, 540, 1160, 1.15, t, "sad", look=(0.2, 0.1), talk="auto", tears=0.5, **VALE)
    tag2(c, 540, 380, "LA NOTA ERA DE SU PAPÁ", t, w("nota"), "#ffc24a", size=36)
FOCUS["h11"] = (540, 560)

def h12(c, t, T, w):
    rq, sm, oj = w("quita"), w("sonreír"), w("orejas")
    if t < oj - 0.1:
        mood = "creepy" if t > sm - 0.1 else "neutral"
        ventana(c, t, hernan_glass(t, mood, rag=1.0 if t < rq + 0.4 else 0.0, arms="up" if t < sm else "none"), side=-1)
        tag2(c, 700, 560, "NI UN RASGUÑO", t, w("herida"), "#e0303a", "#ffffff")
    else:
        ventana(c, t, lambda c_: M.pasajero(c_, 540, 420, 0.95, t, open_=0.9, body=False), side=-1)
FOCUS["h12"] = (540, 460)
CAM["h12"] = [("sonreír", 1.4, 540, 420), ("orejas", 1.2, 540, 420)]

def chase(t):
    def f(c_):
        vista_atras(c_, t, speed=3.0)
        M.pasajero_gatea(c_, 470, 230, 0.32, t, open_=0.8)
    return f

def h13(c, t, T, w):
    k = w("persigue")
    espejo(c, t, chase(t) if t > k - 0.2 else (lambda c_: vista_atras(c_, t, speed=3.0)), shake_=1.0)
    tag2(c, 540, 840, "80 KM/H", t, w("ochenta"), "#e0303a", "#ffffff", size=60)
FOCUS["h13"] = (540, 520)
CAM["h13"] = [("patas", 1.35, 500, 520)]

def h14(c, t, T, w):
    look = t > w("miras") - 0.2
    cabina(c, t, speed=1.5, mirror=(lambda c_: vista_asiento(c_, t)) if look else (lambda c_: vista_atras(c_, t, 1.5)))
    tag2(c, 680, 560, "10 MIN DESPUÉS", t, w("diez"), "#ffffff")
FOCUS["h14"] = (540, 300)
CAM["h14"] = [("retrovisor", 1.7, 540, 260)]

def h15(c, t, T, w):
    k = w("volteas")
    if t < k:
        espejo(c, t, lambda c_: vista_asiento(c_, t))
        tag2(c, 540, 840, "VACÍO", t, w("vacío"), "#ffffff", size=56)
    else:
        def girl(c_): bust(c_, 540, 1060, 0.95, t, "smile", look=(0, 0), **VALE_FANT)
        asiento_atras(c, t, girl=girl, child=False)
        glow(c, 540, 600, 400, "#bfe8ff", 0.12)
FOCUS["h15"] = (540, 540)
CAM["h15"] = [("ahí", 1.3, 540, 560)]

def h16(c, t, T, w):
    rect(c, 0, 0, P, P, "#12141c"); glow(c, 540, 500, 520, "#bfe8ff", 0.14)
    bust(c, 540, 1160, 1.15, t, "creepy" if t > w("otra") - 0.1 else "smile", look=(0, 0), talk="auto", **VALE_FANT)
    for sx in (-1, 1): M._drip(c, 540 + sx * 62, 740, t + sx, "#10141c", 4 + sx)
    tag2(c, 540, 380, "«OTRA VEZ»", t, w("otra"), "#5fb4ff", "#ffffff")
FOCUS["h16"] = (540, 560)

def h17(c, t, T, w):
    rect(c, 0, 0, P, P, "#12141c"); glow(c, 540, 500, 520, "#bfe8ff", 0.14)
    bust(c, 540, 1160, 1.15, 0.5, "creepy", look=(0, 0), **VALE_FANT); overlay(c, "#000", 0.6)

# ---------------- PARTE 3 ----------------
def i01(c, t, T, w):
    espejo(c, t, lambda c_: vista_asiento(c_, t))
    h = ease(clamp((t - w("detrás")) / 0.6))
    if h > 0:
        c.save(); c.translate(960, 1080 - 300 * h); ell(c, 0, 0, 60, 46, "#c4ccd2")
        for k in range(4): line(c, [(-40 + k * 26, -20), (-50 + k * 30, -110)], "#c4ccd2", 20)
        c.restore()
    tag2(c, 540, 860, "NO SALE EN EL ESPEJO", t, w("retrovisor"), "#5fb4ff", "#ffffff", size=36)
FOCUS["i01"] = (540, 560)

def i02(c, t, T, w):
    estacion(c, t)
    carro(c, 330, 900, 0.55, t, AMARILLO, lights=1.0, front=lambda c_: conductor_tu(c_, "worry", t))
    k = w("sale")
    if t > k - 0.2: bust(c, 760, 1180, 0.7, t, "tired", look=(-0.5, 0), **PATRU)
    tag2(c, 840, 620, "3:00 a. m.", t, w("tres"), "#ffffff")
    tag2(c, 560, 640, "¡PIII!", t, w("pitas"), "#ffc24a")
FOCUS["i02"] = (540, 660)
CAM["i02"] = []

def i03(c, t, T, w):
    asiento_atras(c, t, child=True)
    tag2(c, 540, 380, "VACÍO", t, w("vacío"), "#e0303a", "#ffffff", size=56)
    tag2(c, 820, 480, "SOLO LA MALETA", t, w("maleta"), "#e86aa0", "#ffffff")
FOCUS["i03"] = (620, 620)

def i04(c, t, T, w):
    estacion(c, t)
    carro(c, 300, 900, 0.5, t, AMARILLO, lights=0.4)
    pal = t > w("pálido") - 0.1
    bust(c, 740, 1120, 0.8, t, "shock" if pal else "neutral", look=(-0.6, 0), arms="phone", sweat=1.0 if pal else 0.0,
         **dict(PATRU, skin="#c8b8a8" if pal else PATRU["skin"]))
    tag2(c, 300, 560, "HRN 482", t, w("placa"), "#f4d02a")
FOCUS["i04"] = (620, 640)
CAM["i04"] = []

def i05(c, t, T, w):
    afiche(c, t)
    tag2(c, 540, 900, "EN ESE MISMO CRUCE", t, w("cruce"), "#e0303a", "#ffffff")
FOCUS["i05"] = (540, 460)
CAM["i05"] = [("hernán", 1.35, 390, 620), ("valentina", 1.35, 680, 620)]

def i06(c, t, T, w):
    afiche(c, t, stamp=clamp((t - w("nunca") + 0.1) / 0.3))
FOCUS["i06"] = (540, 500)

def i07(c, t, T, w):
    cuaderno(c, t, open_=ease(clamp((t - w("cuaderno")) / 0.6)))
    tag2(c, 520, 920, "ÚLTIMA PÁGINA", t, w("última"), "#ffc24a")
FOCUS["i07"] = (520, 560)

def i08(c, t, T, w):
    cuaderno(c, t, 1.0)
    c.save(); c.translate(500, 560); c.rotate(-0.05)
    lines_ = [("Si alguien para,", "alguien"), ("que no se baje.", "baje"), ("Eso se queda", "queda"), ("con el que se baja.", "baja.")]
    for i, (l, tok) in enumerate(lines_):
        k = w("si") - 0.2 + i * 0.9
        a = clamp((t - k) / 0.5)
        if a <= 0: continue
        c.save(); c.rectangle(-300, -300, 600 * a + 10, 600); c.clip()
        hw(c, l, -280, -170 + i * 100, 64, "#b0202a" if i >= 2 else "#2a2a6a"); c.restore()
    c.restore()
FOCUS["i08"] = (500, 560)

def i09(c, t, T, w):
    noche(c, t, dawn=1.0, fog_a=0.15)
    k = w("puerta")
    carro(c, 640, 880, 0.62, t, AZUL, lights=0.8, door=1.0 if t > k - 0.2 else 0.0, inner=0.8, face=-1)
    carro(c, 170, 920, 0.42, t, "#e8e8e8", lights=0.6, patrol=True)
    tag2(c, 640, 420, "NADIE ADENTRO", t, w("nadie"), "#e0303a", "#ffffff")
FOCUS["i09"] = (560, 700)
CAM["i09"] = [("cinturón", 1.4, 640, 700)]

def i10(c, t, T, w):
    cabina(c, t, note=True, keys=True)
    overlay(c, "#ffb860", 0.08)
    tag2(c, 720, 420, "TU LETRA", t, w("letra"), "#e0303a", "#ffffff")
FOCUS["i10"] = (380, 800)
CAM["i10"] = [("timón", 1.6, 360, 800)]

def i11(c, t, T, w):
    rect(c, 0, 0, P, P, "#2a2420")
    paper_note(c, 540, 560, 1.4, ["Si usted paró,", "no se baje del carro."], t, w("si") - 0.4, rot=0.03)
    tag2(c, 540, 920, "TU LETRA", t, 0.0, "#e0303a", "#ffffff")
FOCUS["i11"] = (540, 540)

def i12(c, t, T, w):
    k = w("voz")
    walk = ease(clamp((t - w("bajó")) / 3.0))
    def out(c_):
        sc = 0.6 - 0.3 * walk
        bust(c_, 480 + 220 * walk, 520 + 380 * sc - 40 * walk, sc, t, "neutral", look=(0.6, -0.2), **PATRU)
        if t > k - 0.3:
            def tree(c2): pass
            M.pasajero(c_, 860, 300, 0.16, t, open_=0.3 + 0.4 * TALK(), arms=1.0, beanie=True)
            line(c_, [(930, 700), (940, 100)], "#1c2418", 70)
    ventana(c, t, out, dawn=1.0)
    tag2(c, 300, 600, "SE BAJÓ", t, w("bajó"), "#e0303a", "#ffffff")
FOCUS["i12"] = (640, 460)
CAM["i12"] = [("voz", 1.5, 820, 380)]

def i13(c, t, T, w):
    def who(c_):
        M.pasajero(c_, 520, 420, 0.75, t, open_=0.25 + 0.6 * TALK(), arms=1.0, beanie=True, look=(0.3, 0))
    bosque(c, t, dawn=1.0, who=who)
    tag2(c, 540, 940, "CON TU VOZ", t, w("cabo"), "#e0303a", "#ffffff")
FOCUS["i13"] = (520, 460)
CAM["i13"] = [("frío", 1.25, 520, 440)]

def i14(c, t, T, w):
    bosque(c, 0.0, dawn=1.0, who=lambda c_: M.pasajero(c_, 520, 420, 0.75, 0.3, open_=0.8, arms=1.0, beanie=True))
    overlay(c, "#000", 0.6)

PANELS = {k: v for k, v in globals().items() if len(k) == 3 and k[0] in "ghi" and k[1:].isdigit() and callable(v)}

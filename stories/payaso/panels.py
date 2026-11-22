import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect_path, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp, text_w
from povlib import *
from scenes import hw, popin, tag2, stairs, glass, paper_note, chair

# Estilo clásico («Tu IA te hizo rico»): protagonista de gorro naranja, colores planos
YOU = dict(hat="beanie", skin="#c48a5c", shirt="#3c8a5a", cap_col="#e8702a")
SOFI = dict(hat="bun", skin="#d09a70", shirt="#f08aa8", hair_col="#3a2414")
TOMAS = dict(hat="none", skin="#c88f62", shirt="#5fa0e0", hair_col="#2a1a10")
PAPA = dict(hat="none", skin="#d0a07a", shirt="#2a2f44", hair_col="#2a1e18")
MAMA = dict(hat="bun", skin="#d8a882", shirt="#8a2a4a", hair_col="#4a2a1a")
GUARD = dict(hat="cap", skin="#a8704a", shirt="#4a5a7a", cap_col="#2a3048", mustache=True)
FOCUS = {}; CAM = {}

def clown(c, x, y, s, t, mood="creepy", wet=0.0, sit=True, a=1.0):
    def f():
        c.push_group()
        bust(c, 0, 0, 1.0, t * 0.15, mood, look=(0, 0), hat="none", skin="#f2efe6", shirt="#6a2a8a", hair_col="#f2efe6")
        hy = -380
        for sx in (-1, 1):
            for k in range(3): circ(c, sx * (150 + k * 14), hy - 40 + k * 40, 44, "#e8402a")
        for sx in (-54, 54): poly(c, [(sx, hy - 60), (sx + 16, hy + 4), (sx, hy + 66), (sx - 16, hy + 4)], hx("#2a3a8a", 0.55))
        circ(c, 0, hy + 46, 26, "#e0201a"); circ(c, -8, hy + 38, 8, hx("#ffffff", 0.6))
        for k in range(7): circ(c, -150 + k * 50, -230, 36, "#f4f0e8")
        for k in range(3): circ(c, 0, -140 + k * 70, 14, "#e8402a")
        if wet:
            for sx in (-54, 54): ell(c, sx + 8, hy + 60 + (t * 40 % 60), 8, 14, hx("#9fdcff", 0.8 * wet))
        c.pop_group_to_source(); c.paint_with_alpha(a)
    scaled(c, x, y, s, f)

def sala(c, t, statue=1.0, dent=0.0, tv=True, dark=0.0, you=None):
    vgrad(c, 0, 0, P, P, "#2c3350", "#1b2036")
    rect(c, 0, 760, P, 320, "#3a2c2a")
    # chimenea
    rect(c, 760, 380, 300, 400, "#5a4a48"); rect(c, 800, 560, 220, 200, "#140c0c"); rect(c, 740, 360, 340, 30, "#6a5a58")
    glow(c, 910, 700, 260, "#ff8a3a", 0.35 + 0.08 * math.sin(t * 9)); poly(c, [(860, 760), (890, 660), (910, 720), (940, 640), (970, 760)], "#ff9a3a")
    # cuadro y lámpara
    rect(c, 300, 150, 260, 180, "#4a3a38"); rect(c, 316, 166, 228, 148, "#7a8aa8"); poly(c, [(316, 314), (420, 220), (544, 314)], "#5a6a88")
    # sofá grande
    sx0 = 80
    rrect(c, sx0, 500, 560, 170, 40, "#7a3a3a"); rrect(c, sx0 + 20, 600 + 30 * dent, 520, 110, 30, "#8a4a4a"); rrect(c, sx0 - 20, 560, 80, 200, 30, "#6a2a2a"); rrect(c, sx0 + 500, 560, 80, 200, 30, "#6a2a2a")
    if dent: ell(c, sx0 + 280, 640 + 30 * dent, 120, 26 * dent, hx("#000", 0.3))
    # estatua del payaso en la esquina
    if statue > 0: clown(c, 690, 860, 0.55, t, "creepy", a=statue)
    if tv: glow(c, 540, 1080, 500, "#5fb4ff", 0.18)
    if you: you(c)
    if dark: overlay(c, "#000010", dark)

def small_sofa_you(c, t, mood="worry", look=(0.8, -0.2), arms="phone", talk=0.0):
    rrect(c, 0, 900, 700, 200, 40, "#3a5a7a")
    bust(c, 320, 1180, 0.9, t, mood, look=look, arms=arms, talk=talk, **YOU)

def chat(c, t, msgs, typing=None, title="Papá de Sofi"):
    rect(c, 0, 0, P, P, "#1b2036")
    glow(c, 540, 540, 600, "#5fb4ff", 0.15)
    rrect(c, 250, 40, 580, 1000, 50, "#111"); c.save(); rrect_path(c, 266, 56, 548, 968, 40); c.clip()
    rect(c, 266, 56, 548, 968, "#0b141a"); rect(c, 266, 56, 548, 120, "#1f2c34")
    circ(c, 330, 116, 32, "#5a6a88"); txt(c, title, 380, 112, "#e9edef", 34); txt(c, "en línea" if typing is None or t < typing else "escribiendo...", 380, 150, "#8fd0a0", 24, False, False)
    y = 210
    for (tm, text, mine) in msgs:
        if t < tm: continue
        a = clamp((t - tm) / 0.2); lines_ = text if isinstance(text, list) else [text]
        h = bubble(c, 540 if mine else 290, y, 260 if mine else 470, lines_, "#005c4b" if mine else "#1f2c34", "#e9edef", 30, "r" if mine else "l", a)
        y += h + 36
    c.restore()

def kids_room(c, t, empty=True, closet=0.0, kids=False, window=1.0, dark=0.35):
    vgrad(c, 0, 0, P, P, "#3a3a6a", "#24244a")
    rect(c, 0, 780, P, 300, "#4a3a5a")
    for k in range(18): circ(c, 60 + k * 58, 80 + (k % 3) * 40, 5, "#ffe08a")
    # ventana
    rect(c, 420, 120, 240, 260, "#2a2040"); rect(c, 436, 136, 208, 228, "#0a1030"); circ(c, 600, 190, 22, "#f4efd0")
    # camas
    for bx, col in ((60, "#f08aa8"), (300, "#5fa0e0")):
        rect(c, bx, 640, 220, 160, "#8a6a4a"); rrect(c, bx + 10, 620, 200, 70, 20, col); rrect(c, bx + 20, 590, 90, 50, 20, "#ffffff")
        if not empty: circ(c, bx + 70, 600, 40, "#d09a70")
    # clóset
    rect(c, 720, 200, 300, 600, "#6a4a3a")
    if closet > 0:
        rect(c, 720, 200, 300 * closet, 600, "#100a10")
        if kids:
            c.save(); c.rectangle(720, 200, 300 * closet, 600); c.clip()
            bust(c, 820, 900, 0.5, t, "smile", look=(-0.5, 0), **SOFI); bust(c, 930, 920, 0.5, t + 1, "neutral", look=(-0.6, 0), **TOMAS); c.restore()
    else:
        line(c, [(870, 200), (870, 800)], "#4a3a2a", 6); circ(c, 850, 500, 9, "#c9a24a"); circ(c, 890, 500, 9, "#c9a24a")
    if dark: overlay(c, "#000010", dark)

def house_back(c, t, kid_window=1.0, you_arms=False, sofi=False, jump=0.0):
    vgrad(c, 0, 0, P, P, "#141a3a", "#2c3350")
    circ(c, 960, 330, 40, "#f4efd0")
    rect(c, 100, 200, 880, 880, "#c8b89a"); poly(c, [(80, 210), (540, 40), (1000, 210)], "#7a3a2a")
    rect(c, 380, 300, 260, 220, "#3a2a20"); rect(c, 396, 316, 228, 188, "#ffd890")
    poly(c, [(60, 640), (1020, 640), (1080, 720), (0, 720)], "#5a4a48")   # techo del garaje
    if kid_window and jump == 0.0: bust(c, 510, 560, 0.45, t, "sad", look=(0, 0.6), **TOMAS)
    if jump > 0:
        jy = 520 + 300 * ease(jump)
        bust(c, 510, jy, 0.45, t, "shock", **TOMAS)
    rect(c, 0, 720, P, 360, "#1a2a1a")
    bust(c, 420, 1200, 0.75, t, "worry", look=(0.4, -1), arms="up" if you_arms else "none", **YOU)
    if sofi: bust(c, 720, 1160, 0.5, t, "worry", look=(-0.6, -0.6), **SOFI)

def porteria(c, t, police=0.0):
    vgrad(c, 0, 0, P, P, "#141a3a", "#2c3350")
    rect(c, 560, 360, 440, 480, "#c8c0b0"); rect(c, 600, 420, 360, 200, "#ffd890"); poly(c, [(540, 370), (1020, 370), (980, 300), (580, 300)], "#3a3a4a")
    ui(c, 34); txt(c, "PORTERÍA", 780, 700, "#3a3a4a", 34, True)
    c.save(); c.rectangle(600, 420, 360, 200); c.clip(); bust(c, 780, 760, 0.5, t, "worry", arms="phone", **GUARD); c.restore()
    rect(c, 0, 840, P, 240, "#3a3a3a")
    if police:
        r = 0.5 + 0.5 * math.sin(t * 12)
        glow(c, 200, 300, 500, "#ff2a2a", 0.35 * police * r); glow(c, 400, 300, 500, "#2a6aff", 0.35 * police * (1 - r))
    bust(c, 200, 1160, 0.7, t, "worry", look=(1, 0), **YOU)
    bust(c, 390, 1150, 0.42, t, "sad", look=(-0.5, 0), **SOFI); bust(c, 480, 1160, 0.42, t + 1, "sad", look=(-0.5, 0), **TOMAS)

def crayon_note(c, x, y, s, lines_, t, t0=0.0):
    def f():
        c.rotate(0.05)
        rect(c, -300, -200, 600, 400, hx("#000", 0.3)); rect(c, -306, -210, 600, 400, "#fbf6e6")
        for i, l in enumerate(lines_):
            a = clamp((t - t0 - i * 0.7) / 0.6)
            if a <= 0: continue
            c.save(); c.rectangle(-300, -210, 600 * a, 400); c.clip()
            c.select_font_face("Montserrat", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(58)
            for j in range(2):
                c.move_to(-260 + j * 2, -80 + i * 110 + j); src(c, hx("#d0241c", 0.8)); c.show_text(l)
            c.restore()
    scaled(c, x, y, s, f)

def drawing(c, x, y, s, t, last=False, rot=0.0):
    def f():
        c.rotate(rot)
        rect(c, -170, -130, 340, 260, "#fbf6e6")
        if last:
            rrect(c, -130, 20, 200, 70, 20, "#3a5a7a")
            circ(c, -40, -20, 34, "#e8a070"); c.new_path(); c.arc(-40, -30, 36, math.pi, 2 * math.pi); fill(c, "#e8702a")
            rect(c, -70, 10, 60, 60, "#3c8a5a"); rect(c, 0, 0, 24, 40, "#222")
            for k in range(3): line(c, [(60 + k * 20, -100), (40 + k * 20, -60)], "#d0241c", 4)
        else:
            for bx in (-110, 10):
                rect(c, bx, -10, 100, 50, "#5fa0e0" if bx > 0 else "#f08aa8"); circ(c, bx + 25, -20, 18, "#e8a070")
                for k in range(3): txt(c, "z", bx + 60 + k * 12, -40 - k * 14, "#333", 20, False, False)
        line(c, [(-150, 110), (150, 110)], hx("#d0241c", 0.6), 3)
    scaled(c, x, y, s, f)

def milk(c, x, y, s, a=1.0):
    def f():
        poly(c, [(-36, -110), (36, -110), (28, 0), (-28, 0)], hx("#dfeee0", 0.55 * a))
        poly(c, [(-33, -60), (33, -60), (26, -4), (-26, -4)], hx("#fbfaf4", 0.95 * a))
        line(c, [(-20, -100), (-16, -10)], hx("#ffffff", 0.6 * a), 5)
    scaled(c, x, y, s, f)

def apt(c, t, statue=0.0, fridge=0.0):
    vgrad(c, 0, 0, P, P, "#2c3350", "#1b2036")
    rect(c, 0, 800, P, 280, "#3a2c2a")
    rect(c, 90, 140, 260, 260, "#0c1124"); c.new_path(); c.rectangle(90, 140, 260, 260); c.set_line_width(16); src(c, "#4a3a38"); c.stroke()
    circ(c, 290, 200, 24, "#f4efd0"); circ(c, 280, 194, 22, "#0c1124")
    rect(c, 420, 520, 300, 200, "#111"); rect(c, 432, 532, 276, 176, "#1a2a4a"); rect(c, 540, 720, 60, 80, "#333")
    if statue > 0: clown(c, 880, 1000, 0.6, t, "creepy", a=statue)

# ---------------- PARTE 1 ----------------
def g01(c, t, T, w):
    sala(c, t, statue=1.0)
    small_sofa_you(c, t, "neutral", look=(0.8, -0.3), arms="none")
    tag2(c, 200, 360, "11:00 p.m.", t, w("once"), "#ffffff")
FOCUS["g01"] = (540, 640)

def g02(c, t, T, w):
    sala(c, t, statue=1.0)
CAM["g02"] = [("estatua", 1.9, 700, 660)]

def g03(c, t, T, w):
    rect(c, 0, 0, P, P, "#1b2036")
    def lista():
        rect(c, -300, -380, 600, 760, "#fbf6e6"); rect(c, -300, -380, 600, 80, "#e8c86a"); txt(c, "INSTRUCCIONES", 0, -326, "#3a2a10", 40, True, True)
        for i, (tok, l) in enumerate((("nueve", "1. Niños a dormir: 9 p.m."), ("nadie", "2. No le abras a nadie"), ("escríbenos", "3. Cualquier cosa, escríbenos"))):
            if t > w(tok) - 0.4: txt(c, l, -260, -200 + i * 120, "#1c2a5a", 36, False, True)
    scaled(c, 540, 560, 1.0, lista)
FOCUS["g03"] = (540, 500)

def g04(c, t, T, w):
    kids_room(c, t, empty=False, dark=0.25)
    bust(c, 860, 1160, 0.8, t, "smile", look=(-0.8, -0.2), **YOU)
FOCUS["g04"] = (400, 640)

def g05(c, t, T, w):
    kids_room(c, t, empty=False, dark=0.25)
    bust(c, 440, 1080, 1.0, t, "neutral", look=(0.4, 0), talk="auto", **TOMAS)
FOCUS["g05"] = (440, 640)

def g06(c, t, T, w):
    rect(c, 0, 0, P, P, "#2c3350")
    bust(c, 540, 1100, 1.15, t, "happy", **YOU)
    tag2(c, 540, 380, "¿AMIGO IMAGINARIO?", t, w("imaginario"), "#ffffff")
FOCUS["g06"] = (540, 600)

def g07(c, t, T, w):
    sala(c, t, statue=1.0)
    small_sofa_you(c, t, "worry", look=(1, -0.5))
FOCUS["g07"] = (560, 720)

def g08(c, t, T, w):
    rect(c, 0, 0, P, P, "#1b2036"); glow(c, 540, 600, 500, "#ff8a3a", 0.2)
    clown(c, 540, 1140, 1.25, t, "creepy", wet=clamp((t - w("mojados")) / 0.4))
FOCUS["g08"] = (540, 560)

def g09(c, t, T, w):
    chat(c, t, [(w("perdón") - 0.2, ["perdón, ¿puedo tapar", "la estatua del payaso", "con una cobija?", "me da cosa"], True)])
FOCUS["g09"] = (540, 400)

def g10(c, t, T, w):
    chat(c, t, [(0, ["perdón, ¿puedo tapar", "la estatua del payaso", "con una cobija?", "me da cosa"], True)], typing=w("dos"))
    tag2(c, 540, 880, "1 min... 2 min...", t, w("minuto"), "#ffffff")
FOCUS["g10"] = (540, 500)

MSG0 = ["perdón, ¿puedo tapar", "la estatua del payaso", "con una cobija?", "me da cosa"]
def g11(c, t, T, w):
    chat(c, t, [(0, MSG0, True), (0.1, ["Saca a los niños de", "la casa. YA.", "Llama a la policía."], False)])
FOCUS["g11"] = (540, 640)

def g12(c, t, T, w):
    chat(c, t, [(0, MSG0, True), (0, ["Saca a los niños de", "la casa. YA.", "Llama a la policía."], False), (w("por"), ["¿por qué?"], True)])
FOCUS["g12"] = (540, 760)

def g13(c, t, T, w):
    rect(c, 0, 0, P, P, "#0b141a")
    sc = popin(t, 0.1)
    if sc > 0.01:
        c.save(); c.translate(540, 540); c.scale(sc, sc); c.translate(-540, -540)
        bubble(c, 160, 420, 760, ["Nosotros no tenemos", "ninguna estatua", "de payaso."], "#1f2c34", "#ffffff", 56, "l"); c.restore()
FOCUS["g13"] = (540, 560)

def g14(c, t, T, w):
    sala(c, t, statue=0.0)
    if t < w("vacía"): clown(c, 690, 860, 0.55, t, "creepy", a=clamp(1 - (t - 0.3) / 0.4) if t > 0.3 else 1.0)
FOCUS["g14"] = (720, 640)
CAM["g14"] = [("esquina", 1.7, 720, 660)]

def g15(c, t, T, w):
    sala(c, t, statue=0.0, dent=ease(clamp((t - w("hundido") + 0.3) / 0.6)))
FOCUS["g15"] = (360, 620)
CAM["g15"] = [("sofá", 1.6, 360, 620)]

def g16(c, t, T, w):
    sala(c, t, statue=0.0, dent=1.0, dark=0.6)

# ---------------- PARTE 2 ----------------
def h01(c, t, T, w):
    sala(c, t, statue=0.0, dent=1.0)
    small_sofa_you(c, t, "shock", look=(0.2, -0.4), arms="none")
FOCUS["h01"] = (420, 620)

def h02(c, t, T, w):
    if t < w("cuarto") - 0.2:
        stairs(c, t, light=0.4, night=False); bust_back_you(c, t)
    else:
        kids_room(c, t, empty=True, dark=0.45)
        tag2(c, 300, 400, "VACÍAS", t, w("vacías"), "#e0303a", "#ffffff")
FOCUS["h02"] = (300, 640)

def bust_back_you(c, t):
    def f():
        rrect(c, -200, -240, 400, 330, 100, YOU["shirt"]); circ(c, 0, -380, 138, YOU["skin"])
        c.new_path(); c.arc(0, -392, 146, math.pi, 2 * math.pi); c.close_path(); fill(c, YOU["cap_col"]); circ(c, 0, -540, 26, "#f2a15a")
    scaled(c, 380, 1200, 0.8, f)

def h03(c, t, T, w):
    kids_room(c, t, empty=True, dark=0.45)
    for k in range(3):
        a = (t * 0.7 + k / 3) % 1
        txt(c, "ji", 820 + k * 40, 480 - 120 * a, hx("#ffffff", 1 - a), 40, True)
FOCUS["h03"] = (860, 500)

def h04(c, t, T, w):
    kids_room(c, t, empty=True, closet=ease(clamp((t - w("abres")) / 1.2)), kids=True, dark=0.3)
FOCUS["h04"] = (870, 560)

def h05(c, t, T, w):
    rect(c, 0, 0, P, P, "#100a10")
    bust(c, 420, 1080, 0.9, t, "smile", look=(0.5, 0), talk="auto", **SOFI)
    bust(c, 760, 1120, 0.8, t + 1, "worry", look=(-0.5, 0), **TOMAS)
    tag2(c, 540, 380, "CUENTA HASTA 100", t, w("cien"), "#ffc24a")
FOCUS["h05"] = (420, 620)

def h06(c, t, T, w):
    stairs(c, t, light=0.0); overlay(c, "#000010", 0.3)
    glow(c, 200, 900, 300, "#ff3a2a", 0.2)
FOCUS["h06"] = (300, 860)

def h07(c, t, T, w):
    stairs(c, t, light=0.0); overlay(c, "#000010", 0.3)
    n = 91 if t < w("noventa") + 1.4 else 92
    sc = 1 + 0.3 * math.exp(-((t - (w("noventa") if n == 91 else w("noventa") + 1.4)) * 6))
    c.save(); c.translate(540, 560); c.scale(sc, sc); ui(c, 200); outline_t(c, str(n), 0, 70, "#e0303a"); c.restore()
FOCUS["h07"] = (540, 540)

def outline_t(c, s, x, y, col):
    w_ = text_w(c, s); c.new_path(); c.move_to(x - w_ / 2, y); c.text_path(s); c.set_line_width(14); c.set_line_join(cairo.LINE_JOIN_ROUND)
    src(c, "#000"); c.stroke_preserve(); src(c, col); c.fill()

def h08(c, t, T, w):
    kids_room(c, t, empty=True, dark=0.3)
    bust(c, 300, 1120, 0.8, t, "worry", look=(0.8, -0.5), **YOU)
    rect(c, 436, 136, 208, 228, hx("#ffc24a", 0.25 + 0.15 * math.sin(t * 6)))
    tag2(c, 540, 460, "ÚNICA SALIDA", t, w("salida"), "#ffc24a")
FOCUS["h08"] = (480, 400)

def h09(c, t, T, w):
    house_back(c, t, you_arms=True, sofi=t > w("sofi"))
FOCUS["h09"] = (500, 560)

def h10(c, t, T, w):
    rect(c, 0, 0, P, P, "#0a1030")
    bust(c, 540, 1060, 1.0, t, "creepy", look=(0, 0), talk="auto", **TOMAS)
FOCUS["h10"] = (540, 600)

def h11(c, t, T, w):
    stairs(c, t, light=0.0); overlay(c, "#000010", 0.3)
    sc = popin(t, 0.0)
    if sc > 0.01: c.save(); c.translate(540, 560); c.scale(sc, sc); ui(c, 240); outline_t(c, "100", 0, 80, "#e0303a"); c.restore()
FOCUS["h11"] = (540, 540)

def h12(c, t, T, w):
    stairs(c, t, light=0.0); overlay(c, "#000010", 0.25)
    for k in range(5):
        if t > 0.4 + k * 0.7:
            x = 160 + k * 95; y = 960 - k * 100
            ell(c, x, y, 50, 16, "#e8402a"); ell(c, x + 30, y - 4, 26, 12, "#e8402a")
FOCUS["h12"] = (400, 780)

def h13(c, t, T, w):
    house_back(c, t, you_arms=True, sofi=True, jump=clamp((t - w("salta")) / 0.6))
FOCUS["h13"] = (480, 700)

def h14(c, t, T, w):
    porteria(c, t, police=clamp((t - w("llegan")) / 0.5))
    tag2(c, 300, 380, "8 MINUTOS", t, w("ocho"), "#ffffff")
FOCUS["h14"] = (500, 640)

def h15(c, t, T, w):
    k = w("vaso")
    if t < k - 0.2:
        sala(c, t, statue=0.0, dent=1.0)
        r = 0.5 + 0.5 * math.sin(t * 12); glow(c, 100, 200, 400, "#ff2a2a", 0.25 * r); glow(c, 1000, 200, 400, "#2a6aff", 0.25 * (1 - r))
    else:
        sala(c, t, statue=0.0, dent=1.0)
        milk(c, 300, 690, 1.2)
        if t > w("nota") - 0.2: crayon_note(c, 540, 380, 0.6 * popin(t, w("nota") - 0.2), [], t)
FOCUS["h15"] = (320, 620)

def h16(c, t, T, w):
    rect(c, 0, 0, P, P, "#1b2036")
    crayon_note(c, 540, 540, 1.4, ["Gracias por", "cuidarlos.", "Ya sé dónde vives."], t, 0.0)
FOCUS["h16"] = (540, 560)

def h17(c, t, T, w):
    rect(c, 0, 0, P, P, "#1b2036"); crayon_note(c, 540, 540, 1.2, ["Ya sé dónde vives."], 9.0); overlay(c, "#000", 0.6)

# ---------------- PARTE 3 ----------------
def i01(c, t, T, w):
    porteria(c, t, police=1.0)
    tag2(c, 760, 900, "«UNA BROMA»", t, w("broma"), "#ffffff")
FOCUS["i01"] = (400, 600)

def i02(c, t, T, w):
    rect(c, 0, 0, P, P, "#2c3350"); rect(c, 0, 820, P, 260, "#3a2c2a")
    bust(c, 330, 1060, 0.85, t, "worry", look=(0.5, 0), **PAPA)
    bust(c, 700, 1060, 0.85, t, "sad", look=(-0.5, 0), tears=0.5, **MAMA)
    bust(c, 520, 1180, 0.45, t, "sad", **SOFI)
FOCUS["i02"] = (540, 620)

def i03(c, t, T, w):
    rect(c, 0, 0, P, P, "#2c3350")
    bust(c, 540, 1080, 1.1, t, "worry", look=(0, 0), talk="auto", **MAMA)
FOCUS["i03"] = (540, 600)

def i04(c, t, T, w):
    kids_room(c, t, empty=False, dark=0.5)
    for k in range(3):
        if t > w("dulces") - 0.2: circ(c, 120 + k * 40, 600, 14, ("#e0303a", "#ffc24a", "#5fb4ff")[k])
    if t > w("canta") - 0.2:
        for k in range(3):
            a = (t * 0.5 + k / 3) % 1; circ(c, 600 + k * 60, 520 - 160 * a, 10, hx("#ffffff", 1 - a)); line(c, [(609 + k * 60, 520 - 160 * a), (609 + k * 60, 484 - 160 * a)], hx("#ffffff", 1 - a), 4)
    tag2(c, 540, 900, "HACE 8 MESES", t, w("ocho"), "#ffffff")
FOCUS["i04"] = (300, 620)

def i05(c, t, T, w):
    rect(c, 0, 0, P, P, "#2c3350")
    bust(c, 330, 1060, 0.85, t, "shock", **PAPA); bust(c, 700, 1060, 0.85, t, "shock", **MAMA)
    tag2(c, 540, 380, "HASTA HOY", t, w("hoy"), "#e0303a", "#ffffff")
FOCUS["i05"] = (540, 620)

def i06(c, t, T, w):
    kids_room(c, t, empty=True, closet=1.0, dark=0.2)
    def dog():
        ell(c, 0, 0, 120, 60, "#7a5a3a"); circ(c, 110, -50, 50, "#7a5a3a"); poly(c, [(90, -100), (110, -150), (130, -100)], "#5a3a2a")
        circ(c, 125, -60, 8, "#111"); ell(c, 160, -40, 14, 10, "#111")
        for lx in (-80, -30, 40, 80): rect(c, lx, 40, 22, 70, "#7a5a3a")
        if t > w("ladrar"): ell(c, 150, -20, 20, 12 + 8 * abs(math.sin(t * 14)), "#5a1a1a")
    scaled(c, 680, 820, 0.9, dog)
FOCUS["i06"] = (820, 600)

def i07(c, t, T, w):
    rect(c, 0, 0, P, P, "#1a1214")
    rect(c, 300, 200, 480, 700, "#6a4a3a"); rect(c, 360, 260, 360, 600, "#050305")
    if t > w("cobija") - 0.2: rrect(c, 380, 700, 320, 140, 30, "#5a6a4a")
    if t > w("latas") - 0.2:
        for k in range(4): rect(c, 400 + k * 50, 640, 34, 50, "#a8a8b0")
    if t > w("dibujos") - 0.2:
        rr = random.Random(5)
        for k in range(10): drawing(c, rr.uniform(400, 680), rr.uniform(320, 600), 0.32, t, rot=rr.uniform(-0.4, 0.4))
    glow(c, 540, 500, 300, "#ffd890", 0.15)
FOCUS["i07"] = (540, 560)
CAM["i07"] = [("hueco", 1.3, 540, 560)]

def i08(c, t, T, w):
    rect(c, 0, 0, P, P, "#1a1214")
    for k in range(4):
        if t > 0.2 + k * 0.6: drawing(c, 280 + (k % 2) * 520, 330 + (k // 2) * 400, 1.25, t, rot=(-0.08, 0.06, 0.05, -0.04)[k])
FOCUS["i08"] = (540, 540)

def i09(c, t, T, w):
    rect(c, 0, 0, P, P, "#1a1214")
    drawing(c, 540, 520, 2.3, t, last=True)
FOCUS["i09"] = (540, 520)

def i10(c, t, T, w):
    rect(c, 0, 0, P, P, "#1a1214")
    drawing(c, 540, 380, 1.8, t, last=True)
    a = clamp((t - w("dirección")) / 0.8)
    if a > 0:
        c.save(); c.rectangle(160, 650, 760 * a, 160); c.clip()
        ui(c, 64); outline_t(c, "Calle 63 # 14-20", 540, 760, "#d0241c"); c.restore()
FOCUS["i10"] = (540, 640)

def i11(c, t, T, w):
    rect(c, 0, 0, P, P, "#2c3350"); rect(c, 0, 820, P, 260, "#3a2c2a")
    rrect(c, 120, 820, 840, 200, 30, "#5a4a6a")
    bust(c, 540, 1100, 0.9, t, "tired", eyebags=1.0, **YOU)
    for i in range(3): tag2(c, 260 + i * 280, 380, f"DÍA {i + 1}", t, w("tres") + i * 0.35, "#ffffff")
FOCUS["i11"] = (540, 620)

def i12(c, t, T, w):
    apt(c, t)
    bust(c, 540, 1120, 0.9, t, "smile" if t < w("cosas") else "neutral", look=(0.4, 0), **YOU)
FOCUS["i12"] = (540, 620)

def i13(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#2c3350", "#1b2036")
    rect(c, 300, 120, 480, 900, "#d8dce0"); rect(c, 330, 160, 420, 820, "#f4f8ff")
    glow(c, 540, 500, 500, "#e8f4ff", 0.4)
    for k in range(3): rect(c, 330, 380 + k * 200, 420, 10, "#c0c8d0")
    rrect(c, 360, 300, 120, 80, 10, "#c0402a"); rrect(c, 600, 500, 100, 70, 10, "#e8c86a")
    if t > w("vaso") - 0.2: milk(c, 540, 560, 1.5 * popin(t, w("vaso") - 0.2))
FOCUS["i13"] = (540, 500)

def i14(c, t, T, w):
    apt(c, t, statue=1.0 if t > w("estatua") - 0.1 else 0.0)
    c.save(); c.rectangle(0, 0, 420, P); c.clip(); bust(c, 180, 1150, 0.8, t, "shock" if t > w("estatua") else "worry", look=(1, 0), sweat=1.0, **YOU); c.restore()
FOCUS["i14"] = (860, 700)
CAM["i14"] = [("estatua", 1.6, 860, 700)]

def i15(c, t, T, w):
    apt(c, 0.0, statue=1.0); overlay(c, "#000", 0.6)

PANELS = {k: v for k, v in globals().items() if len(k) == 3 and k[0] in "ghi" and k[1:].isdigit() and callable(v)}

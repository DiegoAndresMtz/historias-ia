import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect_path, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp, text_w
from povlib import *

YOU = dict(hat="hair", skin="#c48a5c", shirt="#2f6f8f", hair_col="#1d1410", mole=True)
GAB = dict(hat="hair", skin="#c48a5c", shirt="#2b2b33", hair_col="#1d1410", mole=True, hood=True)
MAMA = dict(hat="bun", skin="#b67a50", shirt="#8a3a5a", hair_col="#2a1a14")
PAPA = dict(hat="none", skin="#a8704a", shirt="#3a5a8a", hair_col="#1a120e", mustache=True)


def hw(c, s, x, y, size, col="#1c2a5a", center=False):
    c.select_font_face("Crimson Text", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)
    if center: x -= text_w(c, s) / 2
    c.move_to(x, y); src(c, col); c.show_text(s)

def sepia(c, a=1.0):
    c.save(); c.set_operator(cairo.OPERATOR_HSL_SATURATION); rect(c, 0, 0, P, P, hx("#808080", 0.85 * a)); c.restore()
    rect(c, 0, 0, P, P, hx("#7a4a1a", 0.22 * a))
    rr = random.Random(int(a * 100))
    for k in range(30): circ(c, rr.uniform(0, P), rr.uniform(0, P), rr.uniform(1, 3), hx("#ffffff", 0.08))

def popin(t, t0, d=0.3): return pop(t, t0, d)

# ---------------- escenarios ----------------
def dining(c, t, night=True, lamp=1.0, photo=True, warm=False):
    top, bot = ("#2a1f1c", "#140e0d") if night else ("#c9a27a", "#8f6a4a")
    if warm: top, bot = "#5a3a26", "#2a1a12"
    vgrad(c, 0, 0, P, 820, top, bot)
    rect(c, 0, 560, P, 260, hx("#000", 0.18)); rect(c, 0, 556, P, 8, hx("#000", 0.3))
    # ventana
    rrect(c, 640, 150, 300, 330, 8, "#3a2a20")
    vgrad(c, 656, 166, 268, 298, "#0a1430" if night else "#9fd0f0", "#1a2650" if night else "#e8f0f0")
    if night: circ(c, 860, 230, 28, hx("#f0ecd8", 0.9))
    rect(c, 786, 166, 8, 298, "#3a2a20"); rect(c, 656, 312, 268, 8, "#3a2a20")
    poly(c, [(620, 130), (690, 130), (670, 500), (610, 520)], "#7a3a3a"); poly(c, [(960, 130), (890, 130), (910, 500), (970, 520)], "#7a3a3a")
    if photo: dad_photo(c, 250, 300, 0.8, t)
    if lamp > 0:
        line(c, [(540, 0), (540, 110)], "#111", 4)
        poly(c, [(470, 170), (610, 170), (575, 110), (505, 110)], "#c9a24a")
        glow(c, 540, 180, 520, "#ffcf80", 0.35 * lamp)
        c.new_path(); c.move_to(470, 170); c.line_to(610, 170); c.line_to(900, 820); c.line_to(180, 820); c.close_path(); src(c, hx("#ffd890", 0.06 * lamp)); c.fill()

def dad_photo(c, x, y, s, t, ribbon=True, glow_a=0.0):
    def f():
        if glow_a: glow(c, 0, 0, 260, "#ffc24a", 0.4 * glow_a)
        rect(c, -120, -150, 240, 300, "#5a3a22"); rect(c, -104, -134, 208, 268, "#d8cdb8")
        c.save(); c.rectangle(-104, -134, 208, 268); c.clip(); vgrad(c, -104, -134, 208, 268, "#8aa0b0", "#5a6a78")
        bust(c, 0, 230, 0.55, 0.0, "smile", **PAPA); c.restore()
        if ribbon: poly(c, [(60, -150), (120, -150), (120, -90)], "#111"); poly(c, [(72, -150), (120, -102), (120, -90), (60, -150)], "#000")
    scaled(c, x, y, s, f)

def table_front(c, y=820, night=True):
    rect(c, 0, y, P, P - y, "#e9dfc8" if not night else "#c9bfa8")
    for k in range(0, P, 60): rect(c, k, y, 30, P - y, hx("#c0392b", 0.10))
    rect(c, 0, y, P, 10, hx("#000", 0.25))

def plate(c, x, y, s, food=True, empty=False, t=0.0, pops=None):
    def f():
        ell(c, 0, 10, 150, 52, hx("#000", 0.25)); ell(c, 0, 0, 150, 52, "#f7f5f0"); ell(c, 0, 0, 108, 36, "#ebe7de")
        if food and not empty:
            p = pops or (1, 1, 1)
            if p[0] > 0: scaled(c, -40, -6, p[0], lambda: (ell(c, 0, 0, 56, 22, "#fbfaf4"), ell(c, -10, -6, 30, 10, "#ffffff")))
            if p[1] > 0:
                def bn():
                    ell(c, 0, 0, 42, 18, "#5a2418")
                    rr = random.Random(3)
                    for k in range(14): ell(c, rr.uniform(-30, 30), rr.uniform(-10, 10), 7, 4, "#3a140c")
                scaled(c, 40, -4, p[1], bn)
            if p[2] > 0:
                def md():
                    for k, (dx, dy) in enumerate(((-20, 0), (0, 6), (20, -2))):
                        c.save(); c.translate(dx, dy); c.rotate(0.3 * (k - 1)); ell(c, 0, 0, 22, 11, "#c0601a"); ell(c, 0, -2, 18, 8, "#f0a030"); c.restore()
                scaled(c, 0, 22, p[2], md)
    scaled(c, x, y, s, f)

def glass(c, x, y, s, a=1.0):
    def f():
        poly(c, [(-36, -110), (36, -110), (28, 0), (-28, 0)], hx("#dfeee0", 0.55 * a))
        poly(c, [(-32, -80), (32, -80), (26, -4), (-26, -4)], hx("#d4e86a", 0.8 * a))
        line(c, [(-20, -100), (-16, -10)], hx("#ffffff", 0.6 * a), 5)
    scaled(c, x, y, s, f)

def chair(c, x, y, s, col="#5a3a22", back=True):
    def f():
        if back: rect(c, -90, -260, 22, 260, col); rect(c, 68, -260, 22, 260, col); rect(c, -90, -260, 180, 40, col); rect(c, -90, -170, 180, 22, col)
        rect(c, -100, 0, 200, 30, col); rect(c, -90, 30, 18, 160, col); rect(c, 72, 30, 18, 160, col)
    scaled(c, x, y, s, f)

def bust_back(c, x, y, s, t, shirt="#2b2b33", hair="#1d1410", skin="#c48a5c", hood=True, sway=0.0):
    wk = walk_amt(("back", shirt, hair), x, y, s, t)
    def f():
        br = math.sin(t * 2.0) * 0.4; c.translate(math.sin(t * 3) * 6 * sway, 0)
        if wk > 0: ph = t * 8.5; c.translate(0, -abs(math.sin(ph)) * 26 * wk); c.rotate(math.sin(ph) * 0.045 * wk)
        legs(c, t, wk)
        rrect(c, -209, -249 - br * 3, 418, 348, 108, OUT); rrect(c, -200, -240 - br * 3, 400, 330, 100, shirt)
        if hood: c.new_path(); c.arc(0, -250, 170, math.pi, 2 * math.pi); fill(c, hx("#000", 0.25))
        hy = -380 - br * 4
        circ(c, -132, hy + 10, 33, OUT); circ(c, 132, hy + 10, 33, OUT); circ(c, -132, hy + 10, 26, skin); circ(c, 132, hy + 10, 26, skin)
        circ(c, 0, hy, 146, OUT); circ(c, 0, hy, 138, hair)
        rect(c, -50, hy + 110, 100, 40, skin)
    scaled(c, x, y, s, f)

def stairs(c, t, light=0.0, night=True):
    vgrad(c, 0, 0, P, P, "#1c1618" if night else "#5a4a40", "#0c0a0b" if night else "#3a2e28")
    for k in range(9):
        x0 = 120 + k * 95; y0 = 1000 - k * 100
        rect(c, x0, y0, P - x0, 100, "#3a2a22" if k % 2 else "#33251e"); rect(c, x0, y0, P - x0, 14, "#5a4030")
    line(c, [(100, 980), (900, 180)], "#5a4030", 14)
    for k in range(9): line(c, [(150 + k * 95, 980 - k * 100), (150 + k * 95, 900 - k * 100)], "#4a3428", 8)
    if light: glow(c, 980, 80, 400, "#ffd890", 0.4 * light); rect(c, 920, 0, 140, 160, hx("#ffd890", 0.5 * light))

def door_in(c, t, under=0.0, shadow=0.0, ring=0.0):
    vgrad(c, 0, 0, P, P, "#231b1a", "#0e0b0b")
    rect(c, 300, 80, 480, 940, "#3a2416"); rect(c, 330, 110, 420, 910, "#5a3a22")
    rect(c, 370, 160, 340, 330, hx("#000", 0.18)); rect(c, 370, 540, 340, 400, hx("#000", 0.18))
    circ(c, 540, 330, 18, "#111"); circ(c, 540, 330, 10, "#c9a24a")
    circ(c, 700, 600, 20, "#c9a24a"); rect(c, 690, 640, 22, 50, "#9a7a3a")
    rect(c, 330, 1010, 420, 12, hx("#ffd890", 0.8 * under))
    if under: glow(c, 540, 1020, 300, "#ffd890", 0.3 * under)
    if shadow:
        rect(c, 430, 1008, 70, 14, hx("#000", 0.9 * shadow)); rect(c, 580, 1008, 70, 14, hx("#000", 0.9 * shadow))
    rect(c, 0, 1020, P, 60, "#1a1412")
    if ring > 0:
        rrect(c, 820, 420, 70, 110, 10, "#d8d0c0"); circ(c, 855, 475, 22, "#c9a24a")
        for k in range(3):
            r = 50 + k * 45 + (t * 160) % 45
            c.new_path(); c.arc(855, 475, r, -0.8, 0.8); c.set_line_width(7); src(c, hx("#ffc24a", 0.8 * ring * (1 - k / 3))); c.stroke()

def house_ext(c, t):
    vgrad(c, 0, 0, P, P, "#1a1e3a", "#3a2a3a")
    circ(c, 860, 160, 50, hx("#f0ecd8", 0.9)); glow(c, 860, 160, 200, "#f0ecd8", 0.2)
    rect(c, 200, 300, 680, 700, "#c9b89a"); poly(c, [(170, 310), (540, 130), (910, 310)], "#7a3a2a")
    rect(c, 200, 640, 680, 16, "#a89878")
    for x0 in (270, 600):
        rect(c, x0, 380, 200, 180, "#3a2a20"); rect(c, x0 + 12, 392, 176, 156, "#ffd890" if x0 == 270 else "#1a2040")
        rect(c, x0 + 96, 392, 8, 156, "#3a2a20")
    rect(c, 270, 700, 200, 180, "#3a2a20"); rect(c, 282, 712, 176, 156, "#ffd890")
    rect(c, 600, 690, 140, 310, "#5a2a1a"); circ(c, 720, 850, 9, "#c9a24a")
    for k in range(12): rect(c, 200 + k * 58, 990, 40, 10, hx("#000", 0.2))
    rect(c, 0, 1000, P, 80, "#2a2a2a")
    ui(c, 34); txt(c, "Bucaramanga", 540, 1060, hx("#ffffff", 0.8), 34, True)

def bedroom(c, t, clock="2:00"):
    vgrad(c, 0, 0, P, P, "#0c1024", "#05060e")
    rect(c, 640, 120, 300, 300, "#1a2040"); rect(c, 786, 120, 8, 300, "#0c1024"); circ(c, 860, 200, 26, hx("#f0ecd8", 0.7))
    c.new_path(); c.move_to(640, 420); c.line_to(940, 420); c.line_to(700, 1080); c.line_to(300, 1080); c.close_path(); src(c, hx("#9ab0ff", 0.07)); c.fill()
    rrect(c, 60, 620, 330, 160, 16, "#2a1a14"); rrect(c, 110, 660, 230, 90, 12, "#05060a")
    ui(c, 72); txt(c, clock, 225, 735, "#ff3a3a", 72, True)
    glow(c, 225, 700, 200, "#ff3a3a", 0.18)

def you_bed(c, t, mood="worry", look=(0, -1)):
    rrect(c, 200, 820, 880, 300, 40, "#3a4a7a"); rrect(c, 260, 760, 400, 120, 50, "#d8d8e8")
    c.save(); c.rectangle(0, 0, P, 860); c.clip()
    bust(c, 470, 1180, 0.85, t, mood, look=look, **YOU); c.restore()
    rrect(c, 160, 860, 920, 260, 40, "#4a5a8a"); line(c, [(200, 900), (1040, 880)], hx("#000", 0.2), 6)

def band(c, x, y, s, name, date="14 · MAR · 2006", rot=0.0, hl=0.0, smudge=False, glow_a=0.0, col="#5fb4ff"):
    def f():
        c.rotate(rot)
        if glow_a: glow(c, 0, 0, 380, "#ffc24a", 0.45 * glow_a)
        rrect(c, -330, -58, 660, 116, 50, hx("#000", 0.3)); rrect(c, -330, -64, 660, 116, 50, "#f6f4ee")
        rrect(c, -330, -64, 120, 116, 50, col); rect(c, -260, -64, 50, 116, col)
        rrect(c, -190, -44, 330, 76, 8, "#ffffff"); rect(c, 150, -44, 140, 76, "#ffffff")
        for k in range(16): rect(c, 160 + k * 8, -36, 3 + (k * 7) % 4, 60, "#222")
        txt(c, "RN · HOSP. SAN JUAN", -180, -16, "#666", 22, False)
        if smudge:
            txt(c, "M", -180, 22, "#1a1a2a", 40, False, True)
            for k in range(5): ell(c, -110 + k * 26, 8, 22, 14, hx("#3a3a5a", 0.5))
        else: txt(c, name, -180, 22, "#1a1a2a", 40, False, True)
        if hl: rrect(c, -192, 26, 340 * hl, 6, 3, "#e0303a")
        txt(c, date, -180, 48, "#e0303a" if hl else "#333", 22, False, True)
    scaled(c, x, y, s, f)

def shoebox(c, x, y, s, t, open_=0.0, ribbon=1.0):
    def f():
        rrect(c, -280, -120, 560, 260, 14, "#c9a070"); rect(c, -280, -40, 560, 6, hx("#000", 0.15))
        if open_ < 0.5:
            rrect(c, -296, -150, 592, 90, 14, "#d8b080")
            if ribbon: rect(c, -18, -150, 36, 290, "#c0202a"); rect(c, -296, -18, 592, 30, "#c0202a"); ell(c, -30, -150, 40, 20, "#c0202a"); ell(c, 30, -150, 40, 20, "#c0202a")
        else:
            rrect(c, -260, -110, 520, 70, 10, "#7a5a3a")
            c.save(); c.translate(0, -200); c.rotate(-0.15); rrect(c, -296, -60, 592, 90, 14, "#d8b080"); c.restore()
    scaled(c, x, y, s, f)

def paper_note(c, x, y, s, lines_, t, t0=0.0, rot=-0.04, red=False, sig=None):
    def f():
        c.rotate(rot)
        rect(c, -300, -220, 600, 460, hx("#000", 0.3)); rect(c, -306, -230, 600, 460, "#fbf6e6")
        for k in range(8): rect(c, -280, -160 + k * 52, 550, 2, hx("#5fb4ff", 0.35))
        for i, l in enumerate(lines_):
            a = clamp((t - t0 - i * 0.6) / 0.5)
            if a <= 0: continue
            c.save(); c.rectangle(-290, -230, 570 * a + 10, 460); c.clip()
            hw(c, l, -270, -120 + i * 80, 56, "#b0202a" if red else "#1c2a5a"); c.restore()
    scaled(c, x, y, s, f)

def tag2(c, x, y, s_, t, t0, col="#ffc24a", tcol="#11131a", size=40):
    sc = popin(t, t0)
    if sc <= 0.01: return
    c.save(); c.translate(x, y); c.scale(sc, sc); tag(c, 0, 0, s_, col, tcol, size); c.restore()

def hospital(c, t, babies=2, take=0.0):
    vgrad(c, 0, 0, P, P, "#d8e4e0", "#a8b8b4")
    rect(c, 0, 640, P, 440, "#8a9a98")
    rrect(c, 80, 520, 620, 300, 20, "#f0f0f0"); rrect(c, 60, 480, 80, 360, 20, "#c0c8cc")
    bust(c, 330, 860, 0.62, t, "smile", look=(0.6, 0.3), **MAMA)
    rrect(c, 80, 700, 620, 200, 30, "#b8d0e8")
    for k in range(babies):
        bx = 820 if k == 0 else 820 + take * 400
        rrect(c, bx - 110, 700, 220, 140, 20, hx("#ffffff", 0.7)); rect(c, bx - 100, 840, 12, 120, "#999"); rect(c, bx + 88, 840, 12, 120, "#999")
        circ(c, bx, 720, 40, "#e0a880"); ell(c, bx, 760, 70, 34, "#f0d0e0" if k else "#c0d8f0")
    if take > 0:
        poly(c, [(1000 + take * 200, 380), (1080 + take * 200, 380), (1100 + take * 200, 1080), (980 + take * 200, 1080)], hx("#3a4a5a", 0.9))
        circ(c, 1040 + take * 200, 320, 60, hx("#3a4a5a", 0.9))

def chest_scar(c, t, hand=0.0, glow_a=0.0):
    vgrad(c, 0, 0, P, P, "#3a2a26", "#1a1210")
    poly(c, [(100, 0), (980, 0), (1080, 1080), (0, 1080)], "#2f6f8f")
    poly(c, [(300, 0), (780, 0), (630, 1080), (450, 1080)], "#c48a5c")
    ell(c, 700, 300, 120, 500, hx("#3a1408", 0.15))
    if glow_a: glow(c, 545, 560, 260, "#ff3a3a", 0.35 * glow_a)
    line(c, [(545, 300), (540, 820)], "#a05a4a", 14); line(c, [(545, 300), (540, 820)], "#d8907a", 6)
    for k in range(10): line(c, [(522, 330 + k * 50), (566, 330 + k * 50)], "#a05a4a", 5)
    if hand > 0:
        hx_ = 860 - 300 * ease(hand)
        line(c, [(hx_ + 260, 600), (1180, 760)], "#2f6f8f", 170)
        rrect(c, hx_ + 60, 500, 230, 190, 60, "#c48a5c")
        for k in range(4): rrect(c, hx_ - 60 + k * 12, 500 + k * 44, 170, 40, 20, "#c48a5c"); line(c, [(hx_ - 50 + k * 12, 538 + k * 44), (hx_ + 90, 538 + k * 44)], hx("#7a4a2a", 0.4), 3)
        rrect(c, hx_ + 40, 450, 110, 44, 22, "#c48a5c")

def envelope(c, x, y, s, t, open_=0.0, logo=True):
    def f():
        rect(c, -300, -190, 600, 380, hx("#000", 0.3)); rect(c, -306, -200, 600, 380, "#e8c86a")
        poly(c, [(-306, -200), (294, -200), (-6, 20 - 240 * open_)], "#d8b050")
        if logo:
            circ(c, -200, 100, 50, "#ffffff"); rect(c, -214, 66, 28, 68, "#e0303a"); rect(c, -234, 86, 68, 28, "#e0303a")
            txt(c, "HOSPITAL SAN JUAN", -130, 112, "#5a4010", 34, False, True)
    scaled(c, x, y, s, f)

def receipt(c, x, y, s, t, sig=0.0, hl=0.0):
    def f():
        rect(c, -320, -380, 640, 760, hx("#000", 0.3)); rect(c, -330, -390, 640, 760, "#f4efe0")
        txt(c, "HOSPITAL SAN JUAN", -10, -320, "#1a1a2a", 40, True, True)
        txt(c, "RECIBO N.º 0047", -10, -270, "#555", 30, True)
        txt(c, "14 · MAR · 2006", -10, -225, "#555", 28, True)
        rect(c, -280, -200, 540, 3, "#999")
        txt(c, "Concepto:", -280, -140, "#333", 32, False); txt(c, "DONACIÓN", -100, -140, "#1a1a2a", 36, False, True)
        txt(c, "Bebé varón · RN", -280, -80, "#1a1a2a", 34, False, True)
        if hl: rrect(c, -290, -60, 560 * hl, 8, 4, hx("#e0303a", 0.8))
        txt(c, "Valor:", -280, 10, "#333", 32, False); txt(c, "$5.000.000", -150, 14, "#b0202a", 58, False, True)
        rect(c, -280, 200, 400, 3, "#333"); txt(c, "Firma de la madre", -280, 240, "#555", 26, False)
        if sig > 0:
            c.save(); c.rectangle(-280, 100, 420 * sig, 110); c.clip(); hw(c, "Rosa Martínez", -270, 190, 74, "#1c2a8a"); c.restore()
    scaled(c, x, y, s, f)

def road(c, t, crash=0.0):
    vgrad(c, 0, 0, P, 560, "#04050c", "#141a30")
    mountains_(c)
    poly(c, [(0, 1080), (440, 560), (640, 560), (1080, 1080)], "#1a1a1e")
    for k in range(6):
        p = ((t * 0.8 + k / 6) % 1); y0 = 560 + p * p * 520; wd = 4 + 30 * p * p
        rect(c, 540 - wd / 2, y0, wd, 20 + 60 * p * p, "#e8d070")
    rrect(c, 740, 300, 300, 120, 10, "#1a6a3a"); txt(c, "MEDELLÍN 120", 890, 375, "#ffffff", 42, True); rect(c, 880, 420, 14, 150, "#888")
    cx_ = 540 + math.sin(t * 2) * 6
    glow(c, cx_ - 60, 760, 200, "#fff4c0", 0.4); glow(c, cx_ + 60, 760, 200, "#fff4c0", 0.4)
    rrect(c, cx_ - 160, 700, 320, 140, 30, "#3a3a44"); rrect(c, cx_ - 120, 640, 240, 90, 30, "#2a2a34")
    circ(c, cx_ - 90, 790, 26, "#fff4c0"); circ(c, cx_ + 90, 790, 26, "#fff4c0")
    if crash: rect(c, 0, 0, P, P, hx("#000", crash))

def mountains_(c):
    poly(c, [(0, 600), (200, 380), (380, 520), (560, 340), (760, 500), (920, 360), (1080, 480), (1080, 600)], "#0a0d1a")

def three_at_table(c, t, warm=True, gab=True, you_mood="smile", mom_mood="smile", gab_mood="smile"):
    dining(c, t, night=True, warm=warm)
    bust(c, 200, 960, 0.7, t, you_mood, look=(0.5, 0), **YOU)
    bust(c, 540, 900, 0.62, t + 1, mom_mood, look=(0, 0.2), **MAMA)
    if gab: bust(c, 880, 960, 0.7, t + 2, gab_mood, look=(-0.5, 0), **GAB)
    table_front(c, 860)
    plate(c, 220, 930, 0.75); plate(c, 540, 920, 0.7); plate(c, 860, 930, 0.75)


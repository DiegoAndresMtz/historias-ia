import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect_path, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp, text_w
from povlib import *

YOU = dict(hat="hair", skin="#c48a5c", shirt="#2f6f8f", hair_col="#1d1410", mole=True)
GAB = dict(hat="hair", skin="#c48a5c", shirt="#2b2b33", hair_col="#1d1410", mole=True, hood=True)
MAMA = dict(hat="bun", skin="#b67a50", shirt="#8a3a5a", hair_col="#2a1a14")
PAPA = dict(hat="none", skin="#a8704a", shirt="#3a5a8a", hair_col="#1a120e", mustache=True)

FOCUS = {}

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
    def f():
        br = math.sin(t * 2.0); c.translate(math.sin(t * 3) * 6 * sway, 0)
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
    if sc <= 0: return
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
    poly(c, [(380, 0), (700, 0), (640, 1080), (440, 1080)], "#c48a5c")
    c.save(); c.rectangle(380, 0, 320, P); c.clip(); ell(c, 640, 540, 140, 600, hx("#3a1408", 0.18)); c.restore()
    if glow_a: glow(c, 545, 560, 260, "#ff3a3a", 0.35 * glow_a)
    line(c, [(545, 300), (540, 820)], "#a05a4a", 14); line(c, [(545, 300), (540, 820)], "#d8907a", 6)
    for k in range(10): line(c, [(522, 330 + k * 50), (566, 330 + k * 50)], "#a05a4a", 5)
    if hand > 0:
        hx_ = 820 - 260 * ease(hand)
        rrect(c, hx_, 470, 330, 180, 80, "#c48a5c"); rrect(c, hx_ + 20, 480, 300, 30, 15, "#b07a50")
        line(c, [(hx_ + 300, 560), (1080, 640)], "#2f6f8f", 150)

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

# ---------------- PARTE 1 ----------------
def a01(c, t, T, w):
    dining(c, t)
    chair(c, 540, 820, 0.8)
    bust(c, 230, 1000, 0.8, t, "worry", look=(0.8, 0.3), **YOU)
    bust(c, 840, 960, 0.75, t, "neutral", look=(-0.6, 0.6), arms="hold", **MAMA)
    table_front(c)
    plate(c, 230, 910, 0.8); plate(c, 830, 910, 0.8)
    d = ease(clamp(t / 0.8)); plate(c, 540, 900 - 80 * (1 - d), 0.9)
    glow(c, 540, 900, 220, "#ffc24a", 0.25 * (0.5 + 0.5 * math.sin(t * 4)))
    for i, n in enumerate(("NOCHE 1", "NOCHE 2", "NOCHE 3")):
        tag2(c, 190, 340 + i * 72, n, t, w("tres") + i * 0.18, "#e0303a" if i == 2 else "#ffffff", "#ffffff" if i == 2 else "#11131a", 34)
FOCUS["a01"] = (540, 820)

def a02(c, t, T, w):
    dining(c, t)
    bust(c, 330, 1060, 1.05, t, "worry", look=(0.8, 0), talk=0.6 * abs(math.sin(t * 14)) if t < T * 0.8 else 0.0, **YOU)
    bust(c, 860, 1000, 0.75, t, "neutral", look=(0, 1), **MAMA)
    table_front(c, 900)
FOCUS["a02"] = (360, 640)

def a03(c, t, T, w):
    dining(c, t, lamp=0.8)
    bust(c, 540, 1060, 1.15, t, "neutral", look=(0, 1), talk="auto", **MAMA)
    table_front(c, 960)
FOCUS["a03"] = (540, 600)

def a04(c, t, T, w):
    dining(c, t, lamp=0.6)
    k = w("hermano")
    bust(c, 540, 1080, 1.2, t, "shock" if t > k - 0.1 else "worry", look=(0, 0), sweat=1.0 if t > k else 0.0, **YOU)
    if t > k: overlay(c, "#000", 0.25)
FOCUS["a04"] = (540, 560)
CAM = {"a04": [("hermano", 1.45, 540, 560)]}

def a05(c, t, T, w):
    if t < w("papá") - 0.1:
        house_ext(c, t)
    elif t < w("siempre") - 0.1:
        rect(c, 0, 0, P, P, "#1a1416"); dad_photo(c, 540, 520, 2.2, t, glow_a=0.4)
        tag2(c, 540, 960, "Murió cuando tenías 3 años", t, w("murió"), "#ffffff", "#11131a", 36)
    else:
        dining(c, t, night=False, lamp=0)
        bust(c, 380, 1040, 0.9, t, "smile", look=(0.5, 0), **YOU); bust(c, 720, 1000, 0.85, t, "smile", look=(-0.5, 0), **MAMA)
        tag2(c, 540, 340, "SOLO USTEDES DOS", t, w("dos"), "#ffc24a")
FOCUS["a05"] = (540, 560)

def a06(c, t, T, w):
    dining(c, t)
    if t < w("arroz") - 0.2:
        bust(c, 540, 1060, 1.0, t, "neutral", look=(0, 0.8), **YOU); table_front(c, 900)
        tag2(c, 540, 340, "¿VIENE VISITA?", t, w("visita"), "#ffffff")
        return
    table_front(c, 640)
    p = (popin(t, w("arroz")), popin(t, w("fríjoles")), popin(t, w("tajadas")))
    plate(c, 520, 820, 2.0, pops=p)
    gl = popin(t, w("limonada"))
    if gl > 0: glass(c, 900, 900, 1.6 * gl)
FOCUS["a06"] = (560, 800)

def a07(c, t, T, w):
    k = w("mañana")
    if t < k - 0.1:
        dining(c, t, lamp=0.4); chair(c, 540, 860, 1.0); table_front(c, 860)
        plate(c, 540, 930, 1.1)
        ui(c, 60); txt(c, "11:48 p.m.", 540, 160, hx("#ffffff", 0.8), 60, True)
    else:
        vgrad(c, 0, 0, P, P, "#f0e4c8", "#c8b090")
        rect(c, 0, 700, P, 380, "#8a9aa0"); rect(c, 0, 690, P, 14, "#6a7a80")
        glow(c, 900, 200, 500, "#fff4d0", 0.5)
        rrect(c, 300, 420, 480, 300, 20, "#c0c8cc")
        for k2 in range(6): rect(c, 330 + k2 * 76, 420, 10, 300, "#a0a8ac")
        c.save(); c.translate(540, 520); c.rotate(-0.25); ell(c, 0, 0, 60, 190, "#f7f5f0"); ell(c, 0, 0, 40, 140, "#ebe7de"); c.restore()
        for k2 in range(5):
            yy = 560 + ((t * 120 + k2 * 40) % 200); ell(c, 560 + k2 * 6, yy, 6, 10, hx("#9fdcff", 0.8))
        tag2(c, 540, 340, "VACÍO · LAVADO · SECANDO", t, w("vacío"), "#ffc24a", "#11131a", 36)
FOCUS["a07"] = (540, 560)

def a08(c, t, T, w):
    k = w("silla")
    if t < k - 0.2:
        bedroom(c, t, "2:00"); you_bed(c, t, "worry", (0.3, -0.6))
    else:
        dining(c, t, lamp=0.0); overlay(c, "#05081a", 0.55)
        sx = 540 + 90 * ease(clamp((t - k) / 1.2))
        chair(c, sx, 860, 1.0)
        for j in range(3): line(c, [(sx - 140 - j * 30, 800 + j * 40), (sx - 110 - j * 30, 800 + j * 40)], hx("#ffffff", 0.5), 5)
        table_front(c, 920)
FOCUS["a08"] = (300, 700)

def a09(c, t, T, w):
    dining(c, t, lamp=0.0); overlay(c, "#05081a", 0.5)
    chair(c, 640, 860, 1.0)
    k = w("caliente")
    if t > k - 0.1:
        for j in range(4):
            yy = 600 - ((t * 90 + j * 50) % 200)
            line(c, [(560 + j * 40, yy + 60), (575 + j * 40, yy + 30), (560 + j * 40, yy)], hx("#ff8a3a", 0.7), 6)
        glow(c, 640, 860, 220, "#ff6a2a", 0.45)
        rrect(c, 560, 830, 160, 60, 30, "#c48a5c")
    table_front(c, 940)
    c.save(); c.rectangle(0, 0, 360, P); c.clip(); bust(c, 120, 1100, 0.9, t, "worry", look=(1, 0.4), **YOU); c.restore()
FOCUS["a09"] = (640, 780)

def a10(c, t, T, w):
    dining(c, t)
    k = w("ríes")
    bust(c, 300, 1040, 0.95, t, "happy" if t > k - 0.1 else "neutral", look=(0.6, 0), **YOU)
    bust(c, 800, 1000, 0.85, t, "neutral", look=(-0.6, 0), **MAMA)
    table_front(c, 900); plate(c, 540, 960, 0.9)
    tag2(c, 300, 340, "JAJAJA", t, k, "#ffffff")
FOCUS["a10"] = (300, 620)

def a11(c, t, T, w):
    dining(c, t, lamp=0.8)
    k = w("aguan")
    bust(c, 540, 1060, 1.15, t, "sad" if t > k - 0.3 else "neutral", look=(0, 0.3), tears=clamp((t - k) / 0.8), **MAMA)
FOCUS["a11"] = (540, 560)

def a12(c, t, T, w):
    dining(c, t, lamp=0.8)
    bust(c, 540, 1060, 1.15, t, "sad", look=(0, 0), tears=1.0, talk="auto", **MAMA)
FOCUS["a12"] = (540, 600)

def a13(c, t, T, w):
    k = w("caja")
    if t < k - 0.2:
        stairs(c, t, light=0.6)
        bust_back(c, 620 + t * 60, 760 - t * 70, 0.55, t, shirt=MAMA["shirt"], hair=MAMA["hair_col"], skin=MAMA["skin"], hood=False)
    else:
        rect(c, 0, 0, P, P, "#2a1f1c"); table_front(c, 640)
        sb = popin(t, k)
        shoebox(c, 540, 700, 1.4 * sb, t)
        glow(c, 540, 600, 300, "#ffc24a", 0.2)
FOCUS["a13"] = (540, 640)

def a14(c, t, T, w):
    rect(c, 0, 0, P, P, "#2a1f1c"); table_front(c, 560)
    shoebox(c, 540, 860, 1.3, t, open_=1.0)
    k1, k2 = w("tiene"), w("gabriel")
    band(c, 540, 380, 1.25 * popin(t, w("manillas")), "TÚ", rot=-0.05, hl=0.0)
    if t > k2 - 0.2: band(c, 540, 640, 1.25 * popin(t, k2 - 0.2), "GABRIEL", rot=0.04, hl=clamp((t - k2) / 0.5), glow_a=1.0, col="#ff7aa0")
FOCUS["a14"] = (540, 640)
CAM["a14"] = [("manillas", 1.0, 540, 540), ("tiene", 1.5, 540, 380), ("gabriel", 1.5, 540, 640)]

def a15(c, t, T, w):
    k = w("cicatriz")
    if t < w("mismo") - 0.15:
        rect(c, 0, 0, P, P, "#2a1f1c")
        band(c, 540, 400, 1.3, "TÚ", hl=clamp((t - 0.3) / 0.6), rot=-0.03)
        band(c, 540, 680, 1.3, "GABRIEL", hl=clamp((t - 0.6) / 0.6), rot=0.03, col="#ff7aa0")
        tag2(c, 540, 900, "MISMA FECHA", t, w("fecha"), "#e0303a", "#ffffff")
    else:
        chest_scar(c, t, hand=clamp((t - w("mismo")) / 0.8), glow_a=clamp((t - k) / 0.4))
        tag2(c, 540, 1000, "OPERACIÓN DEL CORAZÓN · 2006", t, w("operación"), "#ffffff", "#11131a", 32)
FOCUS["a15"] = (540, 560)

def a16(c, t, T, w):
    k = w("timbre")
    door_in(c, t, under=0.3, ring=clamp((t - k) / 0.2) * (1 if t - k < 2 else 0))
    c.save(); c.rectangle(0, 0, 300, P); c.clip(); bust(c, 120, 1120, 0.85, t, "shock" if t > k else "worry", look=(1, -0.2), **YOU); c.restore()
FOCUS["a16"] = (600, 500)

def a17(c, t, T, w):
    door_in(c, t, under=0.4, shadow=1.0)
    overlay(c, "#000", 0.35)
    bust(c, 400, 1080, 1.15, t, "worry", look=(1, 0), talk="auto", **MAMA)
FOCUS["a17"] = (430, 600)

def a18(c, t, T, w):
    door_in(c, t, under=0.6, shadow=1.0); overlay(c, "#000", 0.6)

# ---------------- PARTE 2 ----------------
def b01(c, t, T, w):
    k = w("timbre")
    door_in(c, t, under=0.5, shadow=1.0, ring=1.0 if 0 < t - k < 1.5 else 0.0)
    c.save(); c.rectangle(0, 0, 300, P); c.clip(); bust(c, 120, 1120, 0.85, t, "worry", look=(1, -0.2), **YOU); c.restore()
    k2 = w("nombre")
    if t > k2 - 0.1:
        sc = popin(t, k2 - 0.1)
        c.save(); c.translate(560, 700); c.scale(sc, sc); bubble(c, -170, -60, 340, ["¿...?"], "#ffffff", "#11131a", 60); c.restore()
FOCUS["b01"] = (560, 600)

def b02(c, t, T, w):
    door_in(c, t, under=0.5, shadow=1.0); overlay(c, "#000", 0.3)
    bust(c, 540, 1080, 1.2, t, "shock", look=(0, 0), sweat=1.0, **YOU)
    for k in range(4):
        r = 120 + ((t * 300 + k * 90) % 360)
        c.new_path(); c.arc(540, 560, r, 0, 2 * math.pi); c.set_line_width(5); src(c, hx("#ff3a5a", 0.5 * (1 - r / 480))); c.stroke()
FOCUS["b02"] = (540, 560)

def peephole(c, t, bag=1.0):
    rect(c, 0, 0, P, P, "#000")
    c.save(); c.new_path(); c.arc(540, 540, 470, 0, 2 * math.pi); c.clip()
    vgrad(c, 0, 0, P, P, "#1a2040", "#0a0c18")
    poly(c, [(0, 760), (1080, 760), (1080, 1080), (0, 1080)], "#3a3a3a")
    glow(c, 540, 300, 400, "#ffd890", 0.25); line(c, [(540, 60), (540, 200)], "#222", 4); circ(c, 540, 210, 20, "#ffd890")
    for k in range(10): line(c, [(0, 700 + k * 6), (1080, 700 + k * 6)], hx("#000", 0.05), 2)
    if bag:
        poly(c, [(470, 900), (610, 900), (630, 760), (450, 760)], "#b08850"); poly(c, [(450, 760), (630, 760), (610, 735), (470, 735)], "#9a7440")
    g = cairo.RadialGradient(540, 540, 250, 540, 540, 470); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.9)
    c.rectangle(0, 0, P, P); c.set_source(g); c.fill()
    c.restore()

def b03(c, t, T, w):
    if t < w("miras") + 0.6:
        door_in(c, t, under=0.5)
        c.save(); c.rectangle(0, 0, 420, P); c.clip(); bust(c, 300, 1100, 0.9, t, "worry", look=(1, -0.6), **YOU); c.restore()
    else:
        peephole(c, t, bag=1.0 if t > w("bolsa") - 0.2 else 0.0)
        tag2(c, 540, 1000, "NO HAY NADIE", t, w("nadie"), "#ffffff")
FOCUS["b03"] = (540, 800)

def b04(c, t, T, w):
    rect(c, 0, 0, P, P, "#2a1f1c"); table_front(c, 600)
    poly(c, [(160, 980), (480, 980), (500, 620), (140, 620)], "#b08850")
    rrect(c, 520, 700, 340, 200, 24, hx("#e8f0f4", 0.8)); rrect(c, 540, 690, 300, 40, 14, "#5fb4ff")
    k = w("nota")
    if t > k - 0.2:
        paper_note(c, 760, 460, 0.6 * popin(t, k - 0.2), [], t)
FOCUS["b04"] = (660, 700)

def b05(c, t, T, w):
    rect(c, 0, 0, P, P, "#2a1f1c")
    paper_note(c, 540, 540, 1.4, ["Gracias por la", "comida, mamá.", "Ya casi.", "              — G"], t, 0.2)
FOCUS["b05"] = (540, 560)

def b06(c, t, T, w):
    stairs(c, t, light=0.3)
    bust(c, 420, 980, 0.85, t, "sad", look=(0.6, 0), **MAMA)
    bust(c, 860, 1120, 0.95, t, "worry", look=(-0.8, -0.2), **YOU)
FOCUS["b06"] = (420, 600)

def b07(c, t, T, w):
    k = w("hospital")
    if t < k - 0.2:
        stairs(c, t, light=0.3); bust(c, 540, 1080, 1.1, t, "sad", look=(0, 0.2), talk="auto", **MAMA)
        tag2(c, 540, 340, "GEMELOS", t, w("gemelos"), "#ffc24a")
    else:
        hospital(c, t, babies=2, take=clamp((t - w("muerto")) / 1.5)); sepia(c)
        ui(c, 40); txt(c, "2006", 120, 90, "#ffffff", 40, True)
FOCUS["b07"] = (600, 640)

def b08(c, t, T, w):
    k = w("entregaron")
    if t < k - 0.2:
        hospital(c, t, babies=1); sepia(c)
        rect(c, 760, 680, 200, 200, hx("#000", 0.5)); tag2(c, 860, 600, "?", t, w("cuerpo"), "#e0303a", "#ffffff", 60)
    else:
        rect(c, 0, 0, P, P, "#d8cdb8"); sepia(c)
        band(c, 540, 540, 1.5 * popin(t, k - 0.2), "GABRIEL", col="#ff7aa0")
FOCUS["b08"] = (540, 600)

def b09(c, t, T, w):
    rect(c, 0, 0, P, P, "#2a1f1c"); table_front(c, 500)
    envelope(c, 360, 640, 0.75, t, open_=1.0, logo=False)
    k = w("foto")
    if t > k - 0.3:
        def ph():
            c.rotate(0.06); rect(c, -200, -250, 400, 480, "#fbf8f0")
            c.save(); c.rectangle(-170, -220, 340, 340); c.clip(); vgrad(c, -170, -220, 340, 340, "#7a8a9a", "#4a5a6a")
            bust(c, 0, 220, 0.55, t, "neutral", **GAB); c.restore()
        scaled(c, 720, 560, 0.95 * popin(t, k - 0.3), ph)
        tag2(c, 720, 900, "IDÉNTICO A TI", t, w("idéntico"), "#e0303a", "#ffffff")
FOCUS["b09"] = (700, 560)

def b10(c, t, T, w):
    rect(c, 0, 0, P, P, "#1a1416")
    paper_note(c, 540, 540, 1.4, [], t)
FOCUS["b10"] = (540, 540)

def b11(c, t, T, w):
    rect(c, 0, 0, P, P, "#1a1416")
    paper_note(c, 540, 540, 1.4, ["No me morí.", "Me vendieron."], t, 0.0, red=True)
    if t > w("vendieron"): overlay(c, "#300000", 0.25)
FOCUS["b11"] = (540, 540)

def b12(c, t, T, w):
    k = w("amanezca")
    dining(c, t, lamp=0.3); overlay(c, "#05081a", 0.45 if t < k - 0.4 else 0.15)
    if t > k - 0.4: rect(c, 0, 0, P, P, hx("#ff9a50", 0.15))
    bust_back(c, 540, 1000, 0.75, t, sway=0.3)
    table_front(c, 900); plate(c, 540, 960, 0.9, empty=t > k)
    tag2(c, 220, 340, "2:00 a.m." if t < k - 0.4 else "5:30 a.m.", t, 0.2, "#ffffff")
FOCUS["b12"] = (540, 640)

def b13(c, t, T, w):
    bedroom(c, t, "2:00"); you_bed(c, t, "shock" if t > w("silla") else "worry", (0.4, -0.6))
    if t > w("silla"):
        for j in range(3): line(c, [(620 + j * 30, 300 + j * 40), (700 + j * 30, 300 + j * 40)], hx("#ffffff", 0.5), 5)
FOCUS["b13"] = (420, 700)

def b14(c, t, T, w):
    dining(c, t, lamp=0.35); overlay(c, "#05081a", 0.35)
    bust_back(c, 600, 1000, 0.8, t, sway=0.4)
    table_front(c, 920)
    c.save(); c.rectangle(0, 0, 280, P); c.clip(); stairs_mini = None; bust(c, 100, 1140, 0.75, t, "worry", look=(1, 0), **YOU); c.restore()
    tag2(c, 230, 340, "DESCALZO", t, w("descalzo"), "#ffffff")
FOCUS["b14"] = (600, 640)

def b15(c, t, T, w):
    dining(c, t, lamp=0.35); overlay(c, "#05081a", 0.3)
    k = w("voltea") + 0.6
    if t < k: bust_back(c, 540, 1060, 1.0, t)
    else: bust(c, 540, 1060, 1.0, t, "neutral", look=(0, 0), **GAB)
FOCUS["b15"] = (540, 600)
CAM["b15"] = [("tiene", 1.35, 540, 560), ("ojos", 1.8, 540, 540), ("lunar", 2.4, 500, 720)]

def b16(c, t, T, w):
    dining(c, t, lamp=0.35); overlay(c, "#05081a", 0.25)
    bust(c, 540, 1060, 1.1, t, "smile", look=(0, 0), talk="auto", **GAB)
FOCUS["b16"] = (540, 600)

def b17(c, t, T, w):
    dining(c, t, lamp=0.35, photo=False); overlay(c, "#05081a", 0.25)
    dad_photo(c, 330, 360, 1.3, t, glow_a=0.5)
    bust(c, 820, 1080, 0.95, t, "neutral", look=(-1, -0.5), **GAB)
FOCUS["b17"] = (330, 400)

def b18(c, t, T, w):
    dining(c, t, lamp=0.25); overlay(c, "#05081a", 0.35)
    bust(c, 540, 1060, 1.2, t, "worry", look=(0, 0), talk="auto", **GAB)
FOCUS["b18"] = (540, 580)

def b19(c, t, T, w):
    dining(c, t, lamp=0.2); overlay(c, "#05081a", 0.5)
    bust(c, 540, 1060, 1.0, t, "neutral", **GAB); overlay(c, "#000", 0.55)

# ---------------- PARTE 3 ----------------
def c01(c, t, T, w):
    dining(c, t, lamp=0.4); overlay(c, "#05081a", 0.3)
    bust(c, 280, 1040, 0.85, t, "shock", look=(1, 0), **YOU)
    bust(c, 800, 1040, 0.85, t, "neutral", look=(-1, 0), **GAB)
    table_front(c, 920)
FOCUS["c01"] = (540, 620)

def c02(c, t, T, w):
    stairs(c, t, light=0.6 + 0.2 * math.sin(t * 3))
    bust_back(c, 200, 1160, 0.7, t)
    if t > w("persona"): glow(c, 980, 80, 300, "#ff3a3a", 0.3)
FOCUS["c02"] = (900, 200)
CAM["c02"] = [("solo", 1.6, 880, 260)]

def c03(c, t, T, w):
    rect(c, 0, 0, P, P, "#2a1f1c"); table_front(c, 500)
    k = w("recibo")
    envelope(c, 540, 560, 1.2, t, open_=clamp((t - w("adentro")) / 0.6))
    if t > k - 0.3:
        c.save(); c.translate(0, -260 * ease(clamp((t - k + 0.3) / 0.8))); receipt(c, 540, 600, 0.6, t); c.restore()
FOCUS["c03"] = (540, 560)

def c04(c, t, T, w):
    rect(c, 0, 0, P, P, "#2a1f1c")
    receipt(c, 540, 600, 1.25, t, hl=clamp((t - w("bebé")) / 0.6))
FOCUS["c04"] = (540, 560)
CAM["c04"] = [("cinco", 1.5, 460, 560), ("donación", 1.5, 540, 420)]

def c05(c, t, T, w):
    rect(c, 0, 0, P, P, "#2a1f1c")
    receipt(c, 540, 400, 1.25, t, sig=clamp((t - w("firma")) / 0.9))
FOCUS["c05"] = (500, 680)
CAM["c05"] = [("firma", 1.6, 420, 680)]

def c06(c, t, T, w):
    stairs(c, t, light=0.5)
    k = w("ahí")
    if t > k - 0.3:
        bust(c, 820, 420, 0.55, t, "sad", look=(-0.6, 0.6), **MAMA)
        overlay(c, "#000", 0.15)
    for j in range(3):
        if t > 0.3 + j * 0.45 and t < k: ell(c, 900 - j * 60, 360 + j * 90, 22, 10, hx("#000", 0.6))
    bust(c, 200, 1140, 0.8, t, "shock", look=(1, -1), **YOU)
FOCUS["c06"] = (800, 360)

def c07(c, t, T, w):
    stairs(c, t, light=0.3)
    bust(c, 420, 1000, 0.9, t, "sad", look=(0.6, 0.8), tears=0.6, **MAMA)
    c.save(); c.rectangle(720, 0, 360, P); c.clip(); bust(c, 960, 1180, 1.0, t, "worry", look=(-1, 0), **YOU); c.restore()
FOCUS["c07"] = (420, 600)

def c08(c, t, T, w):
    if t < w("operación") - 0.2:
        rect(c, 0, 0, P, P, "#d8e4e0"); rrect(c, 300, 500, 480, 300, 30, hx("#bfe0f0", 0.6)); rrect(c, 300, 760, 480, 200, 20, "#c0c8cc")
        circ(c, 540, 650, 60, "#e0a880"); ell(c, 540, 720, 100, 50, "#c0d8f0")
        line(c, [(200, 300), (300, 300), (330, 240), (360, 360), (390, 300), (880, 300)], "#2ad07a", 6)
        tag2(c, 540, 340, "CORAZÓN MALO", t, w("corazón"), "#e0303a", "#ffffff"); sepia(c, 0.7)
    elif t < w("papá") - 0.2:
        rect(c, 0, 0, P, P, "#d8cdb8"); sepia(c, 0.7)
        sc = popin(t, w("operación"))
        c.save(); c.translate(540, 540); c.scale(sc, sc); ui(c, 130); outline_text_(c, "$5.000.000", 0, 40, "#e0303a"); c.restore()
    else:
        rect(c, 0, 0, P, P, "#3a3028")
        bust(c, 330, 1060, 0.85, t, "sad", arms="head", **PAPA)
        bust(c, 780, 1040, 0.85, t, "worry", look=(-0.6, 0), tears=0.5, **MAMA); sepia(c, 0.6)
        tag2(c, 330, 340, "SIN TRABAJO", t, w("trabajo"), "#ffffff")
FOCUS["c08"] = (540, 580)

def outline_text_(c, s, x, y, col):
    w_ = text_w(c, s); c.new_path(); c.move_to(x - w_ / 2, y); c.text_path(s); c.set_line_width(14); c.set_line_join(cairo.LINE_JOIN_ROUND)
    src(c, "#000"); c.stroke_preserve(); src(c, col); c.fill()

def c09(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#c8d4d0", "#8a9a98"); rect(c, 0, 760, P, 320, "#7a8a88")
    for k in range(4): rect(c, 60 + k * 260, 200, 180, 360, hx("#ffffff", 0.3))
    bust(c, 340, 1040, 0.9, t, "worry", look=(1, 0), **MAMA)
    poly(c, [(700, 380), (900, 380), (960, 1080), (640, 1080)], "#e8eef0"); circ(c, 800, 300, 90, "#d8a878"); c.new_path(); c.arc(800, 290, 96, math.pi, 2 * math.pi); fill(c, "#1a1414")
    rect(c, 740, 200, 120, 40, "#ffffff"); rect(c, 790, 205, 20, 30, "#e0303a")
    if t > w("medellín") - 0.2: tag2(c, 800, 340, "PAREJA EN MEDELLÍN", t, w("medellín") - 0.2, "#ffc24a")
    sepia(c, 0.7)
FOCUS["c09"] = (560, 560)

def c10(c, t, T, w):
    stairs(c, t, light=0.2); overlay(c, "#000", 0.2)
    bust(c, 540, 1080, 1.2, t, "sad", look=(0, 0), tears=1.0, talk="auto", **MAMA)
FOCUS["c10"] = (540, 580)

def c11(c, t, T, w):
    chest_scar(c, t, hand=clamp(t / 0.8), glow_a=0.5 + 0.5 * math.sin(t * 7))
    tag2(c, 540, 340, "ESTÁS VIVO PORQUE...", t, w("vivo"), "#e0303a", "#ffffff", 38)
FOCUS["c11"] = (540, 560)

def c12(c, t, T, w):
    k = w("carretera")
    if t < k - 0.2:
        rect(c, 0, 0, P, P, "#1a1416"); dad_photo(c, 540, 540, 2.0, t, glow_a=0.3)
        tag2(c, 540, 960, "SE ENTERÓ AÑOS DESPUÉS", t, w("enteró"), "#ffffff", "#11131a", 34)
    else:
        road(c, t, crash=clamp((t - w("buscar") - 0.6) / 0.5))
        tag2(c, 540, 340, "LO IBA A BUSCAR", t, w("buscar"), "#ffc24a")
FOCUS["c12"] = (540, 600)

def c13(c, t, T, w):
    dining(c, t, lamp=0.4, photo=False); overlay(c, "#05081a", 0.2)
    dad_photo(c, 330, 360, 1.3, t, glow_a=0.3)
    bust(c, 820, 1080, 0.95, t, "sad", look=(-1, -0.5), **GAB)
FOCUS["c13"] = (820, 620)

def c14(c, t, T, w):
    stairs(c, t, light=0.3)
    bust(c, 300, 1000, 0.8, t, "sad", look=(1, 0), tears=0.8, **MAMA)
    bust(c, 780, 1080, 1.0, t, "neutral", look=(-0.8, 0), talk="auto", **GAB)
FOCUS["c14"] = (760, 600)

def c15(c, t, T, w):
    dining(c, t, lamp=0.6, warm=True)
    bust(c, 540, 1060, 1.15, t, "smile", look=(0, 0), talk="auto", tears=0.5, **GAB)
FOCUS["c15"] = (540, 600)

def c16(c, t, T, w):
    three_at_table(c, t)
    tag2(c, 540, 340, "3 PLATOS", t, w("tres"), "#ffc24a")
FOCUS["c16"] = (540, 760)

def c17(c, t, T, w):
    dining(c, t, warm=True); table_front(c, 640)
    lift = ease(clamp((t - w("dejó")) / 0.8))
    if lift > 0: band(c, 540, 820, 1.0 * lift, "", smudge=True, glow_a=lift, col="#9a7aff")
    plate(c, 540, 820 - 300 * lift, 2.0, empty=True)
FOCUS["c17"] = (540, 760)

def c18(c, t, T, w):
    rect(c, 0, 0, P, P, "#1a1416")
    band(c, 540, 540, 1.45, "", smudge=True, hl=clamp((t - w("fecha")) / 0.5), glow_a=1.0, col="#9a7aff")
    tag2(c, 540, 820, "¿UN TERCERO?", t, w("misma"), "#e0303a", "#ffffff", 46)
FOCUS["c18"] = (540, 540)
CAM["c18"] = [("tercera", 1.0, 540, 540), ("fecha", 1.7, 420, 600)]

def c19(c, t, T, w):
    rect(c, 0, 0, P, P, "#1a1416"); band(c, 540, 300, 1.2, "", smudge=True, col="#9a7aff"); overlay(c, "#000", 0.6)

PANELS = {k: v for k, v in globals().items() if len(k) == 3 and k[0] in "abc" and k[1:].isdigit() and callable(v)}

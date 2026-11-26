import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect_path, rrect, circ, ell, poly, line, glow, vgrad, overlay, flick, ease, clamp, text_w

P = 1080  # panel size

def back_ease(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def pop(t, t0, d=0.35): return back_ease((t - t0) / d) if t >= t0 else 0.0
def fade(t, t0, d=0.3): return ease((t - t0) / d)

def ui(c, size, bold=True):
    c.select_font_face("Montserrat", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)
def mono(c, size): c.select_font_face("DejaVu Sans Mono", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)
def txt(c, s, x, y, col, size=40, center=False, bold=True, font=None):
    (font or ui)(c, size) if font else ui(c, size, bold)
    if center: x -= text_w(c, s) / 2
    c.move_to(x, y); src(c, col); c.show_text(s)

def scaled(c, x, y, s, fn):
    if s <= 0.001: return
    c.save(); c.translate(x, y); c.scale(s, s); fn(); c.restore()

def card(c, x, y, w, h, r=24, col="#ffffff", shadow=0.25, border=None):
    if shadow: rrect(c, x + 6, y + 10, w, h, r, hx("#000", shadow))
    rrect(c, x, y, w, h, r, col)
    if border:
        c.new_path(); rrect_path(c, x, y, w, h, r); c.set_line_width(5); src(c, border); c.stroke()

def bubble(c, x, y, w, lines, col="#ffffff", tcol="#11131a", size=36, side="l", a=1.0):
    h = 30 + len(lines) * size * 1.3
    c.push_group()
    card(c, x, y, w, h, 28, col, 0.2)
    if side == "l": poly(c, [(x + 30, y + h - 4), (x + 10, y + h + 22), (x + 62, y + h - 4)], col)
    else: poly(c, [(x + w - 30, y + h - 4), (x + w - 10, y + h + 22), (x + w - 62, y + h - 4)], col)
    for i, l in enumerate(lines): txt(c, l, x + 26, y + 22 + size + i * size * 1.3, tcol, size)
    c.pop_group_to_source(); c.paint_with_alpha(a)
    return h

def tag(c, x, y, s_, col="#ffc24a", tcol="#11131a", size=34, a=1.0):
    ui(c, size); w = text_w(c, s_) + 44
    c.push_group(); card(c, x - w / 2, y - size - 14, w, size + 34, (size + 34) / 2, col, 0.25); txt(c, s_, x, y + 4, tcol, size, True)
    c.pop_group_to_source(); c.paint_with_alpha(a)

def callout(c, x, y, r, t, t0, fn, px=None, py=None):
    s = pop(t, t0)
    if s <= 0: return
    if px is not None:
        line(c, [(px, py), (x, y)], hx("#ffffff", 0.9 * min(1, s)), 5)
        circ(c, px, py, 10, hx("#ffffff", min(1, s)))
    c.save(); c.translate(x, y); c.scale(s, s)
    circ(c, 4, 8, r + 8, hx("#000", 0.3)); circ(c, 0, 0, r + 8, "#ffffff")
    c.save(); c.new_path(); c.arc(0, 0, r, 0, 2 * math.pi); c.clip(); fn(); c.restore()
    c.restore()

# ---------- character (bust) ----------
TALK = 0.0   # lo fija el render en cada cuadro según la voz
_POS = {}; _SEEN = {"t": None, "n": {}}
def walk_amt(key, x, y, s, t):
    """Detecta si un personaje se está moviendo entre cuadros: entonces camina (rebote de pasos)."""
    if _SEEN["t"] != t: _SEEN["t"] = t; _SEEN["n"] = {}
    i = _SEEN["n"].get(key, 0); _SEEN["n"][key] = i + 1; key = (key, i)
    prev = _POS.get(key); _POS[key] = (t, x, y, s)
    if not prev: return 0.0
    dt = t - prev[0]
    if dt <= 0 or dt > 0.2: return 0.0
    v = math.hypot(x - prev[1], y - prev[2]) / dt + abs(s - prev[3]) / dt * 900
    return max(0.0, min(1.0, (v - 25) / 90))
OUT = "#120c0e"
APPEAL = False   # estilo «que enamore»: ojos con iris y brillos, cachetes, pestañas, cejas suaves
OUTLINE = True   # contorno y sombras (estilo nuevo); False = estilo clásico

def legs(c, t, wk, pants="#262b38", shoe="#151318", skin=None):
    """Piernas y zapatos bajo el torso (local: el torso termina en y=90). Al caminar dan zancadas."""
    ph = t * 8.5
    for sx in (-1, 1):
        sw = math.sin(ph) * sx * wk
        c.save(); c.translate(sx * 85, 70); c.rotate(sw * 0.35)
        rrect(c, -52, 0, 104, 330, 40, OUT if OUTLINE else pants); rrect(c, -46, 0, 92, 322, 36, pants)
        ell(c, sx * 18, 330, 74, 34, shoe)
        c.restore()

def bust(c, x, y, s, t, mood="neutral", look=(0, 0), arms="none", hat="beanie", skin="#c48a5c", shirt="#3c8a5a",
         eyebags=0.0, tears=0.0, mustache=False, hair_col="#2a1a14", cap_col="#e8702a", sweat=0.0, talk=0.0, shake=0.0, apron=False, gray=False,
         mole=False, hood=False, eye_col="#6a3a1a", lashes=None, glasses=False, freckles=False, pants="#262b38"):
    if talk == "auto": talk = TALK
    c.save(); c.translate(x, y); c.scale(s, s)
    if shake: c.translate(math.sin(t * 60) * 4 * shake, math.cos(t * 47) * 2 * shake)
    # --- vida: caminar con pasos (no deslizarse), respirar sin flotar ---
    wk = walk_amt((hat, shirt, skin), x, y, s, t)
    if wk > 0:
        ph = t * 8.5
        c.translate(0, -abs(math.sin(ph)) * 26 * wk); c.rotate(math.sin(ph) * 0.045 * wk)
    legs(c, t, wk, pants=pants)
    br = math.sin(t * 2.0)
    c.save(); c.translate(0, -br * 1.2); c.scale(1 + 0.008 * br, 1)
    # torso (contorno + sombra)
    if OUTLINE: rrect(c, -209, -249, 418, 348, 108, OUT)
    rrect(c, -200, -240, 400, 330, 100, shirt)
    if OUTLINE: c.save(); rrect_path(c, -200, -240, 400, 330, 100); c.clip(); ell(c, 170, -60, 150, 260, hx("#000", 0.16)); c.restore()
    if hood: c.new_path(); c.arc(0, -240, 150, 0, math.pi); fill(c, hx("#000", 0.22)); line(c, [(-40, -200), (-46, -120)], "#d8d8d8", 6); line(c, [(40, -200), (46, -120)], "#d8d8d8", 6)
    if apron: rrect(c, -110, -200, 220, 300, 30, "#f1ece2")
    else:
        poly(c, [(-40, -240), (0, -195), (40, -240)], hx("#000", 0.18))
        if hat == "beanie": line(c, [(-26, -225), (-30, -160)], "#e9e4da", 6); line(c, [(26, -225), (30, -160)], "#e9e4da", 6)
    # arms
    hand = skin
    if arms == "laptop":
        line(c, [(-170, -150), (-150, -40), (-80, -10)], shirt, 62); line(c, [(170, -150), (150, -40), (80, -10)], shirt, 62)
        circ(c, -80, -10, 30, hand); circ(c, 80, -10, 30, hand)
    elif arms == "up":
        wv = math.sin(t * 9) * 12
        line(c, [(-170, -170), (-250, -330), (-260 + wv, -480)], shirt, 62); line(c, [(170, -170), (250, -330), (260 - wv, -480)], shirt, 62)
        circ(c, -260 + wv, -490, 32, hand); circ(c, 260 - wv, -490, 32, hand)
    elif arms == "head":
        line(c, [(-170, -170), (-230, -300), (-150, -420)], shirt, 62); line(c, [(170, -170), (230, -300), (150, -420)], shirt, 62)
    elif arms == "phone":
        line(c, [(170, -170), (210, -260), (120, -300)], shirt, 62)
    elif arms == "count":
        line(c, [(170, -170), (230, -260), (230, -380)], shirt, 62)
    elif arms == "hold":
        line(c, [(-170, -150), (-140, -60), (-60, -40)], shirt, 62); line(c, [(170, -150), (140, -60), (60, -40)], shirt, 62)
    c.restore()
    # head: actuación (inclina y asiente al hablar, mira alrededor, tiembla de miedo)
    hy = -380 - br * 1.2
    seed = sum(ord(ch) for ch in str(shirt) + str(hat))
    k_ = int(t / 1.9 + seed * 0.13)
    rr = random.Random(k_ * 31 + seed)
    if mood != "creepy" and look == (0, 0) and talk <= 0.05:
        look = (rr.uniform(-0.35, 0.35), rr.uniform(-0.2, 0.15))
    tilt = 0.05 * math.sin(t * 1.3 + seed) + (0.07 * math.sin(t * 2.6 + seed) * min(1.0, talk * 2.5) if talk > 0.05 else 0.0)
    nod = 10 * talk if talk > 0.05 else 0.0
    trem = 2.2 if mood in ("shock", "worry", "scared") else 0.0
    c.save(); c.translate(math.sin(t * 41) * trem, hy + 150 + nod + math.cos(t * 37) * trem * 0.6); c.rotate(tilt); c.translate(0, -(hy + 150))
    if OUTLINE: rect(c, -42, hy + 96, 84, 70, OUT); circ(c, -132, hy + 10, 33, OUT); circ(c, 132, hy + 10, 33, OUT); circ(c, 0, hy, 146, OUT)
    rect(c, -34, hy + 100, 68, 60, skin)
    circ(c, -132, hy + 10, 26, skin); circ(c, 132, hy + 10, 26, skin)
    if APPEAL: ell(c, -134, hy + 12, 11, 15, hx("#7a3a20", 0.22)); ell(c, 134, hy + 12, 11, 15, hx("#7a3a20", 0.22))
    circ(c, 0, hy, 138, skin)
    if OUTLINE: c.save(); c.new_path(); c.arc(0, hy, 138, 0, 2 * math.pi); c.clip(); circ(c, 95, hy + 55, 150, hx("#3a1408", 0.14)); circ(c, -60, hy - 70, 70, hx("#ffffff", 0.07)); c.restore()
    if mole: circ(c, -38, hy + 128, 7, "#3a2216")
    if hat == "beanie":
        c.new_path(); c.arc(0, hy - 12, 146, math.pi * 1.0, math.pi * 2.0); c.close_path(); fill(c, cap_col)
        rrect(c, -152, hy - 40, 304, 52, 24, hx("#000", 0.0)); rrect(c, -150, hy - 42, 300, 50, 22, "#c95a1c")
        for k in range(-130, 140, 26): rect(c, k, hy - 38, 6, 42, hx("#000", 0.1))
        circ(c, 0, hy - 160, 26, "#f2a15a")
    elif hat == "cap":
        c.new_path(); c.arc(0, hy - 18, 142, math.pi * 1.02, math.pi * 1.98); c.close_path(); fill(c, cap_col)
        ell(c, 70, hy - 34, 120, 22, hx("#000", 0.25)); ell(c, 70, hy - 40, 120, 22, cap_col)
        circ(c, 0, hy - 150, 12, hx("#000", 0.2))
        if gray: rect(c, -140, hy - 30, 24, 50, "#bdb8b2"); rect(c, 116, hy - 30, 24, 50, "#bdb8b2")
    elif hat == "bun":
        c.new_path(); c.arc(0, hy - 6, 144, math.pi * 1.02, math.pi * 1.98); c.close_path(); fill(c, hair_col)
        poly(c, [(-144, hy), (-110, hy - 70), (0, hy - 100), (110, hy - 70), (144, hy), (100, hy - 50), (-100, hy - 50)], hair_col)
        circ(c, 0, hy - 160, 56, hair_col)
        circ(c, -134, hy + 40, 9, "#e3c15a"); circ(c, 134, hy + 40, 9, "#e3c15a")
    elif hat == "hair":
        c.new_path(); c.arc(0, hy - 8, 146, math.pi * 1.0, math.pi * 2.0); c.close_path(); fill(c, hair_col)
        poly(c, [(-146, hy - 8), (-150, hy + 40), (-128, hy - 20)], hair_col); poly(c, [(146, hy - 8), (150, hy + 40), (128, hy - 20)], hair_col)
        poly(c, [(-120, hy - 60), (-60, hy - 20), (-20, hy - 70), (30, hy - 24), (80, hy - 72), (120, hy - 40), (110, hy - 110), (-110, hy - 110)], hair_col)
        for k in (-90, -30, 30, 90): poly(c, [(k - 30, hy - 120), (k, hy - 170), (k + 30, hy - 120)], hair_col)
    else:
        c.new_path(); c.arc(0, hy - 10, 144, math.pi * 1.05, math.pi * 1.95); c.close_path(); fill(c, hair_col)
    if APPEAL and hat in ("hair", "bun", "none"):
        c.new_path(); c.arc(-20, hy - 40, 100, math.pi * 1.15, math.pi * 1.45); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND); src(c, hx("#ffffff", 0.16)); c.stroke()
    if lashes is None: lashes = hat == "bun"
    # face
    ex = 54; ey = hy + 4
    bp = 3.1 + (seed % 17) / 10.0
    ph_b = (t + seed * 0.21) % bp; cyc = int((t + seed * 0.21) / bp)
    blink = ph_b < 0.12 or (cyc % 3 == 2 and 0.26 < ph_b < 0.36)
    if mood in ("happy", "proud"):
        for sx in (-ex, ex):
            c.new_path(); c.arc(sx, ey + 10, 30, math.pi * 1.15, math.pi * 1.85); c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND); src(c, "#1a1110"); c.stroke()
    elif mood == "creepy":
        for sx in (-ex, ex):
            circ(c, sx, ey, 48, "#f4f4ec"); circ(c, sx + look[0] * 8, ey + look[1] * 8, 7, "#0a0a0a")
            c.new_path(); c.arc(sx, ey, 48, 0, 2 * math.pi); c.set_line_width(3); src(c, hx("#5a1a1a", 0.5)); c.stroke()
    else:
        for sx in (-ex, ex):
            if APPEAL: ell(c, sx, ey, 40, 47, "#ffffff")
            else: circ(c, sx, ey, 40, "#ffffff")
            if blink and mood != "shock":
                rect(c, sx - 44, ey - 50, 88, 100, skin)
                if APPEAL: c.new_path(); c.arc(sx, ey - 6, 30, math.pi * 0.15, math.pi * 0.85); c.set_line_width(7); src(c, "#1a1110"); c.stroke()
                else: line(c, [(sx - 30, ey + 4), (sx + 30, ey + 4)], "#1a1110", 7)
            elif APPEAL:
                ir = 14 if mood == "shock" else 25
                px, py = sx + look[0] * 13, ey + 3 + look[1] * 13
                circ(c, px, py, ir, eye_col); circ(c, px, py + ir * 0.25, ir * 0.7, hx("#000000", 0.18))
                circ(c, px, py, ir * 0.52, "#120806")
                circ(c, px - ir * 0.36, py - ir * 0.38, ir * 0.36, "#ffffff"); circ(c, px + ir * 0.36, py + ir * 0.4, ir * 0.15, "#ffffff")
                c.new_path(); c.arc(sx, ey + 6, 45, math.pi * 1.13, math.pi * 1.87); c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND); src(c, "#1a1110"); c.stroke()
                if lashes:
                    o = 1 if sx > 0 else -1
                    for k in range(3): line(c, [(sx + o * (30 + k * 6), ey - 26 + k * 10), (sx + o * (44 + k * 9), ey - 38 + k * 8)], "#1a1110", 5)
                if mood == "tired":
                    c.new_path(); c.rectangle(sx - 44, ey - 50, 88, 46); fill(c, skin); line(c, [(sx - 36, ey - 4), (sx + 36, ey - 4)], "#1a1110", 6)
            else:
                pr = 9 if mood == "shock" else 18
                px, py = sx + look[0] * 14, ey + look[1] * 14
                circ(c, px, py, pr, "#1a1110"); circ(c, px - pr * 0.35, py - pr * 0.4, pr * 0.35, "#ffffff")
                if mood == "tired":
                    c.new_path(); c.rectangle(sx - 42, ey - 44, 84, 40); fill(c, skin); line(c, [(sx - 36, ey - 4), (sx + 36, ey - 4)], "#1a1110", 6)
    if eyebags > 0:
        for sx in (-ex, ex):
            c.new_path(); c.arc(sx, ey + 30, 30, math.pi * 0.15, math.pi * 0.85); c.set_line_width(8); src(c, hx("#6b3d6b", 0.55 * eyebags)); c.stroke()
    # brows
    bw = {"shock": (-20, 16), "sad": (-6, 10), "worry": (-4, 12), "scared": (-12, 16), "angry": (10, -8)}.get(mood, (0, 0))
    if talk > 0.05: bw = (bw[0], bw[1] + 9 * talk)
    for sx in (-1, 1):
        line(c, [(sx * (ex + 32), ey - 62 + bw[0] * 0.3), (sx * (ex - 26), ey - 66 - bw[1])], ("#2a1a14" if not gray else "#8e8a86"), 12 if APPEAL else 9)
    # nose
    if APPEAL: c.new_path(); c.arc(0, ey + 36, 13, math.pi * 0.2, math.pi * 0.8); c.set_line_width(6); src(c, hx("#7a4a2a", 0.55)); c.stroke()
    else: ell(c, 0, ey + 44, 12, 9, hx("#8a5a3a", 0.5))
    if mustache: poly(c, [(-60, ey + 66), (0, ey + 52), (60, ey + 66), (46, ey + 82), (0, ey + 70), (-46, ey + 82)], "#3a2a20" if not gray else "#cfc9c0")
    my = ey + 92
    if mood == "creepy" and talk <= 0.08:
        c.new_path(); c.move_to(-82, my - 22); c.curve_to(-50, my + 36, 50, my + 36, 82, my - 22); c.curve_to(40, my + 6, -40, my + 6, -82, my - 22); fill(c, "#2a0808")
        for k in range(-60, 70, 20): line(c, [(k, my - 2), (k, my + 12)], hx("#f4f0e0", 0.9), 5)
    elif talk > 0.08: ell(c, 0, my, 22 + 8 * talk, 5 + 22 * talk, "#4a1212"); ell(c, 0, my + 10 * talk, 12 + 4 * talk, 4 + 6 * talk, hx("#e86a6a", 0.8))
    elif mood == "happy": c.new_path(); c.move_to(-50, my - 10); c.curve_to(-30, my + 40, 30, my + 40, 50, my - 10); c.close_path(); fill(c, "#5a1a1a"); ell(c, 0, my + 14, 20, 8, "#e86a6a")
    elif mood in ("smile", "proud"): c.new_path(); c.arc(0, my - 30, 44, math.pi * 0.2, math.pi * 0.8); c.set_line_width(9); src(c, "#3a1a12"); c.stroke()
    elif mood == "shock": ell(c, 0, my + 6, 22, 30, "#3a0f0c")
    elif mood in ("sad", "worry"): c.new_path(); c.arc(0, my + 30, 36, math.pi * 1.2, math.pi * 1.8); c.set_line_width(8); src(c, "#3a1a12"); c.stroke()
    elif APPEAL: c.new_path(); c.arc(0, my - 22, 28, math.pi * 0.28, math.pi * 0.72); c.set_line_width(7); src(c, "#3a1a12"); c.stroke()
    else: line(c, [(-26, my), (26, my)], "#3a1a12", 8)
    if APPEAL and mood not in ("happy", "proud", "smile", "creepy"): ell(c, -92, ey + 48, 24, 13, hx("#ff7a8a", 0.25)); ell(c, 92, ey + 48, 24, 13, hx("#ff7a8a", 0.25))
    if mood in ("happy", "proud", "smile"): ell(c, -92, ey + 46, 24, 14, hx("#ff7a8a", 0.4)); ell(c, 92, ey + 46, 24, 14, hx("#ff7a8a", 0.4))
    if tears > 0:
        for sx in (-ex, ex):
            dy = (t * 120) % 140
            ell(c, sx + (8 if sx > 0 else -8), ey + 40 + dy, 9, 14, hx("#7fd0ff", 0.85 * tears))
    if sweat > 0:
        dy = (t * 60) % 80
        ell(c, 120, hy - 70 + dy, 12, 18, hx("#9fdcff", 0.9 * sweat))
    if freckles:
        for sx in (-1, 1):
            for k in range(4): circ(c, sx * (78 + (k % 2) * 18), ey + 30 + (k // 2) * 14, 4.5, hx("#7a3a1a", 0.45))
    if glasses:
        for sx in (-ex, ex):
            c.new_path(); c.arc(sx, ey, 50, 0, 2 * math.pi); c.set_line_width(9); src(c, glasses if isinstance(glasses, str) else "#3a2a1a"); c.stroke()
            circ(c, sx - 16, ey - 20, 10, hx("#ffffff", 0.25))
        line(c, [(-ex + 50, ey - 4), (ex - 50, ey - 4)], glasses if isinstance(glasses, str) else "#3a2a1a", 8)
    c.restore()
    # hand overlays
    if arms == "head":
        circ(c, -150, hy - 40, 34, skin); circ(c, 150, hy - 40, 34, skin)
    if arms == "phone":
        c.save(); c.translate(110, -330); c.rotate(-0.15); rrect(c, -40, -80, 80, 150, 14, "#15161b"); rrect(c, -32, -70, 64, 128, 8, "#5fb4ff"); c.restore()
        circ(c, 120, -290, 30, skin)
    if arms == "count":
        circ(c, 230, -390, 30, skin); rrect(c, 220, -470, 22, 70, 11, skin)
    c.restore()

# ---------- props ----------
def laptop_back(c, x, y, s, t, glow_a=1.0, logo="#5fb4ff", tape=False):
    def f():
        rrect(c, -230, -300, 460, 300, 18, "#3b3f4a"); rrect(c, -230, -300, 460, 300, 18, hx("#000", 0.0))
        circ(c, 0, -150, 34, hx(logo, 0.4 + 0.5 * glow_a))
        rect(c, 120, -270, 70, 40, "#ffd23b"); rect(c, -190, -80, 60, 30, "#ff6a8a")
        poly(c, [(-260, 0), (260, 0), (290, 40), (-290, 40)], "#2a2d35")
        if tape:
            line(c, [(260, 20), (330, 40), (420, 30)], "#1a1a1a", 10)
            rect(c, 300, 22, 40, 34, hx("#d9cfa0", 0.95))
    scaled(c, x, y, s, f)

def screen(c, x, y, w, h, title="", col="#14182a", bar="#1d2340"):
    card(c, x, y, w, h, 26, col, 0.35)
    c.save(); c.new_path(); rrect_path(c, x, y, w, h, 26); c.clip(); rect(c, x, y, w, 70, bar); c.restore()
    for k, cc in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")): circ(c, x + 40 + k * 34, y + 35, 11, cc)
    if title: txt(c, title, x + w / 2, y + 47, "#9fd0ff", 32, True)

def phone_ui(c, x, y, w, h, bg="#f3f4f8"):
    rrect(c, x - 14, y - 14, w + 28, h + 28, 56, "#121317"); rrect(c, x, y, w, h, 44, bg)
    rrect(c, x + w / 2 - 60, y + 14, 120, 26, 13, "#121317")

def piggy(c, x, y, s, t, crack=0.0, tape=False, coin_drop=0.0):
    def f():
        if crack >= 1:
            rr = random.Random(4)
            for k in range(9):
                ang = rr.uniform(0, 2 * math.pi); d = 140 * min(1, crack - 1 + 0.6)
                c.save(); c.translate(math.cos(ang) * d, -80 + math.sin(ang) * d * 0.6); c.rotate(ang)
                poly(c, [(-40, -30), (35, -38), (44, 26), (-30, 36)], "#f29ab5"); c.restore()
            return
        ell(c, 0, -110, 170, 125, "#f29ab5")
        for lx in (-100, -40, 40, 100): rrect(c, lx - 22, -30, 44, 50, 14, "#e57fa0")
        circ(c, -150, -150, 32, "#f29ab5"); ell(c, -190, -110, 34, 30, "#f7b4c9"); circ(c, -198, -112, 6, "#c45a7d"); circ(c, -180, -112, 6, "#c45a7d")
        poly(c, [(-110, -220), (-90, -270), (-60, -225)], "#e57fa0")
        circ(c, -120, -150, 10, "#2a1a14")
        rrect(c, -20, -238, 70, 14, 7, "#8c3a5a")
        c.new_path(); c.move_to(160, -120); c.curve_to(210, -150, 200, -80, 230, -110); c.set_line_width(8); src(c, "#e57fa0"); c.stroke()
        if crack > 0:
            pts = [(-10, -235), (10, -180), (-20, -140), (20, -90), (0, -40)]
            n = int(len(pts) * min(1, crack * 1.2)) + 1
            line(c, pts[:max(2, n)], "#7a2a4a", 6)
        if tape:
            for (a, b) in (((-60, -200), (60, -60)), ((50, -210), (-40, -40))): line(c, [a, b], hx("#e8dca0", 0.9), 26, cap=False)
    scaled(c, x, y, s, f)

def coins(c, x, y, s, t, n=6):
    for k in range(n):
        cx = x + (k - n / 2) * 40 * s; cy = y - abs(math.sin(t * 3 + k)) * 10
        ell(c, cx, cy, 34 * s, 30 * s, "#e8b93a"); ell(c, cx, cy, 24 * s, 21 * s, "#f6d36a")

def taxi(c, x, y, s, t):
    def f():
        ell(c, 0, 0, 300, 16, hx("#000", 0.35))
        rrect(c, -300, -150, 600, 110, 30, "#f2c230"); rrect(c, -170, -250, 330, 110, 40, "#f2c230")
        rrect(c, -150, -235, 140, 80, 14, "#1a2230"); rrect(c, 10, -235, 130, 80, 14, "#1a2230")
        rrect(c, -50, -290, 100, 40, 10, "#ffffff"); txt(c, "TAXI", 0, -260, "#11131a", 28, True)
        for k in range(10): rect(c, -300 + k * 60, -105, 30, 14, "#11131a" if k % 2 == 0 else "#f2c230")
        for wx in (-180, 180): circ(c, wx, -40, 52, "#141414"); circ(c, wx, -40, 22, "#7d7d7d")
        rect(c, -306, -130, 18, 24, "#fff2c0")
    scaled(c, x, y, s, f)

def money_burst(c, x, y, t, t0, n=10):
    if t < t0: return
    p = t - t0; rr = random.Random(9)
    for k in range(n):
        ang = rr.uniform(-2.6, -0.5); sp = rr.uniform(300, 600)
        bx = x + math.cos(ang) * sp * p; by = y + math.sin(ang) * sp * p + 500 * p * p
        a = clamp(1 - (p - 1.0) / 0.6)
        if a <= 0: continue
        c.save(); c.translate(bx, by); c.rotate(p * 3 + k)
        rect(c, -40, -22, 80, 44, hx("#3fae5a", a)); rect(c, -32, -14, 64, 28, hx("#6fd08a", a)); txt(c, "$", 0, 10, hx("#1f6a3a", a), 26, True)
        c.restore()

def clock_tag(c, x, y, s_, a=1.0, dark=True):
    tag(c, x, y, s_, "#1a1d2a" if dark else "#ffffff", "#ffffff" if dark else "#11131a", 32, a)

def check(c, x, y, r, a=1.0):
    circ(c, x, y, r, hx("#2fbf5a", a)); line(c, [(x - r * 0.45, y), (x - r * 0.1, y + r * 0.35), (x + r * 0.5, y - r * 0.35)], hx("#ffffff", a), r * 0.22)

def room_night(c, t):
    vgrad(c, 0, 0, P, P, "#2c3350", "#1b2036")
    rect(c, 0, 800, P, 280, "#3a2c2a")
    rect(c, 90, 140, 260, 260, "#0c1124"); c.new_path(); c.rectangle(90, 140, 260, 260); c.set_line_width(16); src(c, "#4a3a38"); c.stroke()
    line(c, [(220, 140), (220, 400)], "#4a3a38", 8, cap=False)
    circ(c, 290, 200, 24, "#f4efd0"); circ(c, 280, 194, 22, "#0c1124")
    for k in range(6): circ(c, 120 + k * 37, 330 - (k % 2) * 60, 2.5, "#ffffff")
    rect(c, 820, 180, 130, 170, "#f4f1e8"); rect(c, 820, 180, 130, 40, "#d0241c")
    for k in range(4):
        for j in range(3): rect(c, 836 + k * 28, 236 + j * 34, 18, 20, hx("#999", 0.6))
    glow(c, 540, 600, 520, "#5fb4ff", 0.12)

"""Monstruos con más miedo: ojos negros con pupila que brilla, sonrisas con dientes afilados,
piel agrietada, sombras duras y temblores. Se usan en cualquier escena: monstruo(c, x, y, escala, t)."""
import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect, circ, ell, poly, line, glow

def _twitch(t, seed=0, amp=1.0):
    # tic nervioso: quieto casi siempre, sacudidas cortas de vez en cuando
    ph = (t * 0.7 + seed * 0.37) % 1.0
    if ph < 0.08:
        r = random.Random(int(t * 30) + seed)
        return r.uniform(-1, 1) * 10 * amp, r.uniform(-1, 1) * 6 * amp, r.uniform(-1, 1) * 0.06 * amp
    return 0.0, 0.0, 0.0

def _radial(c, x, y, r0, r1, stops):
    g = cairo.RadialGradient(x, y, r0, x, y, r1)
    for o, col in stops: g.add_color_stop_rgba(o, *hx(col) if isinstance(col, str) else col)
    return g

def _skull_head(c, w, h, skin, dark):
    """Cabeza alargada con mejillas hundidas y luz desde abajo."""
    c.new_path(); c.move_to(0, -h)
    c.curve_to(w * 1.05, -h, w * 1.1, -h * 0.1, w * 0.62, h * 0.55)
    c.curve_to(w * 0.4, h * 0.95, -w * 0.4, h * 0.95, -w * 0.62, h * 0.55)
    c.curve_to(-w * 1.1, -h * 0.1, -w * 1.05, -h, 0, -h); c.close_path()
    c.set_source(_radial(c, 0, h * 0.3, 10, h * 1.3, [(0, skin), (0.7, dark), (1, "#000000")])); c.fill_preserve()
    c.set_line_width(6); src(c, "#000000"); c.stroke()
    for sx in (-1, 1):   # mejillas hundidas
        ell(c, sx * w * 0.55, h * 0.18, w * 0.22, h * 0.28, hx("#000000", 0.35))

def _eyes(c, w, h, t, glow_col="#ff2a1a", look=(0, 0), size=1.0, blink_never=True):
    for sx in (-1, 1):
        ex, ey = sx * w * 0.38, -h * 0.18
        ell(c, ex, ey, w * 0.26 * size, h * 0.2 * size, "#000000")            # cuenca negra
        ell(c, ex, ey + 4, w * 0.2 * size, h * 0.15 * size, "#050000")
        px, py = ex + look[0] * 10, ey + look[1] * 8
        glow(c, px, py, 70 * size, glow_col, 0.55 + 0.25 * math.sin(t * 5))
        circ(c, px, py, 7 * size, glow_col); circ(c, px, py, 3 * size, "#ffffff")

def _grin(c, w, h, t, open_=0.3, teeth=18, lip="#3a0000", stretch=1.0):
    y0 = h * 0.38; ww = w * 0.75 * stretch; op = h * (0.08 + 0.3 * open_)
    c.new_path(); c.move_to(-ww, y0 - h * 0.12)
    c.curve_to(-ww * 0.5, y0 + op * 1.6, ww * 0.5, y0 + op * 1.6, ww, y0 - h * 0.12)
    c.curve_to(ww * 0.5, y0 + op * 0.2, -ww * 0.5, y0 + op * 0.2, -ww, y0 - h * 0.12); c.close_path()
    src(c, "#120000"); c.fill_preserve(); c.set_line_width(5); src(c, lip); c.stroke()
    for k in range(teeth):     # dientes de arriba y de abajo, afilados y desiguales
        f = (k + 0.5) / teeth; x = -ww * 0.92 + f * ww * 1.84
        top = y0 - h * 0.12 + (op * 0.2 + h * 0.12) * (1 - (2 * f - 1) ** 2) * 0.9
        bot = y0 - h * 0.12 + (op * 1.6 + h * 0.12) * (1 - (2 * f - 1) ** 2) * 0.75
        lt = 14 + (k * 7 % 5) * 4
        poly(c, [(x - 7, top), (x + 7, top), (x + 1, top + lt)], "#e8e0c8")
        poly(c, [(x - 6, bot), (x + 6, bot), (x - 1, bot - lt * 0.8)], "#d8d0b0")

def _cracks(c, w, h, seed=3, col="#2a0a0a", n=7):
    r = random.Random(seed)
    for _ in range(n):
        x, y = r.uniform(-w * 0.7, w * 0.7), r.uniform(-h * 0.9, h * 0.6); pts = [(x, y)]
        for _ in range(4): x += r.uniform(-30, 30); y += r.uniform(10, 34); pts.append((x, y))
        line(c, pts, hx(col, 0.7), 3)

def _drip(c, x, y, t, col="#5a0000", seed=0):
    d = (t * 25 + seed * 40) % 90
    line(c, [(x, y), (x, y + d)], hx(col, 0.9), 5); circ(c, x, y + d, 6, hx(col, 0.9))

def payaso_malo(c, x, y, s, t, open_=0.4, look=(0, 0)):
    """Payaso: maquillaje agrietado, ojos negros, sonrisa de oreja a oreja con colmillos."""
    dx, dy, rot = _twitch(t, 1)
    c.save(); c.translate(x + dx * s, y + dy * s); c.scale(s, s); c.rotate(rot)
    # cuerpo y gorguera sucia
    poly(c, [(-230, 220), (230, 220), (300, 700), (-300, 700)], "#2a0a2a")
    for k in range(9): circ(c, -200 + k * 50, 230, 42, "#9a9080"); circ(c, -200 + k * 50, 236, 30, hx("#3a2a20", 0.4))
    # pelo enmarañado
    r = random.Random(4)
    for k in range(26):
        a = math.pi * (0.9 + 1.2 * k / 25); rr = 210 + r.uniform(-20, 40)
        circ(c, math.cos(a) * rr * 0.9, -40 + math.sin(a) * rr * 0.75, r.uniform(30, 52), "#6a0a06")
    _skull_head(c, 190, 250, "#e8e4d8", "#7a7468")
    _cracks(c, 190, 250, 5, "#3a3028", 9)
    for sx in (-1, 1):   # rombos corridos que chorrean
        poly(c, [(sx * 72, -150), (sx * 96, -46), (sx * 72, 40), (sx * 48, -46)], hx("#1a1a40", 0.8))
        _drip(c, sx * 72, 40, t, "#1a1a40", 2 + sx)
    _eyes(c, 190, 250, t, "#ffd21a", look)
    circ(c, 0, 10, 34, "#7a0000"); circ(c, -10, 0, 9, hx("#ffffff", 0.35))
    c.new_path(); c.move_to(-200, 60); c.curve_to(-120, 220, 120, 220, 200, 60); c.set_line_width(30); src(c, hx("#8a0000", 0.85)); c.stroke()
    _grin(c, 190, 250, t, open_, teeth=20, lip="#8a0000", stretch=1.15)
    _drip(c, -60, 150, t, "#6a0000", 5); _drip(c, 70, 150, t, "#6a0000", 9)
    c.restore()

def imitadora(c, x, y, s, t, open_=0.6, face_skin="#b08a70"):
    """La que imita: alta, flaca, brazos hasta el piso, cara humana estirada."""
    dx, dy, rot = _twitch(t, 2, 1.4)
    c.save(); c.translate(x + dx * s, y + dy * s); c.scale(s, s)
    sw = math.sin(t * 1.3) * 12
    poly(c, [(-90, 160), (90, 160), (140, 980), (-140, 980)], "#07070a")
    for sx in (-1, 1):
        line(c, [(sx * 80, 200), (sx * (200 + sw), 520), (sx * (230 + sw), 900)], "#07070a", 40)
        for k in range(4): line(c, [(sx * (230 + sw), 900), (sx * (220 + sw + k * 18), 1040)], "#07070a", 9)
    c.rotate(rot - 0.12)          # cabeza ladeada
    c.save(); c.scale(0.8, 1.35); _skull_head(c, 150, 170, face_skin, "#4a3428"); c.restore()
    _eyes(c, 120, 200, t, "#f4f4ec", (0, 0), 0.9)
    _grin(c, 120, 260, t, open_, teeth=22, lip="#2a0000", stretch=1.5)
    c.restore()

def sombra(c, x, y, s, t, eyes=1.0, smile=0.0):
    """Silueta en la oscuridad: solo se ven los ojos y, a veces, la sonrisa."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source(_radial(c, 0, 0, 40, 520, [(0, "#000000"), (0.6, (0, 0, 0, 0.85)), (1, (0, 0, 0, 0))])); c.paint_with_alpha(0.9)
    poly(c, [(-120, -260), (120, -260), (200, 700), (-200, 700)], "#000000")
    circ(c, 0, -330, 120, "#000000")
    if eyes:
        for sx in (-1, 1):
            glow(c, sx * 42, -370, 90, "#ff2a1a", 0.7 * eyes); circ(c, sx * 42, -370, 12, hx("#ff3a2a", eyes)); circ(c, sx * 42, -370, 5, hx("#ffffff", eyes))
    if smile:
        c.save(); c.translate(0, -330); _grin(c, 110, 160, t, 0.2 * smile, teeth=16, lip="#000000"); c.restore()
    c.restore()

def cara_ventana(c, x, y, s, t, hands=True):
    """Cara pálida pegada al vidrio, ojos enormes y manos de dedos largos."""
    c.save(); c.translate(x, y); c.scale(s, s)
    _skull_head(c, 170, 210, "#c8c4b8", "#5a5650")
    _cracks(c, 170, 210, 8, "#3a3a3a", 5)
    for sx in (-1, 1):
        ell(c, sx * 66, -40, 52, 64, "#000000"); circ(c, sx * 66 + math.sin(t * 0.8) * 6, -40, 8, "#f4f4ec")
    _grin(c, 170, 210, t, 0.15, teeth=14, lip="#2a2a2a", stretch=0.9)
    if hands:
        for sx in (-1, 1):
            hx0 = sx * 260
            ell(c, hx0, 60, 70, 90, "#b8b4a8")
            for k in range(4): line(c, [(hx0 + (k - 1.5) * 34, 0), (hx0 + (k - 1.5) * 44, -200)], "#b8b4a8", 22)
    c.restore()

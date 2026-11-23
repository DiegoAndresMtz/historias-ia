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

def _veins(c, w, h, seed=11, col="#2a0a3a", n=6):
    """Venas oscuras que salen de los ojos y del cuello."""
    r = random.Random(seed)
    for k in range(n):
        sx = -1 if k % 2 else 1
        x, y = sx * w * 0.38 + r.uniform(-10, 10), -h * 0.05; pts = [(x, y)]
        for _ in range(5): x += sx * r.uniform(4, 22); y += r.uniform(12, 30); pts.append((x, y))
        line(c, pts, hx(col, 0.75), 4)
        bx, by = pts[2]; line(c, [(bx, by), (bx + sx * 26, by + 8), (bx + sx * 40, by + 26)], hx(col, 0.55), 3)

def infectado(c, x, y, s, t, open_=0.45, look=(0, 0), hair="long", hair_col="#1a1210", shirt="#5a4a6a",
              cap_col="#2a3048", bite=True, arm_up=0.0, seed=3, skin="#9aa58a"):
    """Infectado/a: piel gris verdosa agrietada, venas negras, cuencas negras con pupila amarilla que brilla,
    boca rasgada con dientes afilados, mordida que sangra en el cuello y tic nervioso."""
    dx, dy, rot = _twitch(t, seed, 1.5)
    c.save(); c.translate(x + dx * s, y + dy * s); c.scale(s, s); c.rotate(rot)
    # cuerpo con camisa rota
    poly(c, [(-220, 210), (220, 210), (290, 700), (-290, 700)], shirt)
    poly(c, [(-220, 210), (-60, 210), (-120, 420)], hx("#000", 0.25))
    for k in range(5): poly(c, [(-180 + k * 80, 700), (-150 + k * 80, 610), (-120 + k * 80, 700)], hx("#000", 0.35))
    for k in range(6): ell(c, -150 + k * 60, 300 + (k % 3) * 90, 14, 22, hx("#4a0000", 0.55))   # manchas de sangre
    if arm_up:
        a = arm_up
        line(c, [(200, 260), (300, 260 - 220 * a), (330, 200 - 520 * a)], shirt, 70)
        cx_, cy_ = 330, 200 - 520 * a
        circ(c, cx_, cy_, 40, skin)
        line(c, [(cx_, cy_), (cx_ + 8, cy_ - 110)], skin, 18)            # dedo que señala
        for k in range(3): line(c, [(cx_ - 30 + k * 14, cy_ + 10), (cx_ - 40 + k * 18, cy_ - 40)], skin, 14)
    # cuello con mordida
    rect(c, -60, 160, 120, 90, skin)
    if bite:
        ell(c, 34, 200, 40, 26, "#3a0008"); ell(c, 34, 200, 26, 14, "#7a0010")
        for k in range(5): circ(c, 6 + k * 14, 186 + (k % 2) * 26, 4, "#1a0004")
        _drip(c, 30, 220, t, "#7a0010", seed); _drip(c, 52, 216, t + 0.4, "#7a0010", seed + 2)
    # pelo de atrás
    if hair == "long":
        r = random.Random(seed)
        for k in range(30):
            xx = -200 + k * 14 + r.uniform(-6, 6)
            line(c, [(xx * 0.8, -200), (xx * 1.05, 40), (xx * 1.15 + r.uniform(-20, 20), 300 + r.uniform(-40, 80))], hair_col, 16)
    _skull_head(c, 175, 235, skin, "#3a4430")
    _cracks(c, 175, 235, seed + 4, "#2a0a0a", 10)
    _veins(c, 175, 235, seed + 7)
    if hair == "long":
        c.new_path(); c.arc(0, -150, 170, math.pi * 1.05, math.pi * 1.95); c.close_path(); fill(c, hair_col)
        r = random.Random(seed + 1)
        for k in range(9):   # mechones mojados sobre la cara
            xx = -150 + k * 37
            line(c, [(xx, -190), (xx + r.uniform(-10, 10), -60 + r.uniform(0, 70))], hair_col, 18)
    elif hair == "cap":
        c.new_path(); c.arc(0, -150, 172, math.pi * 1.02, math.pi * 1.98); c.close_path(); fill(c, cap_col)
        ell(c, 90, -168, 150, 26, hx("#000", 0.3)); ell(c, 90, -174, 150, 26, cap_col)
        for sx in (-1, 1): rect(c, sx * 150 - 15, -150, 30, 60, "#bdb8b2")   # canas
    _eyes(c, 175, 235, t, "#d8ff2a", look, 1.05)
    _grin(c, 175, 235, t, open_, teeth=20, lip="#5a0010", stretch=1.25)
    for sx in (-1, 1):   # comisuras rasgadas
        line(c, [(sx * 175 * 0.95, 235 * 0.24), (sx * 175 * 1.1, 235 * 0.16)], "#3a0008", 6)
    _drip(c, -40, 150, t, "#6a0010", seed + 5); _drip(c, 60, 160, t + 0.7, "#6a0010", seed + 9)
    c.restore()

def bebe_infectado(c, x, y, s, t, open_=0.5, hand=True):
    """Bebé infectado asomado en la oscuridad: cabeza grande y calva, piel agrietada,
    cuencas negras con pupila que brilla y una boca de dientes afilados. Mano chiquita de dedos largos."""
    dx, dy, rot = _twitch(t, 7, 1.8)
    c.save(); c.translate(x + dx * s, y + dy * s); c.scale(s, s); c.rotate(rot + 0.18)
    _skull_head(c, 160, 170, "#a0a890", "#3a4032")
    _cracks(c, 160, 170, 21, "#2a0a0a", 9)
    _veins(c, 160, 170, 23, n=4)
    _eyes(c, 160, 190, t, "#d8ff2a", (0.4, 0.3), 1.15)
    _grin(c, 140, 200, t, open_, teeth=14, lip="#5a0010", stretch=1.2)
    c.restore()
    if hand:
        c.save(); c.translate(x + 220 * s, y + 160 * s); c.scale(s, s)
        ell(c, 0, 0, 46, 38, "#a0a890")
        for k in range(4): line(c, [(-30 + k * 20, -10), (-50 + k * 30, -90 - (k % 2) * 16)], "#a0a890", 14)
        for k in range(4): circ(c, -50 + k * 30, -92 - (k % 2) * 16, 6, "#2a1a10")    # uñas negras
        _cracks(c, 40, 30, 31, "#2a0a0a", 3)
        c.restore()

def pasajero(c, x, y, s, t, open_=0.45, look=(0, 0), bend=0.0, arms=0.0, beanie=False, body=True, seed=13):
    """El Pasajero: altísimo y flaco, piel gris de papel mojado y agrietada, cuello largo que se dobla,
    cuencas negras con pupila celeste que brilla, sonrisa de oreja a oreja con dientes afilados,
    dedos larguísimos y tic nervioso. (x, y) = centro de la cabeza; el cuerpo baja ~1100 px.
    bend: ladea la cabeza (radianes). arms: 0 brazos colgando, 1 manos arriba, cerca de la cara."""
    dx, dy, rot = _twitch(t, seed, 1.6)
    skin, dark = "#a7aca6", "#3c423c"
    c.save(); c.translate(x + dx * s, y + dy * s); c.scale(s, s)
    sw = math.sin(t * 1.1) * 10
    if body:
        # torso esquelético con costillas
        line(c, [(0, 150), (0, 330)], skin, 70)                                   # cuello largo
        poly(c, [(-150, 320), (150, 320), (110, 900), (-110, 900)], "#0a0b0c")
        poly(c, [(-130, 330), (130, 330), (96, 760), (-96, 760)], hx(skin, 0.95))
        for k in range(6):
            yy = 400 + k * 52
            c.new_path(); c.move_to(-110 + k * 4, yy); c.curve_to(-40, yy + 26, 40, yy + 26, 110 - k * 4, yy)
            c.set_line_width(9); src(c, hx(dark, 0.8)); c.stroke()
        line(c, [(0, 340), (0, 740)], hx(dark, 0.6), 8)
        c.save(); c.translate(0, 560); _cracks(c, 90, 170, seed + 2, "#2a1a1a", 6); c.restore()
        for sx in (-1, 1):
            if arms > 0:
                hx_, hy_ = sx * (150 + 40 * (1 - arms)), 120 - 260 * arms
                line(c, [(sx * 130, 350), (sx * (260 + sw * 0.3), 330 - 80 * arms), (hx_ + sx * 30, hy_ + 40)], skin, 34)
                bx, by = hx_ + sx * 30, hy_ + 40
            else:
                line(c, [(sx * 130, 350), (sx * (220 + sw), 680), (sx * (250 + sw), 1040)], skin, 34)
                bx, by = sx * (250 + sw), 1040
            ell(c, bx, by, 34, 40, skin)
            base = -math.pi / 2 if arms > 0 else math.pi / 2
            for k in range(4):   # dedos larguísimos con uñas negras
                ang = base + (-0.45 + k * 0.3) * sx
                fx_, fy_ = bx + math.cos(ang) * 200, by + math.sin(ang) * 200
                mx_, my_ = bx + math.cos(ang + 0.25 * sx) * 105, by + math.sin(ang + 0.25 * sx) * 105
                line(c, [(bx, by), (mx_, my_), (fx_, fy_)], skin, 12)
                circ(c, fx_, fy_, 7, "#120a0a")
    c.rotate(rot + bend)
    _skull_head(c, 150, 215, skin, dark)
    _cracks(c, 95, 150, seed, "#2a1414", 9)
    _veins(c, 150, 215, seed + 5, "#1a1428", 6)
    _eyes(c, 150, 215, t, "#9af0ff", look, 1.3)
    _grin(c, 150, 215, t, open_, teeth=24, lip="#4a0a10", stretch=1.35)
    for sx in (-1, 1):   # comisuras rasgadas hasta las orejas
        line(c, [(sx * 150 * 1.0, 215 * 0.26), (sx * 150 * 1.22, 215 * 0.02)], "#3a0008", 7)
    _drip(c, -50, 180, t, "#5a0010", seed + 1); _drip(c, 70, 190, t + 0.6, "#5a0010", seed + 3)
    if beanie:   # tu gorro naranja, robado
        c.new_path(); c.arc(0, -150, 150, math.pi, 2 * math.pi); c.close_path(); fill(c, "#e8702a")
        rrect(c, -158, -178, 316, 52, 22, "#c95a1c"); circ(c, 0, -306, 26, "#f2a15a")
    c.restore()

def pasajero_gatea(c, x, y, s, t, open_=0.6, seed=17):
    """El Pasajero corriendo en cuatro patas: cuerpo bajo y estirado, extremidades de araña."""
    dx, dy, rot = _twitch(t, seed, 1.2)
    skin = "#a7aca6"
    c.save(); c.translate(x + dx * s, y + dy * s); c.scale(s, s)
    ph = t * 14
    ell(c, 0, 0, 260, 70, skin); ell(c, 0, 20, 220, 40, hx("#3c423c", 0.5))
    for k in range(4):   # patas de araña
        bx = -200 + k * 130; up = math.sin(ph + k * 1.7)
        kx, ky = bx - 70 + 40 * up, -120 - 30 * up
        fx_ = bx + 50 + 60 * up
        line(c, [(bx, 0), (kx, ky), (fx_, 190)], skin, 26)
        for j in range(3): line(c, [(fx_, 190), (fx_ + 20 + j * 22, 220)], skin, 8)
    line(c, [(220, -10), (310, -60)], skin, 50)
    c.save(); c.translate(330, -90); c.rotate(0.15 + rot)
    _skull_head(c, 120, 170, skin, "#3c423c")
    _cracks(c, 80, 120, seed, "#2a1414", 7)
    _eyes(c, 120, 170, t, "#9af0ff", (0.6, 0), 1.3)
    _grin(c, 120, 170, t, open_, teeth=18, lip="#4a0a10", stretch=1.35)
    c.restore()
    c.restore()

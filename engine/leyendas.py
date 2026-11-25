"""Leyendas colombianas para la ruleta: un retrato aterrador de cada una (icono) + la ruleta animada.
icono(nombre, c, x, y, s, t) dibuja la cabeza/torso centrados en (x, y) en un círculo de radio ~120*s.
"""
import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect, circ, ell, poly, line, glow, vgrad, ease, clamp, text_w
from monstruos import _skull_head, _eyes, _grin, _cracks, _drip, _twitch

LEYENDAS = ["La Llorona", "El Silbón", "La Patasola", "El Mohán", "La Madremonte", "La Tunda", "El Sombrerón", "El Pollo Maligno"]
COLORES = ["#1d2440", "#2a1430", "#3a1212", "#123024", "#1e3412", "#3a2a08", "#121218", "#3a1a06"]

def _hair_strands(c, w, top, bottom, col, n=22, seed=1, sway=0.0, t=0.0):
    r = random.Random(seed)
    for k in range(n):
        x0 = -w + 2 * w * k / (n - 1)
        pts = [(x0, top)]
        for j in range(1, 6):
            y = top + (bottom - top) * j / 5
            pts.append((x0 * (1 + 0.08 * j) + r.uniform(-8, 8) + math.sin(t * 1.5 + k) * sway * j, y))
        line(c, pts, col, r.uniform(10, 18))

def llorona(c, s, t):
    _hair_strands(c, 150, -260, 260, "#08080a", 26, 2, 3, t)
    _skull_head(c, 120, 170, "#d8dce0", "#6a7080")
    _eyes(c, 120, 170, t, "#dfe8ff", (0, 0.2), 0.9)
    for sx in (-1, 1): line(c, [(sx * 46, -14), (sx * 50, 60), (sx * 44, 120)], hx("#000", 0.85), 9)   # lágrimas negras
    c.save(); c.translate(0, -10); _grin(c, 120, 170, t, 0.9, teeth=10, lip="#000", stretch=0.55); c.restore()
    _hair_strands(c, 120, -240, -40, "#0a0a0c", 9, 5, 2, t)                                               # mechones sobre la cara
    poly(c, [(-140, 170), (140, 170), (200, 300), (-200, 300)], "#e8e8ec")

def silbon(c, s, t):
    poly(c, [(-60, 120), (60, 120), (90, 300), (-90, 300)], "#1a1208")
    c.save(); c.scale(0.8, 1.25); _skull_head(c, 100, 130, "#b8a890", "#3a3020"); c.restore()
    _eyes(c, 90, 170, t, "#ff3a1a", (0, 0), 0.85)
    _grin(c, 90, 200, t, 0.2, teeth=12, lip="#1a0000", stretch=0.8)
    ell(c, 0, -150, 230, 34, "#2a1c0c"); poly(c, [(-90, -150), (90, -150), (70, -260), (-70, -260)], "#2a1c0c")
    rect(c, -90, -175, 180, 18, "#5a3a1a")
    ell(c, 150, 200, 70, 90, "#6a5a3a")                                                                 # el costal de huesos
    for k in range(3): ell(c, 130 + k * 16, 150 + k * 22, 18, 8, "#e8e0c8")

def patasola(c, s, t):
    r = random.Random(7)
    for k in range(30):
        a = math.pi * (0.85 + 1.3 * k / 29); rr = r.uniform(170, 230)
        line(c, [(0, -40), (math.cos(a) * rr, -40 + math.sin(a) * rr * 0.9)], "#160a06", r.uniform(12, 22))
    _skull_head(c, 120, 160, "#8a6a4a", "#2a1a0a")
    _cracks(c, 120, 160, 4, "#1a0a04", 6)
    _eyes(c, 120, 160, t, "#ffb21a", (0, 0), 1.0)
    _grin(c, 120, 170, t, 0.7, teeth=16, lip="#5a0000", stretch=1.1)
    for sx in (-1, 1): poly(c, [(sx * 34, 70), (sx * 22, 70), (sx * 28, 118)], "#f0e8d0")              # colmillos
    _drip(c, -30, 110, t, "#7a0000", 3)

def _tabaco(c, x, y, ang, t, L_=110):
    """Tabaco grueso con la punta encendida y humo."""
    c.save(); c.translate(x, y); c.rotate(ang)
    line(c, [(0, 0), (L_, 0)], "#3a220e", 26); line(c, [(0, -6), (L_, -6)], "#5a3a1a", 8)
    glow(c, L_ + 6, 0, 70, "#ff6a1a", 0.55 + 0.25 * math.sin(t * 5)); circ(c, L_ + 6, 0, 14, "#ff8a2a"); circ(c, L_ + 8, 0, 7, "#fff0c0")
    c.restore()
    for k in range(5):   # humo que sube
        a = (t * 0.35 + k / 5) % 1
        ex = x + math.cos(ang) * (L_ + 6); ey = y + math.sin(ang) * (L_ + 6)
        ell(c, ex + math.sin(t * 1.3 + k) * 30 * a, ey - 40 - 260 * a, 26 + 50 * a, 16 + 30 * a, hx("#c8c8b8", 0.28 * (1 - a)))

def _musgo(c, w, top, bottom, n, seed, t, sway=2.0, cols=("#2a3a1a", "#3a4a22", "#1a2410", "#4a5a2a")):
    r = random.Random(seed)
    for k in range(n):
        x0 = -w + 2 * w * k / max(1, n - 1) + r.uniform(-8, 8)
        pts = [(x0, top + r.uniform(-10, 10))]
        Lb = bottom + r.uniform(-60, 40)
        for j in range(1, 6):
            yy = top + (Lb - top) * j / 5
            pts.append((x0 + r.uniform(-12, 12) + math.sin(t * 1.4 + k * 0.6 + j) * sway * j, yy))
        line(c, pts, r.choice(cols), r.uniform(9, 16))

def mohan(c, s, t, tabaco=True):
    r = random.Random(11)
    for k in range(70):                                                                                 # melena de musgo y bejuco
        a = r.uniform(math.pi * 0.75, math.pi * 2.25); rr = r.uniform(150, 250)
        pts = [(0, -20)]
        for j in range(1, 5): pts.append((math.cos(a) * rr * j / 4 + r.uniform(-12, 12), -20 + math.sin(a) * rr * j / 4 + math.sin(t + k) * 3 * j))
        line(c, pts, r.choice(["#2a3a1a", "#3a4a22", "#1a2410", "#4a3a1a"]), r.uniform(10, 18))
    _skull_head(c, 125, 165, "#6a4a2a", "#1a0e04")
    _cracks(c, 120, 160, 13, "#0a0602", 8)
    for sx in (-1, 1): poly(c, [(sx * 20, -66), (sx * 96, -44), (sx * 92, -30), (sx * 18, -50)], "#0a0602")   # cejas gruesas
    _eyes(c, 120, 160, t, "#ff3a0a", (0, 0.1), 1.0)
    _musgo(c, 120, 50, 280, 30, 5, t, 2.5)                                                              # barba de musgo hasta el pecho
    c.save(); c.translate(0, -14); _grin(c, 115, 175, t, 0.45, teeth=14, lip="#1a0a00", stretch=0.85); c.restore()
    for k in range(4): poly(c, [(-36 + k * 24, 40), (-24 + k * 24, 40), (-30 + k * 24, 66)], "#e8c23a")   # dientes de oro
    for k in range(3): circ(c, -24 + k * 24, 46, 6, "#fff4b0")
    _drip(c, 60, 120, t, "#1a2a3a", 4); _drip(c, -70, 110, t, "#1a2a3a", 5)                            # le escurre agua del río
    if tabaco: _tabaco(c, 50, 50, -0.35, t)

def madremonte(c, s, t):
    r = random.Random(3)
    for k in range(60):
        a = r.uniform(0, 2 * math.pi); rr = r.uniform(60, 230)
        ell(c, math.cos(a) * rr, math.sin(a) * rr * 0.9, r.uniform(20, 40), r.uniform(10, 18), r.choice(["#1e3a12", "#2a4a1a", "#14280c", "#3a5a22"]))
    circ(c, 0, -10, 110, "#0a1206")
    for sx in (-1, 1): glow(c, sx * 44, -30, 70, "#9aff4a", 0.6); circ(c, sx * 44, -30, 12, "#c8ff7a"); circ(c, sx * 44, -30, 5, "#000")
    for k in range(14):
        a = r.uniform(0, 2 * math.pi); ell(c, math.cos(a) * 90, -10 + math.sin(a) * 90, 26, 12, "#2a4a1a")
    c.save(); c.translate(0, 30); _grin(c, 90, 120, t, 0.3, teeth=12, lip="#0a1206", stretch=0.7); c.restore()

def tunda_cara(c, s, t, monster=1.0, busto=True):
    if busto: poly(c, [(-150, 150), (150, 150), (210, 300), (-210, 300)], "#d8a81a")                    # vestido amarillo
    c.save(); c.scale(0.85, 1.25); _skull_head(c, 120, 140, "#5a3a24", "#1a0a04"); c.restore()
    _cracks(c, 110, 170, 9, "#100604", 6)
    _eyes(c, 110, 180, t, "#ffd21a", (0, 0), 0.95)
    _grin(c, 110, 230, t, 0.6, teeth=20, lip="#1a0000", stretch=1.35)
    # pañuelo en la cabeza
    c.new_path(); c.arc(0, -120, 120, math.pi, 2 * math.pi); c.close_path(); fill(c, "#c8301a")
    poly(c, [(90, -150), (170, -190), (150, -120)], "#c8301a")
    for k in range(5): circ(c, -80 + k * 40, -170, 8, "#f0c03a")

def sombreron(c, s, t):
    poly(c, [(-170, 140), (170, 140), (230, 300), (-230, 300)], "#0a0a0e")
    circ(c, 0, 0, 120, "#050508")
    glow(c, 0, 10, 160, "#ff1a1a", 0.25)
    for sx in (-1, 1): glow(c, sx * 40, 10, 60, "#ff2a1a", 0.8); circ(c, sx * 40, 10, 10, "#ff4a2a"); circ(c, sx * 40, 10, 4, "#fff")
    c.save(); c.translate(0, -40); _grin(c, 80, 160, t, 0.15, teeth=12, lip="#000", stretch=0.7); c.restore()
    ell(c, 0, -80, 250, 50, "#000000"); ell(c, 0, -86, 250, 44, "#14141a")
    poly(c, [(-100, -86), (100, -86), (80, -230), (-80, -230)], "#14141a"); rect(c, -100, -110, 200, 20, "#2a2a34")

def pollo_maligno(c, s, t):
    r = random.Random(9)
    for k in range(40):
        a = r.uniform(0, 2 * math.pi); rr = r.uniform(80, 220)
        poly(c, [(0, 20), (math.cos(a) * rr, 20 + math.sin(a) * rr), (math.cos(a + 0.12) * rr * 0.9, 20 + math.sin(a + 0.12) * rr * 0.9)], r.choice(["#3a1a06", "#2a1004", "#4a2208"]))
    circ(c, 0, -20, 120, "#2a1206")
    for k in range(5): poly(c, [(-60 + k * 30, -130), (-45 + k * 30, -200 - (k % 2) * 30), (-30 + k * 30, -130)], "#a01010")  # cresta
    for sx in (-1, 1):
        ell(c, sx * 50, -40, 34, 30, "#f4f0d0"); circ(c, sx * 50, -40, 12, "#000"); glow(c, sx * 50, -40, 50, "#ffcc1a", 0.4)
        line(c, [(sx * 84, -70), (sx * 20, -60)], "#000", 10)
    poly(c, [(-40, 0), (40, 0), (0, 120)], "#c8a020"); poly(c, [(-40, 0), (40, 0), (0, 40)], "#8a6a10")
    for k in range(4): poly(c, [(-28 + k * 18, 6), (-20 + k * 18, 6), (-24 + k * 18, 30)], "#f4f0e0")

ICONOS = {"La Llorona": llorona, "El Silbón": silbon, "La Patasola": patasola, "El Mohán": mohan, "La Madremonte": madremonte,
          "La Tunda": tunda_cara, "El Sombrerón": sombreron, "El Pollo Maligno": pollo_maligno}

def icono(nombre, c, x, y, s, t):
    dx, dy, rot = _twitch(t, LEYENDAS.index(nombre), 0.6)
    c.save(); c.translate(x + dx * s, y + dy * s); c.scale(s, s); c.rotate(rot)
    ICONOS[nombre](c, s, t); c.restore()

# ---------- ruleta ----------
N = len(LEYENDAS); SEG = 2 * math.pi / N
def angulo(t, dur, target, vueltas=5):
    """Ángulo del disco: arranca rápido y frena; al final la porción 'target' queda bajo el puntero (arriba)."""
    final = vueltas * 2 * math.pi + (-(target + 0.5) * SEG)
    p = clamp(t / dur)
    return final * (1 - (1 - p) ** 3)

def ticks(dur, target, fps=200):
    """Tiempos en que el puntero cruza un borde de porción (para el sonido de clic)."""
    out = []; prev = None
    for i in range(int(dur * fps) + 1):
        a = angulo(i / fps, dur, target); k = math.floor(a / SEG)
        if prev is not None and k != prev: out.append(i / fps)
        prev = k
    return out

def ruleta(c, cx, cy, R, t, dur, target, win=0.0):
    a = angulo(t, dur, target)
    glow(c, cx, cy, R * 1.25, "#ff2a1a", 0.18 + 0.3 * win)
    circ(c, cx, cy, R + 26, "#1a0a06"); circ(c, cx, cy, R + 14, "#c9a24a")
    for i, nombre in enumerate(LEYENDAS):
        a0 = -math.pi / 2 + a + i * SEG
        c.new_path(); c.move_to(cx, cy); c.arc(cx, cy, R, a0, a0 + SEG); c.close_path()
        src(c, COLORES[i]); c.fill_preserve(); c.set_line_width(5); src(c, "#c9a24a"); c.stroke()
        c.save(); c.translate(cx, cy); c.rotate(a0 + SEG / 2 + math.pi / 2)
        c.save(); c.rectangle(-R, -R, 2 * R, 2 * R); c.new_path(); c.move_to(0, 0); c.arc(0, 0, R, -math.pi / 2 - SEG / 2, -math.pi / 2 + SEG / 2); c.close_path(); c.clip()
        icono(nombre, c, 0, -R * 0.56, R / 700, t + i)
        c.restore()
        c.select_font_face("Montserrat", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(R * 0.068)
        w = text_w(c, nombre.upper()); c.move_to(-w / 2, -R * 0.86); c.text_path(nombre.upper())
        c.set_line_width(5); src(c, "#000"); c.stroke_preserve(); src(c, "#ffffff"); c.fill()
        c.restore()
    if win > 0:   # resalta la ganadora
        c.save(); c.translate(cx, cy)
        c.new_path(); c.arc(0, 0, R + 4, -math.pi / 2 - SEG / 2, -math.pi / 2 + SEG / 2); c.line_to(0, 0); c.close_path()
        c.set_line_width(14); src(c, hx("#ffd21a", win)); c.stroke(); c.restore()
    circ(c, cx, cy, R * 0.16, "#1a0a06"); circ(c, cx, cy, R * 0.12, "#c9a24a"); circ(c, cx, cy, R * 0.05, "#5a0000")
    poly(c, [(cx - 38, cy - R - 50), (cx + 38, cy - R - 50), (cx, cy - R + 26)], "#e0303a")
    c.new_path(); c.move_to(cx - 38, cy - R - 50); c.line_to(cx + 38, cy - R - 50); c.line_to(cx, cy - R + 26); c.close_path(); c.set_line_width(5); src(c, "#000"); c.stroke()

# ---------- La Tunda de cuerpo entero ----------
def tunda(c, x, y, s, t, cara="monstruo", pierna=1.0, mom_skin="#5a3a24"):
    """Mujer de vestido amarillo y pañuelo rojo; pierna derecha de palo negro (molinillo). y = pies."""
    dx, dy, rot = _twitch(t, 5, 0.8)
    c.save(); c.translate(x + dx * s, y + dy * s); c.scale(s, s)
    sway = math.sin(t * 2.2) * 6
    # piernas: una humana, otra de palo
    rrect(c, -70, -320, 46, 320, 20, mom_skin); ell(c, -48, -6, 40, 14, mom_skin)
    if pierna:
        poly(c, [(22, -340), (64, -340), (54, 0), (32, 0)], "#140c08")
        for k in range(5): ell(c, 43, -300 + k * 62, 30, 12, "#2a1a10")
        ell(c, 43, -4, 26, 22, "#0a0604")
    # vestido
    r = random.Random(2)
    hem = [(-150 + sway + k * 30, -330 + (r.uniform(0, 40) if k % 2 else 0)) for k in range(11)]
    poly(c, hem[::-1] + [(-90, -760), (90, -760)][::-1][::-1] if False else [(-90, -760)] + hem + [(90, -760)], "#d8a81a")
    rect(c, -26, -800, 52, 60, mom_skin)
    for k in range(4): line(c, [(-140 + k * 90 + sway, -330), (-80 + k * 50, -740)], hx("#8a6a0a", 0.5), 6)
    poly(c, [(-150 + sway, -330), (150 + sway, -330), (140 + sway, -300), (-140 + sway, -300)], "#a07a10")
    # brazos largos
    for sx in (-1, 1): line(c, [(sx * 100, -740), (sx * 150, -560), (sx * 140, -380)], mom_skin, 30)
    for sx in (-1, 1):
        for k in range(4): line(c, [(sx * 140, -380), (sx * (130 + k * 12), -320)], mom_skin, 8)
    c.save(); c.translate(0, -930); c.rotate(rot - 0.1)
    if cara == "monstruo": tunda_cara(c, 1, t, busto=False)
    elif cara == "sombra":   # de lejos: cara en sombra, solo dos puntos amarillos
        c.save(); c.scale(0.85, 1.25); circ(c, 0, 0, 125, "#120a06"); c.restore()
        for sx in (-1, 1): glow(c, sx * 38, -20, 50, "#ffd21a", 0.5); circ(c, sx * 38, -20, 7, "#ffe27a")
        c.new_path(); c.arc(0, -120, 120, math.pi, 2 * math.pi); c.close_path(); fill(c, "#c8301a")
        poly(c, [(90, -150), (170, -190), (150, -120)], "#c8301a")
    c.restore(); c.restore()

# ---------- La Llorona de cuerpo entero ----------
def _llorona_hair(c, hy, t, length, parted=0.0, seed=4, cap=True):
    """Pelo negro, largo y mojado. parted=0 tapa la cara; 1 = abierto a los lados (deja ver la cara)."""
    r = random.Random(seed)
    for k in range(34):
        f = k / 33.0; x0 = -88 + 176 * f
        if parted: x0 = (-1 if f < 0.5 else 1) * (92 + 70 * abs(f - 0.5) * 2) * parted + x0 * (1 - parted)
        y0 = hy - 20 - math.sqrt(max(0, 98 ** 2 - min(abs(x0), 97) ** 2)) * 0.85
        pts = [(x0, y0)]
        for j in range(1, 8):
            yy = y0 + (length + hy - y0) * j / 7
            widen = 1 + 0.35 * j / 7
            pts.append((x0 * widen + r.uniform(-7, 7) + math.sin(t * 1.3 + k * 0.7 + j) * 2.5 * j, yy))
        line(c, pts, r.choice(["#050507", "#0b0b10", "#101016"]), r.uniform(9, 15))
    if cap:
        c.new_path(); c.arc(0, hy - 20 - 40 * parted, 98, math.pi, 2 * math.pi); c.close_path(); fill(c, "#07070a")

def llorona_cuerpo(c, x, y, s, t, cara="pelo", brazos="caidos", rodillas=False, bulto=False, glow_a=1.0, alto=1.0):
    """Mujer de blanco, altísima, pelo negro hasta la cintura. y = pies (o rodillas si rodillas=True).
    cara: 'pelo' (tapada, un ojo brilla entre el pelo) | 'calavera' (se abre el pelo) | 'sombra' (lejos, sin detalle)
    brazos: 'caidos' | 'abiertos' | 'lavando' | 'pelo' | 'bulto'"""
    dx, dy, rot = _twitch(t, 0, 0.7)
    c.save(); c.translate(x + dx * s, y + dy * s); c.scale(s, s)
    H = (0.62 if rodillas else 1.0) * alto
    top = -800 * H; sh = top + 40           # hombros
    hy = top - 110                           # centro de la cabeza
    glow(c, 0, (top + 0) / 2, 700 * max(H, 0.7), "#bcd4ff", 0.16 * glow_a)
    sway = math.sin(t * 1.6) * 10
    skin = "#b9c2cc"; skin_d = "#7d8794"
    # vestido blanco, largo y rasgado
    r = random.Random(8)
    hem_w = 260 if rodillas else 190
    hem = []
    for k in range(15):
        f = k / 14.0
        hem.append((-hem_w + 2 * hem_w * f + sway * (0.5 + f), (r.uniform(-10, 34) if k % 2 else r.uniform(-50, -10))))
    body = [(-70, sh), (-110, sh + 140 * H)] + hem + [(110, sh + 140 * H), (70, sh)]
    c.new_path(); c.move_to(*body[0])
    for p in body[1:]: c.line_to(*p)
    c.close_path()
    g = cairo.LinearGradient(0, top, 0, 0); g.add_color_stop_rgba(0, *hx("#f2f4f8")); g.add_color_stop_rgba(0.7, *hx("#d6dce6")); g.add_color_stop_rgba(1, *hx("#9aa6b8", 0.55))
    c.set_source(g); c.fill_preserve(); c.set_line_width(5); src(c, hx("#5a6472", 0.8)); c.stroke()
    for k in range(6):   # manchas de agua y barro
        xx = -120 + k * 48 + sway * 0.4
        line(c, [(xx * 0.5, sh + 60), (xx, -60 + (k % 3) * 20)], hx("#5a6472", 0.35), 6)
    if rodillas:   # la falda empozada en el suelo
        ell(c, 0, 0, 300, 40, hx("#cfd6e0", 0.9)); ell(c, 0, 4, 300, 30, hx("#8a96a8", 0.4))
    # brazos largos y flacos con dedos largos
    def hand(hx_, hy_, ang):
        circ(c, hx_, hy_, 22, skin)
        for k in range(5):
            a = ang + (k - 2) * 0.22; L_ = 70 + (k % 3) * 14
            line(c, [(hx_, hy_), (hx_ + math.cos(a) * L_ * 0.55, hy_ + math.sin(a) * L_ * 0.55), (hx_ + math.cos(a + 0.25) * L_, hy_ + math.sin(a + 0.25) * L_)], skin, 9)
            circ(c, hx_ + math.cos(a + 0.25) * L_, hy_ + math.sin(a + 0.25) * L_, 4, "#2a2a30")
    for sx in (-1, 1):
        sxp = sx * 82
        if brazos == "abiertos":
            pts = [(sxp, sh + 10), (sx * 260, sh - 60), (sx * 470, sh - 150 + math.sin(t * 2 + sx) * 12)]; ang = -0.4 if sx > 0 else math.pi + 0.4
        elif brazos == "lavando":
            pts = [(sxp, sh + 10), (sx * 150, sh + 220 * H), (sx * 60 + math.sin(t * 4 + sx) * 30, sh + 470 * H)]; ang = math.pi / 2
        elif brazos == "pelo":
            pts = [(sxp, sh + 10), (sx * 200, sh - 40), (sx * 120, hy - 30)]; ang = -math.pi / 2 if sx > 0 else -math.pi / 2
        elif brazos == "bulto":
            pts = [(sxp, sh + 10), (sx * 150, sh + 170), (sx * 50, sh + 240)]; ang = math.pi if sx > 0 else 0
        else:
            pts = [(sxp, sh + 10), (sx * 135, sh + 280 * H), (sx * 150, sh + 560 * H)]; ang = math.pi / 2
        line(c, pts, skin_d, 34); line(c, pts, skin, 26)
        hand(pts[-1][0], pts[-1][1], ang)
    # cuello y cabeza
    rect(c, -26, top - 30, 52, 70, skin)
    c.save(); c.translate(0, hy); c.rotate(rot - 0.12)
    if cara == "calavera":
        _llorona_hair(c, 0, t, 420 * H + 200, parted=1.0, cap=False)
        c.save(); c.scale(0.8, 0.8); _skull_head(c, 110, 150, "#d8dce0", "#6a7080")
        _eyes(c, 110, 150, t, "#dfe8ff", (0, 0.2), 0.95)
        for sx in (-1, 1): line(c, [(sx * 42, -14), (sx * 46, 60), (sx * 40, 120)], hx("#000", 0.85), 9)
        c.save(); c.translate(0, -10); _grin(c, 110, 150, t, 0.85, teeth=12, lip="#000", stretch=0.6); c.restore()
        c.restore()
        c.new_path(); c.arc(0, -70, 100, math.pi, 2 * math.pi); c.close_path(); fill(c, "#07070a")
    elif cara == "sombra":
        _llorona_hair(c, 0, t, 420 * H + 200, parted=0.0)
    else:
        c.save(); c.scale(0.8, 0.8); _skull_head(c, 110, 150, "#c8ccd4", "#4a5060"); c.restore()
        _llorona_hair(c, 0, t, 420 * H + 200, parted=0.0)
        # un ojo que brilla entre el pelo
        glow(c, 34, -10, 60, "#dfe8ff", 0.5 + 0.25 * math.sin(t * 4)); circ(c, 34, -10, 7, "#eaf0ff"); circ(c, 34, -10, 3, "#000")
    c.restore()
    if bulto:
        ell(c, 0, sh + 230, 120, 80, "#6a6050")
        for k in range(5): line(c, [(-100 + k * 40, sh + 180), (-80 + k * 40, sh + 290)], hx("#3a3428", 0.7), 6)
        ell(c, -30, sh + 200, 46, 40, "#4a3e30"); circ(c, -38, sh + 196, 6, "#000"); circ(c, -18, sh + 196, 6, "#000")
        for sx in (-1, 1): line(c, [(sx * 150, sh + 170), (sx * 50, sh + 240)], skin, 26)
    c.restore()

# ---------- El Mohán de cuerpo entero ----------
def mohan_cuerpo(c, x, y, s, t, cara="monstruo", brazos="caidos", tabaco=True, glow_a=1.0):
    """Gigante peludo del río: cuerpo cubierto de musgo y bejuco, brazos larguísimos con uñas negras,
    ojos de brasa, dientes de oro y tabaco encendido. y = pies (alto ~ 1000*s).
    cara: 'monstruo' | 'sombra' (lejos: silueta con ojos y brasa)
    brazos: 'caidos' | 'abiertos' | 'tiple' (toca el tiple) | 'agarra' (manos hacia adelante, abajo)"""
    dx, dy, rot = _twitch(t, 3, 0.8)
    c.save(); c.translate(x + dx * s, y + dy * s); c.scale(s, s)
    glow(c, 0, -500, 720, "#ff5a1a", 0.10 * glow_a)
    body = "#1e140a"; hair = ("#2a3a1a", "#3a4a22", "#1a2410", "#4a3a1a")
    # piernas peludas y pies enormes
    for sx in (-1, 1):
        rrect(c, sx * 110 - 50, -300, 100, 300, 40, body)
        ell(c, sx * 120 + sx * 20, -10, 90, 34, "#140c06")
        for k in range(4): poly(c, [(sx * 120 + sx * 70 + k * sx * 0 - 30 + k * 18, -14), (sx * 120 + sx * 70 - 22 + k * 18, -14), (sx * 120 + sx * 70 - 26 + k * 18, 8)], "#000")
    # torso jorobado
    c.new_path(); c.move_to(-230, -300); c.curve_to(-300, -600, -200, -820, 0, -830); c.curve_to(200, -820, 300, -600, 230, -300); c.close_path(); fill(c, body)
    _musgo(c, 250, -800, -240, 40, 21, t, 2.0, hair)
    # brazos
    def arm(pts):
        line(c, pts, "#0e0a04", 74); line(c, pts, body, 62)
        r = random.Random(int(pts[-1][0]))
        for k in range(len(pts) - 1):
            (ax, ay), (bx, by) = pts[k], pts[k + 1]
            for j in range(5):
                f = (j + 0.5) / 5; px, py = ax + (bx - ax) * f, ay + (by - ay) * f
                line(c, [(px, py), (px + r.uniform(-14, 14), py + 50 + r.uniform(0, 40))], r.choice(hair), 10)
    def hand(hx_, hy_, ang):
        ell(c, hx_, hy_, 62, 54, "#2a1a0c")
        for k in range(5):
            a = ang + (k - 2) * 0.3; L_ = 110 + (k % 3) * 24
            mx, my = hx_ + math.cos(a) * L_ * 0.6, hy_ + math.sin(a) * L_ * 0.6
            ex, ey = hx_ + math.cos(a + 0.2) * L_, hy_ + math.sin(a + 0.2) * L_
            line(c, [(hx_, hy_), (mx, my), (ex, ey)], "#2a1a0c", 22)
            poly(c, [(ex - 9, ey - 9), (ex + 9, ey + 9), (ex + math.cos(a + 0.5) * 50, ey + math.sin(a + 0.5) * 50)], "#050302")   # uñas negras
    sh = -720
    if brazos == "tiple":   # tiple de madera viejo
        c.save(); c.translate(20, sh + 300); c.rotate(-0.5)
        ell(c, 0, 0, 120, 90, "#8a5a2a"); ell(c, 0, 0, 108, 78, "#a06a32"); circ(c, 10, 0, 28, "#2a1a0a")
        rect(c, 100, -16, 300, 32, "#5a3a1a"); rect(c, 390, -26, 70, 52, "#3a2210")
        for k in range(4): line(c, [(-60, -12 + k * 8), (460, -12 + k * 8)], hx("#e8e0c8", 0.8), 2)
        c.restore()
    sh = -720
    for sx in (-1, 1):
        if brazos == "abiertos":
            pts = [(sx * 190, sh), (sx * 380, sh - 60), (sx * 560, sh - 200 + math.sin(t * 2 + sx) * 14)]; ang = -0.5 if sx > 0 else math.pi + 0.5
        elif brazos == "tiple":
            pts = [(190, sh), (330, sh + 80), (300, sh + 145)] if sx > 0 else [(-190, sh), (-230, sh + 200), (-10, sh + 300 + math.sin(t * 9) * 12)]
            ang = -math.pi / 2 - 0.4 if sx > 0 else -0.3
        elif brazos == "agarra":
            pts = [(sx * 190, sh), (sx * 300, sh + 260), (sx * 220, sh + 520 + math.sin(t * 3 + sx) * 20)]; ang = math.pi / 2
        else:
            pts = [(sx * 190, sh), (sx * 270, sh + 330), (sx * 250, sh + 660)]; ang = math.pi / 2
        arm(pts); hand(pts[-1][0], pts[-1][1], ang)
    # cabeza
    c.save(); c.translate(0, -930); c.rotate(rot); c.scale(0.95, 0.95)
    if cara == "sombra":
        r = random.Random(11)
        for k in range(60):
            a = r.uniform(math.pi * 0.75, math.pi * 2.25); rr = r.uniform(150, 240)
            line(c, [(0, -20), (math.cos(a) * rr, -20 + math.sin(a) * rr)], "#0e1408", 16)
        c.save(); c.scale(1, 1.3); circ(c, 0, 0, 125, "#0a0804"); c.restore()
        _musgo(c, 110, 60, 260, 22, 5, t, 2.0, ("#0e1408", "#141c0c"))
        for sx in (-1, 1): glow(c, sx * 44, -10, 70, "#ff3a0a", 0.7); circ(c, sx * 44, -10, 10, "#ff7a3a"); circ(c, sx * 44, -10, 4, "#fff")
        if tabaco: _tabaco(c, 50, 50, -0.35, t)
    else:
        mohan(c, 1, t, tabaco)
    c.restore()
    c.restore()

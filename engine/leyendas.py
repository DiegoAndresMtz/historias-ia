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

def _sombrero(c, t, seed=6, col="#2a1c0c", band="#5a3a1a"):
    """Sombrero llanero de ala ancha, viejo y roto (el ala con mordiscos)."""
    r = random.Random(seed)
    pts = []
    for k in range(40):
        a = 2 * math.pi * k / 40; rr = 1.0 - (0.16 if r.random() < 0.18 else r.uniform(0, 0.05))
        pts.append((math.cos(a) * 270 * rr, -150 + math.sin(a) * 44 * rr))
    poly(c, pts, "#140c04"); c.save(); c.translate(0, -6); c.scale(0.97, 0.9); poly(c, pts, col); c.restore()
    poly(c, [(-100, -156), (100, -156), (84, -300), (40, -318), (-30, -312), (-86, -296)], col)
    poly(c, [(-60, -300), (40, -318), (10, -290)], hx("#000", 0.35))                                  # abolladura
    poly(c, [(-100, -156), (100, -156), (96, -186), (-96, -186)], band)
    for k in range(5): line(c, [(-80 + k * 40, -186), (-84 + k * 40, -296)], hx("#000", 0.18), 4)
    poly(c, [(150, -150), (190, -140), (176, -122)], "#000")                                          # roto del ala

def silbon(c, s, t, busto=True, grita=0.0):
    """Cabeza del Silbón: cara larguísima de calavera, cuencas negras con brasa roja, mejillas chupadas,
    boca fruncida de silbar con dientes de aguja (grita>0 la abre en un alarido), pelo tieso y sombrero roto."""
    if busto:
        poly(c, [(-200, 300), (-150, 170), (-40, 140), (40, 140), (150, 170), (200, 300)], "#2e2216")
        for k in range(6): poly(c, [(-190 + k * 70, 300), (-160 + k * 70, 250), (-130 + k * 70, 300)], "#120c06")   # camisa rota
        rect(c, -26, 100, 52, 70, "#7a6a4c"); line(c, [(-14, 104), (-20, 160)], hx("#000", 0.4), 4); line(c, [(14, 104), (20, 160)], hx("#000", 0.4), 4)
        costal(c, 170, 250, 0.5, t)                                                                  # el costal de huesos
    _hair_strands(c, 110, -150, 150, "#0c0a08", 16, 13, 2.5, t)                                     # pelo tieso hasta los hombros
    c.save(); c.scale(0.78, 1.32); _skull_head(c, 105, 130, "#b4a27a", "#2a1e10"); c.restore()
    _cracks(c, 70, 160, 21, "#140a02", 9)
    for sx in (-1, 1):                                                                             # pómulos y mejillas chupadas
        line(c, [(sx * 70, 0), (sx * 40, 60), (sx * 46, 120)], hx("#000", 0.5), 7)
        line(c, [(sx * 64, -20), (sx * 78, 10)], hx("#fff0c0", 0.18), 5)
    g = cairo.LinearGradient(0, -180, 0, 10)                                                       # sombra del sombrero sobre la frente
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92); g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    c.save(); c.scale(0.78, 1.32); c.new_path(); c.arc(0, -40, 110, 0, 2 * math.pi); c.restore(); c.set_source(g); c.fill()
    _eyes(c, 82, 172, t, "#ff2a0a", (0, 0.15), 0.85)
    for sx in (-1, 1): line(c, [(sx * 62, -58), (sx * 12, -40)], "#000", 10)                       # ceño
    poly(c, [(-8, 10), (8, 10), (0, 34)], "#000")                                                  # nariz hundida
    my = 92
    if grita > 0:
        ow, oh = 30 + 26 * grita, 34 + 70 * grita
        ell(c, 0, my + oh * 0.3, ow + 10, oh + 10, "#2a0a04"); ell(c, 0, my + oh * 0.3, ow, oh, "#0a0000")
        for k in range(14):
            a = 2 * math.pi * k / 14; ex, ey = math.cos(a) * ow, my + oh * 0.3 + math.sin(a) * oh
            poly(c, [(ex - math.sin(a) * 6, ey + math.cos(a) * 6), (ex + math.sin(a) * 6, ey - math.cos(a) * 6), (ex * 0.55, my + oh * 0.3 + (ey - my - oh * 0.3) * 0.55)], "#e8dcc0")
    else:
        for k in range(14):                                                                        # labios arrugados, fruncidos
            a = 2 * math.pi * k / 14
            line(c, [(math.cos(a) * 18, my + math.sin(a) * 20), (math.cos(a) * 40, my + math.sin(a) * 40)], hx("#2a1208", 0.85), 4)
        ell(c, 0, my, 30, 30, "#5a2414"); ell(c, 0, my, 16, 18, "#050000")
        for k in range(9):                                                                         # dientes de aguja hacia adentro
            a = 2 * math.pi * k / 9 + 0.3
            poly(c, [(math.cos(a - 0.25) * 17, my + math.sin(a - 0.25) * 18), (math.cos(a + 0.25) * 17, my + math.sin(a + 0.25) * 18), (math.cos(a) * 5, my + math.sin(a) * 5)], "#e8dcc0")
    _drip(c, 34, 150, t, "#4a0000", 2)
    c.save(); c.translate(0, -12); c.scale(0.86, 0.86); _sombrero(c, t); c.restore()

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

def _pluma(c, x, y, ang, L_, w_, col, edge="#5a4a3a"):
    """Pluma desflecada (punta en ang)."""
    ca, sa = math.cos(ang), math.sin(ang); nx, ny = -sa, ca
    pts = [(x + nx * w_, y + ny * w_), (x + ca * L_ * 0.8 + nx * w_ * 0.8, y + sa * L_ * 0.8 + ny * w_ * 0.8),
           (x + ca * L_, y + sa * L_), (x + ca * L_ * 0.8 - nx * w_ * 0.8, y + sa * L_ * 0.8 - ny * w_ * 0.8), (x - nx * w_, y - ny * w_)]
    poly(c, pts, col)
    line(c, [(x, y), (x + ca * L_ * 0.92, y + sa * L_ * 0.92)], hx(edge, 0.55), 3)

def _cresta(c, t, x=0, y=-120, s=1.0):
    """Cresta de gallo roja, carnosa y mojada."""
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = math.sin(t * 3) * 4
    pts = [(-90, 10)]
    for k in range(6):
        cx_ = -75 + k * 30; h = 95 + (k % 2) * 40 + (25 if k in (2, 3) else 0)
        pts += [(cx_ - 12, -h * 0.55), (cx_ + sw * (k / 5), -h), (cx_ + 14, -h * 0.55)]
    pts += [(95, 10)]
    poly(c, pts, "#7a0608")
    c.save(); c.translate(-4, 6); c.scale(0.9, 0.86); poly(c, pts, "#c0121a"); c.restore()
    for k in range(5): ell(c, -60 + k * 30, -50 - (k % 2) * 16, 7, 14, hx("#ff8a8a", 0.45))
    _drip(c, 30, 0, t, "#8a0008", 5)
    c.restore()

def pollo_maligno(c, s, t, busto=True, open_=0.75):
    """Cabeza del Pollo Maligno: orejas de murciélago, cresta de gallo, cuencas negras con pupila amarilla,
    pico ganchudo y boca de colmillos, barbillas rojas y gorguera de plumas de gallinazo."""
    r = random.Random(9)
    if busto:
        for k in range(44):   # gorguera de plumas negras desflecadas
            a = math.pi * (0.05 + 0.9 * k / 43) + r.uniform(-0.05, 0.05)
            _pluma(c, r.uniform(-60, 60), 150, a, r.uniform(110, 190), r.uniform(16, 26), r.choice(["#120a06", "#1e120a", "#0a0604"]))
        poly(c, [(-170, 190), (170, 190), (240, 300), (-240, 300)], "#0e0806")
    for k in range(30):       # plumas erizadas detrás de la cabeza
        a = math.pi * (0.95 + 1.1 * k / 29); rr = r.uniform(190, 250)
        _pluma(c, 0, -10, a, rr, r.uniform(14, 22), r.choice(["#160c06", "#24140a", "#0c0604"]))
    for sx in (-1, 1):        # orejas de murciélago
        tw = math.sin(t * 7 + sx) * 0.04
        c.save(); c.translate(sx * 85, -95); c.rotate(sx * (0.45 + tw))
        poly(c, [(-sx * 40, 30), (sx * 10, -190), (sx * 55, 30)], "#1a0e0c")
        poly(c, [(-sx * 22, 20), (sx * 10, -150), (sx * 38, 20)], "#5a1a1e")
        for k in range(3): line(c, [(sx * 10, -140 + k * 10), (sx * (-10 + k * 18), 20)], hx("#2a0a0a", 0.8), 3)
        c.restore()
    _cresta(c, t, 0, -128, 1.05)
    c.save(); c.scale(1.0, 1.05); _skull_head(c, 125, 150, "#4a3634", "#0c0606"); c.restore()
    for k in range(5): line(c, [(-70 + k * 4, -110 + k * 16), (70 - k * 4, -110 + k * 16)], hx("#000", 0.25), 3)   # arrugas
    _cracks(c, 115, 150, 12, "#0a0202", 7)
    _eyes(c, 125, 150, t, "#ffd21a", (0, 0.3), 1.15)
    for sx in (-1, 1): line(c, [(sx * 92, -70), (sx * 18, -38)], "#000", 12)    # ceño
    # nariz de murciélago (hoja nasal)
    poly(c, [(-26, -10), (0, -48), (26, -10), (14, 18), (-14, 18)], "#2a1a18")
    ell(c, -10, 8, 6, 9, "#000"); ell(c, 10, 8, 6, 9, "#000")
    # boca con colmillos y pico ganchudo encima
    c.save(); c.translate(0, 12); _grin(c, 125, 150, t, open_ + 0.12 * math.sin(t * 5), teeth=18, lip="#3a0000", stretch=0.95); c.restore()
    for sx in (-1, 1): poly(c, [(sx * 40, 62), (sx * 24, 62), (sx * 33, 128)], "#f4ecd0")   # colmillos
    poly(c, [(-34, 20), (34, 20), (10, 74), (0, 96), (-10, 74)], "#b8901a")              # pico ganchudo
    poly(c, [(-20, 24), (6, 24), (-2, 62)], hx("#f0d070", 0.6))
    _drip(c, -36, 120, t, "#7a0000", 3); _drip(c, 44, 112, t, "#7a0000", 8)
    for sx in (-1, 1):        # barbillas rojas colgando
        sw = math.sin(t * 2.5 + sx) * 6
        ell(c, sx * 70 + sw, 150, 26, 44, "#9a0a10"); ell(c, sx * 66 + sw, 140, 10, 18, hx("#ff7a7a", 0.4))

def pollo_cuerpo(c, x, y, s, t, cara="monstruo", alas="plegadas", glow_a=1.0, open_=0.75):
    """El Pollo Maligno de cuerpo entero: pajarraco gigante, alas de buitre, cuello pelado, patas escamosas con garras.
    y = pies (alto ~1300*s). alas: 'plegadas' | 'abiertas' | 'envuelve'. cara: 'monstruo' | 'sombra'."""
    dx, dy, rot = _twitch(t, 7, 0.8)
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, -700, 760, "#ffb21a", 0.08 * glow_a)
    r = random.Random(21)
    # patas escamosas, rodilla hacia atrás, garras plantadas
    for sx in (-1, 1):
        hip = (sx * 90, -430); knee = (sx * 120 + 40, -230); ank = (sx * 110, -40)
        line(c, [hip, knee], "#140a06", 70)
        line(c, [knee, ank], "#7a6a4a", 34)
        for k in range(7):
            f = k / 7; px = knee[0] + (ank[0] - knee[0]) * f; py = knee[1] + (ank[1] - knee[1]) * f
            line(c, [(px - 16, py), (px + 16, py + 4)], hx("#3a2e1a", 0.8), 3)
        for a in (-2.7, -1.9, -0.4) if sx < 0 else (-0.45, -1.25, -2.75):
            pass
        toes = [(-150, 0), (-40, 10), (70, 4)]
        for k, (tx, ty) in enumerate(toes):
            ex = ank[0] + tx * 0.9; ey = ty
            line(c, [ank, (ex, ey)], "#7a6a4a", 22)
            poly(c, [(ex - 10, ey - 10), (ex + 10, ey + 6), (ex + (24 if tx > 0 else -24) + (8 if tx == -40 else 0), ey + 30)], "#050302")
        line(c, [ank, (ank[0] + 50, -20)], "#7a6a4a", 18); poly(c, [(ank[0] + 46, -30), (ank[0] + 58, -14), (ank[0] + 96, -8)], "#050302")   # espolón
    c.translate(dx, 0); c.translate(0, -500); c.rotate(rot * 0.4); c.translate(0, 500)
    # alas detrás del cuerpo (abiertas)
    def ala(sx, spread, flap):
        base = (sx * 150, -820)
        for k in range(16):
            f = k / 15
            ang = (-math.pi / 2 - sx * (0.25 + 1.35 * spread * f)) if sx > 0 else (-math.pi / 2 - sx * (0.25 + 1.35 * spread * f))
            ang = math.pi / 2 - (math.pi / 2 + 0.2 + 1.5 * spread * (1 - f)) * sx * 1.0 if False else ang
            a = -math.pi / 2 + sx * (0.35 + (1.9 * spread + 0.4) * f) + flap * sx
            L_ = 380 + 360 * spread * (1 - abs(f - 0.55)) + r.uniform(-30, 30)
            ox, oy = base[0] + sx * 140 * spread * f, base[1] + 60 * f
            _pluma(c, ox, oy, a, L_, 34 + 8 * spread, r.choice(["#0e0806", "#160c08", "#1a100a"]), "#4a3a2a")
        for k in range(6):
            a = -math.pi / 2 + sx * (0.6 + 1.6 * spread * k / 5) + flap * sx
            line(c, [base, (base[0] + math.cos(a) * 300 * (0.6 + spread * 0.6), base[1] + math.sin(a) * 300 * (0.6 + spread * 0.6))], "#0a0604", 26)
    if alas == "abiertas":
        flap = math.sin(t * 2.2) * 0.12
        for sx in (-1, 1): ala(sx, 1.0, flap)
    # cuerpo de plumas negras, jorobado
    c.new_path(); c.move_to(-200, -420); c.curve_to(-300, -650, -210, -900, -40, -930)
    c.curve_to(150, -930, 300, -700, 220, -420); c.curve_to(120, -360, -110, -360, -200, -420); c.close_path(); fill(c, "#120a06")
    for k in range(70):   # plumaje desflecado
        px = r.uniform(-230, 230); py = r.uniform(-900, -420)
        if (px / 260) ** 2 + ((py + 660) / 280) ** 2 > 1: continue
        _pluma(c, px, py, math.pi / 2 + r.uniform(-0.4, 0.4), r.uniform(50, 90), r.uniform(12, 18), r.choice(["#1a0e08", "#24160c", "#0e0804"]), "#5a4a38")
    if alas in ("plegadas", "envuelve"):
        for sx in (-1, 1):   # alas plegadas como capa, puntas hasta las rodillas
            spread = 0.0 if alas == "plegadas" else 0.25
            for k in range(12):
                f = k / 11
                bx = sx * (170 + 40 * f + 160 * spread); by = -880 + 90 * f
                a = math.pi / 2 - sx * (0.12 + 0.25 * f) + (-sx * 0.9 * spread)
                _pluma(c, bx, by, a, 420 + 120 * f, 36, r.choice(["#0e0806", "#140a06", "#1a100a"]), "#4a3a2a")
    # cuello pelado y arrugado de gallinazo
    line(c, [(0, -880), (10, -980), (0, -1060)], "#3a2420", 92)
    line(c, [(0, -880), (10, -980), (0, -1060)], "#6a4440", 74)
    for k in range(7): line(c, [(-34, -900 - k * 24), (40, -896 - k * 24)], hx("#2a1414", 0.7), 4)
    for k in range(16):  # collar de plumas en la base del cuello
        a = math.pi * (0.0 + k / 15); _pluma(c, math.cos(a) * 90, -880 + 20, math.pi / 2 + (a - math.pi / 2) * 0.6, 90, 18, "#0a0604")
    c.save(); c.translate(0, -1170); c.rotate(rot); c.scale(0.95, 0.95)
    if cara == "sombra":
        for k in range(24):
            a = math.pi * (0.95 + 1.1 * k / 23); _pluma(c, 0, -10, a, r.uniform(180, 240), 18, "#060304")
        for sx in (-1, 1):
            c.save(); c.translate(sx * 85, -95); c.rotate(sx * 0.45); poly(c, [(-sx * 40, 30), (sx * 10, -190), (sx * 55, 30)], "#060304"); c.restore()
        c.save(); c.translate(0, -128); poly(c, [(-90, 10), (-60, -100), (-30, -70), (0, -150), (30, -80), (60, -110), (95, 10)], "#5a0408"); c.restore()
        c.save(); c.scale(1, 1.05); circ(c, 0, 0, 130, "#060304"); c.restore()
        for sx in (-1, 1): glow(c, sx * 48, -26, 80, "#ffd21a", 0.7); circ(c, sx * 48, -26, 10, "#ffe27a"); circ(c, sx * 48, -26, 4, "#fff")
    else:
        pollo_maligno(c, 1, t, busto=False, open_=open_)
    c.restore()
    if alas == "envuelve":   # alas cerrándose hacia adelante (atrapa a alguien)
        for sx in (-1, 1):
            for k in range(9):
                f = k / 8
                _pluma(c, sx * (260 - 40 * f), -860 + 60 * f, math.pi / 2 + sx * (0.5 - 0.2 * f), 520, 40, r.choice(["#0a0604", "#120a06"]), "#3a2a1a")
    c.restore()

ICONOS = {"La Llorona": llorona, "El Silbón": silbon, "La Patasola": patasola, "El Mohán": mohan, "La Madremonte": madremonte,
          "La Tunda": tunda_cara, "El Sombrerón": sombreron, "El Pollo Maligno": pollo_maligno}

def icono(nombre, c, x, y, s, t):
    dx, dy, rot = _twitch(t, LEYENDAS.index(nombre), 0.6)
    c.save(); c.translate(x + dx * s, y); c.scale(s, s); c.translate(0, -400); c.rotate(rot * 0.5); c.translate(0, 400); c.rotate(rot)
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
    c.save(); c.translate(x + dx * s, y); c.scale(s, s); c.translate(0, -400); c.rotate(rot * 0.5); c.translate(0, 400)
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
    c.save(); c.translate(x + dx * s, y); c.scale(s, s); c.translate(0, -400); c.rotate(rot * 0.5); c.translate(0, 400)
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
    c.save(); c.translate(x + dx * s, y); c.scale(s, s); c.translate(0, -400); c.rotate(rot * 0.5); c.translate(0, 400)
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

# ---------- El Silbón de cuerpo entero ----------
def _raices(c, x, y, ang, t, L_=150, n=5, skin="#8a7a58", seed=0):
    """Mano huesuda con dedos larguísimos como raíces y uñas negras."""
    r = random.Random(seed)
    ell(c, x, y, 30, 26, skin)
    for k in range(n):
        a = ang + (k - (n - 1) / 2) * 0.24; pts = [(x, y)]; px, py = x, y
        for j in range(1, 5):
            aa = a + math.sin(t * 2 + k + j) * 0.05 + r.uniform(-0.12, 0.12)
            px += math.cos(aa) * L_ / 4; py += math.sin(aa) * L_ / 4; pts.append((px, py))
        line(c, pts, "#2a2014", 13); line(c, pts, skin, 8)
        for j in (1, 2): circ(c, pts[j][0], pts[j][1], 6, skin)                                         # nudillos
        poly(c, [(px - 5, py - 5), (px + 5, py + 5), (px + math.cos(a) * 26, py + math.sin(a) * 26)], "#050302")

def costal(c, x, y, s, t, mueve=0.0, abierto=False):
    """Costal viejo de fique, con huesos asomados. mueve>0: algo patalea adentro."""
    c.save(); c.translate(x, y); c.scale(s, s)
    k1 = math.sin(t * 7) * 18 * mueve; k2 = math.sin(t * 5.3 + 1) * 22 * mueve
    c.new_path(); c.move_to(-60, -200); c.curve_to(-170 + k1, -120, -180, 120 + k2, -60, 170)
    c.curve_to(20, 200, 150, 180, 160 + k2, 60); c.curve_to(170, -60 + k1, 90, -170, 50, -200); c.close_path()
    src(c, "#6a5634"); c.fill_preserve(); c.set_line_width(7); src(c, "#2a2010"); c.stroke()
    for k in range(9): line(c, [(-140 + k * 34, -120), (-150 + k * 36, 160)], hx("#3a2e18", 0.35), 3)    # tejido
    for k in range(4): line(c, [(-150, -60 + k * 60), (150, -70 + k * 60)], hx("#3a2e18", 0.3), 3)
    if mueve:   # bultos de pies y manos empujando desde adentro
        ell(c, -100 + k1, 40, 34, 40, hx("#8a7448", 0.9)); ell(c, 90, -40 + k2, 30, 44, hx("#8a7448", 0.9))
    if not abierto:
        line(c, [(-60, -200), (50, -200)], "#3a2a14", 16)
        for a, L_ in ((-1.9, 90), (-1.4, 110), (-1.1, 80)):        # huesos asomados
            ex, ey = math.cos(a) * L_, -200 + math.sin(a) * L_
            line(c, [(0, -200), (ex, ey)], "#e2d8bc", 16); circ(c, ex, ey, 13, "#efe6cc"); circ(c, ex + 8, ey + 4, 10, "#efe6cc")
    c.restore()

def silbon_cuerpo(c, x, y, s, t, cara="monstruo", brazos="caidos", con_costal=True, mueve=0.0, bend=0.0, glow_a=1.0, ardor=0.0, mordidas=0.0):
    """El Silbón de cuerpo entero: altísimo (~1850*s), flaquísimo, piernas de palo, pies descalzos plantados,
    pantalón remangado y camisa rota que deja ver costillas, brazos hasta las rodillas con dedos de raíz,
    sombrero roto y el costal de huesos al hombro.
    cara: 'monstruo' | 'sombra' (lejos: silueta y dos brasas) | 'grita'
    brazos: 'caidos' | 'costal' (lo carga al hombro) | 'agarra' (manos hacia adelante) | 'arriba'
    bend: radianes que se dobla el torso desde la cadera (+ adelante/derecha, - hacia atrás).
    ardor: piernas quemadas de ají (0..1). mordidas: marcas de perro en los talones."""
    dx, dy, rot = _twitch(t, 1, 0.8)
    skin, skin_d, cloth, rags = "#8a7a58", "#2a2014", "#3a2c1a", "#4a3a24"
    c.save(); c.translate(x, y); c.scale(s, s)
    glow(c, 0, -900, 900, "#ff3a1a", 0.07 * glow_a)
    # piernas de palo con rodillas nudosas; pies plantados
    for sx in (-1, 1):
        hip, knee, ank = (sx * 58, -820), (sx * 74, -430), (sx * 62, -70)
        line(c, [hip, knee, ank], skin_d, 44); line(c, [hip, knee, ank], skin, 34)
        circ(c, knee[0], knee[1], 30, skin_d); circ(c, knee[0], knee[1], 24, skin)
        line(c, [(knee[0] - 8, knee[1] + 40), (ank[0] - 6, ank[1] - 30)], hx("#000", 0.25), 5)              # canilla
        # pie largo descalzo con dedos huesudos
        poly(c, [(ank[0] - 30, ank[1]), (ank[0] + 24, ank[1] - 10), (ank[0] + sx * 120, -14), (ank[0] + sx * 130, 4), (ank[0] - 40, 4)], skin_d)
        poly(c, [(ank[0] - 24, ank[1] + 4), (ank[0] + 20, ank[1] - 4), (ank[0] + sx * 112, -12), (ank[0] + sx * 118, -2), (ank[0] - 34, -2)], skin)
        for k in range(4):
            tx = ank[0] + sx * (70 + k * 16); line(c, [(tx, -10), (tx + sx * 18, 2)], skin, 9); circ(c, tx + sx * 20, 3, 5, "#050302")
        if mordidas:   # mordidas de los perros de la maldición
            for k in range(4): circ(c, ank[0] - 20 + k * 12, ank[1] + 10 - (k % 2) * 14, 5, hx("#8a0000", mordidas))
            _drip(c, ank[0] - 10, ank[1] + 16, t + sx, hx("#7a0000", mordidas), 3 + sx)
        if ardor:
            for k in range(5): ell(c, knee[0] + (k - 2) * 10, knee[1] + 80 + k * 50, 22, 14, hx("#c8200a", 0.75 * ardor))
            glow(c, knee[0], knee[1] + 160, 160, "#ff5a1a", 0.25 * ardor)
        # pantalón remangado y roto hasta la rodilla
        r = random.Random(30 + sx)
        hem = [(knee[0] + sx * 46, knee[1] + 40)] + [(knee[0] + sx * (46 - j * 23), knee[1] + 40 + r.uniform(-10, 40)) for j in range(1, 5)]
        poly(c, [(sx * 6, -880), (sx * 104, -880)] + hem, cloth)
    c.save(); c.translate(dx, 0)
    c.translate(0, -820); c.rotate(bend + rot * 0.3); c.translate(0, 820)
    sh_y = -1360
    # costal detrás de la espalda
    if con_costal and brazos == "costal":
        costal(c, -150, -1120, 1.05, t, mueve)
    # torso flaco, camisa rota con costillas
    torso = [(-70, -820), (-96, -1000), (-150, sh_y), (150, sh_y), (96, -1000), (70, -820)]
    poly(c, torso, skin)
    for k in range(7):
        yy = -1300 + k * 50; line(c, [(-80 + k * 3, yy), (-20, yy + 18), (20, yy + 18), (80 - k * 3, yy)], hx(skin_d, 0.7), 7)
    r = random.Random(40)
    poly(c, [(-150, sh_y), (-40, sh_y), (-70, -1180), (-110, -1060), (-96, -1000)], rags)               # jirones de camisa
    poly(c, [(150, sh_y), (50, sh_y), (90, -1200), (60, -1080), (96, -1000)], rags)
    poly(c, [(-70, -820), (-96, -1000), (-50, -960), (-20, -1010), (10, -940), (50, -990), (96, -1000), (70, -820)], rags)
    rect(c, -76, -850, 152, 30, "#1a120a"); rect(c, -14, -852, 28, 34, "#6a5a3a")                       # cabuya de cinturón
    # brazos larguísimos
    for sx in (-1, 1):
        shp = (sx * 140, sh_y + 20)
        if brazos == "agarra":
            el, hd, ang = (sx * 190 + 120, sh_y + 300), (sx * 120 + 360, sh_y + 420 + math.sin(t * 3 + sx) * 20), 0.25
        elif brazos == "arriba":
            el, hd, ang = (sx * 290, sh_y - 200), (sx * 330, sh_y - 520 + math.sin(t * 4 + sx) * 20), -math.pi / 2 + sx * 0.3
        elif brazos == "costal" and sx < 0:
            el, hd, ang = (-230, sh_y + 160), (-150, sh_y - 30), -math.pi / 2
        else:
            el, hd, ang = (sx * 190, sh_y + 380), (sx * 200, sh_y + 760 + math.sin(t * 1.4 + sx) * 10), math.pi / 2 + sx * 0.12
        line(c, [shp, el, hd], skin_d, 36); line(c, [shp, el, hd], skin, 27)
        circ(c, el[0], el[1], 18, skin)
        _raices(c, hd[0], hd[1], ang, t, 170, 5, skin, 7 + sx)
        poly(c, [(shp[0] - 40, shp[1] - 30), (shp[0] + 40, shp[1] - 30), (shp[0] + sx * 60, shp[1] + 120)], rags)   # manga rota
    if con_costal and brazos == "costal":
        line(c, [(-150, sh_y - 30), (-150, -1300)], "#3a2a14", 14)                                         # boca del costal en el puño
    # cuello de tendones y cabeza
    rect(c, -26, sh_y - 90, 52, 100, skin)
    for sx in (-1, 1): line(c, [(sx * 16, sh_y - 86), (sx * 22, sh_y + 6)], hx("#000", 0.35), 5)
    c.save(); c.translate(0, sh_y - 200); c.rotate(rot); c.scale(0.92, 0.92)
    if cara == "sombra":
        _hair_strands(c, 110, -150, 150, "#050403", 16, 13, 2.5, t)
        c.save(); c.scale(0.78, 1.32); circ(c, 0, 0, 120, "#060403"); c.restore()
        for sx in (-1, 1): glow(c, sx * 30, -30, 70, "#ff2a0a", 0.75); circ(c, sx * 30, -30, 8, "#ff6a3a"); circ(c, sx * 30, -30, 3, "#fff")
        c.save(); c.translate(0, -12); c.scale(0.86, 0.86); _sombrero(c, t, col="#0a0604", band="#140c06"); c.restore()
    else:
        silbon(c, 1, t, busto=False, grita=(1.0 if cara == "grita" else 0.0))
    c.restore()
    c.restore()
    c.restore()

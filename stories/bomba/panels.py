import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect_path, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp, text_w, mountains
from povlib import *
from scenes import hw, popin, tag2
import monstruos as M

# Estilo clásico («Tu IA te hizo rico»): protagonista de gorro naranja, colores planos
YOU = dict(hat="beanie", skin="#c48a5c", shirt="#b8322a", cap_col="#e8702a")
EFRAIN = dict(hat="cap", skin="#a8704a", shirt="#4a5a7a", cap_col="#2a3048", mustache=True, gray=True)
SOLDADO = dict(hat="cap", skin="#b07a52", shirt="#4a5a32", cap_col="#3a4628")
FOCUS = {}; CAM = {}

def talk_open(base=0.35):
    return base + 0.5 * povlib_talk()

def povlib_talk():
    import povlib
    return povlib.TALK

# ---------------- utilería ----------------
def cobija(c, x, y, s, open_=0.0, stains=0.0, t=0.0):
    def f():
        if open_ < 0.5:
            ell(c, 0, 0, 150, 110, "#e8c23a"); ell(c, -20, -20, 110, 70, "#f4d45a")
            for k in range(4): line(c, [(-120 + k * 60, -60), (-90 + k * 60, 70)], hx("#b8901a", 0.6), 6)
            circ(c, 90, -50, 46, "#e8c23a"); circ(c, 90, -50, 30, hx("#b8901a", 0.35))
        else:
            poly(c, [(-260, -120), (250, -150), (280, 130), (-240, 150)], "#e8c23a")
            poly(c, [(-200, -80), (200, -100), (220, 90), (-190, 110)], "#f4d45a")
            for k in range(6): line(c, [(-220 + k * 80, -130), (-200 + k * 80, 140)], hx("#b8901a", 0.5), 5)
            if stains > 0:
                rr = random.Random(9)
                for k in range(7):
                    if stains * 7 < k: break
                    hx_, hy_ = rr.uniform(-160, 140), rr.uniform(-60, 70); ro = rr.uniform(-0.6, 0.6)
                    c.save(); c.translate(hx_, hy_); c.rotate(ro)
                    ell(c, 0, 0, 16, 12, hx("#8a0010", 0.85))
                    for j in range(4): line(c, [(-9 + j * 6, -6), (-13 + j * 9, -24 - (j % 2) * 5)], hx("#8a0010", 0.85), 5)
                    c.restore()
    scaled(c, x, y, s, f)

def extintor(c, x, y, s):
    def f():
        rrect(c, -40, -160, 80, 260, 30, "#d0241c"); rect(c, -40, -60, 80, 40, "#f4f0e0")
        rect(c, -14, -200, 28, 44, "#333"); line(c, [(10, -190), (70, -200), (90, -150)], "#222", 10)
    scaled(c, x, y, s, f)

def fig(c, x, y, s, t, seed=0, eyes=1.0):
    """Infectado lejano: silueta negra con ojos amarillos y tic."""
    dx, dy, rot = M._twitch(t, seed, 1.0)
    c.save(); c.translate(x + dx * s * 0.4, y); c.scale(s, s); c.rotate(rot * 0.6)
    poly(c, [(-60, -260), (60, -260), (90, 0), (-90, 0)], "#05060a")
    line(c, [(-55, -240), (-90, -120), (-80, -20)], "#05060a", 26); line(c, [(55, -240), (90, -120), (80, -20)], "#05060a", 26)
    circ(c, 0, -320, 62, "#05060a")
    if eyes:
        for sx in (-1, 1):
            glow(c, sx * 22, -326, 40, "#d8ff2a", 0.6 * eyes); circ(c, sx * 22, -326, 7, hx("#d8ff2a", eyes))
    c.restore()

def crowd_pos(n=30):
    """Gente parada en el borde de la luz: a los lados y al fondo, nunca encima de la bomba."""
    rr = random.Random(4); out = []
    for k in range(n):
        side = k % 3
        if side == 0: x = rr.uniform(10, 230); y = rr.uniform(700, 900); s = 0.22 + (y - 700) / 200 * 0.12
        elif side == 1: x = rr.uniform(850, 1070); y = rr.uniform(700, 900); s = 0.22 + (y - 700) / 200 * 0.12
        else: x = rr.uniform(260, 820); y = rr.uniform(655, 680); s = rr.uniform(0.12, 0.16)
        out.append((x, y, s, side == 2))
    return sorted(out, key=lambda p: p[1])

def crowd(c, t, n=30, eyes=1.0, back=0.0, far=None):
    for k, (x, y, s, f) in enumerate(crowd_pos(n)):
        if far is not None and f != far: continue
        x += (x - 540) * back * 1.4; y -= back * 40
        fig(c, x, y, s * (1 - 0.4 * back), t + k * 0.37, k, eyes)

def station_lights(c, t, lights):
    if lights <= 0: return
    rect(c, 140, 300, 800, 60, hx("#e8e4d8", 1.0)); rect(c, 140, 356, 800, 14, "#d0241c")
    for k in range(4): rect(c, 200 + k * 200, 368, 80, 10, hx("#fffbe0", lights))
    glow(c, 540, 520, 560, "#fff4c8", 0.32 * lights)

def bomba_ext(c, t, lights=1.0, people=0, back=0.0, eyes=1.0, woman=None, spark=0.0):
    vgrad(c, 0, 0, P, P, "#03040b", "#141a36")
    for k in range(40):
        rr = random.Random(k); circ(c, rr.uniform(0, P), rr.uniform(0, 400), rr.uniform(1, 2.5), hx("#ffffff", 0.5))
    mountains(c, 640)
    rect(c, 0, 640, P, 440, "#141418")
    poly(c, [(0, 1080), (380, 690), (700, 690), (1080, 1080)], "#202026")
    for k in range(6): rect(c, 530, 720 + k * 60, 20, 30, hx("#e8c23a", 0.5))
    if people: crowd(c, t, people, eyes=eyes, back=back, far=True)
    # poste y cables
    rect(c, 1000, 330, 18, 370, "#2a2420"); rect(c, 960, 350, 100, 12, "#2a2420")
    line(c, [(940, 356), (980, 380), (1010, 356)], "#0a0a0a", 4); line(c, [(1010, 356), (1080, 380)], "#0a0a0a", 4)
    line(c, [(950, 362), (880, 372)], "#0a0a0a", 4)
    # techo y columnas
    rect(c, 230, 370, 26, 330, "#c8c0b0"); rect(c, 824, 370, 26, 330, "#c8c0b0")
    station_lights(c, t, lights)
    if lights <= 0: rect(c, 140, 300, 800, 60, "#3a3a40"); rect(c, 140, 356, 800, 14, "#5a1a1a")
    # surtidores
    for px in (360, 660):
        rrect(c, px, 520, 90, 180, 10, "#d0241c" if lights else "#4a1a1a"); rect(c, px + 14, 540, 62, 40, hx("#bff4ff", 0.9 * lights + 0.1))
    # aviso
    rect(c, 60, 420, 140, 90, "#1c4a2a" if lights else "#10241a"); txt(c, "KM 58", 130, 462, hx("#ffffff", 0.4 + 0.6 * lights), 30, True)
    txt(c, "VÍA AL LLANO", 130, 494, hx("#ffffff", 0.4 + 0.6 * lights), 18, True)
    if woman: woman(c)
    if people: crowd(c, t, people, eyes=eyes, back=back, far=False)
    if spark > 0:
        glow(c, 1000, 356, 300 * spark, "#bfe8ff", 0.9 * spark)
        for k in range(10):
            a = k * 0.63 + t * 3; r = 60 + 120 * spark
            line(c, [(1000, 356), (1000 + math.cos(a) * r, 356 + math.sin(a) * r)], hx("#ffffff", spark), 4)
    if lights < 1: overlay(c, "#000008", 0.55 * (1 - lights))

def store_glass(c, t, lights=1.0, outside=None, cracks=0.0, glass_fx=True, handle=True):
    """Interior: muro de vidrio con la puerta y la noche afuera."""
    vgrad(c, 0, 0, P, P, "#3a3e4a" if lights else "#0a0b10", "#24262e" if lights else "#050508")
    c.save(); c.rectangle(80, 110, 920, 640); c.clip()
    vgrad(c, 80, 110, 920, 640, "#04050c", "#10131f")
    rect(c, 80, 640, 920, 120, "#16161a")
    # surtidor afuera
    rrect(c, 700, 470, 80, 170, 10, "#d0241c" if lights else "#3a1010"); rect(c, 712, 490, 56, 36, hx("#bff4ff", 0.8 * lights + 0.1))
    if lights: glow(c, 740, 330, 420, "#fff4c8", 0.18 * lights); rect(c, 80, 300, 920, 30, hx("#e8e4d8", 0.8 * lights))
    if outside: outside(c)
    c.restore()
    # marcos
    for x0 in (80, 380, 700, 1000): rect(c, x0 - 10, 110, 20, 650, "#9aa0aa" if lights else "#1a1c22")
    rect(c, 70, 100, 940, 20, "#9aa0aa" if lights else "#1a1c22"); rect(c, 70, 750, 940, 20, "#9aa0aa" if lights else "#1a1c22")
    if handle:
        rect(c, 660, 560, 14, 140, "#c8ccd4" if lights else "#2a2c32")
        ui(c, 22); txt(c, "EMPUJE", 620, 730, hx("#d0241c", 0.8), 22, True)
    if glass_fx:
        for k in range(3): line(c, [(160 + k * 340, 160), (240 + k * 340, 300)], hx("#ffffff", 0.08), 18)
    if cracks > 0:
        rr = random.Random(2); cx, cy = 540, 430
        for k in range(14):
            a = k / 14 * 2 * math.pi + rr.uniform(-0.2, 0.2); L = (120 + rr.uniform(0, 260)) * cracks
            pts = [(cx, cy)]
            for j in range(1, 5): pts.append((cx + math.cos(a + rr.uniform(-0.15, 0.15)) * L * j / 4, cy + math.sin(a + rr.uniform(-0.15, 0.15)) * L * j / 4))
            line(c, pts, hx("#dfe8ff", 0.8), 3)
        for r in (60, 130):
            if cracks > r / 200: c.new_path(); c.arc(cx, cy, r * cracks, 0, 2 * math.pi); c.set_line_width(2); src(c, hx("#dfe8ff", 0.5)); c.stroke()

def counter(c, t, lights=1.0, blanket=None):
    rect(c, 0, 830, P, 250, "#7a2a22" if lights else "#1a0a08"); rect(c, 0, 820, P, 26, "#c8b8a0" if lights else "#2a2620")
    rect(c, 760, 740, 180, 90, "#2a2a30"); rect(c, 776, 752, 148, 50, hx("#5fff9a", 0.5 * lights + 0.05))
    if blanket: blanket(c)

def radio(c, x, y, s, t, on=1.0, alert=0.0):
    def f():
        rrect(c, -220, -120, 440, 240, 30, "#3a3a40"); rrect(c, -200, -100, 200, 200, 20, "#222")
        for k in range(7): line(c, [(-190, -80 + k * 26), (-10, -80 + k * 26)], "#444", 6)
        rect(c, 30, -80, 160, 70, hx("#ffb84a", 0.7 * on)); line(c, [(150, -120), (210, -330)], "#555", 8)
        circ(c, 60, 50, 30, "#555"); circ(c, 150, 50, 30, "#555")
        if alert:
            r = 0.5 + 0.5 * math.sin(t * 10); circ(c, 180, -100, 16, hx("#ff2a2a", 0.4 + 0.6 * r)); glow(c, 180, -100, 120, "#ff2a2a", 0.4 * r * alert)
    scaled(c, x, y, s, f)

def bano(c, t, dark=0.0, water=True):
    vgrad(c, 0, 0, P, P, "#b8c4c0", "#8a9894")
    for k in range(12):
        line(c, [(k * 90, 0), (k * 90, 760)], hx("#6a7874", 0.5), 3); line(c, [(0, k * 70), (P, k * 70)], hx("#6a7874", 0.5), 3)
    rect(c, 0, 760, P, 320, "#5a6460")
    rect(c, 560, 180, 300, 240, "#9ab0b8"); rect(c, 576, 196, 268, 208, "#c8dce4"); line(c, [(600, 220), (680, 380)], hx("#ffffff", 0.5), 8)
    rrect(c, 540, 520, 340, 90, 30, "#e8ecee"); rect(c, 690, 470, 20, 60, "#9aa")
    if water:
        for k in range(4): line(c, [(705 + k * 2, 530), (705 + k * 2, 560 + (t * 300 + k * 20) % 30)], hx("#bfe8ff", 0.8), 3)
    rect(c, 680, 610, 60, 160, "#d8dcde")
    glow(c, 540, 120, 400, "#fff8e0", 0.2)
    if dark: overlay(c, "#000008", dark)

def pasillo(c, t, door=0.3, dark=0.0, you=True, ext=True):
    vgrad(c, 0, 0, P, P, "#2a2e3a", "#1a1c24")
    poly(c, [(0, 1080), (420, 640), (660, 640), (1080, 1080)], "#3a3a42")
    for side in (-1, 1):
        for k in range(3):
            x0 = 540 + side * (520 - k * 120); w = 110 - k * 25
            xs = x0 if side < 0 else x0 - w
            rect(c, xs, 260 + k * 90, w, 560 - k * 160, "#1a2a3a")
            rect(c, xs + 8, 270 + k * 90, w - 16, 540 - k * 160, hx("#8fd8ff", 0.35))
            for j in range(5):
                for i in range(2): rect(c, xs + 14 + i * (w - 40) / 2, 300 + k * 90 + j * (100 - k * 30), 14, 40 - k * 8, ("#d0241c", "#3a8a3a", "#e8a02a")[(i + j + k) % 3])
    # puerta del baño al fondo
    rect(c, 470, 400, 140, 240, "#5a4a3a")
    if door > 0: poly(c, [(470, 400), (470 + 140 * (1 - door), 410), (470 + 140 * (1 - door), 630), (470, 640)], "#3a2e24"); rect(c, 470 + 140 * (1 - door), 400, 140 * door, 240, hx("#fff4c8", 0.6))
    rect(c, 478, 360, 124, 30, "#2a6a9a"); txt(c, "BAÑO", 540, 383, "#ffffff", 20, True)
    rect(c, 470, 636, 140, 6, hx("#fff4c8", 0.8))
    if you:
        bust(c, 300, 1220, 0.85, t, "worry", look=(0.6, -0.4), arms="hold", **YOU)
        if ext: extintor(c, 300, 1080, 0.9)
    if dark: overlay(c, "#000008", dark)

def eyes_dark(c, x, y, r, t, a=1.0):
    for sx in (-1, 1):
        glow(c, x + sx * r * 2, y, r * 6, "#d8ff2a", 0.6 * a); circ(c, x + sx * r * 2, y, r, hx("#d8ff2a", a)); circ(c, x + sx * r * 2, y, r * 0.4, hx("#ffffff", a))

def flashlight(c, x, y, ang, t, a=1.0):
    g = cairo.RadialGradient(x, y, 10, x, y, 900)
    g.add_color_stop_rgba(0, 1, 0.98, 0.85, 0.5 * a); g.add_color_stop_rgba(1, 1, 0.98, 0.85, 0)
    c.new_path(); c.move_to(x, y); c.arc(x, y, 900, ang - 0.35, ang + 0.35); c.close_path(); c.set_source(g); c.fill()

def planta(c, t, on=0.0, light=0.0, flash=1.0, cord=0.0):
    vgrad(c, 0, 0, P, P, "#4a4640", "#2a2824")
    rect(c, 0, 760, P, 320, "#3a3632")
    for k in range(3): rrect(c, 80 + k * 90, 640, 70, 120, 10, "#c0402a")
    # planta eléctrica
    vib = math.sin(t * 60) * 3 * on
    c.save(); c.translate(vib, 0)
    rrect(c, 420, 460, 480, 300, 20, "#e8b82a"); rect(c, 440, 480, 220, 180, "#2a2a2a")
    for k in range(6): line(c, [(450, 500 + k * 26), (650, 500 + k * 26)], "#444", 6)
    circ(c, 780, 560, 60, "#3a3a3a"); circ(c, 780, 560, 30, "#5a5a5a")
    rect(c, 680, 680, 200, 40, "#1a1a1a"); txt(c, "PLANTA 5 KVA", 780, 708, "#e8b82a", 22, True)
    rect(c, 860, 470, 20, 20, hx("#3aff6a" if on else "#ff3a2a", 0.9))
    c.restore()
    line(c, [(470, 600), (420 - 160 * cord, 640 + 60 * cord)], "#111", 6); circ(c, 420 - 160 * cord, 640 + 60 * cord, 18, "#111")
    if on:
        for k in range(3):
            a = (t * 1.2 + k / 3) % 1; circ(c, 600 + 30 * k, 440 - 200 * a, 30 + 40 * a, hx("#8a8a8a", 0.35 * (1 - a)))
    if light < 1: overlay(c, "#000006", 0.86 * (1 - light))
    if flash and light < 1: flashlight(c, 200, 1000, -0.6, t, flash)

def mask(c, x, y, s):
    """Máscara antigás sobre la cara de un bust (x, y = mismo origen del bust)."""
    hy = y - 380 * s
    def f():
        ell(c, 0, 50, 120, 100, "#2a2e2a"); circ(c, -54, -6, 40, "#1a1e1a"); circ(c, 54, -6, 40, "#1a1e1a")
        circ(c, -54, -6, 30, hx("#9ad8c8", 0.6)); circ(c, 54, -6, 30, hx("#9ad8c8", 0.6))
        circ(c, 0, 110, 46, "#4a4e4a"); circ(c, 0, 110, 30, "#3a3e3a")
        for k in range(5): line(c, [(-20 + k * 10, 92), (-20 + k * 10, 128)], "#2a2e2a", 3)
        line(c, [(-120, 0), (-150, -10)], "#1a1a1a", 12); line(c, [(120, 0), (150, -10)], "#1a1a1a", 12)
    scaled(c, x, hy, s, f)

def cctv(c, t, stamp, draw, rec=True):
    """Imagen de cámara de seguridad en gris con líneas y hora."""
    rect(c, 0, 0, P, P, "#0a0a0a")
    c.save(); c.rectangle(60, 160, 960, 760); c.clip()
    vgrad(c, 60, 160, 960, 760, "#5a5e5a", "#3a3e3a")
    draw(c)
    for k in range(0, 760, 6): rect(c, 60, 160 + k + (t * 40) % 6, 960, 2, hx("#000", 0.18))
    glow(c, 540, 540, 700, "#000", 0.0)
    c.restore()
    c.new_path(); c.rectangle(60, 160, 960, 760); c.set_line_width(8); src(c, "#222"); c.stroke()
    mono(c, 40); src(c, "#f4f4f4"); c.move_to(90, 890); c.show_text(stamp)
    mono(c, 34); src(c, "#f4f4f4"); c.move_to(780, 890); c.show_text("CAM 02")
    if rec and (t % 1) < 0.6: circ(c, 900, 220, 16, "#ff2a2a"); mono(c, 30); src(c, "#ff2a2a"); c.move_to(924, 230); c.show_text("REC")

def cctv_store(c, t, door=0.0, you=True, crawl=None, blanket=True):
    """Vista en gris desde arriba: puerta, mostrador y tú."""
    rect(c, 60, 160, 960, 260, "#2a2e2a"); rect(c, 400, 180, 240, 230, "#6a6e6a" if door else "#4a4e4a")
    if door: rect(c, 400, 180, 60 * door, 230, "#1a1a1a")
    rect(c, 60, 660, 960, 90, "#6a6a66"); rect(c, 60, 750, 960, 170, "#4a4a46")
    if you:
        circ(c, 470, 560, 46, "#8a8a86"); c.new_path(); c.arc(470, 548, 48, math.pi, 2 * math.pi); fill(c, "#aaa")
        rrect(c, 420, 600, 100, 70, 30, "#7a7a76")
        if blanket: ell(c, 460, 470, 60, 40, "#c8c8b8")
    if crawl is not None:
        x, y = crawl
        ell(c, x, y, 36, 22, "#9a9e96"); circ(c, x + 34, y - 8, 20, "#9a9e96")
        for k in range(4): line(c, [(x - 20 + k * 14, y + 10), (x - 30 + k * 20, y + 30)], "#9a9e96", 6)
        for sx in (-1, 1): glow(c, x + 34 + sx * 8, y - 10, 18, "#ffffff", 0.8); circ(c, x + 34 + sx * 8, y - 10, 4, "#ffffff")

def tienda_you(c, t, mood="worry", look=(0.4, -0.5), arms="none", x=540, s=0.9, **kw):
    bust(c, x, 1260, s, t, mood, look=look, arms=arms, **dict(YOU, **kw))

# ---------------- PARTE 1 ----------------
def woman_glass(x, y, s, t, open_=0.35, bundle=True, arm=0.0, hand=False):
    def f(c):
        M.infectado(c, x, y, s, t, open_=open_, arm_up=arm)
        if bundle: cobija(c, x - 40 * s / 0.4, y + 330 * s / 0.4 * 0.8, s * 1.2)
        if hand:
            def h():
                ell(c, 0, 0, 50, 60, "#9aa58a"); ell(c, 0, 10, 30, 30, hx("#5a0010", 0.5))
                for k in range(4): line(c, [(-30 + k * 20, -30), (-34 + k * 22, -120)], "#9aa58a", 16)
                for k in range(4): line(c, [(-34 + k * 22, -120), (-34 + k * 22, -80)], hx("#7a0010", 0.7), 6)
            scaled(c, x + 330 * s, y + 60 * s, s / 0.42 * 0.55, h)
    return f

def g01(c, t, T, w):
    k = w("golpea")
    hit = sum(math.exp(-((t - (k + i * 0.28)) * 14) ** 2) for i in range(3)) if t > k - 0.2 else 0
    store_glass(c, t, outside=woman_glass(560, 440 + hit * 6, 0.42, t, hand=True))
    counter(c, t)
    tag2(c, 540, 960, "MORDIDA", t, w("mordida"), "#e0303a", "#ffffff")
FOCUS["g01"] = (560, 460)

def g02(c, t, T, w):
    bomba_ext(c, t)
    tag2(c, 820, 420, "3:00 a. m.", t, w("tres"), "#ffffff")
FOCUS["g02"] = (520, 560)

def g03(c, t, T, w):
    rect(c, 0, 0, P, P, "#1c1e26"); rect(c, 0, 760, P, 320, "#4a2a22")
    radio(c, 540, 640, 1.2, t, on=1.0, alert=clamp((t - w("alerta")) / 0.3))
    if t < w("alerta"):
        rr = random.Random(int(t * 20))
        for k in range(30): rect(c, rr.uniform(320, 760), rr.uniform(420, 860), 6, 2, hx("#ffffff", 0.5))
FOCUS["g03"] = (540, 620)

def g04(c, t, T, w):
    rect(c, 0, 0, P, P, "#100608"); glow(c, 540, 540, 600, "#ff2a2a", 0.15 + 0.08 * math.sin(t * 8))
    card(c, 120, 300, 840, 620, 30, "#1a0c0e", 0.4, border="#ff3a3a")
    rect(c, 120, 300, 840, 100, "#c0201a"); txt(c, "ALERTA SANITARIA", 540, 366, "#ffffff", 50, True)
    rows = (("brote", "BROTE EN VILLAVICENCIO"), ("mordido", "NO LE ABRA A NADIE MORDIDO"), ("hora", "EN 1 HORA DEJA DE"), ("persona", "SER PERSONA"))
    for i, (tok, l) in enumerate(rows):
        if t > w(tok) - 0.3: txt(c, l, 540, 490 + i * 100, "#ffd0d0" if i < 2 else "#ff4a4a", 44, True)
FOCUS["g04"] = (540, 600)

def g05(c, t, T, w):
    store_glass(c, t)
    counter(c, t)
    tienda_you(c, t, "worry", look=(-0.2, -0.3), arms="phone")
    tag2(c, 820, 600, "SIN SEÑAL", t, w("señal"), "#e0303a", "#ffffff")
    if t > w("efraín") - 0.3:
        tag2(c, 260, 600, "Don Efraín: se fue 12:00", t, w("efraín"), "#ffc24a", size=32)
FOCUS["g05"] = (540, 640)

def g06(c, t, T, w):
    store_glass(c, t, outside=woman_glass(540, 470, 0.85, t, open_=0.1, bundle=False, hand=True), handle=False)
    for k in range(2):   # lágrimas negras
        line(c, [(470 + k * 140, 430), (470 + k * 140, 430 + min(180, (t * 60) % 220))], hx("#100008", 0.85), 8)
FOCUS["g06"] = (540, 420)
CAM["g06"] = [("negros", 1.45, 540, 400)]

def g07(c, t, T, w):
    import povlib
    store_glass(c, t, outside=woman_glass(540, 460, 0.8, t, open_=0.1 + 0.6 * povlib.TALK, bundle=False), handle=False)
    cobija(c, 520, 900, 1.2)
FOCUS["g07"] = (540, 500)

def g08(c, t, T, w):
    rect(c, 0, 0, P, P, "#0c0e18"); glow(c, 540, 600, 500, "#fff4c8", 0.12)
    cobija(c, 540, 620, 2.6)
    tag2(c, 540, 900, "NO LLORA · NO SE MUEVE", t, w("mueve"), "#ffffff", size=36)
FOCUS["g08"] = (540, 600)

def g09(c, t, T, w):
    a = ease(clamp((t - w("aleja")) / 2.0))
    def out(c_):
        M.infectado(c_, 560 + 220 * a, 470 - 60 * a, 0.36 - 0.16 * a, t, open_=0.2, arm_up=0)
    store_glass(c, t, outside=out)
    cobija(c, 470, 700, 0.8)
    counter(c, t)
FOCUS["g09"] = (500, 620)

def g10(c, t, T, w):
    op = clamp((t - w("rendija")) / 0.5) * (1 - clamp((t - w("golpe") + 0.1) / 0.15))
    store_glass(c, t)
    rect(c, 380, 110, 320, 650, hx("#000", 0.0))
    if op > 0: rect(c, 380, 110, 70 * op, 650, "#05060c")
    if t < w("cierras"): cobija(c, 470, 700, 0.8)
    tienda_you(c, t, "shock" if op > 0 else "worry", look=(-0.4, -0.6), arms="none", x=420, s=0.85)
    if op > 0:
        line(c, [(520, 1000), (480, 820), (390 + 70 * op, 700)], YOU["shirt"], 50); circ(c, 400 + 70 * op, 690, 28, YOU["skin"])
    if t > w("cierras"): cobija(c, 420, 1050, 0.8)
    tag2(c, 760, 860, "¡CLIC!", t, w("seguro"), "#ffffff")
FOCUS["g10"] = (460, 600)

def g11(c, t, T, w):
    dk = clamp((t - w("oscuridad")) / 0.8)
    vgrad(c, 0, 0, P, P, "#05060c", "#141a28")
    glow(c, 540, 700, 600, "#fff4c8", 0.12 * (1 - dk))
    M.infectado(c, 540, 470, 1.05, t, open_=0.2 + 0.6 * ease(clamp((t - w("sonríe")) / 0.6)), look=(0, 0.3))
    overlay(c, "#000", 0.92 * dk)
    if dk > 0: eyes_dark(c, 540, 420, 10 * (1 - 0.4 * dk), t, 1 - 0.6 * dk)
FOCUS["g11"] = (540, 520)
CAM["g11"] = [("dientes", 1.4, 540, 560)]

def g12(c, t, T, w):
    rect(c, 0, 0, P, P, "#2a2a30"); rect(c, 0, 700, P, 380, "#7a2a22"); rect(c, 0, 690, P, 20, "#c8b8a0")
    op = clamp((t - w("destapas")) / 0.6)
    cobija(c, 540, 760, 1.6, open_=op)
    bust(c, 540, 1180, 0.7, t, "shock" if t > w("vacía") else "worry", look=(0, 0.8), arms="hold", **YOU)
    tag2(c, 540, 420, "VACÍA", t, w("vacía"), "#e0303a", "#ffffff", size=56)
FOCUS["g12"] = (540, 700)

def g13(c, t, T, w):
    rect(c, 0, 0, P, P, "#2a2a30")
    cobija(c, 540, 580, 2.2, open_=1.0, stains=clamp((t - w("sangre") + 0.2) / 1.2))
    if t > w("tibia") - 0.2:
        for k in range(3):
            a = (t * 0.6 + k / 3) % 1; line(c, [(420 + k * 120, 480 - 120 * a), (440 + k * 120, 420 - 120 * a)], hx("#ffb080", 0.5 * (1 - a)), 8)
FOCUS["g13"] = (540, 580)
CAM["g13"] = [("deditos", 1.5, 520, 580)]

def g14(c, t, T, w):
    pasillo(c, t, door=0.0, dark=0.2, ext=False)
    if t > w("agua") - 0.2:
        for k in range(3):
            a = (t * 0.8 + k / 3) % 1; txt(c, "shhh", 640 + k * 40, 600 - 140 * a, hx("#bfe8ff", 1 - a), 34, True)
FOCUS["g14"] = (540, 520)
CAM["g14"] = [("baño", 1.5, 540, 520)]

def g15(c, t, T, w):
    pasillo(c, 0.0, door=0.0, dark=0.6, you=False)

# ---------------- PARTE 2 ----------------
def h01(c, t, T, w):
    rect(c, 0, 0, P, P, "#2a2a30"); rect(c, 0, 700, P, 380, "#7a2a22"); rect(c, 0, 690, P, 20, "#c8b8a0")
    cobija(c, 540, 600, 1.4, open_=1.0, stains=1.0)
    if t > w("baño") - 0.2:
        for k in range(3):
            a = (t * 0.8 + k / 3) % 1; txt(c, "shhh", 820 + k * 30, 500 - 140 * a, hx("#bfe8ff", 1 - a), 34, True)
FOCUS["h01"] = (540, 600)

def h02(c, t, T, w):
    pasillo(c, t, door=0.25 if t > w("entreabierta") - 0.3 else 0.0, dark=0.15)
    tag2(c, 300, 760, "EXTINTOR", t, w("extintor"), "#ffc24a")
FOCUS["h02"] = (500, 560)

def efrain_sit(c, t, mood="worry", talk=0.0, sweat=0.5, wash=True):
    bano(c, t)
    bust(c, 360, 1160, 0.9, t, mood, look=(0.6, 0.3), talk=talk, sweat=sweat, arms="hold" if wash else "none", **EFRAIN)
    # mano mordida
    ell(c, 420, 1040, 54, 40, EFRAIN["skin"]); ell(c, 430, 1030, 36, 22, "#5a1a5a"); ell(c, 430, 1030, 22, 12, "#8a1020")

def h03(c, t, T, w):
    efrain_sit(c, t)
    tag2(c, 700, 860, "MORDIDA", t, w("mordida"), "#e0303a", "#ffffff")
FOCUS["h03"] = (420, 760)
CAM["h03"] = [("mordida", 1.5, 440, 860)]

def h04(c, t, T, w):
    bano(c, t)
    bust(c, 540, 1100, 1.1, t, "worry", look=(0.3, 0), talk="auto", sweat=1.0, **EFRAIN)
FOCUS["h04"] = (540, 600)

def h05(c, t, T, w):
    efrain_sit(c, t, "sad")
    tag2(c, 780, 400, "3 HORAS", t, w("tres"), "#e0303a", "#ffffff")
    tag2(c, 780, 500, "1 HORA = FIN", t, w("persona"), "#ffc24a")
FOCUS["h05"] = (500, 640)

def h06(c, t, T, w):
    bano(c, t, dark=0.35)
    k = w("negros")
    if t < k - 0.15:
        bust(c, 540, 1100, 1.1, t, "sad", look=(0, -0.2), sweat=1.0, **EFRAIN)
    else:
        M.infectado(c, 540, 470, 0.95, t, open_=0.15, hair="cap", shirt=EFRAIN["shirt"], bite=False, seed=5)
FOCUS["h06"] = (540, 460)
CAM["h06"] = [("lucecita", 1.5, 540, 420)]

def h07(c, t, T, w):
    import povlib
    bano(c, t, dark=0.5)
    M.infectado(c, 540, 500, 1.1, t, open_=0.2 + 0.7 * povlib.TALK, hair="cap", shirt=EFRAIN["shirt"], bite=False, seed=5)
FOCUS["h07"] = (540, 520)

def h08(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#2a2e3a", "#1a1c24"); rect(c, 0, 900, P, 180, "#3a3a42")
    k = w("golpear")
    sh = math.sin(t * 40) * 8 * (1 if t > k else 0) * (0.5 + 0.5 * math.sin(t * 3))
    c.save(); c.translate(sh, 0)
    rect(c, 330, 140, 420, 780, "#5a4a3a"); rect(c, 360, 170, 360, 330, hx("#000", 0.15)); rect(c, 360, 540, 360, 340, hx("#000", 0.15))
    c.restore()
    rect(c, 700, 500, 90, 30, "#9aa0aa"); rect(c, 740 - 40 * clamp((t - w("seguro")) / 0.3), 496, 40, 38, "#c8ccd4")
    if t > w("reírse") - 0.2:
        for k2 in range(4):
            a = (t * 0.7 + k2 / 4) % 1; txt(c, "JA", 420 + k2 * 80, 600 - 200 * a, hx("#e0303a", 1 - a), 56, True)
    rect(c, 330, 916, 420, 8, hx("#fff4c8", 0.7))
FOCUS["h08"] = (540, 540)

def h09(c, t, T, w):
    store_glass(c, t)
    counter(c, t)
    tienda_you(c, t, "shock", look=(0, -0.6), sweat=1.0)
FOCUS["h09"] = (540, 620)

def h10(c, t, T, w):
    n = 0
    for tok, v in (("diez", 10), ("veinte", 20), ("treinta", 30)):
        if t > w(tok) - 0.1: n = v
    bomba_ext(c, t, people=n)
    for tok, s in (("diez", "10"), ("veinte", "20"), ("treinta", "30")):
        if t > w(tok) - 0.1 and (n == int(s)): tag2(c, 540, 420, s, t, w(tok), "#e0303a", "#ffffff", size=70)
FOCUS["h10"] = (540, 620)

def h11(c, t, T, w):
    bomba_ext(c, t, people=30)
    c.new_path(); c.arc(540, 560, 470 + 6 * math.sin(t * 3), 0, 2 * math.pi); c.set_line_width(6); src(c, hx("#fff4c8", 0.25)); c.stroke()
FOCUS["h11"] = (540, 600)

def h12(c, t, T, w):
    arm = ease(clamp((t - w("levanta")) / 0.8))
    bomba_ext(c, t, people=30, woman=lambda c_: M.infectado(c_, 540, 700, 0.38, t, open_=0.3, arm_up=arm))
    if t > w("cables") - 0.2:
        c.new_path(); c.arc(1000, 356, 50 + 10 * math.sin(t * 8), 0, 2 * math.pi); c.set_line_width(6); src(c, hx("#e0303a", 0.9)); c.stroke()
FOCUS["h12"] = (560, 640)
CAM["h12"] = [("adelante", 1.6, 540, 640), ("cables", 1.4, 820, 460)]

def h13(c, t, T, w):
    sp = clamp(1 - abs(t - w("chispazo")) / 0.6)
    bomba_ext(c, t, people=30, spark=sp, woman=lambda c_: M.infectado(c_, 540, 700, 0.38, t, open_=0.5, arm_up=1.0))
FOCUS["h13"] = (860, 440)

def h14(c, t, T, w):
    off = 1.0 if t > w("apagan") else 0.0
    if t > w("apagan") - 0.4 and t < w("apagan") and int(t * 20) % 2: off = 1.0
    bomba_ext(c, t, lights=1 - off, people=30, eyes=1.0)
    if off:
        overlay(c, "#000", 0.8)
        for (x, y, s, f) in crowd_pos(30):
            eyes_dark(c, x, y - 326 * s, max(2, 10 * s), t, 0.9)
FOCUS["h14"] = (540, 600)

def h15(c, t, T, w):
    store_glass(c, t, lights=0, cracks=clamp((t - w("crujir")) / 2.5))
    counter(c, t, lights=0)
    overlay(c, "#000", 0.55)
    eyes_dark(c, 300, 620, 9, t, 1.0)
    if t > w("respira") - 0.2:
        eyes_dark(c, 760, 1000, 5, t, clamp((t - w("respira") + 0.2) / 0.5))
FOCUS["h15"] = (560, 700)
CAM["h15"] = [("chiquito", 1.6, 760, 900)]

def h16(c, t, T, w):
    store_glass(c, 0.0, lights=0, cracks=1.0); counter(c, 0.0, lights=0); overlay(c, "#000", 0.7)

# ---------------- PARTE 3 ----------------
def i01(c, t, T, w):
    store_glass(c, t, lights=0, cracks=1.0)
    counter(c, t, lights=0)
    overlay(c, "#000", 0.55)
    eyes_dark(c, 300, 620, 9, t, 1.0); eyes_dark(c, 760, 1000, 5, t, 0.8 + 0.2 * math.sin(t * 4))
FOCUS["i01"] = (560, 700)

def i02(c, t, T, w):
    on = clamp((t - w("linterna")) / 0.3)
    pasillo(c, t, door=0.0, dark=0.9 - 0.3 * on, you=False)
    if on: flashlight(c, 540, 1080, -math.pi / 2 + 0.2 * math.sin(t * 5), t, on)
    bust(c, 540 + 30 * math.sin(t * 9), 1240, 0.8, t, "shock", look=(0, -0.6), arms="phone", **YOU)
FOCUS["i02"] = (540, 640)

def i03(c, t, T, w):
    n1, n2 = w("una"), w("dos")
    cord = 0.0
    for kk in (n1, n2):
        if kk - 0.1 < t < kk + 0.6: cord = math.sin(clamp((t - kk + 0.1) / 0.7) * math.pi)
    planta(c, t, on=0.0, light=0.0, cord=cord)
    bust(c, 230, 1130, 0.75, t, "shock", look=(0.8, -0.3), arms="hold", sweat=1.0, **YOU)
    tag2(c, 740, 380, "1", t, n1, "#ffffff", size=60)
    tag2(c, 860, 380, "2", t, n2, "#ffffff", size=60)
    tag2(c, 600, 900, "NADA", t, w("nada"), "#e0303a", "#ffffff")
    if t > w("revienta") - 0.1:
        tag2(c, 540, 520, "¡CRASH!", t, w("revienta"), "#e0303a", "#ffffff", size=70)
FOCUS["i03"] = (520, 640)

def i04(c, t, T, w):
    on = 1.0 if t > w("ruge") - 0.1 else 0.0
    planta(c, t, on=on, light=on, cord=math.sin(clamp((t - w("tres") + 0.1) / 0.7) * math.pi) if t < w("ruge") else 0.0)
    bust(c, 230, 1130, 0.75, t, "shock" if not on else "worry", look=(0.8, -0.3), arms="hold", **YOU)
    tag2(c, 740, 380, "3", t, w("tres"), "#3aff6a", size=60)
FOCUS["i04"] = (520, 640)

def i05(c, t, T, w):
    back = ease(clamp((t - w("corriendo")) / 1.6))
    bomba_ext(c, t, lights=1.0, people=30, back=back, eyes=1.0 - back)
    if t > w("gritos") - 0.2:
        for k in range(3):
            a = (t * 0.6 + k / 3) % 1; txt(c, "¡AAAH!", 200 + k * 330, 620 - 100 * a, hx("#e0303a", 1 - a), 40, True)
FOCUS["i05"] = (540, 600)

def i06(c, t, T, w):
    planta(c, t, on=1.0, light=1.0, flash=0)
    sun = clamp((t - w("amanece")) / 1.0)
    bust(c, 300, 1200, 0.8, t, "tired", eyebags=1.0, look=(0.5, 0), arms="hold", **YOU); extintor(c, 300, 1100, 0.9)
    if t > w("reírse") - 0.2:
        for k in range(3):
            a = (t * 0.5 + k / 3) % 1; txt(c, "ja", 820 + k * 40, 440 - 100 * a, hx("#e0303a", 0.7 * (1 - a)), 36, True)
    if sun: overlay(c, "#ffb860", 0.18 * sun)
    tag2(c, 760, 860, "6:00 a. m.", t, w("amanece"), "#ffc24a")
FOCUS["i06"] = (420, 640)

def i07(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#e8a86a", "#8a7a8a"); mountains(c, 640, ("#5a4a5a", "#4a3a4a")); rect(c, 0, 700, P, 380, "#4a4a4a")
    for k, x in enumerate((180, 860)):
        bust(c, x, 1180, 0.7, t + k, "neutral", look=(-0.5 if x > 540 else 0.5, 0), **SOLDADO); mask(c, x, 1180, 0.7)
    bust(c, 540, 1160, 0.75, t, "worry", look=(0, 0), arms="up" if t > w("revisan") else "none", **YOU)
    tag2(c, 540, 380, "NI UN RASGUÑO", t, w("rasguño"), "#3aff6a")
FOCUS["i07"] = (540, 640)

def i08(c, t, T, w):
    vgrad(c, 0, 0, P, P, "#e8a86a", "#8a7a8a")
    bust(c, 540, 1120, 1.1, t, "neutral", look=(0, 0), **SOLDADO); mask(c, 540, 1120, 1.1)
FOCUS["i08"] = (540, 560)

def i09(c, t, T, w):
    rect(c, 0, 0, P, P, "#2a2e38")
    rrect(c, 520, 300, 460, 340, 20, "#111"); rect(c, 540, 320, 420, 300, "#3a3e3a")
    for k in range(4): rect(c, 550 + (k % 2) * 205, 330 + (k // 2) * 145, 195, 135, ("#5a5e5a", "#4a4e4a")[k % 2])
    bust(c, 760, 1200, 0.75, t, "neutral", look=(0, -0.6), **SOLDADO); mask(c, 760, 1200, 0.75)
    bust(c, 250, 1200, 0.8, t, "worry", look=(0.6, -0.3), talk=0.3 if t < w("baño") else 0, **YOU)
    tag2(c, 750, 700, "CÁMARAS", t, w("cámaras"), "#ffffff")
FOCUS["i09"] = (560, 560)

def i10(c, t, T, w):
    g = w("gateando"); a = ease(clamp((t - g) / 3.0))
    crawl = (470 + 0 * a, 470 + 120 * a) if t > g - 0.2 else None
    cctv(c, t, "03:12:07", lambda c_: cctv_store(c_, t, door=0.6 if t < g + 0.8 else 0.0, crawl=crawl))
    if crawl:
        c.new_path(); c.arc(crawl[0] + 10, crawl[1], 80, 0, 2 * math.pi); c.set_line_width(6); src(c, hx("#e0303a", 0.9)); c.stroke()
FOCUS["i10"] = (500, 520)
CAM["i10"] = [("gateando", 1.5, 480, 520)]

def i11(c, t, T, w):
    a = ease(clamp((t - w("mete")) / 1.5))
    cctv(c, t, "03:12:15", lambda c_: cctv_store(c_, t, crawl=(470 + 60 * a, 590 + 120 * a) if a < 1 else None, blanket=False))
    if a >= 1:
        c.new_path(); c.arc(540, 720, 90, 0, 2 * math.pi); c.set_line_width(6); src(c, hx("#e0303a", 0.9)); c.stroke()
    tag2(c, 540, 400, "TÚ ESTÁS AHÍ", t, w("ahora"), "#e0303a", "#ffffff")
FOCUS["i11"] = (520, 640)

def i12(c, t, T, w):
    st = "03:12:20"
    for tok, s in (("cuatro", "04:00:00"), ("cinco", "05:00:00"), ("seis", "06:00:00")):
        if t > w(tok) - 0.1: st = s
    cctv(c, t, st + "  ▶▶", lambda c_: cctv_store(c_, t, you=st != "04:00:00" and st != "05:00:00", blanket=False))
    tag2(c, 540, 400, "NUNCA SALE", t, w("nunca"), "#e0303a", "#ffffff")
FOCUS["i12"] = (540, 640)

def i13(c, t, T, w):
    rect(c, 0, 0, P, P, "#2a2e38")
    bust(c, 540, 1120, 1.1, t, "shock", look=(0, 0.6), arms="up", **SOLDADO); mask(c, 540, 1120, 1.1)
FOCUS["i13"] = (540, 560)

def i14(c, t, T, w):
    rect(c, 0, 0, P, P, "#08080c")
    # tu tenis y tu pierna detrás del mostrador
    rect(c, 560, 0, 160, 700, "#2a3a5a"); rrect(c, 520, 660, 300, 110, 40, "#e8e8e8"); rect(c, 520, 740, 300, 30, "#d0241c")
    rect(c, 0, 770, P, 310, "#141418")
    k = w("tobillo")
    if t > k - 0.3:
        a = ease(clamp((t - k + 0.3) / 0.4))
        M.bebe_infectado(c, 340, 760 - 80 * a, 0.75, t, open_=0.3 + 0.5 * clamp((t - w("dientes")) / 0.5), hand=False)
        c.save(); c.translate(585, 660); c.scale(0.9, 0.9)
        ell(c, 0, 0, 48, 40, "#a0a890")
        for j in range(4): line(c, [(-20 + j * 14, -20), (30 + j * 8, -60 + j * 26)], "#a0a890", 14)
        c.restore()
    else:
        eyes_dark(c, 340, 720, 8, t, 0.9)
FOCUS["i14"] = (460, 640)
CAM["i14"] = [("dientes", 1.35, 420, 640)]

def i15(c, t, T, w):
    rect(c, 0, 0, P, P, "#08080c"); M.bebe_infectado(c, 340, 680, 0.75, 0.0, open_=0.8, hand=False); overlay(c, "#000", 0.6)

PANELS = {k: v for k, v in globals().items() if len(k) == 3 and k[0] in "ghi" and k[1:].isdigit() and callable(v)}

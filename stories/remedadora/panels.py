import math, random
import cairocffi as cairo
from lib import hx, src, fill, rect, rrect_path, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp, text_w
from povlib import *
from scenes import *

YOU = dict(hat="hair", skin="#c48a5c", shirt="#4a4a58", hair_col="#1d1410", mole=False)
MAMA = dict(hat="bun", skin="#b67a50", shirt="#3a5a9a", hair_col="#2a1a14")
FAKE = dict(hat="bun", skin="#a88a74", shirt="#3a5a9a", hair_col="#2a1a14")   # la Remedadora: casi igual
FOCUS = {}; CAM = {}

# ---------------- escenarios ----------------
def living(c, t, dark=0.55, phone_glow=0.0):
    vgrad(c, 0, 0, P, P, "#141a2c", "#07090f")
    rect(c, 0, 640, P, 440, "#0d1018")
    # puerta de la calle
    rect(c, 700, 160, 300, 640, "#2a1a12"); rect(c, 720, 180, 260, 620, "#3a2416"); circ(c, 850, 320, 12, "#111"); circ(c, 950, 500, 14, "#9a7a3a")
    rect(c, 720, 796, 260, 6, hx("#9ab0ff", 0.25))
    # pasillo
    rect(c, 60, 180, 220, 620, "#05060a"); rect(c, 60, 180, 220, 8, "#1a2030")
    # mesa del comedor con el celular
    rect(c, 300, 700, 360, 24, "#3a2a20"); rect(c, 320, 724, 20, 200, "#2a1e16"); rect(c, 620, 724, 20, 200, "#2a1e16")
    rrect(c, 450, 676, 70, 26, 6, "#111")
    if phone_glow: glow(c, 485, 680, 200, "#9fd0ff", 0.4 * phone_glow); rrect(c, 454, 680, 62, 16, 4, hx("#bfe4ff", phone_glow))
    line(c, [(510, 690), (600, 700), (640, 760)], "#ddd", 3)
    overlay(c, "#000010", dark * 0.5)

def chat(c, t, msgs, typing=None, title="Mamá"):
    rect(c, 0, 0, P, P, "#05060a")
    glow(c, 540, 540, 600, "#5fb4ff", 0.12)
    rrect(c, 250, 40, 580, 1000, 50, "#111"); c.save(); rrect_path(c, 266, 56, 548, 968, 40); c.clip()
    rect(c, 266, 56, 548, 968, "#0b141a"); rect(c, 266, 56, 548, 120, "#1f2c34")
    circ(c, 330, 116, 32, "#c0527a"); txt(c, title, 380, 112, "#e9edef", 36); txt(c, "en línea" if typing is None else "escribiendo...", 380, 150, "#8fd0a0", 24, False, False)
    y = 220
    for (tm, text, mine) in msgs:
        if t < tm: continue
        a = clamp((t - tm) / 0.2); lines_ = text if isinstance(text, list) else [text]
        h = bubble(c, 560 if mine else 290, y, 230 if mine else 480, lines_, "#005c4b" if mine else "#1f2c34", "#e9edef", 32, "r" if mine else "l", a)
        y += h + 40
    if typing is not None and t > typing:
        rrect(c, 290, y, 130, 64, 30, "#1f2c34")
        for k in range(3): circ(c, 325 + k * 30, y + 32, 9, hx("#c0c8cc", 0.4 + 0.6 * (math.sin(t * 8 - k) > 0)))
    c.restore()
    txt(c, "2:14", 540, 30, "#ffffff", 26, True)

def hallway(c, t, door=0.0, light=0.0, eye=0.0):
    vgrad(c, 0, 0, P, P, "#10131f", "#05060a")
    poly(c, [(0, 0), (300, 220), (300, 860), (0, 1080)], "#0c0f18"); poly(c, [(1080, 0), (780, 220), (780, 860), (1080, 1080)], "#0c0f18")
    rect(c, 300, 220, 480, 640, "#080a12")
    rect(c, 420, 300, 240, 560, "#3a2416")
    if door > 0:
        g = 240 * door; rect(c, 420, 300, g, 560, "#000000")
        if light: rect(c, 420, 300, g, 560, hx("#2a2a3a", light))
        if eye: circ(c, 420 + g * 0.5, 520, 10, hx("#f4f4ec", eye)); circ(c, 420 + g * 0.5 + 30, 520, 10, hx("#f4f4ec", eye))
    circ(c, 640, 600, 9, "#9a7a3a")
    rect(c, 420, 856, 240, 6, hx("#9ab0ff", 0.12))

def peephole_fig(c, t, stare=1.0, smile=False, who=FAKE, mood="creepy", lean=0.0):
    rect(c, 0, 0, P, P, "#000")
    c.save(); c.new_path(); c.arc(540, 540, 470, 0, 2 * math.pi); c.clip()
    vgrad(c, 0, 0, P, P, "#18203a", "#070a14")
    glow(c, 540, 160, 420, "#ffd890", 0.2); circ(c, 540, 160, 18, "#ffd890")
    rect(c, 0, 880, P, 200, "#2a2a2a")
    c.save(); c.translate(540, 540); s = 1.0 + 0.06 * lean; c.scale(s * 1.12, s); c.translate(-540, -540)
    bust(c, 540, 1180, 1.05, t * 0.2 if stare else t, mood if not smile else "creepy", look=(0, 0), **who)
    c.restore()
    g = cairo.RadialGradient(540, 540, 230, 540, 540, 470); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.95)
    c.rectangle(0, 0, P, P); c.set_source(g); c.fill()
    c.restore()

def phone_close(c, t, typing=True, msg=None):
    rect(c, 0, 0, P, P, "#120d0b"); rect(c, 0, 640, P, 440, "#2a1e16")
    glow(c, 540, 600, 520, "#9fd0ff", 0.25)
    c.save(); c.translate(540, 640); c.rotate(-0.12)
    rrect(c, -170, -330, 340, 640, 40, "#0a0a0a"); rrect(c, -156, -316, 312, 612, 30, "#0b141a")
    rect(c, -156, -260, 312, 90, "#1f2c34"); txt(c, "Mamá", -80, -205, "#e9edef", 32, False, True)
    if typing: txt(c, "escribiendo...", -80, -178, "#8fd0a0", 22, False, False)
    if msg: bubble(c, -140, -120, 280, msg, "#005c4b", "#e9edef", 28, "r")
    rect(c, -20, 300, 40, 60, "#ddd"); c.restore()
    line(c, [(560, 1000), (700, 1080)], "#ddd", 6)

def bedroom_mom(c, t, mood="worry", talk=0.0, lamp=0.7, tears=0.0, rosary=False):
    vgrad(c, 0, 0, P, P, "#1a1420", "#08060a")
    glow(c, 160, 560, 420, "#ffcf80", 0.35 * lamp); rrect(c, 90, 520, 140, 110, 20, "#c9a24a"); rect(c, 150, 630, 20, 120, "#6a5a3a")
    rect(c, 60, 740, 220, 340, "#3a2a20")
    rrect(c, 260, 640, 780, 160, 40, "#e8e0d0")
    bust(c, 640, 1060, 0.95, t, mood, look=(-0.3, 0), talk=talk, tears=tears, **MAMA)
    rrect(c, 220, 860, 860, 260, 40, "#5a3a5a")
    if rosary:
        for k in range(12): circ(c, 520 + k * 14, 900 + math.sin(k / 2) * 30, 7, "#c9b48a")
        rect(c, 690, 930, 6, 40, "#c9b48a"); rect(c, 678, 942, 30, 6, "#c9b48a")

def window_rain(c, t, fig=1.0, who="tia", laugh=False):
    vgrad(c, 0, 0, P, P, "#0c0f18", "#05060a")
    rect(c, 180, 120, 720, 720, "#2a1a12"); rect(c, 200, 140, 680, 680, "#0a1020")
    if fig > 0:
        col = "#7a5a6a" if who == "tia" else "#5a5a6a"
        bust(c, 540, 1060, 1.0, t * 0.5, "creepy" if laugh else "sad", look=(0, 0), tears=0.0 if laugh else 1.0,
             **dict(hat="bun" if who != "novia" else "none", skin="#9a8a7a", shirt=col, hair_col="#2a1a14"))
        overlay(c, "#05081a", 0.25)
        for hx_ in (330, 750): rrect(c, hx_ - 40, 400, 80, 120, 30, hx("#c0a890", 0.8))
    rr = random.Random(int(t * 12))
    for k in range(60):
        x = rr.uniform(200, 880); y0 = (rr.uniform(0, 680) + t * 400) % 680 + 140
        line(c, [(x, y0), (x - 4, y0 + 30)], hx("#9ab0ff", 0.35), 2)
    rect(c, 536, 140, 8, 680, "#2a1a12"); rect(c, 200, 476, 680, 8, "#2a1a12")
    rect(c, 0, 840, P, 240, "#1a1420")

def creature(c, t, morph=1.0):
    vgrad(c, 0, 0, P, P, "#0a0c14", "#000")
    glow(c, 540, 400, 500, "#5a6a9a", 0.15)
    sw = math.sin(t * 1.5) * 10
    poly(c, [(470, 380), (610, 380), (660, 1080), (420, 1080)], "#06070b")
    line(c, [(480, 420), (360 + sw, 700), (330 + sw, 980)], "#06070b", 34); line(c, [(600, 420), (720 - sw, 700), (750 - sw, 980)], "#06070b", 34)
    for k in range(4):
        line(c, [(330 + sw, 980), (300 + sw + k * 14, 1060)], "#06070b", 8); line(c, [(750 - sw, 980), (760 - sw + k * 14, 1060)], "#06070b", 8)
    c.save(); c.translate(540, 300); c.scale(0.55, 0.55 + 0.12 * morph); c.translate(-540, -300)
    bust(c, 540, 680, 1.0, t, "creepy", **FAKE); c.restore()
    rect(c, 380, 360, 320, 200, hx("#06070b", 0.0))

def footprints(c, t, n=1.0, bath=0.0):
    vgrad(c, 0, 0, P, P, "#c8c0b0", "#8a8478")
    glow(c, 900, 120, 500, "#fff4d0", 0.4)
    rect(c, 0, 620, P, 460, "#7a7468")
    for k in range(10):
        if k / 10 > n: break
        x = 120 + k * 85; y = 1000 - k * 40 + (24 if k % 2 else 0)
        ell(c, x, y, 18, 30, hx("#3a3a40", 0.55)); [circ(c, x - 12 + j * 6, y - 34, 5, hx("#3a3a40", 0.55)) for j in range(5)]
    if bath:
        rect(c, 760, 200, 220, 200, "#5a5040"); rect(c, 776, 216, 188, 168, "#0a0c10" if bath > 0.5 else "#a0b0c0")
        poly(c, [(776, 216), (964, 216), (930, 150), (810, 150)], hx("#c0d0e0", 0.7))
        line(c, [(800, 384), (880, 600)], hx("#3a3a40", 0.4), 10)

def kitchen(c, t, who=FAKE, mood="smile", talk=0.0, look=(0, 0)):
    vgrad(c, 0, 0, P, P, "#e8d8b8", "#b89a70")
    glow(c, 880, 160, 500, "#fff4d0", 0.5)
    rect(c, 700, 120, 300, 260, "#5a4a3a"); rect(c, 716, 136, 268, 228, "#cfe6f0")
    rect(c, 0, 640, P, 440, "#8a6a4a"); rect(c, 0, 620, P, 30, "#d8d0c0")
    rrect(c, 120, 520, 160, 110, 16, "#2a2a2a"); ell(c, 200, 520, 70, 14, "#3a3a3a")
    for k in range(3):
        yy = 500 - ((t * 50 + k * 30) % 90); line(c, [(190 + k * 10, yy + 30), (200 + k * 10, yy), (190 + k * 10, yy - 20)], hx("#ffffff", 0.5), 5)
    bust(c, 620, 1060, 1.0, t, mood, look=look, talk=talk, **who)
    rrect(c, 300, 900, 180, 130, 20, "#f4f0e8"); ell(c, 390, 900, 90, 18, "#6a3a1a")

# ---------------- PARTE 1 ----------------
def d01(c, t, T, w):
    chat(c, t, [(w("ábreme") - 0.1, ["Ábreme, que se me", "quedaron las llaves"], False)])
CAM["d01"] = [("tu", 1.0, 540, 540), ("ábreme", 1.35, 520, 380)]

def d02(c, t, T, w):
    hallway(c, t)
    c.save(); c.rectangle(0, 0, P, P); bust(c, 240, 1160, 0.85, t, "worry" if t < w("congela") else "shock", look=(1, -0.3), **YOU); c.restore()
FOCUS["d02"] = (420, 600)

def d03(c, t, T, w):
    hallway(c, t)
    for k in range(3):
        a = (t * 0.8 + k / 3) % 1
        ui(c, 46 + 20 * a); outline_text_(c, "Z", 540 + 40 * a + k * 20, 520 - 160 * a, hx("#cfd8ff", 1 - a))
    tag2(c, 540, 960, "SU MAMÁ ESTÁ AQUÍ ADENTRO", t, w("cuarto"), "#e0303a", "#ffffff", 34)
FOCUS["d03"] = (540, 560)

def outline_text_(c, s, x, y, col):
    w_ = text_w(c, s); c.new_path(); c.move_to(x - w_ / 2, y); c.text_path(s); c.set_line_width(10); c.set_line_join(cairo.LINE_JOIN_ROUND)
    src(c, "#000"); c.stroke_preserve(); src(c, col); c.fill()

def d04(c, t, T, w):
    if t < w("pastillas") - 0.2:
        hospital(c, t, babies=0); sepia(c, 0.8)
        line(c, [(560, 300), (640, 300), (670, 220), (700, 380), (730, 300), (1000, 300)], "#2ad07a", 6)
        tag2(c, 540, 380, "HACE 3 DÍAS", t, 0.2, "#ffffff")
    else:
        bedroom_mom(c, t, "neutral", lamp=0.3)
        rrect(c, 120, 690, 80, 50, 10, "#f0f0f0"); [circ(c, 140 + k * 20, 715, 7, "#e0603a") for k in range(3)]
        tag2(c, 540, 380, "DUERME COMO UNA PIEDRA", t, w("piedra"), "#ffc24a")
FOCUS["d04"] = (560, 560)

def d05(c, t, T, w):
    chat(c, t, [(0, ["Ábreme, que se me", "quedaron las llaves"], False), (w("escribes"), ["¿mamá, dónde", "estás?"], True),
                (w("afuera"), ["Afuera, mijo.", "Hace mucho frío.", "Ábreme."], False)])
FOCUS["d05"] = (540, 560)

def d06(c, t, T, w):
    door_in(c, t, under=0.3)
    bust_back(c, 540, 1240, 1.0, t, shirt=YOU["shirt"], hair=YOU["hair_col"], hood=False)
FOCUS["d06"] = (540, 340)
CAM["d06"] = [("miras", 1.8, 540, 340)]

def d07(c, t, T, w):
    peephole_fig(c, t, stare=1.0, lean=clamp(t / T))
    if t > w("descalza") - 0.1: tag2(c, 540, 980, "DESCALZA", t, w("descalza"), "#ffffff")
FOCUS["d07"] = (540, 560)

def d08(c, t, T, w):
    peephole_fig(c, t, stare=1.0, lean=1.0)
FOCUS["d08"] = (540, 560)
CAM["d08"] = [("parpadea", 2.0, 540, 600)]

def d09(c, t, T, w):
    k = w("celular")
    living(c, t, phone_glow=1.0 if t > k - 0.2 else 0.0)
    if t < k - 0.2: bust(c, 820, 1160, 0.8, t, "shock", look=(-1, 0), **YOU)
FOCUS["d09"] = (485, 690)

def d10(c, t, T, w):
    phone_close(c, t, typing=True)
FOCUS["d10"] = (520, 460)

def d11(c, t, T, w):
    if t < w("mensaje") - 0.1: phone_close(c, t, typing=True)
    else: phone_close(c, t, typing=False, msg=["no le creas a la", "que está en el", "cuarto"])
FOCUS["d11"] = (540, 560)

def d12(c, t, T, w):
    hallway(c, t)
    if t < w("detienen"):
        for k in range(3):
            a = (t * 0.8 + k / 3) % 1; ui(c, 46); outline_text_(c, "Z", 540 + 40 * a, 520 - 160 * a, hx("#cfd8ff", 1 - a))
    else: overlay(c, "#000", 0.3)
FOCUS["d12"] = (540, 560)

def d13(c, t, T, w):
    hallway(c, t, door=0.3 * ease(clamp((t - w("abre")) / 1.5)), eye=clamp((t - w("oscuridad")) / 0.5))
FOCUS["d13"] = (480, 540)
CAM["d13"] = [("oscuridad", 1.9, 470, 520)]

def d14(c, t, T, w):
    hallway(c, t, door=0.3, eye=1.0)
    c.save(); c.rectangle(420, 300, 72, 560); c.clip(); bust(c, 450, 1000, 0.8, t, "worry", look=(1, 0), talk="auto", **MAMA); c.restore()
    overlay(c, "#000010", 0.3)
FOCUS["d14"] = (460, 560)

def d15(c, t, T, w):
    door_in(c, t, under=0.2, shadow=1.0)
    for i, tok in enumerate(("tres", "veces", "despacio")):
        tt = w(tok)
        ui(c, 140)
        if t > tt: sc = 1 + 0.5 * math.exp(-(t - tt) * 6); c.save(); c.translate(540, 700); c.scale(sc, sc); outline_text_(c, "TOC", 0, -200 + i * 140, hx("#ffffff", clamp(1.5 - (t - tt) * 0.4))); c.restore()
    ui(c, 90)
FOCUS["d15"] = (540, 560)

def d16(c, t, T, w):
    door_in(c, t, under=0.3, shadow=1.0); overlay(c, "#000", 0.6)

# ---------------- PARTE 2 ----------------
def e01(c, t, T, w):
    hallway(c, t, door=1.0, light=0.6)
    bust_back(c, 540, 1180, 0.85, t, shirt=YOU["shirt"], hair=YOU["hair_col"], hood=False)
    if t > w("seguro"): tag2(c, 540, 380, "CLIC", t, w("seguro"), "#ffffff")
FOCUS["e01"] = (540, 600)

def e02(c, t, T, w):
    bedroom_mom(c, t, "worry")
FOCUS["e02"] = (640, 600)

def e03(c, t, T, w):
    if t < w("cama") - 0.2:
        bedroom_mom(c, t, "worry", talk="auto")
    else:
        hospital(c, t, babies=0)
        bust(c, 880, 1000, 0.6, t, "creepy", look=(-1, 0), talk="auto", **dict(hat="bun", skin="#c8b0a0", shirt="#d8d8e0", hair_col="#d0d0d0"))
        sepia(c, 0.85)
        if t > w("remedadora") - 0.1: tag2(c, 540, 400, "LA REMEDADORA", t, w("remedadora"), "#e0303a", "#ffffff", 46)
FOCUS["e03"] = (640, 600)

def e04(c, t, T, w):
    creature(c, t, morph=clamp((t - w("ellos")) / 1.0))
    tag2(c, 540, 900, "LA REMEDADORA", t, 0.1, "#e0303a", "#ffffff", 46)
FOCUS["e04"] = (540, 420)

def e05(c, t, T, w):
    if t < w("cara") - 0.1:
        creature(c, t, 0.0); tag2(c, 300, 400, "1. LA VOZ", t, w("voz"), "#ffffff")
    elif t < w("noche") - 0.1:
        creature(c, t, 1.0); tag2(c, 300, 400, "2. LA CARA", t, w("cara"), "#ffffff")
    else:
        door_in(c, t, under=0.3, shadow=1.0); tag2(c, 540, 400, "3. LA PUERTA", t, w("noche"), "#e0303a", "#ffffff")
FOCUS["e05"] = (540, 460)

def e06(c, t, T, w):
    door_in(c, t, under=0.3, shadow=1.0)
    rect(c, 330, 1000, 420, 22, hx("#e0303a", 0.6 + 0.3 * math.sin(t * 6)))
    tag2(c, 540, 400, "NO PUEDE ENTRAR SI NO LA INVITAS", t, w("invita"), "#e0303a", "#ffffff", 32)
FOCUS["e06"] = (540, 760)

def e07(c, t, T, w):
    door_in(c, t, under=0.3, shadow=1.0); overlay(c, "#000", 0.2)
FOCUS["e07"] = (540, 900)

def e08(c, t, T, w):
    peephole_fig(c, t, stare=0.0, mood="sad", who=dict(FAKE, skin="#a88a74"))
    for k in range(2): ell(c, 540 + (k * 2 - 1) * 60, 700 + (t * 120 % 140), 9, 14, hx("#7fd0ff", 0.8))
FOCUS["e08"] = (540, 600)

def e09(c, t, T, w):
    rect(c, 0, 0, P, P, "#05060a")
    c.save(); c.rectangle(0, 0, 536, P); c.clip(); bust(c, 270, 1060, 0.85, t, "worry", look=(0.5, 0), **MAMA); c.restore()
    c.save(); c.rectangle(544, 0, 536, P); c.clip(); bust(c, 810, 1060, 0.85, t, "worry", look=(-0.5, 0), **FAKE); c.restore()
    rect(c, 536, 0, 8, P, "#e0303a")
    tag2(c, 270, 400, "¿?", t, w("cuál"), "#ffffff"); tag2(c, 810, 400, "¿?", t, w("cuál") + 0.2, "#ffffff")
FOCUS["e09"] = (540, 600)

def e10(c, t, T, w):
    rect(c, 0, 0, P, P, "#d8cdb8")
    bust(c, 540, 1060, 1.0, t, "smile", **dict(hat="bun", skin="#a8704a", shirt="#6a3a5a", hair_col="#d8d8d8"))
    sepia(c, 0.8)
    tag2(c, 540, 400, "LA ABUELA", t, w("abuela"), "#ffffff")
FOCUS["e10"] = (540, 600)

def e11(c, t, T, w):
    door_in(c, t, under=0.3, shadow=1.0)
    c.save(); c.rectangle(0, 0, 330, P); c.clip(); bust(c, 180, 1140, 0.85, t, "angry", look=(1, -0.2), talk=0.5 * abs(math.sin(t * 13)) if t < T - 0.5 else 0, **YOU); c.restore()
FOCUS["e11"] = (420, 600)

def e12(c, t, T, w):
    k = w("cama")
    if t < k - 0.2:
        door_in(c, t, under=0.3, shadow=1.0); overlay(c, "#000", 0.3)
        ui(c, 60); outline_text_(c, "...", 540, 560, "#ffffff")
    else:
        bedroom_mom(c, t, "worry", lamp=0.5)
FOCUS["e12"] = (640, 600)

def e13(c, t, T, w):
    bedroom_mom(c, t, "sad", talk="auto", lamp=0.5)
FOCUS["e13"] = (640, 600)

def e14(c, t, T, w):
    bedroom_mom(c, t, "smile", lamp=0.7)
    tag2(c, 640, 400, "ES ELLA", t, w("ella"), "#2ad07a", "#11131a")
FOCUS["e14"] = (640, 600)

def e15(c, t, T, w):
    door_in(c, t, under=0.3, shadow=1.0); overlay(c, "#000", 0.25)
FOCUS["e15"] = (540, 800)

def e16(c, t, T, w):
    peephole_fig(c, t, stare=1.0, smile=True, lean=1.0)
FOCUS["e16"] = (540, 600)

def e17(c, t, T, w):
    rect(c, 0, 0, P, P, "#05060a")
    bust(c, 540, 1080, 1.1, t, "shock", sweat=1.0, **YOU)
FOCUS["e17"] = (540, 560)

def e18(c, t, T, w):
    peephole_fig(c, t, stare=1.0, smile=True, lean=1.0, who=dict(YOU, skin="#a88a74"), mood="creepy")
FOCUS["e18"] = (540, 600)

def e19(c, t, T, w):
    door_in(c, t, under=0.3, shadow=1.0); overlay(c, "#000", 0.6)

# ---------------- PARTE 3 ----------------
def f01(c, t, T, w):
    rect(c, 0, 0, P, P, "#05060a")
    c.save(); c.rectangle(0, 0, 536, P); c.clip(); bust(c, 270, 1060, 0.85, t, "worry", **YOU); c.restore()
    c.save(); c.rectangle(544, 0, 536, P); c.clip(); bust(c, 810, 1060, 0.85, t, "creepy", **dict(YOU, skin="#a88a74")); c.restore()
    rect(c, 536, 0, 8, P, "#e0303a")
FOCUS["f01"] = (810, 600)

def f02(c, t, T, w):
    bedroom_mom(c, t, "worry", rosary=t > w("rosario") - 0.2)
FOCUS["f02"] = (600, 760)

def f03(c, t, T, w):
    bedroom_mom(c, t, "worry", talk="auto", rosary=True)
FOCUS["f03"] = (640, 600)

def f04(c, t, T, w):
    window_rain(c, t, fig=1.0 if t > w("tía") - 0.2 else 0.0)
    tag2(c, 540, 380, "3:20 a.m.", t, 0.1, "#ffffff")
FOCUS["f04"] = (540, 560)

def f05(c, t, T, w):
    bedroom_mom(c, t, "shock" if t > w("cúcuta") else "worry", lamp=0.3, rosary=True)
    if t > w("cúcuta") - 0.1: tag2(c, 640, 400, "VIVE EN CÚCUTA", t, w("cúcuta"), "#e0303a", "#ffffff")
FOCUS["f05"] = (640, 600)

def f06(c, t, T, w):
    window_rain(c, t, fig=1.0, laugh=t > w("ríe") - 0.1)
FOCUS["f06"] = (540, 600)

def f07(c, t, T, w):
    who = "tia" if t < w("abuela") else ("abuela" if t < w("vecino") else ("vecino" if t < w("novia") else "novia"))
    window_rain(c, t, fig=1.0, who=who, laugh=True)
    for i, (tok, s) in enumerate((("abuela", "LA ABUELA"), ("vecino", "EL VECINO"), ("novia", "TU NOVIA"))):
        if t > w(tok) - 0.1 and (i == 2 or t < w((("vecino", "novia", "uno"))[i]) - 0.1): tag2(c, 540, 400, s, t, w(tok), "#e0303a", "#ffffff")
FOCUS["f07"] = (540, 600)

def f08(c, t, T, w):
    k = w("sol")
    window_rain(c, t, fig=0.0)
    a = clamp((t - k + 0.3) / 1.5)
    if a: rect(c, 200, 140, 680, 680, hx("#ffd8a0", 0.7 * a)); glow(c, 540, 480, 600, "#ffe0b0", 0.4 * a)
    tag2(c, 540, 400, "5:40 a.m.", t, k - 0.4, "#ffc24a")
FOCUS["f08"] = (540, 480)

def f09(c, t, T, w):
    door_in(c, t, under=1.0)
    if t > w("abres") - 0.2:
        a = ease(clamp((t - w("abres")) / 0.8)); rect(c, 330, 110, 420 * a, 910, hx("#f0e4c8", 1.0)); glow(c, 540, 500, 500, "#fff4d0", 0.4 * a)
FOCUS["f09"] = (540, 560)

def f10(c, t, T, w):
    footprints(c, t, n=clamp((t - w("huellas")) / 2.5))
FOCUS["f10"] = (500, 800)

def f11(c, t, T, w):
    footprints(c, t, n=1.0, bath=1.0)
FOCUS["f11"] = (870, 300)
CAM["f11"] = [("baño", 1.8, 860, 320)]

def f12(c, t, T, w):
    kitchen(c, t, who=MAMA, mood="smile", look=(0.6, 0.3))
    for k in range(4):
        x = 820 + k * 40 + math.sin(t * 2 + k) * 10; y = 360 - ((t * 60 + k * 40) % 160); circ(c, x, y, 10, hx("#3a2a20", 0.7)); line(c, [(x + 9, y), (x + 9, y - 36), (x + 24, y - 28)], hx("#3a2a20", 0.7), 4)
FOCUS["f12"] = (620, 600)

def f13(c, t, T, w):
    kitchen(c, t, who=MAMA, mood="smile", talk="auto", look=(1, 0))
FOCUS["f13"] = (620, 600)

def f14(c, t, T, w):
    k = w("parpadeado")
    kitchen(c, t * 0.05 if t > k - 0.3 else t, who=MAMA if t < k - 0.3 else FAKE, mood="smile" if t < k - 0.3 else "creepy", look=(0, 0))
FOCUS["f14"] = (620, 600)
CAM["f14"] = [("parpadeado", 1.7, 620, 640)]

def f15(c, t, T, w):
    hallway(c, t * 0.3, door=0.25)
    overlay(c, "#000", 0.1)
FOCUS["f15"] = (480, 560)

def f16(c, t, T, w):
    hallway(c, t, door=0.25)
    c.save(); c.rectangle(420, 300, 60, 560); c.clip(); bust(c, 450, 1000, 0.8, t, "tired", look=(1, 0), talk="auto", **MAMA); c.restore()
FOCUS["f16"] = (460, 560)

def f17(c, t, T, w):
    kitchen(c, 0.0, who=FAKE, mood="creepy"); overlay(c, "#000", 0.6)

PANELS = {k: v for k, v in globals().items() if len(k) == 3 and k[0] in "def" and k[1:].isdigit() and callable(v)}

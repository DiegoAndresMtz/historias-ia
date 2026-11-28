import math, random
from lib import hx, src, fill, rect, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp
from palitos import *
import guion as G

FOCUS = {}; CAM = {}
Y = 940                                     # piso de los personajes

def apron(c, sh): rect(c, sh[0] - 34, sh[1] + 20, 68, 120, "#e8e4dc"); line(c, [(sh[0] - 30, sh[1] + 20), (sh[0] + 30, sh[1] + 20)], "#c0392b", 5)
def venda(c, sh): rect(c, sh[0] + 30, sh[1] + 40, 34, 22, "#f4f4f0"); circ(c, sh[0] + 47, sh[1] + 51, 8, "#b0101a")
def chaleco(c, sh): rect(c, sh[0] - 22, sh[1] + 10, 44, 90, "#2a3a6a")
def casco_sold(c, sh): rect(c, sh[0] - 24, sh[1] + 10, 48, 100, "#4a5a3a")
def linterna(c, p): rect(c, p[0] - 6, p[1] - 10, 30, 16, "#2a2a30"); poly(c, [(p[0] + 24, p[1] - 4), (p[0] + 380, p[1] - 90), (p[0] + 380, p[1] + 90)], hx("#fff6c8", 0.18))

YOU = dict(cap="#f2c230")
HECTOR = dict(hair="bald", carry=apron)
MAMA = dict(hair="long")
NINA = dict(hair="pony", kid=True)
REPA = dict(cap="#e8702a", carry=chaleco)
MUCHA = dict(hair="pony", carry=venda)

def fila(c, t, scared=0.0):
    caja(c, 620, Y - 10)
    stick(c, 760, Y - 10, 0.9, t, face="shock" if scared else "neutral", look=-1, seed=3, hair="pony")   # cajera
    for i, (kw, x) in enumerate(((dict(hair="long"), 520), (YOU, 330), (MAMA, 160))):
        stick(c, x, Y, 1.0, t, face="shock" if scared and i else "neutral", seed=i + 5, **kw)
    stick(c, 60, Y, 0.72, t, seed=9, kid=True, hair="pony", face="shock" if scared else "neutral")

# ---------------- PARTE 1: Día uno ----------------
def d01(c, t, T, w):
    supermercado(c, t)
    k = w("muerde")
    if t < k - 0.4: fila(c, t)
    else:
        caja(c, 620, Y - 10)
        stick(c, 760 - 40 * ease(clamp((t - k) / 0.3)), Y - 10, 0.9, t, face="shock", look=-1, seed=3, hair="pony", arms="up")
        zombi(c, 600 + 60 * ease(clamp((t - k + 0.4) / 0.3)), Y, 1.0, t, seed=1, look=1)
        stick(c, 330, Y, 1.0, t, face="shock", arms="cover", **YOU); stick(c, 160, Y, 1.0, t, face="scared", seed=6, **MAMA)
        if t > k: glow(c, 720, 640, 220, "#ff1020", 0.3)
FOCUS["d01"] = (480, 640)
CAM["d01"] = [(0.0, 1.0, 540, 600), ("muerde", 1.45, 680, 620)]

def d02(c, t, T, w):
    supermercado(c, t, light=0.8)
    caja(c, 620, Y - 10)
    up = ease(clamp((t - w("levanta")) / 0.8))
    if up <= 0:
        c.save(); c.translate(560, Y - 20); c.rotate(-math.pi / 2); stick(c, 0, 0, 0.9, t, hair="pony", seed=3, face="sad"); c.restore()
    else:
        c.save(); c.translate(560, Y - 20); c.rotate(-math.pi / 2 * (1 - up)); zombi(c, 0, 0, 0.9, t, seed=3, look=-1, walk=0.0); c.restore()
    stick(c, 260, Y, 1.0, t, face="shock", **YOU)
    pk = w("parpadea")
    if t > pk - 0.2:
        overlay(c, "#000", 0.6 * ease(clamp((t - pk + 0.2) / 0.2))); cara_zombi(c, 540, 560, 1.2 * (0.9 + 0.1 * ease(clamp((t - pk) / 0.5))), t, 0.8)
FOCUS["d02"] = (540, 620)

def d03(c, t, T, w):
    supermercado(c, t, light=0.9)
    g = w("golpe"); down = ease(clamp((t - g + 0.6) / 0.5))
    n = 5 if t < w("veinte") else 16
    c.save(); c.rectangle(0, 120, 1080, 680); c.clip()
    vgrad(c, 0, 120, 1080, 680, "#0a0c14", "#1a1e2a")
    horda(c, 760, n, 0.85, t, 20, 1060, seed=4, look=1, walk=0.0)
    c.restore()
    reja(c, t, down=down, shake=1.0 if t > g else 0.0)
    for i, x in enumerate((180, 340, 500, 660, 820, 960)):
        kw = [YOU, HECTOR, MAMA, NINA, REPA, MUCHA][i]
        stick(c, x, Y + 60, 1.0, t, look=-1 if x > 540 else 1, face="scared", seed=20 + i, **kw)
    overlay(c, "#000", 0.15)
FOCUS["d03"] = (540, 560)
CAM["d03"] = [(0.0, 1.0, 540, 560), ("veinte", 1.3, 540, 460)]

def d04(c, t, T, w):
    supermercado(c, t, light=0.7)
    toks = ["tú", "héctor", "mamá", "niña", "repartidor", "muchacha"]
    kws = [YOU, HECTOR, MAMA, NINA, REPA, MUCHA]
    xs = [140, 300, 470, 590, 760, 930]
    for i, (tk, kw, x) in enumerate(zip(toks, kws, xs)):
        k = w(tk)
        if t < k - 0.25: continue
        a = ease(clamp((t - k + 0.25) / 0.35))
        stick(c, x - 120 * (1 - a), Y, 1.0, t, walk=1 - a, face="scared" if i == 5 else "neutral", look=1, seed=i * 3,
              arms="hold" if i == 5 else "down", **kw)
        if i == 5 and t > w("vendado"): glow(c, x + 40, Y - 160, 90, "#ff1020", 0.35)
FOCUS["d04"] = (540, 660)

def d05(c, t, T, w):
    off = clamp((t - w("apaga")) / 0.2)
    supermercado(c, t, light=1 - 0.75 * off)
    stick(c, 360, Y, 1.05, t, arms="point", face="angry", **HECTOR)
    stick(c, 700, Y, 1.0, t, face="scared", look=-1, **YOU)
    if t > w("adentro") - 0.2:
        glow(c, 900, 620, 260, "#ff1020", 0.25 * clamp((t - w("adentro")) / 0.3))
FOCUS["d05"] = (520, 640)
CAM["d05"] = [(0.0, 1.0, 540, 600), ("adentro", 1.35, 420, 560)]

def d06(c, t, T, w):
    supermercado(c, t, light=0.1)
    overlay(c, "#030818", 0.4)
    c.save(); c.translate(250, Y - 30); c.rotate(-math.pi / 2); stick(c, 0, 0, 0.9, t, face="sad", seed=2, **YOU); c.restore()
    stick(c, 420, Y, 1.0, t, arms="point", face="scared", look=1, **REPA)
    sc = abs(math.sin(t * 9))
    stick(c, 800, Y, 1.0, t, arms="cover", face="sad", look=-1, seed=7, **MUCHA)
    ks = w("sangre")
    if t > ks - 0.2:
        glow(c, 770, Y - 190, 140, "#ff1020", 0.45); circ(c, 770 + sc * 6, Y - 190, 12, "#b0101a")
FOCUS["d06"] = (700, 660)
CAM["d06"] = [(0.0, 1.0, 540, 620), ("sangre", 1.6, 780, 640)]

def d07(c, t, T, w):
    cuarto_frio(c, t); overlay(c, "#000", 0.55)

# ---------------- PARTE 2: Día dos ----------------
def e01(c, t, T, w):
    kn = abs(math.sin(t * 6)) if t > w("golpear") else 0.0
    cuarto_frio(c, t, knock=kn)
    stick(c, 160, Y, 1.0, t, face="shock" if kn else "scared", **YOU); stick(c, 920, Y, 1.0, t, face="scared", look=-1, **HECTOR)
FOCUS["e01"] = (540, 560)
CAM["e01"] = [(0.0, 1.0, 540, 560), ("golpear", 1.25, 540, 520)]

def e02(c, t, T, w):
    techo_vidrio(c, t)
    k = w("techo")
    if t > k - 0.3:
        for i, x in enumerate((180, 520, 860)):
            a = ease(clamp((t - k + 0.3 - i * 0.2) / 0.4))
            c.save(); c.rectangle(70 + i * 340, 130, 280, 500); c.clip()
            zombi(c, x, 360 + 260 * a, 1.0, t, seed=i + 2, walk=0.0, col="#0a0c10")
            c.restore()
    stick(c, 540, Y + 40, 0.9, t, face="shock", **YOU)
FOCUS["e02"] = (540, 420)

def e03(c, t, T, w):
    calle_noche(c, t)
    for i in range(6): rect(c, 560 + (i % 3) * 120, 760 - (i // 3) * 110 - 110, 110, 100, "#2a5a8a")
    rect(c, 520, 300, 520, 30, "#3a3f4a")
    sp = 2.0 if t > w("rápidos") else 1.0
    for i in range(5):
        p = ((t * 0.25 * sp + i * 0.2) % 1.0)
        x = 560 + i * 90; yy = 900 - p * 600
        zombi(c, x, yy, 0.8, t, seed=i + 11, walk=1.0, look=1)
FOCUS["e03"] = (760, 560)

def e04(c, t, T, w):
    vgrad(c, 0, 0, 1080, 1080, "#10131c", "#1c2030"); rect(c, 0, 820, 1080, 260, "#22252e")
    for i in range(4): rect(c, 80 + i * 260, 820, 10, 260, "#e6c840")
    moto(c, 700, Y, 1.3, t, run=1.0 if t > w("moto") else 0.0)
    stick(c, 420, Y, 1.0, t, arms="point", look=1, **REPA)
    stick(c, 160, Y, 1.0, t, face="scared", look=1, **YOU)
    if t > w("uno") - 0.2: glow(c, 760, 700, 220, "#f2c230", 0.25)
FOCUS["e04"] = (560, 640)

def e05(c, t, T, w):
    supermercado(c, t, light=0.35)
    stick(c, 640, Y, 1.0, t, arms="hug", face="sad", look=-1, **MAMA)
    stick(c, 700, Y, 0.72, t, face="sad", look=-1, seed=4, hair="pony")
    stick(c, 260, Y, 1.0, t, face="scared", look=1, **YOU)
    if t > w("fiebre") - 0.2: glow(c, 700, Y - 230, 120, "#ff5020", 0.3 * (0.6 + 0.4 * math.sin(t * 5)))
FOCUS["e05"] = (560, 660)
CAM["e05"] = [(0.0, 1.0, 540, 620), ("fiebre", 1.5, 680, 700)]

def e06(c, t, T, w):
    k = w("raja")
    techo_vidrio(c, t, crack=ease(clamp((t - k + 0.1) / 0.3)))
    if t > k:
        c.save(); c.rectangle(410, 130, 280, 500); c.clip(); cara_zombi(c, 550, 380, 0.75, t, 1.0); c.restore()
        techo_vidrio_crack = ease(clamp((t - k) / 0.3))
FOCUS["e06"] = (540, 400)
CAM["e06"] = [(0.0, 1.0, 540, 480), ("raja", 1.5, 550, 380)]

def e07(c, t, T, w):
    techo_vidrio(c, t, crack=1.0); overlay(c, "#000", 0.55)

# ---------------- PARTE 3: Día tres ----------------
def f01(c, t, T, w):
    calle_noche(c, t)
    k = w("caer"); x = 100 + 520 * clamp(t / max(0.1, k))
    if t < k: moto(c, x, 880, 0.8, t, run=1); stick(c, x - 10, 800, 0.8, t, sit=True, look=1, **REPA)
    else:
        c.save(); c.translate(620, 880); c.rotate(0.5); moto(c, 0, 0, 0.8, t); c.restore()
        horda(c, 900, 7, 0.8, t, 500, 820, seed=5, look=1, walk=0.3)
    rect(c, 0, 0, 1080, 60, "#0a0c12"); rect(c, 0, 0, 60, 1080, "#0a0c12"); rect(c, 1020, 0, 60, 1080, "#0a0c12")   # marco de ventana
FOCUS["f01"] = (560, 760)
CAM["f01"] = [(0.0, 1.0, 540, 600), ("caer", 1.4, 640, 760)]

def f02(c, t, T, w):
    supermercado(c, t, light=0.6)
    k = w("campana")
    stick(c, 820, Y, 1.05, t, arms="up", face="angry", look=-1, **HECTOR)
    if t > k:
        ring = abs(math.sin(t * 14)); circ(c, 890 + ring * 10, Y - 370, 26, "#e6b422")
        for r_ in (60, 100, 140): c.new_path(); c.arc(890, Y - 370, r_ * (1 + ring * 0.1), -0.9, 0.9); c.set_line_width(4); src(c, hx("#ffe080", 0.5)); c.stroke()
    horda(c, Y, 8, 0.9, t, 40, 620, seed=8, look=1, walk=0.9 if t > k else 0.2)
    if t > w("cede") - 0.1: overlay(c, "#d8e8ff", 0.25 * max(0, 1 - (t - w("cede")) / 0.4))
FOCUS["f02"] = (560, 620)

def f03(c, t, T, w):
    if t < w("callejón") - 0.2:
        supermercado(c, t, light=0.4)
        p = clamp(t / max(0.1, w("callejón")))
        for i, kw in enumerate((YOU, MAMA)): stick(c, 200 + p * 700 - i * 150, Y, 1.0, t, walk=1.0, run=True, look=1, face="scared", **kw)
        stick(c, 200 + p * 700 - 210, Y, 0.72, t, walk=1.0, run=True, look=1, seed=4, hair="pony")
    else:
        callejon(c, t); camion(c, 600, 820, 1.0, t)
        if t > w("ejército") - 0.2: glow(c, 600, 640, 380, "#fff2c0", 0.15)
FOCUS["f03"] = (540, 640)

def f04(c, t, T, w):
    callejon(c, t); camion(c, 900, 840, 0.7, t)
    for i, x in enumerate((180, 300)):
        stick(c, x, Y, 1.0, t, look=1, cap="#4a5a3a", carry=casco_sold, arms="hold", seed=30 + i, hold=linterna if i == 0 else None)
    stick(c, 640, Y, 1.0, t, look=-1, face="scared", arms="up" if t > w("pasas") - 0.3 else "down", **YOU)
    stick(c, 800, Y, 1.0, t, look=-1, face="scared", **MAMA); stick(c, 870, Y, 0.72, t, look=-1, seed=4, hair="pony", face="sad")
FOCUS["f04"] = (540, 660)

def f05(c, t, T, w):
    k = w("tobillo")
    callejon(c, t)
    if t < k - 0.3:
        stick(c, 300, Y, 1.0, t, look=1, cap="#4a5a3a", carry=casco_sold, arms="point", seed=31)
        stick(c, 700, Y, 0.72 * 1.0, t, look=-1, seed=4, hair="pony", face="sad")
    else:                                               # primer plano del tobillo
        vgrad(c, 0, 0, 1080, 1080, "#120a0a", "#05030a")
        line(c, [(540, 0), (540, 700)], SKIN, 70); ell(c, 600, 760, 150, 60, SKIN)
        glow(c, 540, 520, 200, "#ff1020", 0.35)
        for k2 in range(6): circ(c, 500 + k2 * 16, 520 + (k2 % 2) * 22, 9, "#7a0010")
        ell(c, 540, 530, 70, 40, hx("#5a6a50", 0.5))
FOCUS["f05"] = (540, 560)
CAM["f05"] = [(0.0, 1.0, 540, 600), ("tobillo", 1.2, 540, 520)]

def f06(c, t, T, w):
    callejon(c, t)
    k = w("arranca"); go = ease(clamp((t - k) / 1.5))
    camion(c, 600 + 600 * go, 820, 1.0, t)
    stick(c, 380, Y, 1.0, t, arms="hug", look=1, face="sad", **MAMA); stick(c, 440, Y, 0.72, t, look=-1, seed=4, hair="pony", face="sad")
FOCUS["f06"] = (500, 660)

def f07(c, t, T, w):
    callejon(c, t)
    rect(c, 0, 0, 1080, 160, "#3a4a2c"); rect(c, 0, 880, 1080, 200, "#3a4a2c")          # marco: la parte de atrás del camión
    rect(c, 0, 0, 140, 1080, "#3a4a2c"); rect(c, 940, 0, 140, 1080, "#3a4a2c")
    k = w("cabeza")
    s = 0.7
    stick(c, 520, 780, s, t, arms="hug", look=1, face="sad", **MAMA)
    if t < k: stick(c, 570, 780, s * 0.72, t, look=-1, seed=4, hair="pony", face="sad")
    else: stick(c, 570, 780, s, t, kid=True, look=-1, seed=4, zombie=True, col="#9aaa94")
    if t > w("parpadea") - 0.2:
        overlay(c, "#000", 0.6); cara_zombi(c, 540, 540, 1.1, t, 0.4)
FOCUS["f07"] = (540, 640)
CAM["f07"] = [(0.0, 1.0, 540, 600), ("cabeza", 1.5, 560, 640)]

def f08(c, t, T, w):
    callejon(c, t); overlay(c, "#000", 0.55)

PANELS = {k: v for k, v in globals().items() if len(k) == 3 and k[0] in "def" and k[1:].isdigit() and callable(v)}

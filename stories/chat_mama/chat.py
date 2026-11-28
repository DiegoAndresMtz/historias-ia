"""Chat de terror #1 — «Mamá». Historia original."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../engine"))
from lib import hx, rect, rrect, circ, ell, poly, line, glow, vgrad, overlay
import monstruos

HORA = "3:07"
FECHA = "jueves, 27 de noviembre"
NOMBRE = "Mamá"
NOMBRE_GLITCH = "Mamá (2)"
AVATAR_COL = "#c0507a"; AVATAR_TXT = "M"
LOCK_T = 3.0
GANCHO = "Mi mamá está dormida en el cuarto de al lado"
JUMP_DUR = 1.6
ENDCARD_DUR = 3.2
FINAL = ("¿Tú le habrías abierto?", "Sí, era mi mamá", "Nunca")

MSGS = [
    ("in", "hijo ábreme, se me quedaron las llaves"),
    ("in", "está haciendo mucho frío aquí afuera"),
    ("out", "ma?? tú estás dormida en tu cuarto"),
    ("in", "no mi amor, yo apenas voy llegando del turno"),
    ("out", "te acabo de ver. te tapé y todo"),
    ("in", "hijo escúchame bien"),
    ("in", "no entres a mi cuarto"),
    ("glitch",),
    ("in", "eso que está en mi cama no soy yo"),
    ("out", "ma no es chistoso, me estás asustando"),
    ("in", "[mira tu ventana]"),
    ("heart",),
    ("out", "ma... quién está en la ventana de al lado?", 0.8),
    ("in", "NO LO MIRES. baja y ábreme YA"),
    ("out", "ya voy bajando"),
    ("pausa", 1.0),
    ("out", "ma abrí la puerta. no hay nadie afuera"),
    ("in", "gracias por abrirme mi amor", 1.2),
    ("glitch",),
    ("in", "ahora ya somos dos adentro"),
]

def wallpaper(c, t):
    for i in range(40):
        x = (i * 263) % 1080; y = (i * 151) % 900
        circ(c, x, y, 2 + i % 3, hx("#ffffff", 0.25 + 0.2 * math.sin(t * 2 + i)))
    poly(c, [(0, 1500), (300, 1380), (620, 1460), (1080, 1350), (1080, 1920), (0, 1920)], "#0a0814")

def foto(c, w, h, t):
    """Foto tomada desde la calle: tu ventana prendida contigo adentro... y en la de al lado, algo pálido."""
    vgrad(c, 0, 0, w, h, "#05060d", "#141a2c")
    circ(c, w - 90, 80, 34, "#d8dcea")
    rect(c, 40, 170, w - 80, h - 150, "#2a2830")                    # fachada
    poly(c, [(20, 175), (w / 2, 60), (w - 20, 175)], "#3a1e1e")       # techo
    rect(c, 0, h - 40, w, 40, "#0b0b10")
    # tu ventana: luz y tu silueta con el celular
    rect(c, 90, 240, 170, 200, "#f0c060"); glow(c, 175, 340, 200, "#ffb050", 0.35)
    ell(c, 175, 330, 34, 40, "#2a1a14"); rrect(c, 130, 365, 90, 90, 30, "#2a1a14")
    rect(c, 186, 360, 18, 28, "#bfe0ff")
    # ventana de al lado: oscura... con una cara pegada al vidrio
    rect(c, w - 260, 240, 170, 200, "#07070c")
    c.save(); c.rectangle(w - 260, 240, 170, 200); c.clip()
    monstruos.cara_ventana(c, w - 175, 350, 0.3, t, hands=True)
    c.restore()
    line(c, [(w - 260, 340), (w - 90, 340)], "#1a1a22", 6); line(c, [(w - 175, 240), (w - 175, 440)], "#1a1a22", 6)
    line(c, [(90, 340), (260, 340)], "#8a6a30", 6); line(c, [(175, 240), (175, 440)], "#8a6a30", 6)
    rect(c, w / 2 - 50, h - 200, 100, 160, "#3a2418")                  # puerta
    # grano de foto nocturna
    import random; r = random.Random(3)
    for _ in range(700): rect(c, r.uniform(0, w), r.uniform(0, h), 2, 2, hx("#ffffff", r.uniform(0.03, 0.12)))

def monstruo(c, x, y, t):
    monstruos.imitadora(c, x, 820, 2.6, t, open_=1.0, face_skin="#c8b8a8")

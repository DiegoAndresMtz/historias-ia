"""Personajes de palitos (formato «brote zombi», trend de TikTok nov-2026) y zombis.
Todo en coordenadas del panel (1080x1080). y = piso (los pies tocan el suelo: nada flota)."""
import math, random
from lib import hx, src, fill, rect, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp

SKIN = "#f2efe8"; INK = "#14151c"; SCALE = 1.18

def _limb(c, a, b, col, w):
    line(c, [a, b], col, w)

def stick(c, x, y, s, t, col=SKIN, walk=0.0, run=False, arms="down", face="neutral", look=1, cap=None,
          hair=None, kid=False, zombie=False, seed=0, carry=None, hold=None, sit=False):
    """Persona de palitos. walk 0..1 (velocidad del paso), arms: down/up/forward/hold/hug/point/cover/bang."""
    rnd = random.Random(seed)
    sc = s * SCALE * (0.72 if kid else 1.0)
    c.save(); c.translate(x, y); c.scale(sc * look, sc)
    ph = t * (11 if run else 7.5) + seed
    w = 15 if not zombie else 14
    bob = -abs(math.sin(ph)) * 10 * walk
    lean = (0.14 if run else 0.05) * walk
    if zombie:                                  # tirones: el cuerpo se sacude, los pies no se despegan
        j = math.sin(t * 23 + seed) * math.sin(t * 3.1 + seed * 2)
        lean += 0.16 + 0.05 * j
    c.translate(0, bob)
    hip = (0, -130); sh = (math.sin(lean) * 100, -230)
    # piernas
    for k, sgn in enumerate((1, -1)):
        a = math.sin(ph) * sgn * (0.55 if run else 0.4) * walk
        if sit: knee = (sgn * 18 + 70, -130); foot = (sgn * 18 + 75, -20)
        else:
            knee = (hip[0] + math.sin(a) * 60, hip[1] + math.cos(a) * 62)
            foot = (knee[0] + math.sin(a - abs(a) * 0.6) * 62, 0)
        _limb(c, hip, knee, col, w); _limb(c, knee, foot, col, w)
        ell(c, foot[0] + 10, -4, 16, 7, col)
    # torso
    _limb(c, hip, sh, col, w + 3)
    # brazos
    def hand(i):
        sg = 1 if i == 0 else -1
        sw = math.sin(ph + math.pi * i) * 0.5 * walk
        if zombie or arms == "forward":
            jj = math.sin(t * 9 + i * 2 + seed) * 8 if zombie else 0
            return (sh[0] + 95, sh[1] + 25 + i * 18 + jj), (sh[0] + 50, sh[1] + 15 + i * 10)
        if arms == "up": return (sh[0] + sg * 70, sh[1] - 95), (sh[0] + sg * 45, sh[1] - 45)
        if arms == "hold": return (sh[0] + 60, sh[1] + 70 - i * 10), (sh[0] + 30 * sg + 30, sh[1] + 55)
        if arms == "hug": return (sh[0] + 70, sh[1] + 40), (sh[0] + 60, sh[1] + 5)
        if arms == "point": return ((sh[0] + 110, sh[1] - 30), (sh[0] + 55, sh[1] - 12)) if i == 0 else ((sh[0] - 25, sh[1] + 90), (sh[0] - 22, sh[1] + 45))
        if arms == "cover": return (sh[0] + 10 + 18 * sg, sh[1] - 45), (sh[0] + 45, sh[1] + 30)
        if arms == "bang":
            k = abs(math.sin(t * 9 + i * 1.6 + seed))
            return (sh[0] + 85 + 15 * k, sh[1] - 60 + 30 * k), (sh[0] + 45, sh[1] - 10)
        return (sh[0] + sg * 30 + math.sin(sw) * 60, sh[1] + 100), (sh[0] + sg * 20 + math.sin(sw) * 30, sh[1] + 50)
    for i in (1, 0):
        hnd, elb = hand(i)
        _limb(c, sh, elb, col, w - 2); _limb(c, elb, hnd, col, w - 2); circ(c, hnd[0], hnd[1], 9, col)
    if carry: carry(c, sh)
    # cabeza
    hx_, hy_ = sh[0] + math.sin(lean) * 20, sh[1] - 52
    tilt = (0.35 + 0.15 * math.sin(t * 17 + seed) * math.sin(t * 2.3)) if zombie else 0.05 * math.sin(t * 1.3 + seed)
    c.save(); c.translate(hx_, hy_); c.rotate(tilt)
    HC = "#2a1e18"
    if hair == "long": rrect(c, -48, -30, 96, 110, 40, HC)                      # pelo largo por detrás
    if hair == "pony": ell(c, -50, 6, 14, 30, HC)
    circ(c, 0, 0, 40, col)
    if hair in ("long", "pony"):
        c.new_path(); c.arc(0, -4, 42, math.pi * 1.02, math.pi * 1.98); c.close_path(); fill(c, HC)
    if cap: c.new_path(); c.arc(0, -6, 41, math.pi, 2 * math.pi); c.close_path(); fill(c, cap); rect(c, -42, -10, 84, 10, hx(cap, 1)); circ(c, 0, -48, 9, cap)
    ex = 15
    if zombie:
        for sx in (-1, 1):
            circ(c, 12 + sx * ex, -4, 9, "#1a0000"); glow(c, 12 + sx * ex, -4, 22, "#ff2020", 0.5); circ(c, 12 + sx * ex, -4, 4, "#ff3030")
        poly(c, [(-2, 14), (30, 10), (34, 26), (0, 28)], "#1a0000")
        for k in range(4): poly(c, [(2 + k * 8, 14), (6 + k * 8, 14), (4 + k * 8, 20)], "#e8e0c0")
        line(c, [(-28, -24), (-12, -8)], "#5a6a50", 3); line(c, [(-30, 6), (-20, 20)], "#5a6a50", 3)
    else:
        blink = (t + seed * 0.37) % 3.4 < 0.12
        big = face in ("shock", "scared")
        for sx in (-1, 1):
            if blink: line(c, [(12 + sx * ex - 6, -4), (12 + sx * ex + 6, -4)], INK, 4)
            else:
                circ(c, 12 + sx * ex, -4, 9 if big else 6, INK)
                if big: circ(c, 14 + sx * ex, -6, 3, "#ffffff")
        if face == "shock": ell(c, 16, 20, 9, 12, INK)
        elif face == "scared": line(c, [(4, 22), (12, 18), (20, 22), (28, 18)], INK, 4)
        elif face == "sad": c.new_path(); c.arc(16, 30, 12, math.pi * 1.15, math.pi * 1.85); c.set_line_width(4); src(c, INK); c.stroke()
        elif face == "angry": line(c, [(0, -20), (14, -14)], INK, 4); line(c, [(22, -14), (36, -20)], INK, 4); line(c, [(6, 22), (28, 22)], INK, 4)
        else: c.new_path(); c.arc(16, 12, 10, math.pi * 0.15, math.pi * 0.85); c.set_line_width(4); src(c, INK); c.stroke()
        if face in ("shock", "scared"):
            for k in range(2): circ(c, -30 + k * 6, -16 + k * 14, 4, hx("#9ad0ff", 0.8))
    c.restore()
    if hold: hold(c, hand(0)[0])
    c.restore()

def zombi(c, x, y, s, t, seed=0, walk=0.6, look=-1, col="#8a9e84", lunge=0.0):
    stick(c, x + math.sin(t * 2 + seed) * 4, y, s, t, col=col, walk=walk, zombie=True, look=look, seed=seed)

def horda(c, y, n, s, t, x0=0, x1=1080, seed=0, look=-1, walk=0.5, dark=0.0):
    r = random.Random(seed)
    items = sorted([(r.uniform(x0, x1), r.uniform(-30, 30), r.randint(0, 99)) for _ in range(n)], key=lambda q: q[1])
    for xx, dy, sd in items:
        col = ["#7d927a", "#8a9e84", "#6f8470", "#94a08a"][sd % 4]
        if dark: col = hx(col, 1)
        zombi(c, xx, y + dy, s * (1 + dy / 300), t, seed=sd, walk=walk, look=look, col=col)
    if dark: overlay(c, "#000", dark)

def cara_zombi(c, x, y, s, t, open_=0.6):
    """Primer plano de zombi: piel gris verdosa, venas, ojos rojos, boca abierta con dientes."""
    c.save(); c.translate(x + math.sin(t * 31) * 3, y); c.scale(s, s); c.rotate(0.12 * math.sin(t * 5) * math.sin(t * 13))
    ell(c, 0, 0, 260, 300, "#7c8f78"); ell(c, -40, -40, 200, 240, hx("#94a690", 0.6))
    r = random.Random(4)
    for _ in range(14):
        a = r.uniform(0, 6.28); x0 = math.cos(a) * 200; y0 = math.sin(a) * 240
        line(c, [(x0, y0), (x0 * 0.8 + r.uniform(-30, 30), y0 * 0.8 + r.uniform(-30, 30)), (x0 * 0.6, y0 * 0.6)], "#4a5e48", 4)
    for sx in (-1, 1):
        ell(c, sx * 95, -50, 70, 58, "#1a1010"); glow(c, sx * 95, -45, 90, "#ff1a1a", 0.6)
        circ(c, sx * 95, -45, 26, "#ff2a2a"); circ(c, sx * 95, -45, 9, "#2a0000")
        line(c, [(sx * 40, -130), (sx * 150, -110)], "#3a4636", 14)
    op = 60 + 90 * open_ * (0.8 + 0.2 * math.sin(t * 7))
    ell(c, 0, 150, 150, op, "#1a0000")
    for k in range(9):
        xx = -120 + k * 30
        poly(c, [(xx, 150 - op * 0.8), (xx + 26, 150 - op * 0.8), (xx + 13, 150 - op * 0.8 + 40)], "#e6dcb8")
        poly(c, [(xx, 150 + op * 0.8), (xx + 26, 150 + op * 0.8), (xx + 13, 150 + op * 0.8 - 36)], "#d6caa0")
    for k in range(3): line(c, [(-60 + k * 50, 150 + op * 0.8), (-58 + k * 50, 150 + op * 0.8 + 40 + k * 20)], "#6a0000", 7)
    c.restore()

# ---------------- escenarios ----------------
def lamparas(c, t, y=70, n=4, on=1.0, flick_seed=0):
    for i in range(n):
        x = 135 + i * 270
        f = on * (0.75 + 0.25 * math.sin(t * 40 + i * 3 + flick_seed) if (int(t * 6 + i * 7 + flick_seed) % 11) else 0.15)
        rect(c, x - 90, y, 180, 14, hx("#f4f8ff", 0.4 + 0.6 * f)); glow(c, x, y + 10, 340, "#dfe8ff", 0.16 * f)

def supermercado(c, t, light=1.0, cola=True):
    vgrad(c, 0, 0, 1080, 1080, "#2a2e38", "#14161c")
    rect(c, 0, 760, 1080, 320, "#22252c")
    for i in range(12): line(c, [(i * 100 - 200, 1080), (540 + (i - 6) * 30, 760)], "#2c3038", 3)
    for k, xx in enumerate((40, 760)):                     # estanterías
        rect(c, xx, 260, 280, 500, "#3a3f4a")
        for r_ in range(5):
            rect(c, xx, 290 + r_ * 95, 280, 8, "#555b68")
            for j in range(7):
                col = ["#c0392b", "#e6b422", "#2e86c1", "#27ae60", "#f39c12", "#8e44ad", "#ecf0f1"][(j + r_ + k) % 7]
                rect(c, xx + 10 + j * 38, 300 + r_ * 95 - 52, 30, 52, hx(col, 0.85))
    rect(c, 380, 200, 320, 46, "#c0392b");
    lamparas(c, t, on=light)
    overlay(c, "#000", 0.25 * (1 - light) + 0.15)

def caja(c, x, y):
    rect(c, x, y - 150, 300, 150, "#4a505c"); rect(c, x, y - 160, 300, 16, "#6a707c")
    rect(c, x + 200, y - 230, 70, 70, "#2a2e36"); rect(c, x + 208, y - 222, 54, 40, "#5ad0ff")

def reja(c, t, x0=0, x1=1080, y0=120, y1=780, down=1.0, shake=0.0):
    h = (y1 - y0) * down; dx = math.sin(t * 40) * shake * 6
    c.save(); c.translate(dx, 0)
    for i in range(int((x1 - x0) / 36) + 1):
        line(c, [(x0 + i * 36, y0), (x0 + i * 36, y0 + h)], "#8a8f99", 6)
    for j in range(int(h / 60) + 1):
        line(c, [(x0, y0 + j * 60), (x1, y0 + j * 60)], "#a0a5ae", 5)
    rect(c, x0, y0 + h - 16, x1 - x0, 18, "#b8bcc4")
    c.restore()

def cuarto_frio(c, t, knock=0.0):
    vgrad(c, 0, 0, 1080, 1080, "#1e2630", "#0e1218")
    rect(c, 0, 820, 1080, 260, "#1a1e24")
    dx = math.sin(t * 50) * 6 * knock
    rect(c, 330 + dx, 220, 420, 600, "#b8c4cc"); rect(c, 350 + dx, 240, 380, 560, "#a8b4bc")
    rect(c, 690 + dx, 470, 26, 120, "#5a646c")
    rect(c, 330, 160, 420, 50, "#2a6aa0")
    if knock > 0: glow(c, 540, 820, 300, "#9ad0ff", 0.12 * knock)
    lamparas(c, t, y=40, n=3)

def techo_vidrio(c, t, crack=0.0):
    vgrad(c, 0, 0, 1080, 1080, "#05070c", "#0c1220")
    for i in range(3):
        rect(c, 60 + i * 340, 120, 300, 520, "#101828"); rect(c, 70 + i * 340, 130, 280, 500, hx("#3a5070", 0.35))
    r = random.Random(9)
    if crack > 0:
        for _ in range(int(30 * crack)):
            x0 = r.uniform(380, 700); y0 = r.uniform(200, 560); a = r.uniform(0, 6.3); L_ = r.uniform(40, 160) * crack
            line(c, [(x0, y0), (x0 + math.cos(a) * L_, y0 + math.sin(a) * L_)], "#d8e8ff", 3)

def calle_noche(c, t, sirena=0.0):
    vgrad(c, 0, 0, 1080, 1080, "#070912", "#151a28")
    for i in range(5):
        h = 300 + (i * 97) % 260; rect(c, i * 230 - 20, 760 - h, 200, h, "#0c0f18")
        for k in range(int(h / 70)):
            if (i + k) % 3 == 0: rect(c, i * 230 + 20 + (k % 2) * 90, 790 - h + k * 70, 50, 34, hx("#f0c060", 0.35))
    rect(c, 0, 760, 1080, 320, "#191c24"); rect(c, 0, 900, 1080, 10, "#c8b040")
    if sirena:
        f = 0.5 + 0.5 * math.sin(t * 12); glow(c, 200, 600, 500, "#ff2030", 0.25 * f * sirena); glow(c, 880, 600, 500, "#2050ff", 0.25 * (1 - f) * sirena)

def camion(c, x, y, s, t, luces=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -380, -330, 500, 290, "#4a5a3a"); rect(c, -380, -340, 500, 20, "#3a4a2c")
    for k in range(6): line(c, [(-370 + k * 90, -330), (-370 + k * 90, -40)], "#3e4c30", 6)
    rect(c, 120, -250, 220, 210, "#55683f"); rect(c, 160, -230, 140, 90, "#9ab0c8")
    for wx in (-250, 230): circ(c, wx, -30, 62, "#15161a"); circ(c, wx, -30, 24, "#5a5c62")
    if luces: glow(c, 350, -100, 260, "#fff2c0", 0.35 * luces)
    c.restore()

def moto(c, x, y, s, t, run=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for wx in (-110, 110):
        circ(c, wx, -50, 50, "#15161a"); circ(c, wx, -50, 18, "#6a6c72")
    poly(c, [(-120, -90), (40, -120), (120, -90), (90, -60), (-90, -60)], "#c0392b")
    rect(c, -10, -150, 90, 40, "#e8702a"); line(c, [(110, -60), (90, -170)], "#2a2a30", 10)
    if run: glow(c, 160, -110, 200, "#fff2c0", 0.4)
    c.restore()

def callejon(c, t):
    vgrad(c, 0, 0, 1080, 1080, "#06070c", "#12151e")
    poly(c, [(0, 0), (300, 200), (300, 800), (0, 1080)], "#0c0e14"); poly(c, [(1080, 0), (780, 200), (780, 800), (1080, 1080)], "#0c0e14")
    poly(c, [(300, 800), (780, 800), (1080, 1080), (0, 1080)], "#1a1d26")
    rect(c, 360, 640, 90, 150, "#2a3a2a"); rect(c, 620, 600, 110, 190, "#22262e")

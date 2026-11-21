import math, random
import cairocffi as cairo
W, H, FPS = 1080, 1920, 30

def hx(h, a=1.0):
    if not isinstance(h, str): return h
    h = h.lstrip("#")
    if len(h) == 3: h = "".join(ch * 2 for ch in h)
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)
def src(c, col): c.set_source_rgba(*hx(col))
def fill(c, col): src(c, col); c.fill()
def rect(c, x, y, w, h, col): c.rectangle(x, y, w, h); fill(c, col)
def rrect_path(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()
def rrect(c, x, y, w, h, r, col): rrect_path(c, x, y, w, h, r); fill(c, col)
def circ(c, x, y, r, col): c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); fill(c, col)
def ell(c, x, y, rx, ry, col):
    c.new_path(); c.save(); c.translate(x, y); c.scale(max(rx, .01), max(ry, .01)); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); fill(c, col)
def poly(c, pts, col):
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.close_path(); fill(c, col)
def line(c, pts, col, w, cap=True):
    c.new_path(); c.set_line_width(w)
    if cap: c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    src(c, col); c.stroke()
def glow(c, x, y, r, col, a):
    if a <= 0 or r <= 0: return
    g = cairo.RadialGradient(x, y, 0, x, y, r); rr, gg, bb, _ = hx(col)
    g.add_color_stop_rgba(0, rr, gg, bb, a); g.add_color_stop_rgba(0.35, rr, gg, bb, a * 0.4); g.add_color_stop_rgba(1, rr, gg, bb, 0)
    c.new_path(); c.set_source(g); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
def vgrad(c, x, y, w, h, top, bot):
    g = cairo.LinearGradient(0, y, 0, y + h); g.add_color_stop_rgba(0, *hx(top)); g.add_color_stop_rgba(1, *hx(bot))
    c.new_path(); c.set_source(g); c.rectangle(x, y, w, h); c.fill()
def overlay(c, col, a):
    if a > 0: c.set_source_rgba(*hx(col, min(1, a))); c.paint()
def flick(t, seed=0): return 0.86 + 0.07 * math.sin(t * 13 + seed) + 0.05 * math.sin(t * 29.3 + seed * 2) + 0.03 * math.sin(t * 7.1)
def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def cam(c, z, cx=W / 2, cy=H / 2, dx=0, dy=0): c.translate(cx + dx, cy + dy); c.scale(z, z); c.translate(-cx, -cy)
def shake(c, t, amp, f=38):
    if amp > 0: c.translate(amp * math.sin(t * f) + amp * 0.5 * math.sin(t * f * 1.7), amp * math.cos(t * f * 1.3))
def text_w(c, s): return c.text_extents(s)[4]

rng = random.Random(11)
STARS = [(rng.uniform(0, W), rng.uniform(0, H * 0.5), rng.uniform(1.2, 3.0), rng.uniform(0, 6)) for _ in range(110)]
FLIES = [(rng.uniform(0, W), rng.uniform(900, 1500), rng.uniform(0, 6.28), rng.uniform(0.3, 0.9)) for _ in range(26)]
DUST = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0, 6.28), rng.uniform(1, 3)) for _ in range(60)]

# ---------------- environment ----------------
def sky(c, t, top="#03040b", bot="#1a2140", stars=True, sa=1.0):
    vgrad(c, 0, 0, W, H, top, bot)
    if stars:
        for x, y, r, ph in STARS: circ(c, x, y, r, hx("#d8deff", sa * (0.3 + 0.3 * math.sin(t * 1.4 + ph))))
def moon(c, x, y, r, a=1.0):
    glow(c, x, y, r * 4.5, "#bcd0ff", 0.22 * a); circ(c, x, y, r, hx("#e9eefc", a))
    circ(c, x - r * 0.3, y - r * 0.2, r * 0.18, hx("#cfd6ea", a)); circ(c, x + r * 0.25, y + r * 0.3, r * 0.12, hx("#cfd6ea", a))
def mountains(c, base, cols=("#0d1226", "#080b19")):
    poly(c, [(0, base), (0, base - 300), (200, base - 520), (420, base - 360), (650, base - 640), (880, base - 420), (W, base - 540), (W, base)], cols[0])
    poly(c, [(0, base), (0, base - 200), (280, base - 360), (520, base - 230), (780, base - 430), (W, base - 260), (W, base)], cols[1])
def bushes(c, y, n, r, col, seed=0, jitter=10, xoff=0):
    rr = random.Random(seed)
    for i in range(n):
        x = (i + 0.5) * W / n + rr.uniform(-jitter, jitter) + xoff
        ell(c, x, y + rr.uniform(-6, 6), r * rr.uniform(0.85, 1.15), r * 0.8, col)
        circ(c, x - r * 0.35, y - r * 0.45, r * 0.55, col); circ(c, x + r * 0.3, y - r * 0.5, r * 0.5, col)
def banana(c, x, y, s, col="#06100b", t=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    poly(c, [(-14, 0), (14, 0), (9, -330), (-9, -330)], col)
    sw = math.sin(t * 0.9) * 0.05
    for ang, ln in ((-2.4, 230), (-1.9, 260), (-1.2, 250), (-0.7, 220), (-2.9, 200), (-0.2, 190)):
        a = ang + sw
        x1, y1 = math.cos(a) * ln, -330 + math.sin(a) * ln
        c.new_path(); c.move_to(0, -330); c.curve_to(math.cos(a - .3) * ln * .5, -330 + math.sin(a - .3) * ln * .5, x1 * 0.9, y1 - 30, x1, y1 + 10)
        c.curve_to(x1 * 0.7, y1 + 40, math.cos(a + .3) * ln * .4, -330 + math.sin(a + .3) * ln * .4, 0, -330); fill(c, col)
    c.restore()
def fog(c, y, t, a=0.18, col="#b7c3e6", speed=12, n=6, h=90):
    for i in range(n):
        x = ((i * 260 + t * speed * (1 + i % 3 * 0.4)) % (W + 700)) - 350
        g = cairo.RadialGradient(x, y + (i % 3) * 30, 0, x, y + (i % 3) * 30, 340)
        rr, gg, bb, _ = hx(col); g.add_color_stop_rgba(0, rr, gg, bb, a); g.add_color_stop_rgba(1, rr, gg, bb, 0)
        c.save(); c.translate(0, y); c.scale(1, h / 340); c.translate(0, -y)
        c.new_path(); c.set_source(g); c.arc(x, y + (i % 3) * 30, 340, 0, 2 * math.pi); c.fill(); c.restore()
def fireflies(c, t, a=1.0, ymin=0, ymax=H):
    for x, y, ph, sp in FLIES:
        if not (ymin <= y <= ymax): continue
        xx = x + math.sin(t * sp + ph) * 40; yy = y + math.cos(t * sp * 0.7 + ph) * 30
        b = clamp(math.sin(t * 2.2 * sp + ph * 3)) * a
        if b > 0.05: glow(c, xx, yy, 22, "#d8ff7a", 0.55 * b); circ(c, xx, yy, 2.5, hx("#f4ffc0", b))
def motes(c, t, a=0.25, col="#ffd9a0"):
    for x, y, ph, r in DUST:
        circ(c, (x + math.sin(t * .3 + ph) * 30) % W, (y - t * 12 * r) % H, r, hx(col, a * (0.5 + 0.5 * math.sin(t + ph))))
def bulb(c, x, y, t, on=1.0, r=520, swing=0.0, wire=300):
    ang = math.sin(t * 1.3) * swing
    bx, by = x + math.sin(ang) * wire, y - wire + math.cos(ang) * wire
    line(c, [(x, y - wire), (bx, by - 20)], "#151110", 3)
    if on > 0: glow(c, bx, by, r * flick(t, 3), "#ffb35c", 0.5 * on)
    rect(c, bx - 9, by - 30, 18, 16, "#3a3a3a")
    ell(c, bx, by, 18, 22, hx("#fff1c4", 0.35 + 0.65 * on) if on > 0 else "#3d3a36")
    return bx, by
def moths(c, x, y, t, n=4):
    for i in range(n):
        a = t * (2.5 + i * 0.7) + i * 1.7
        mx, my = x + math.cos(a) * (50 + i * 14), y + math.sin(a * 1.3) * (35 + i * 9)
        w = abs(math.sin(t * 30 + i)) * 7 + 2
        ell(c, mx - 4, my, w, 3, "#5a4a3a"); ell(c, mx + 4, my, w, 3, "#5a4a3a")

def finca(c, x, y, s, t, bulb_on=1.0, wall="#7f7c8e", roof="#5c2a22", door_lit=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -400, -340, 800, 340, wall)
    for i in range(-400, 400, 18): rect(c, i, -340, 1, 340, hx("#000", 0.05))
    rect(c, -400, -60, 800, 60, hx("#3d3240"))
    rect(c, -60, -260, 120, 260, "#2b1b12" if door_lit <= 0 else hx("#ffb35c", door_lit))
    rect(c, -60, -260, 120, 8, "#1a110b")
    for wx in (-270, 190):
        rect(c, wx, -260, 80, 110, "#0d0f1a")
        rect(c, wx - 34, -264, 32, 118, "#2c4d3c"); rect(c, wx + 82, -264, 32, 118, "#2c4d3c")
    c.restore()
    if bulb_on > 0: glow(c, x + 120 * s, y - 300 * s, 430 * s * flick(t, 1), "#ffae55", 0.42 * bulb_on)
    c.save(); c.translate(x, y); c.scale(s, s)
    poly(c, [(-470, -335), (470, -335), (390, -480), (-390, -480)], roof)
    for i in range(-460, 470, 26):
        line(c, [(i, -335), (i * 0.83, -480)], hx("#000", 0.18), 2, cap=False)
    rect(c, -480, -345, 960, 14, "#3d1c16")
    for cx in (-360, -180, 180, 360): rect(c, cx - 11, -335, 22, 335, "#3b2a1d")
    rect(c, -420, -8, 840, 14, "#2a2320")
    if bulb_on > 0:
        line(c, [(120, -335), (120, -305)], "#111", 2); circ(c, 120, -296, 9, hx("#fff1c4", bulb_on))
    c.restore()

def tranquera(c, x, y, s, col="#3b2a1d"):
    c.save(); c.translate(x, y); c.scale(s, s)
    rect(c, -12, -230, 24, 230, col); rect(c, 300, -230, 24, 230, col)
    for yy in (-200, -140, -80): rect(c, 0, yy, 312, 18, col)
    line(c, [(10, -60), (300, -200)], col, 16, cap=False)
    c.restore()

def truck(c, x, y, s, t, wheel_rot=0.0, lights=0.0, driver=0.0, col="#4f5f3a"):
    c.save(); c.translate(x, y); c.scale(s, s)
    ell(c, 0, 0, 330, 18, hx("#000", 0.35))
    rrect(c, -330, -170, 660, 110, 18, col)
    rrect(c, -330, -190, 230, 50, 16, col)
    rrect(c, -150, -300, 200, 140, 24, col)
    rrect(c, -125, -280, 150, 92, 14, "#1a2230")
    if driver > 0:
        circ(c, -50, -232, 30, hx("#050506", driver)); ell(c, -50, -258, 54, 9, hx("#050506", driver)); rrect(c, -78, -296, 56, 40, 10, hx("#050506", driver))
    rect(c, 60, -210, 270, 30, hx("#000", 0.18)); rect(c, 60, -232, 270, 22, col)
    rect(c, -340, -95, 680, 22, "#2b2b2b")
    rect(c, -334, -150, 18, 26, "#f3e3a4" if lights > 0 else "#9a937b")
    rect(c, 322, -150, 12, 26, "#a0302a")
    for wx in (-200, 200):
        circ(c, wx, -50, 62, "#141414"); circ(c, wx, -50, 30, "#6d6d6d")
        for k in range(4):
            a = wheel_rot + k * math.pi / 2
            line(c, [(wx, -50), (wx + math.cos(a) * 26, -50 + math.sin(a) * 26)], "#3a3a3a", 6)
    c.restore()
    if lights > 0:
        g = cairo.LinearGradient(x - 340 * s, 0, x - 900 * s, 0); g.add_color_stop_rgba(0, 1, .93, .7, .45 * lights); g.add_color_stop_rgba(1, 1, .93, .7, 0)
        c.new_path(); c.move_to(x - 335 * s, y - 145 * s); c.line_to(x - 950 * s, y - 230 * s); c.line_to(x - 950 * s, y - 20 * s); c.close_path(); c.set_source(g); c.fill()

# ---------------- characters ----------------
SKIN = "#c08a5e"; HAIR = "#1b1412"
def eyes_pair(c, x, y, r, gap, look=(0, 0), blink=False, glow_e=False, scared=0.0):
    for sx in (-gap, gap):
        if glow_e:
            glow(c, x + sx, y, r * 2.6, "#ffffff", 0.35); ell(c, x + sx, y, r * 0.9, r * 0.5, "#f8f8f8"); continue
        if blink:
            line(c, [(x + sx - r, y), (x + sx + r, y)], "#1a1110", 6); continue
        rr = r * (1 + 0.18 * scared)
        circ(c, x + sx, y, rr, "#f5f1e8")
        pr = r * (0.42 - 0.17 * scared)
        circ(c, x + sx + look[0] * r * 0.42, y + look[1] * r * 0.42, pr, "#120c0a")
        circ(c, x + sx + look[0] * r * 0.42 - pr * 0.35, y + look[1] * r * 0.42 - pr * 0.35, pr * 0.3, "#ffffff")
def brows(c, x, y, gap, scared, col="#1b1412", w=6):
    for sx in (-1, 1):
        inner = y - 10 * scared; outer = y + 4 * scared
        line(c, [(x + sx * (gap + 26), outer), (x + sx * (gap - 22), inner)], col, w)
def mouth(c, x, y, talk=0.0, w=26, scared=0.0):
    if scared > 0.5: ell(c, x, y + 4, w * 0.38, w * 0.48 * scared, "#2a0f0c"); return
    if talk > 0.05: ell(c, x, y, w * 0.6, 4 + talk * 14, "#3a1410"); return
    line(c, [(x - w / 2, y), (x + w / 2, y + 2 * scared)], "#3a1a12", 5)

def arm(c, pts, col, w=44, hand=SKIN, hr=21):
    line(c, pts, col, w); circ(c, pts[-1][0], pts[-1][1], hr, hand)

def joven(c, x, y, s, t, look=(0, 0), scared=0.0, arms="down", blink=None, shirt="#8c2f2a", shake_a=0.0, run=None, pants="#2f3d5c", hair="spiky", glasses=False, skin=None, plaid=True, glove=0.0):
    global SKIN
    _sk = SKIN
    if skin: SKIN = skin
    c.save(); c.translate(x, y); c.scale(s, s)
    if run is not None: c.translate(0, -abs(math.sin(run)) * 14)
    if shake_a > 0: c.translate(math.sin(t * 61) * 4 * shake_a, math.cos(t * 47) * 2 * shake_a)
    br = math.sin(t * 2.1) * (1 + scared * 1.5)
    ll = max(0, math.sin(run)) * 50 if run is not None else 0
    lr = max(0, -math.sin(run)) * 50 if run is not None else 0
    rect(c, -60, -230, 52, 230 - ll, pants); rect(c, 8, -230, 52, 230 - lr, pants)
    rect(c, -8, -230, 16, 40, pants)
    ell(c, -36, -2 - ll, 40, 14, "#1a1412"); ell(c, 36, -2 - lr, 40, 14, "#1a1412")
    c.save(); c.translate(0, -225); c.scale(1 + 0.004 * br, 1 + 0.012 * br); c.translate(0, 225)
    rrect(c, -88, -460, 176, 250, 34, shirt)
    c.save(); rrect_path(c, -88, -460, 176, 250, 34); c.clip()
    if plaid:
        for i in range(-88, 90, 34): rect(c, i, -460, 9, 250, hx("#000", 0.16))
        for j in range(-460, -210, 40): rect(c, -88, j, 176, 8, hx("#000", 0.13))
    c.restore()
    rect(c, -88, -232, 176, 18, "#3a2a20")
    poly(c, [(-26, -460), (0, -428), (26, -460)], hx("#000", 0.25))
    sh_l, sh_r = (-80, -440), (80, -440)
    if arms == "down":
        sw = math.sin(t * 2.1) * 2
        arm(c, [sh_l, (-104, -340), (-100 + sw, -250)], shirt); arm(c, [sh_r, (104, -340), (100 - sw, -250)], shirt)
    elif arms == "paper":
        arm(c, [sh_l, (-108, -350), (-58, -310)], shirt); arm(c, [sh_r, (108, -350), (58, -310)], shirt)
        c.save(); c.translate(0, -330); c.rotate(-0.05)
        rect(c, -70, -95, 140, 110, "#efe6cf")
        for k in range(5): rect(c, -55, -78 + k * 18, 90 - (k % 2) * 25, 5, hx("#3a2c22", 0.6))
        c.restore()
        circ(c, -58, -305, 21, SKIN); circ(c, 58, -305, 21, SKIN)
    elif arms == "switch":
        arm(c, [sh_l, (-104, -340), (-100, -250)], shirt)
        arm(c, [sh_r, (170, -430), (235, -455)], shirt)
    elif arms == "phone":
        arm(c, [sh_l, (-104, -340), (-100, -250)], shirt)
        arm(c, [sh_r, (140, -400), (100, -520)], shirt)
    elif arms == "run":
        sw = math.sin(run if run is not None else t * 8) * 45
        arm(c, [sh_l, (-112, -350 - sw * 0.3), (-96, -290 - sw)], shirt); arm(c, [sh_r, (112, -350 + sw * 0.3), (96, -290 + sw)], shirt)
    elif arms == "raise":
        arm(c, [sh_l, (-104, -340), (-100, -250)], shirt)
        hc = "#2a2a2e" if glove > 0.5 else SKIN
        arm(c, [sh_r, (170, -520), (150, -660)], shirt, hand=hc, hr=26)
    elif arms == "wave":
        arm(c, [sh_l, (-104, -340), (-100, -250)], shirt)
        wv = math.sin(t * 7) * 30
        arm(c, [sh_r, (150, -560), (130 + wv, -700)], shirt)
    elif arms == "envelope":
        arm(c, [sh_l, (-104, -340), (-100, -250)], shirt)
        arm(c, [sh_r, (110, -340), (40, -320)], shirt)
        c.save(); c.translate(30, -330); c.rotate(-0.15); rect(c, -50, -30, 100, 60, "#e8dcc0"); poly(c, [(-50, -30), (0, 5), (50, -30)], "#cdbd9c"); c.restore()
        circ(c, 40, -318, 21, SKIN)
    elif arms == "cover":
        arm(c, [sh_l, (-130, -350), (-30, -490)], shirt, hand=shirt); arm(c, [sh_r, (130, -350), (30, -490)], shirt, hand=shirt)
    elif arms == "phone_front":
        arm(c, [sh_l, (-104, -340), (-100, -250)], shirt)
        arm(c, [sh_r, (110, -340), (40, -330)], shirt)
        rrect(c, 8, -410, 52, 96, 10, "#111"); rect(c, 13, -403, 42, 82, "#bcd6ff")
        circ(c, 40, -325, 21, SKIN)
    c.restore()
    rect(c, -22, -488, 44, 40, SKIN)
    hy = -555
    circ(c, -80, hy + 5, 17, SKIN); circ(c, 80, hy + 5, 17, SKIN)
    circ(c, 0, hy, 82, SKIN)
    c.new_path(); c.arc(0, hy - 8, 86, math.pi * 1.04, math.pi * 1.96); c.close_path(); fill(c, HAIR)
    if hair == "spiky":
        poly(c, [(-86, hy - 14), (-52, hy - 44), (-24, hy - 18), (8, hy - 48), (40, hy - 20), (84, hy - 38), (70, hy - 78), (-70, hy - 78)], HAIR)
    elif hair == "side":
        poly(c, [(-88, hy - 10), (-70, hy - 70), (20, hy - 96), (88, hy - 50), (86, hy - 20), (30, hy - 52), (-40, hy - 40)], HAIR)
    elif hair == "gray":
        c.new_path(); c.arc(0, hy - 8, 86, math.pi * 1.04, math.pi * 1.96); c.close_path(); fill(c, "#7d7a78")
        poly(c, [(-88, hy - 10), (-70, hy - 70), (20, hy - 96), (88, hy - 50), (86, hy - 20), (30, hy - 52), (-40, hy - 40)], "#8c8987")
    b = (blink if blink is not None else ((t % 3.9) < 0.11)) and scared < 0.7
    eyes_pair(c, 0, hy + 2, 23, 32, look=look, blink=b, scared=scared)
    brows(c, 0, hy - 34, 32, scared)
    ell(c, 0, hy + 30, 7, 5, hx("#8a5a3a", 0.7))
    mouth(c, 0, hy + 52, 0, 24, scared)
    if glasses:
        for gx in (-32, 32):
            c.new_path(); c.arc(gx, hy + 2, 30, 0, 2 * math.pi); c.set_line_width(6); src(c, "#1a1a1a"); c.stroke()
        line(c, [(-2, hy), (2, hy)], "#1a1a1a", 6)
    if scared > 0.6:
        dy = (t * 40) % 60
        ell(c, 70, hy - 30 + dy, 6, 10, hx("#bfe3ff", 0.8))
    if arms == "cover":
        ell(c, -24, -500, 30, 24, "#9c6a45"); ell(c, 24, -500, 30, 24, "#a8754f")
        for k in range(3): line(c, [(-8 - k * 14, -520), (-8 - k * 14, -484)], hx("#000", 0.2), 2)
    if arms == "phone":
        c.save(); c.translate(84, -575); c.rotate(0.25)
        rrect(c, -20, -50, 40, 100, 9, "#111"); rect(c, -15, -44, 30, 88, hx("#6ea8ff", 0.85)); c.restore()
        circ(c, 100, -520, 22, SKIN)
    c.restore()
    SKIN = _sk

def joven_back(c, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    br = math.sin(t * 2.1)
    c.save(); c.scale(1, 1 + 0.01 * br)
    rrect(c, -170, -150, 340, 300, 60, "#5e1f1c")
    for i in range(-170, 170, 40): rect(c, i, -150, 10, 300, hx("#000", 0.2))
    c.restore()
    rect(c, -34, -200, 68, 70, "#8a6040")
    circ(c, -82, -270, 18, "#8a6040"); circ(c, 82, -270, 18, "#8a6040")
    circ(c, 0, -280, 88, HAIR)
    for k in range(7): poly(c, [(-80 + k * 26, -330), (-70 + k * 26, -372 + (k % 2) * 14), (-56 + k * 26, -330)], HAIR)
    c.restore()

def abuelo(c, x, y, s, t, arms="down", look=(0, 0), blink=None, sil=0.0, walk=0.0, eyes_glow=False, talk=0.0):
    def C(col): return hx("#050506") if sil >= 1 else col
    c.save(); c.translate(x, y); c.scale(s, s)
    bob = abs(math.sin(walk * 6)) * 8 if walk else 0
    c.translate(0, -bob)
    lg = math.sin(walk * 6) * 18 if walk else 0
    rect(c, -56 + lg * 0.3, -220, 48, 220, C("#3b3129")); rect(c, 8 - lg * 0.3, -220, 48, 220, C("#3b3129"))
    ell(c, -34, -2, 40, 14, C("#1d140f")); ell(c, 34, -2, 40, 14, C("#1d140f"))
    poly(c, [(-170, -210), (170, -210), (70, -470), (-70, -470)], C("#5b3a24"))
    for yy, col in ((-250, "#2c1d14"), (-275, "#a8743f"), (-300, "#2c1d14")):
        k = (yy + 470) / 260
        hw = 70 + 100 * k
        rect(c, -hw, yy, 2 * hw, 12, C(col))
    if arms == "give":
        arm(c, [(110, -300), (190, -330), (250, -360)], C("#5b3a24"), w=50, hand=C("#9a6a48"))
        c.save(); c.translate(282, -370); c.rotate(0.1); rect(c, -40, -55, 80, 70, C("#efe6cf")); c.restore()
    else:
        circ(c, -120, -235, 21, C("#9a6a48")); circ(c, 120, -235, 21, C("#9a6a48"))
    rect(c, -20, -500, 40, 36, C("#9a6a48"))
    hy = -560
    circ(c, 0, hy, 76, C("#9a6a48"))
    if sil < 1:
        b = blink if blink is not None else ((t % 4.4) < 0.12)
        ell(c, 0, hy - 40, 80, 30, hx("#000", 0.22))
        eyes_pair(c, 0, hy - 4, 15, 28, look=look, blink=b, glow_e=eyes_glow)
        line(c, [(-52, hy - 30), (-14, hy - 26)], "#d2ccc3", 9); line(c, [(52, hy - 30), (14, hy - 26)], "#d2ccc3", 9)
        if talk > 0.05: ell(c, 0, hy + 50, 16, 3 + 10 * talk, "#2a0f0c")
        poly(c, [(-44, hy + 30), (0, hy + 18), (44, hy + 30), (34, hy + 44), (0, hy + 34), (-34, hy + 44)], "#d8d2c8")
    ell(c, 0, hy - 58, 150, 26, C("#e3d6b8"))
    rrect(c, -72, hy - 150, 144, 98, 30, C("#e3d6b8"))
    rect(c, -73, hy - 84, 146, 22, C("#1a1412"))
    c.restore()

def dog(c, x, y, s, t, eyes=0.0, vis=0.5, ph=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    col = hx("#030406", vis)
    ell(c, 0, -120, 120, 55, col)
    for lx in (-80, -50, 60, 90): rect(c, lx - 10, -110, 20, 110, col)
    tw = math.sin(t * 3 + ph) * 15
    line(c, [(110, -140), (170, -190 + tw)], col, 14)
    ell(c, -130, -175, 55, 45, col); poly(c, [(-170, -160), (-230, -150), (-225, -128), (-160, -130)], col)
    poly(c, [(-150, -210), (-140, -265), (-115, -215)], col); poly(c, [(-115, -210), (-100, -262), (-82, -205)], col)
    c.restore()
    if eyes > 0:
        for sx in (-22, 6):
            ex, ey = x + (-150 + sx) * s, y - 182 * s
            glow(c, ex, ey, 40 * s * 2, "#e8fff0", 0.28 * eyes); ell(c, ex, ey, 9 * s * 1.6, 5 * s * 1.6, hx("#f3fff6", eyes))

def flaco(c, x, y, s, t, rise=0.0, eyes=0.0, vis=0.6):
    c.save(); c.translate(x, y); c.scale(s, s)
    col = hx("#020203", vis)
    h = 260 + 640 * ease(rise)
    for sg in (-1, 1):
        line(c, [(sg * 24, -h * 0.55), (sg * 60, -h * 0.28), (sg * 30, 0)], col, 22)
        line(c, [(sg * 40, -h * 0.9), (sg * 120, -h * 0.6), (sg * 130, -h * 0.25)], col, 16)
    ell(c, 0, -h * 0.72, 62, h * 0.22, col)
    ell(c, 0, -h - 40, 50, 75, col)
    c.restore()
    if eyes > 0:
        ey = y - (260 + 640 * ease(rise) + 40) * s
        for sx in (-20, 20):
            glow(c, x + sx * s, ey, 70 * s, "#ffffff", 0.35 * eyes); ell(c, x + sx * s, ey, 11 * s, 6 * s, hx("#ffffff", eyes))


def mujer(c, x, y, s, t, look=(0, 0), talk=0.0, scared=0.0, blink=None, hair="bun", top="#7a4a6a", skirt="#4a3a5a", apron=False, hair_col="#2a1a14", skin="#b98058", blazer=None, item=None, shake_a=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if shake_a > 0: c.translate(math.sin(t * 61) * 4 * shake_a, 0)
    br = math.sin(t * 2.0)
    rect(c, -44, -170, 30, 170, skin); rect(c, 14, -170, 30, 170, skin)
    ell(c, -30, -4, 34, 12, "#1a1412"); ell(c, 30, -4, 34, 12, "#1a1412")
    poly(c, [(-70, -400), (70, -400), (110, -160), (-110, -160)], skirt)
    c.save(); c.translate(0, -300); c.scale(1, 1 + 0.01 * br); c.translate(0, 300)
    rrect(c, -78, -470, 156, 200, 34, top)
    if blazer:
        poly(c, [(-80, -470), (-20, -470), (0, -380), (-10, -270), (-80, -270)], blazer); poly(c, [(80, -470), (20, -470), (0, -380), (10, -270), (80, -270)], blazer)
    if apron:
        rrect(c, -62, -400, 124, 260, 20, "#efe6d6"); rect(c, -78, -330, 156, 12, "#efe6d6")
        rect(c, -30, -300, 60, 40, hx("#000", 0.06))
    c.restore()
    if item == "notebook":
        line(c, [(-74, -450), (-110, -360), (-60, -330)], top if not blazer else blazer, 38); circ(c, -60, -330, 19, skin)
        line(c, [(74, -450), (110, -360), (60, -340)], top if not blazer else blazer, 38)
        c.save(); c.translate(0, -345); rect(c, -55, -60, 110, 80, "#f2efe6"); [rect(c, -45, -48 + k * 14, 80, 4, hx("#555", 0.6)) for k in range(4)]; c.restore()
        circ(c, 60, -340, 19, skin); line(c, [(60, -340), (30, -380)], "#222", 5)
    elif item == "recorder":
        line(c, [(-74, -450), (-104, -350), (-100, -270)], blazer or top, 38); circ(c, -100, -270, 19, skin)
        line(c, [(74, -450), (150, -470), (190, -540)], blazer or top, 38)
        rrect(c, 170, -620, 40, 80, 8, "#222"); circ(c, 190, -600, 8, "#e5413a"); circ(c, 190, -535, 19, skin)
    else:
        line(c, [(-74, -450), (-104, -350), (-100, -270)], blazer or top, 38); line(c, [(74, -450), (104, -350), (100, -270)], blazer or top, 38)
        circ(c, -100, -270, 19, skin); circ(c, 100, -270, 19, skin)
    rect(c, -18, -500, 36, 36, skin)
    hy = -560
    if hair == "long": rrect(c, -92, hy - 70, 184, 220, 70, hair_col)
    circ(c, 0, hy, 76, skin)
    c.new_path(); c.arc(0, hy - 6, 80, math.pi * 1.02, math.pi * 1.98); c.close_path(); fill(c, hair_col)
    poly(c, [(-80, hy - 10), (-40, hy - 62), (30, hy - 70), (80, hy - 16), (60, hy - 60), (-50, hy - 74)], hair_col)
    if hair == "bun": circ(c, 0, hy - 96, 36, hair_col)
    if hair == "pony":
        c.new_path(); c.move_to(60, hy - 50); c.curve_to(140, hy - 40, 130, hy + 60, 100 + math.sin(t * 3) * 6, hy + 110); c.curve_to(110, hy + 40, 110, hy - 20, 50, hy - 30); fill(c, hair_col)
    circ(c, -74, hy + 18, 6, "#e3c15a"); circ(c, 74, hy + 18, 6, "#e3c15a")
    b = (blink if blink is not None else ((t % 4.1) < 0.11)) and scared < 0.7
    eyes_pair(c, 0, hy + 4, 20, 30, look=look, blink=b, scared=scared)
    for sx in (-1, 1): line(c, [(sx * 46, hy - 16), (sx * 54, hy - 22)], "#1a1110", 4)
    brows(c, 0, hy - 28, 30, scared, col=hair_col, w=5)
    ell(c, 0, hy + 28, 6, 4, hx("#8a5a3a", 0.6))
    if talk > 0.05: ell(c, 0, hy + 50, 13, 3 + 10 * talk, "#5a1a1a")
    elif scared > 0.5: ell(c, 0, hy + 50, 10, 12 * scared, "#3a0f0c")
    else: line(c, [(-14, hy + 48), (14, hy + 48)], "#7a2a2a", 6)
    c.restore()

def dog_front(c, x, y, s, t, run=0.0, eyes=1.0, col="#1c1e25"):
    c.save(); c.translate(x, y); c.scale(s, s); c.translate(0, -abs(math.sin(run)) * 16)
    l1 = max(0, math.sin(run)) * 30; l2 = max(0, -math.sin(run)) * 30
    rect(c, -40, -120, 26, 120 - l1, col); rect(c, 14, -120, 26, 120 - l2, col)
    ell(c, 0, -150, 70, 80, col)
    circ(c, 0, -250, 58, col); ell(c, 0, -215, 30, 24, col)
    poly(c, [(-50, -280), (-62, -350), (-20, -300)], col); poly(c, [(50, -280), (62, -350), (20, -300)], col)
    c.restore()
    if eyes > 0:
        for sx in (-22, 22):
            ex, ey = x + sx * s, y + (-262 - abs(math.sin(run)) * 16) * s
            glow(c, ex, ey, 40 * s, "#e8fff0", 0.3 * eyes); ell(c, ex, ey, 9 * s, 5 * s, hx("#f3fff6", eyes))

"""Formato «chat de terror»: una conversación de mensajes que se vuelve aterradora.
Uso: python3 engine/chat.py stories/<historia> salida.mp4 [--still SEG]
La historia vive en stories/<historia>/chat.py (ver stories/chat_mama/chat.py).
"""
import sys, os, math, random, subprocess, importlib.util
import numpy as np
import cairocffi as cairo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import hx, src, fill, rect, rrect, circ, ell, poly, line, glow, vgrad, overlay, ease, clamp
import povlib

W, H, FPS, SR = 1080, 1920, 30, 44100
story = sys.argv[1].rstrip("/")
spec = importlib.util.spec_from_file_location("chat", f"{story}/chat.py"); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
FONT = "Inter"

# ---------------- línea de tiempo ----------------
# Cada mensaje: (lado, texto) con lado "in" (el otro) u "out" (tú); texto "[foto]" usa S.foto.
# Opcional 3.er valor: pausa extra antes. Eventos especiales: ("glitch",), ("heart",), ("pausa", s)
LOCK_T = S.LOCK_T                     # segundos de pantalla bloqueada con el gancho
ev = []; t = LOCK_T
shown = []                            # (t_aparece, lado, texto)
typing_in = []; typing_out = []       # (t0, t1) / (t0, t1, texto)
glitches = []; hearts = []; prev_len = 0
for m in S.MSGS:
    if m[0] == "pausa": t += m[1]; continue
    if m[0] == "glitch": glitches.append(t); continue
    if m[0] == "heart": hearts.append(t); continue
    side, txt = m[0], m[1]; extra = m[2] if len(m) > 2 else 0.0
    t += extra + (0.25 + min(1.1, prev_len / 30.0) if shown else 0.0)
    if side == "in":
        d = 0.8 if txt.startswith("[") else max(0.6, min(1.4, len(txt) / 28.0))
        if not shown and m is S.MSGS[0]: d = 0.0
        if d: typing_in.append((t, t + d))
        t += d
    else:
        d = max(0.45, len(txt) / 32.0)
        typing_out.append((t, t + d, txt)); t += d + 0.12
    shown.append((t, side, txt)); prev_len = 30 if txt.startswith("[") else len(txt)
END_CHAT = t + 1.4
JUMP_T = END_CHAT + 0.55              # silencio corto y luego el susto
END = JUMP_T + S.JUMP_DUR + S.ENDCARD_DUR

# ---------------- dibujo ----------------
def font(c, size, bold=False):
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)
def tw(c, s): return c.text_extents(s)[4]
def text(c, s, x, y, col, size, bold=False, center=False, right=False):
    font(c, size, bold); w_ = tw(c, s)
    if center: x -= w_ / 2
    if right: x -= w_
    c.move_to(x, y); src(c, col); c.show_text(s)
def stroke_text(c, s, x, y, size, col="#ffffff", out="#000000", lw=10):
    font(c, size, True); x -= tw(c, s) / 2
    c.move_to(x, y); c.text_path(s); src(c, out); c.set_line_width(lw); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve(); src(c, col); c.fill()
def wrap(c, s, size, maxw, bold=False):
    font(c, size, bold); out = []; cur = ""
    for wd in s.split():
        tr = (cur + " " + wd).strip()
        if tw(c, tr) <= maxw: cur = tr
        else: out.append(cur); cur = wd
    if cur: out.append(cur)
    return out

TOP, BOT = 230, 1440                  # zona de mensajes (fuera de la interfaz de TikTok)
FS = 52; LH = 64; PADX = 36; PADY = 26; MAXW = 740
COL_IN, COL_OUT = "#24262d", "#5a3fd0"
STAMP = S.HORA

def bubble_h(c, side, txt):
    if txt.startswith("["): return 640
    n = len(wrap(c, txt, FS, MAXW)); return n * LH + PADY * 2 + 26
def draw_bubble(c, y, side, txt, t, born):
    a = ease(clamp((t - born) / 0.18)); sc = 0.85 + 0.15 * a
    h = bubble_h(c, side, txt)
    if txt.startswith("["):
        bw = 620; x = 60 if side == "in" else W - 60 - bw
        c.save(); c.translate(x + bw / 2, y + h / 2); c.scale(sc, sc); c.translate(-(x + bw / 2), -(y + h / 2))
        rrect(c, x, y, bw, h, 28, COL_IN if side == "in" else COL_OUT)
        c.save(); c.translate(x + 14, y + 14); c.rectangle(0, 0, bw - 28, h - 70); c.clip(); S.foto(c, bw - 28, h - 70, t); c.restore()
        text(c, txt[1:-1] if len(txt) > 6 else "", x + 24, y + h - 26, "#e8e8f0", 38)
        text(c, STAMP, x + bw - 20, y + h - 22, "#9a9aa8", 26, right=True)
        c.restore(); return h
    lines = wrap(c, txt, FS, MAXW); font(c, FS)
    bw = max(tw(c, l) for l in lines) + PADX * 2 + (110 if len(lines) == 1 else 0); bw = max(bw, 200)
    x = 50 if side == "in" else W - 50 - bw
    c.save(); c.translate(x + (0 if side == "in" else bw), y + h); c.scale(sc, sc); c.translate(-(x + (0 if side == "in" else bw)), -(y + h))
    rrect(c, x, y, bw, h, 30, COL_IN if side == "in" else COL_OUT)
    for i, l in enumerate(lines): text(c, l, x + PADX, y + PADY + 42 + i * LH, "#f2f2f7", FS)
    text(c, STAMP, x + bw - 22 - (44 if side == "out" else 0), y + h - 18, "#b8b8c8" if side == "out" else "#8a8a98", 26, right=True)
    if side == "out":
        for k in (0, 14): line(c, [(x + bw - 58 + k, y + h - 30), (x + bw - 50 + k, y + h - 22), (x + bw - 36 + k, y + h - 40)], "#7fd0ff", 4)
    c.restore(); return h

def dots(c, x, y, t):
    rrect(c, x, y, 170, 92, 30, COL_IN)
    for i in range(3):
        k = 0.5 + 0.5 * math.sin(t * 9 - i * 0.9); circ(c, x + 48 + i * 37, y + 46 - 6 * k, 11, hx("#c8c8d4", 0.45 + 0.5 * k))

def status_bar(c, light="#ffffff"):
    text(c, STAMP, 70, 70, light, 34, True)
    rrect(c, W - 140, 46, 70, 32, 8, hx(light, 0.9)); rect(c, W - 70, 56, 6, 12, light)
    for i in range(4): rect(c, W - 230 + i * 16, 74 - 8 - i * 7, 10, 8 + i * 7, light)

def header(c, t, name, status):
    rect(c, 0, 0, W, 210, "#14151a")
    status_bar(c)
    line(c, [(80, 150), (56, 130), (80, 110)], "#cfd2ff", 6)
    circ(c, 160, 140, 46, S.AVATAR_COL); text(c, S.AVATAR_TXT, 160, 156, "#ffffff", 44, True, center=True)
    text(c, name, 230, 136, "#ffffff", 44, True); text(c, status, 230, 182, "#8fe39b" if status == "en línea" else "#a7a9ff", 32)
    rect(c, 0, 208, W, 2, "#25262e")

def input_bar(c, t, typed):
    rect(c, 0, BOT + 10, W, H - BOT - 10, "#14151a")
    rrect(c, 40, BOT + 34, W - 200, 96, 48, "#24262d")
    if typed:
        font(c, 42); s = typed
        while tw(c, s) > W - 300: s = s[1:]
        text(c, s, 80, BOT + 96, "#f2f2f7", 42)
        if int(t * 2.5) % 2 == 0: rect(c, 84 + tw(c, s), BOT + 58, 4, 50, "#a7a9ff")
    else:
        text(c, "Mensaje", 80, BOT + 96, "#6c6e7a", 42)
    circ(c, W - 100, BOT + 82, 48, COL_OUT); poly(c, [(W - 122, BOT + 60), (W - 74, BOT + 82), (W - 122, BOT + 104), (W - 112, BOT + 82)], "#ffffff")
    # teclado
    ky = BOT + 160; rect(c, 0, ky, W, H - ky, "#1b1c22")
    rows = ["qwertyuiop", "asdfghjklñ", "zxcvbnm"]
    hit = typed[-1:].lower() if typed else ""
    for r, row in enumerate(rows):
        kw = 98; x0 = (W - len(row) * (kw + 8)) / 2
        for i, ch in enumerate(row):
            on = ch == hit
            rrect(c, x0 + i * (kw + 8), ky + 24 + r * 118, kw, 104, 14, "#5a5c68" if on else "#34353d")
            text(c, ch, x0 + i * (kw + 8) + kw / 2, ky + 96 + r * 118, "#ffffff", 44, center=True)

def lock_screen(c, t):
    vgrad(c, 0, 0, W, H, "#0b0d1c", "#1c1030"); S.wallpaper(c, t)
    overlay(c, "#000", 0.35)
    status_bar(c)
    text(c, S.FECHA, W / 2, 330, "#e8e8f0", 44, center=True)
    text(c, STAMP, W / 2, 520, "#ffffff", 210, True, center=True)
    k = ease(clamp((t - 0.25) / 0.35)); y = 600 - 120 * (1 - k)
    if k > 0:
        c.save(); c.translate(0, 0)
        rrect(c, 50, y, W - 100, 210, 40, hx("#2a2c3a", 0.92 * k))
        circ(c, 120, y + 72, 36, S.AVATAR_COL); text(c, S.AVATAR_TXT, 120, y + 86, "#fff", 34, True, center=True)
        text(c, S.NOMBRE, 180, y + 70, "#ffffff", 40, True); text(c, "ahora", W - 90, y + 70, "#a0a0b0", 32, right=True)
        for i, l in enumerate(wrap(c, S.MSGS[0][1], 40, W - 260)[:2]): text(c, l, 180, y + 128 + i * 50, "#e8e8f0", 40)
        c.restore()
    # gancho: una sola frase concreta, grande
    if t > 0.5:
        a = ease(clamp((t - 0.5) / 0.3))
        for i, l in enumerate(wrap(c, S.GANCHO, 76, W - 140, True)):
            c.save(); c.translate(0, 30 * (1 - a)); stroke_text(c, l, W / 2, 1010 + i * 96, 76, "#ffffff" if i < 1 else "#ffd84a"); c.restore()

def chat(c, t):
    rect(c, 0, 0, W, H, "#0d0e12")
    for i in range(0, H, 140):                      # fondo con dibujito tenue
        for j in range(0, W, 140): circ(c, j + (i // 140 % 2) * 70, i, 3, "#16171d")
    vis = [m for m in shown if m[0] <= t]
    ti = next(((a, b) for a, b in typing_in if a <= t < b), None)
    to = next(((a, b, s) for a, b, s in typing_out if a <= t < b), None)
    # alto total y desplazamiento suave
    hs = [bubble_h(c, s, x) + 22 for _, s, x in vis]
    extra = 114 if ti else 0
    total = sum(hs) + extra
    # animación de subida: el último mensaje entra empujando
    last_born = vis[-1][0] if vis else 0
    push = (1 - ease(clamp((t - last_born) / 0.22))) * (hs[-1] if hs else 0)
    y = BOT - 20 - total + push
    c.save(); c.rectangle(0, 212, W, BOT - 212 + 10); c.clip()
    for (born, s, x), h in zip(vis, hs):
        if y + h > 200: draw_bubble(c, y, s, x, t, born)
        y += h
    if ti: dots(c, 50, y, t)
    c.restore()
    name = S.NOMBRE
    if any(0 <= t - g < 0.9 for g in glitches) or t > END_CHAT - 1.0: name = S.NOMBRE_GLITCH if int(t * 14) % 3 else S.NOMBRE
    header(c, t, name, "escribiendo..." if ti else "en línea")
    typed = to[2][:int(len(to[2]) * clamp((t - to[0]) / (to[1] - to[0] - 0.05)))] if to else ""
    input_bar(c, t, typed)
    # tensión: viñeta roja que crece al final
    tens = clamp((t - (END_CHAT - 9)) / 9)
    if tens > 0:
        g = cairo.RadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1200); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.35, 0, 0, 0.55 * tens)
        c.set_source(g); c.paint()

def glitch_fx(surf, t, amt):
    rnd = random.Random(int(t * 30))
    tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); cc = cairo.Context(tmp); cc.set_source_surface(surf); cc.paint()
    c = cairo.Context(surf)
    for _ in range(int(6 + 10 * amt)):
        y0 = rnd.randint(0, H - 80); hh = rnd.randint(10, 90); dx = rnd.randint(-80, 80) * amt
        c.save(); c.rectangle(0, y0, W, hh); c.clip(); c.set_source_surface(tmp, dx, 0); c.paint(); c.restore()
    c.set_source_rgba(1, 0, 0.1, 0.12 * amt); c.paint()

def jumpscare(c, t):
    k = t - JUMP_T
    rect(c, 0, 0, W, H, "#050203")
    sh = max(0, 1 - k / 0.9)
    c.save(); c.translate(random.uniform(-30, 30) * sh, random.uniform(-30, 30) * sh)
    zoom = 0.85 + 0.35 * ease(clamp(k / 0.25))
    c.translate(W / 2, H / 2); c.scale(zoom, zoom); c.translate(-W / 2, -H / 2)
    S.monstruo(c, W / 2, H * 0.62, t)
    c.restore()
    overlay(c, "#ff0010", 0.25 * (1 if int(k * 20) % 2 else 0) * sh)

def endcard(c, t):
    k = t - (JUMP_T + S.JUMP_DUR)
    rect(c, 0, 0, W, H, "#07070b")
    a = ease(clamp(k / 0.4))
    for i, l in enumerate(wrap(c, S.FINAL[0], 70, W - 160, True)): stroke_text(c, l, W / 2, 640 + i * 90, 70, hx("#ffffff", a), "#000000", 8)
    for i, (lt, s) in enumerate((("A", S.FINAL[1]), ("B", S.FINAL[2]))):
        b = ease(clamp((k - 0.4 - i * 0.25) / 0.3)); y = 900 + i * 170
        rrect(c, 140, y, W - 280, 130, 30, hx("#ffd84a" if i == 0 else "#e0303a", b))
        text(c, f"{lt}  {s}", W / 2, y + 84, hx("#11131a" if i == 0 else "#ffffff", b), 52, True, center=True)
    text(c, "Comenta A o B", W / 2, 1310, hx("#c8c8d4", a), 46, True, center=True)

def frame(t):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(surf)
    if t < LOCK_T:
        lock_screen(c, t)
        if t > LOCK_T - 0.25:                     # toca la notificación: entra al chat
            overlay(c, "#000", ease((t - (LOCK_T - 0.25)) / 0.25))
    elif t < JUMP_T:
        c.save()
        if t < LOCK_T + 0.3:
            z = 1.08 - 0.08 * ease((t - LOCK_T) / 0.3); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
        chat(c, t); c.restore()
        if t < LOCK_T + 0.3: overlay(c, "#000", 1 - ease((t - LOCK_T) / 0.3))
        if t >= END_CHAT: overlay(c, "#000", ease((t - END_CHAT) / 0.3))
    elif t < JUMP_T + S.JUMP_DUR: jumpscare(c, t)
    else: endcard(c, t)
    g = max([1 - (t - x) / 0.9 for x in glitches if 0 <= t - x < 0.9] + [0.0])
    if END_CHAT - 1.0 < t < END_CHAT: g = max(g, 0.7)
    if g > 0: surf.flush(); glitch_fx(surf, t, g)
    return surf

# ---------------- sonido ----------------
rng = np.random.default_rng(7)
def T(d): return np.arange(int(d * SR)) / SR
def env(n, a, d): x = np.arange(n) / SR; return np.minimum(1, x / max(a, 1e-4)) * np.exp(-x / d)
from scipy.signal import butter, sosfilt
def lp(x, f): return sosfilt(butter(2, f, btype="low", fs=SR, output="sos"), x)
def hp(x, f): return sosfilt(butter(2, f, btype="high", fs=SR, output="sos"), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], btype="band", fs=SR, output="sos"), x)
def audio(path):
    N = int((END + 0.5) * SR); out = np.zeros(N)
    def add(sig, t0, g=1.0):
        i = int(t0 * SR)
        if i >= N: return
        sig = sig[:N - i]; out[i:i + len(sig)] += sig * g
    def ding():
        t = T(0.35); s = np.sin(2 * np.pi * 988 * t) * env(len(t), 0.002, 0.08)
        t2 = T(0.4); s2 = np.sin(2 * np.pi * 1480 * t2) * env(len(t2), 0.002, 0.12)
        o = np.zeros(int(0.5 * SR)); o[:len(s)] += s; o[int(0.07 * SR):int(0.07 * SR) + len(s2)] += s2; return o * 0.5
    def swoosh():
        t = T(0.3); return bp(rng.normal(0, 1, len(t)), 1500, 6000) * np.sin(np.pi * t / 0.3) ** 2 * 0.35
    def tap():
        m = int(0.025 * SR); return hp(rng.normal(0, 1, m), 2500) * env(m, 0.0005, 0.004) * 0.5
    def buzz(d=0.45):
        t = T(d); return lp(np.sign(np.sin(2 * np.pi * 160 * t)), 400) * np.sin(np.pi * t / d) * 0.35
    def boom(d=2.6, f0=48):
        t = T(d); f = f0 * (1 + 1.5 * np.exp(-t * 8)); ph = 2 * np.pi * np.cumsum(f) / SR
        return np.sin(ph) * env(len(t), 0.005, 0.8) + lp(rng.normal(0, 1, len(t)), 300) * env(len(t), 0.002, 0.3)
    def scream(d=1.3):
        t = T(d); f = 900 - 500 * t / d + 60 * np.sin(2 * np.pi * 7 * t); ph = 2 * np.pi * np.cumsum(f) / SR
        v = np.tanh(3 * (np.sin(ph) + 0.6 * np.sin(2.01 * ph) + 0.4 * np.sin(3.02 * ph))) + bp(rng.normal(0, 1, len(t)), 1200, 5000) * 0.8
        return bp(v, 300, 6000) * env(len(t), 0.01, 0.6) * 0.55
    def heart():
        t = T(0.7); s = np.zeros(len(t))
        for off, a in ((0, 1), (0.22, 0.7)):
            i = int(off * SR); tt = t[:len(t) - i]; s[i:] += a * np.sin(2 * np.pi * 52 * tt) * env(len(tt), 0.004, 0.08)
        return s
    # bloqueo: vibra dos veces
    add(buzz(), 0.05); add(buzz(), 0.6); add(ding(), 0.25, 0.8)
    for born, side, _ in shown:
        if born < LOCK_T + 0.6: continue
        add(ding() if side == "in" else swoosh(), born - 0.02, 0.85 if side == "in" else 0.7)
    for a, b, s in typing_out:
        n = max(1, int(len(s) * 0.8))
        for i in range(n): add(tap(), a + (b - a) * i / n + rng.uniform(0, 0.02), 0.6)
    # ambiente que sube; silencio antes del susto
    t = np.arange(N) / SR
    grow = np.clip((t - LOCK_T) / (END_CHAT - LOCK_T), 0, 1)
    drone = (np.sin(2 * np.pi * 55 * t) * 0.5 + np.sin(2 * np.pi * 82.4 * t + 0.3 * np.sin(2 * np.pi * 0.2 * t)) * 0.35 + np.sin(2 * np.pi * 110.3 * t) * 0.15)
    wind = lp(rng.normal(0, 1, N), 500) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * t))
    amb = (drone * 0.10 + wind * 0.05) * (0.35 + 0.65 * grow)
    amb[t >= END_CHAT] *= np.clip(1 - (t[t >= END_CHAT] - END_CHAT) / 0.25, 0, 1)
    amb[t >= JUMP_T + S.JUMP_DUR] = (drone * 0.07)[t >= JUMP_T + S.JUMP_DUR]
    out += amb
    for h0 in hearts:
        k = h0
        while k < END_CHAT - 0.2: add(heart(), k, 0.9); k += 0.82 - 0.25 * clamp((k - h0) / 8)
    for g in glitches: add(bp(rng.normal(0, 1, int(0.5 * SR)), 300, 4000) * 0.4, g)
    add(bp(rng.normal(0, 1, int(1.0 * SR)), 200, 5000) * 0.35, END_CHAT - 1.0)
    add(boom(), JUMP_T, 1.3); add(scream(), JUMP_T + 0.02, 1.0)
    add(swoosh(), JUMP_T + S.JUMP_DUR, 0.5)
    out /= np.abs(out).max() / 0.9
    import soundfile as sf; sf.write(path, out.astype(np.float32), SR)

# ---------------- salida ----------------
if __name__ == "__main__":
    if "--still" in sys.argv:
        for ts in sys.argv[sys.argv.index("--still") + 1:]:
            frame(float(ts)).write_to_png(f"/tmp/chat_{ts}.png")
        print("END", round(END, 2)); sys.exit()
    outp = sys.argv[2]; tmpv = outp + ".tmp.mp4"; wav = outp + ".wav"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmpv], stdin=subprocess.PIPE)
    nf = int(END * FPS)
    for i in range(nf):
        s = frame(i / FPS); s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()
    audio(wav)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmpv, "-i", wav, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-shortest", outp], check=True)
    os.remove(tmpv); os.remove(wav)
    print("OK", outp, round(END, 2))

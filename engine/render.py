"""Render de una parte con cortes de cámara, efectos y boca sincronizada.
Uso: python3 engine/render.py stories/<historia> <parte> stills 1.0 5.0 ...
     python3 engine/render.py stories/<historia> <parte> render <procesos> [escenas...]
"""
import sys, os, json, math, re, subprocess, importlib.util, random
ENG = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ENG)
import cairocffi as cairo
from lib import hx, src, rect, rrect, rrect_path, circ, ell, poly, line, glow, overlay, ease, clamp, text_w
import povlib
from povlib import ui, txt, card, pop, fade, P

STORY, PART = sys.argv[1].rstrip("/"), int(sys.argv[2])
sys.path.insert(0, STORY)
def load(name):
    spec = importlib.util.spec_from_file_location(name, f"{STORY}/{name}.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
G = load("guion"); PN = load("panels")
W, H, FPS = 1080, 1920, 30
PY = 420
BUILD = f"{STORY}/build/p{PART}"
D = json.load(open(f"{BUILD}/timeline.json")); TL = D["lines"]; END = D["END"]; AMP = D["amp"]
CLASSIC = getattr(G, "STYLE", "") == "clasico"   # estilo «Tu IA te hizo rico»: sin cortes duros ni contornos
povlib.OUTLINE = not CLASSIC
povlib.APPEAL = CLASSIC or getattr(G, "APPEAL", False)
KEY = G.KEY; FX = getattr(G, "FX", {}); CAM = getattr(G, "CAM", {}); FOCUS = getattr(G, "FOCUS", {})
FOCUS.update(getattr(PN, "FOCUS", {})); CAM.update(getattr(PN, "CAM", {}))

def clean(x): return re.sub(r"[^\wáéíóúñü]", "", x.lower())
bounds = {}
for i, l in enumerate(TL):
    a = 0.0 if i == 0 else l["start"] - 0.15
    b = END if i == len(TL) - 1 else TL[i + 1]["start"] - 0.15
    bounds[l["scene"]] = (round(a * FPS), round(b * FPS), i)

def word_time(li, tok):
    tk = clean(tok)
    for x, a, b in TL[li]["words"]:
        if clean(x).startswith(tk): return a
    return None

# ---------- cámara: cortes duros cada ~2 s ----------
SHOTS = {}
for i, l in enumerate(TL):
    a, b, _ = bounds[l["scene"]]; t0 = a / FPS; dur = (b - a) / FPS
    fx, fy = FOCUS.get(l["scene"], (540, 600))
    if l["scene"] in CAM:
        sh = [(0.0, 1.0, 540, 540)]
        for tok, z, cx, cy in CAM[l["scene"]]:
            wt = word_time(i, tok) if isinstance(tok, str) else t0 + tok
            sh.append(((wt if wt is not None else t0) - 0.05 - t0, z, cx, cy))
    else:
        cycle = [(1.0, 540, 540), (1.32, fx, fy), (1.15, fx + 40, fy - 20)]
        if i % 2: cycle = [cycle[1], cycle[0], cycle[2]]
        sh = [(0.0,) + cycle[0]]
        if dur > 2.6 and i < len(TL) - 1 and not CLASSIC:
            n = int(dur / 2.1)
            starts = [w[1] - t0 for w in l["words"]]
            for k in range(1, n + 1):
                target = dur * k / (n + 1)
                best = min(starts, key=lambda s: abs(s - target))
                if best - sh[-1][0] > 1.1: sh.append((best - 0.05,) + cycle[k % 3])
    SHOTS[l["scene"]] = sh

def camera(scene, t, li):
    sh = SHOTS[scene]; cur = sh[0]; nxt = None
    for k, s in enumerate(sh):
        if t >= s[0]: cur = s; nxt = sh[k + 1][0] if k + 1 < len(sh) else None
    st = cur[0]; en = nxt if nxt is not None else (bounds[scene][1] - bounds[scene][0]) / FPS
    p = clamp((t - st) / max(0.5, en - st))
    z = cur[1] * (1 + (0.0 if CLASSIC else 0.045) * ease(p))   # clásico: plano quieto, sin flotar
    # golpe de zoom en palabras clave
    g = bounds[scene][0] / FPS + t
    for x, a, b in TL[li]["words"]:
        if clean(x) in KEY and a <= g < a + 0.5: z *= 1 + 0.05 * math.exp(-(g - a) * 9)
    cx, cy = cur[2], cur[3] + (-12 * p if cur[1] > 1.05 and not CLASSIC else 0)
    half = 540 / z; cx = min(max(cx, half), P - half); cy = min(max(cy, half), P - half)
    return z, cx, cy

def fx_amt(li, kind, g, d):
    best = 0.0
    for tok, k in FX.get(TL[li]["scene"], []):
        if k != kind: continue
        wt = word_time(li, tok)
        if wt is not None and wt - 0.05 <= g < wt + d: best = max(best, 1 - (g - wt + 0.05) / d)
    return best

# ---------- subtítulos ----------
CHUNKS = []
for l in TL:
    cur = []
    for wd in l["words"]:
        cur.append(wd)
        if len(cur) >= 3 or wd[0][-1] in ".,:;?…": CHUNKS.append(cur); cur = []
    if cur: CHUNKS.append(cur)

def outline_text(c, s, x, y, col, lw=10, a=1.0):
    c.new_path(); c.move_to(x, y); c.text_path(s); c.set_line_width(lw); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_source_rgba(0, 0, 0, 0.95 * a); c.stroke_preserve(); src(c, hx(col, a) if isinstance(col, str) else col); c.fill()

def captions(c, g):
    chunk = None
    for i, ch in enumerate(CHUNKS):
        st = 0.0 if i == 0 else ch[0][1] - 0.05
        nxt = CHUNKS[i + 1][0][1] - 0.05 if i + 1 < len(CHUNKS) else 1e9
        en = nxt if nxt - ch[-1][2] < 0.8 else ch[-1][2] + 0.35
        if st <= g < en: chunk = ch; break
    if not chunk: return
    ui(c, 78)
    disp = [wd[0].upper() for wd in chunk]
    sp = 36; widths = [text_w(c, d) for d in disp]
    rows = [list(range(len(chunk)))]
    if sum(widths) + sp * (len(chunk) - 1) > 960:
        h = (len(chunk) + 1) // 2; rows = [list(range(h)), list(range(h, len(chunk)))]
    for ri, row in enumerate(rows):
        tw = sum(widths[i] for i in row) + sp * (len(row) - 1)
        x = W / 2 - tw / 2; y = PY + 130 + ri * 92
        for i in row:
            word, ws_, we = chunk[i]
            said = g >= ws_ - 0.02
            key = clean(word) in KEY
            col = hx("#ffc24a") if (said and key) else hx("#ffffff", 1.0 if said else 0.55)
            s = 1 + 0.07 * math.exp(-(g - ws_) * 12) if (said and key) else 1.0
            c.save(); c.translate(x + widths[i] / 2, y - 26); c.scale(s, s); c.translate(-(x + widths[i] / 2), -(y - 26))
            outline_text(c, disp[i], x, y, col, 15, 1.0 if said else 0.75); c.restore()
            x += widths[i] + sp

def label(c):
    card(c, 40, 150, 1000, 190, 26, "#ffffff", 0.25)
    fs = 52
    while fs > 34 and max(text_w(c, s) for s in G.TITLE if (ui(c, fs) or True)) > 930: fs -= 2
    txt(c, G.TITLE[0], W / 2, 232, "#11131a", fs, True)
    txt(c, G.TITLE[1], W / 2, 300, "#11131a", fs, True)
    tg = f"PARTE {PART}" + (" · FINAL" if PART == 3 else "")
    ui(c, 30); tw = text_w(c, tg)
    rrect(c, W / 2 - tw / 2 - 22, 118, tw + 44, 50, 25, "#e0303a"); txt(c, tg, W / 2, 154, "#ffffff", 30, True)

def endcard(c, g):
    st = TL[-1]["start"] - 0.1
    if g < st: return
    q, oa, ob, foot = G.ENDCARD[PART]
    ws = TL[-1]["words"]
    def at(tok):
        for x, a, b in ws:
            if clean(x) == tok: return a
        return st
    ta, tb, tc = at("a"), at("b"), at("comenta")
    ui(c, 72); outline_text(c, q, W / 2 - text_w(c, q) / 2, PY + 150, "#ffffff", 14, fade(g, st))
    for (tt, y, L_, s_, col) in ((ta, PY + 230, "A", oa, "#ffc24a"), (tb, PY + 500, "B", ob, "#5fb4ff")):
        a = fade(g, tt - 0.15); s = pop(g, tt - 0.15)
        if a <= 0: continue
        c.save(); c.translate(W / 2, y + 115); c.scale(s, s); c.translate(-W / 2, -(y + 115))
        card(c, 70, y, 940, 230, 34, "#14121b", 0.4, border=col)
        circ(c, 170, y + 115, 64, col); txt(c, L_, 170, y + 145, "#14121b", 84, True)
        ui(c, 46); words = s_.split(); l1 = ""; lines = []
        for wd in words:
            if text_w(c, (l1 + " " + wd).strip()) > 690: lines.append(l1); l1 = wd
            else: l1 = (l1 + " " + wd).strip()
        lines.append(l1)
        for i, l in enumerate(lines): txt(c, l, 270, y + 115 - (len(lines) - 1) * 29 + 16 + i * 58, "#ffffff", 46)
        c.restore()
    b = fade(g, tc)
    if b > 0:
        s = 1 + 0.2 * (1 - b) + 0.04 * math.sin(g * 6)
        ui(c, 74); t2 = "COMENTA  A  o  B"
        c.save(); c.translate(W / 2, PY + 860); c.scale(s, s); outline_text(c, t2, -text_w(c, t2) / 2, 0, "#ffc24a", 14, b); c.restore()
        ui(c, 40); outline_text(c, foot, W / 2 - text_w(c, foot) / 2, PY + 945, "#ffffff", 9, fade(g, tc + 0.8))

PANEL = cairo.ImageSurface(cairo.FORMAT_ARGB32, P, P)
SMALL = cairo.ImageSurface(cairo.FORMAT_ARGB32, 24, 24)
def vignette(c, x, y, w, h, a):
    g = cairo.RadialGradient(x + w / 2, y + h / 2, w * 0.3, x + w / 2, y + h / 2, w * 0.78)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, a)
    c.rectangle(x, y, w, h); c.set_source(g); c.fill()

def render_frame(c, fi):
    g = fi / FPS
    for s, (a, b, i) in bounds.items():
        if a <= fi < b: scene = s; f0 = a; li = i; f1 = b; break
    else:
        scene = TL[-1]["scene"]; f0, f1, li = bounds[scene]
    t = (fi - f0) / FPS; T = (f1 - f0) / FPS
    l = TL[li]
    povlib.TALK = AMP[fi] if (l["voice"] != "N" and fi < len(AMP) and l["start"] <= g <= l["end"]) else 0.0
    z, cx, cy = camera(scene, t, li)
    pc = cairo.Context(PANEL); pc.set_source_rgb(0, 0, 0); pc.paint()
    pc.save(); pc.translate(540, 540); pc.scale(z, z); pc.translate(-cx, -cy)
    def w(tok):
        wt = word_time(li, tok); return (wt - f0 / FPS) if wt is not None else 0.5
    PN.PANELS[scene](pc, t, T, w); pc.restore()
    vignette(pc, 0, 0, P, P, 0.55)
    PANEL.flush()
    # fondo desenfocado
    sc = cairo.Context(SMALL); sc.scale(24 / P, 24 / P); sc.set_source_surface(PANEL, 0, 0); sc.paint(); SMALL.flush()
    k = H / 24 * 1.08
    for j, (ox, oy) in enumerate(((0, 0), (0.5, 0.5), (-0.5, 0.5), (0.5, -0.5), (-0.5, -0.5))):
        c.save(); c.translate(W / 2 - 12 * k + ox * k, H / 2 - 12 * k + oy * k); c.scale(k, k)
        pat = cairo.SurfacePattern(SMALL); pat.set_filter(cairo.FILTER_BILINEAR); pat.set_extend(cairo.EXTEND_PAD); c.set_source(pat); c.paint_with_alpha(1.0 / (j + 1)); c.restore()
    overlay(c, "#000000", 0.42)
    # temblor
    sh = fx_amt(li, "shake", g, 0.55)
    dx = dy = 0
    if sh > 0: rr = random.Random(fi); dx = rr.uniform(-1, 1) * 22 * sh; dy = rr.uniform(-1, 1) * 16 * sh
    c.save(); c.rectangle(0, PY, W, P); c.clip()
    gl = fx_amt(li, "glitch", g, 0.4)
    if gl > 0:
        rr = random.Random(fi * 7)
        for k2 in range(14):
            y0 = k2 * P / 14; off = rr.uniform(-1, 1) * 60 * gl if rr.random() < 0.6 else 0
            c.save(); c.rectangle(0, PY + y0, W, P / 14 + 1); c.clip(); c.set_source_surface(PANEL, off + dx, PY + dy); c.paint(); c.restore()
        c.set_operator(cairo.OPERATOR_ADD)
        c.set_source_surface(PANEL, 14 * gl, PY); c.paint_with_alpha(0.25 * gl)
        c.set_operator(cairo.OPERATOR_OVER)
        rect(c, 0, PY, W, P, hx("#ff2040", 0.12 * gl))
    else:
        c.set_source_surface(PANEL, dx, PY + dy); c.paint()
    fl = fx_amt(li, "flash", g, 0.35)
    if fl > 0: rect(c, 0, PY, W, P, hx("#ffffff", 0.85 * fl ** 1.5))
    c.restore()
    rd = fx_amt(li, "red", g, 1.3)
    if rd > 0:
        gr = cairo.RadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1100)
        gr.add_color_stop_rgba(0, 0.8, 0, 0, 0); gr.add_color_stop_rgba(1, 0.75, 0, 0.05, 0.6 * rd)
        c.rectangle(0, 0, W, H); c.set_source(gr); c.fill()
    label(c)
    if g < TL[-1]["start"] - 0.1: captions(c, g)
    else: endcard(c, g)

OUT = f"{BUILD}/seg"
def render_scene(name):
    a, b, _ = bounds[name]
    tmp = f"{OUT}/{name}.tmp.mp4"; final = f"{OUT}/{name}.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for fi in range(a, b):
        c = cairo.Context(surf); c.set_source_rgb(0, 0, 0); c.paint()
        render_frame(c, fi); surf.flush(); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close(); rc = p.wait()
    if rc == 0: os.replace(tmp, final)
    return name, rc, b - a

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    if sys.argv[3] == "label":   # tarjeta del título sola (para corregirla sin volver a renderizar)
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); label(cairo.Context(surf)); surf.write_to_png(f"{BUILD}/label.png")
    elif sys.argv[3] == "stills":
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        for ts in sys.argv[4:]:
            fi = int(float(ts) * FPS) if not ts[0].isalpha() else bounds[ts.split("+")[0]][0] + int(float(ts.split("+")[1] if "+" in ts else 0.5) * FPS)
            c = cairo.Context(surf); c.set_source_rgb(0, 0, 0); c.paint(); render_frame(c, fi)
            surf.write_to_png(f"{OUT}/st_{ts}.png")
    elif sys.argv[3] == "render":
        from multiprocessing import Pool
        names = sys.argv[5:] or [n for n in bounds if not os.path.exists(f"{OUT}/{n}.mp4")]   # retoma lo que falte
        names.sort(key=lambda n: -(bounds[n][1] - bounds[n][0]))
        with Pool(int(sys.argv[4])) as pool:
            for r in pool.imap_unordered(render_scene, names): print(r, flush=True)
        with open(f"{OUT}/list.txt", "w") as f:
            for n in bounds: f.write(f"file '{n}.mp4'\n")

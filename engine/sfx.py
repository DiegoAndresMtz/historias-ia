"""Música + efectos procedurales, mezclados bajo la voz.
Uso: python3 engine/sfx.py stories/<historia> <parte>  -> build/p<parte>/mix.wav
"""
import sys, json, re, importlib.util
import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve, butter, sosfilt

STORY, PART = sys.argv[1].rstrip("/"), int(sys.argv[2])
spec = importlib.util.spec_from_file_location("guion", f"{STORY}/guion.py"); G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
B = f"{STORY}/build/p{PART}"
SR = 44100
D = json.load(open(f"{B}/timeline.json")); TL = D["lines"]; END = D["END"]; N = int(END * SR)
IDX = {l["scene"]: i for i, l in enumerate(TL)}
rng = np.random.default_rng(PART * 11)
out = np.zeros(N); rev = np.zeros(N); mus = np.zeros(N)
def T(s): return np.arange(int(s * SR)) / SR
def put(buf, sig, t0, g=1.0):
    i = int(t0 * SR)
    if i >= N or i < 0: return
    j = min(N, i + len(sig)); buf[i:j] += sig[:j - i] * g
def add(sig, t0, g=1.0, r=0.25): put(out, sig, t0, g); put(rev, sig, t0, g * r)
def lp(x, f): return sosfilt(butter(2, f, btype="low", fs=SR, output="sos"), x)
def hp(x, f): return sosfilt(butter(2, f, btype="high", fs=SR, output="sos"), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], btype="band", fs=SR, output="sos"), x)
def env(n, a, d): t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def clean(x): return re.sub(r"[^\wáéíóúñü]", "", x.lower())
def S(sc): return TL[IDX[sc]]["start"]
def W(sc, tok):
    for x, a, b in TL[IDX[sc]]["words"]:
        if clean(x).startswith(clean(tok)): return a
    return S(sc)

# ---------- efectos ----------
def ping(f=1760, d=0.4): t = T(d); return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(4 * np.pi * f * t)) * env(len(t), 0.002, 0.09)
def pop_(): t = T(0.12); return np.sin(2 * np.pi * (500 + 1500 * t / 0.12) * t) * env(len(t), 0.002, 0.03)
def whoosh(d=0.5): t = T(d); return bp(rng.normal(0, 1, len(t)), 500, 4000) * np.sin(np.pi * t / d) ** 2 * 0.5
def boom(d=2.5, f0=50):
    t = T(d); f = f0 * (1 + 1.5 * np.exp(-t * 8)); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(len(t), 0.005, 0.7) + lp(rng.normal(0, 1, len(t)), 200) * env(len(t), 0.002, 0.25) * 0.8
def heart():
    t = T(0.7); s = np.zeros(len(t))
    for off, a in ((0, 1), (0.22, 0.7)):
        i = int(off * SR); tt = t[:len(t) - i]; s[i:] += a * np.sin(2 * np.pi * 50 * tt) * env(len(tt), 0.004, 0.07)
    return s
def riser(d, f0=200, f1=1200):
    t = T(d); f = f0 * (f1 / f0) ** (t / d); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * 0.3 + np.sin(ph * 1.06) * 0.2) * (t / d) ** 2 + bp(rng.normal(0, 1, len(t)), 300, 6000) * (t / d) ** 2 * 0.2
def doorbell():
    return np.concatenate([ping(659, 0.55) * 1.2, ping(523, 0.9) * 1.2])
def scrape():
    t = T(0.9); n = bp(rng.normal(0, 1, len(t)), 200, 1500); m = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 23 * t))
    return n * m * np.sin(np.pi * t / 0.9) * 0.9
def paper():
    t = T(0.5); return hp(rng.normal(0, 1, len(t)), 2500) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 9 * t))) * np.sin(np.pi * t / 0.5) * 0.5
def steps():
    s = np.zeros(int(2.2 * SR))
    for k in range(4):
        i = int(k * 0.5 * SR); m = int(0.12 * SR); s[i:i + m] += lp(rng.normal(0, 1, m), 300) * env(m, 0.002, 0.03) * 2
    return s
def creak():
    t = T(1.4); f = 90 + 40 * np.sin(2 * np.pi * 0.7 * t) + 15 * rng.normal(0, 1, len(t)).cumsum() / SR * 30
    ph = 2 * np.pi * np.cumsum(np.abs(f)) / SR; s = np.sign(np.sin(ph)) * 0.3 + np.sin(ph * 3) * 0.2
    return bp(s, 200, 2500) * np.sin(np.pi * t / 1.4) * 0.8
def knock1():
    m = int(0.18 * SR); return lp(rng.normal(0, 1, m), 400) * env(m, 0.001, 0.035) * 2.5 + np.sin(2 * np.pi * 110 * T(0.18)) * env(m, 0.001, 0.05)
def knock3():
    s = np.zeros(int(2.4 * SR))
    for k in range(3): i = int(k * 0.75 * SR); kk = knock1(); s[i:i + len(kk)] += kk
    return s
def lock():
    a = hp(rng.normal(0, 1, int(0.05 * SR)), 1500) * env(int(0.05 * SR), 0.001, 0.01)
    s = np.zeros(int(0.3 * SR)); s[:len(a)] += a; s[int(0.12 * SR):int(0.12 * SR) + len(a)] += a * 1.4; return s
def whisper():
    t = T(1.6); return bp(rng.normal(0, 1, len(t)), 2000, 7000) * (0.5 + 0.5 * np.sin(2 * np.pi * 5 * t) ** 2) * np.sin(np.pi * t / 1.6) * 0.4
FX = {"creak": creak, "knock3": knock3, "lock": lock, "whisper": whisper, "pop": lambda: pop_(), "ping": lambda: ping(1568, 0.5), "boom": lambda: boom(2.8, 45), "boom_s": lambda: boom(1.6, 65) * 0.7,
      "heart": lambda: np.concatenate([heart(), heart()]), "doorbell": doorbell, "scrape": scrape, "paper": paper, "steps": steps,
      "riser_end": lambda: riser(1.2, 200, 900) * 0.6}

hits = []
for sc, lst in getattr(G, "CUES", {}).items():
    if sc not in IDX: continue
    for tok, kind, g in lst:
        tw = W(sc, tok)
        if kind == "riser_end": add(FX[kind](), tw - 1.2, g, 0.4)
        else: add(FX[kind](), tw - (0.05 if kind.startswith("boom") else 0.1), g, 0.4 if kind.startswith("boom") else 0.2)
        if kind == "boom" and g >= 0.9: hits.append(tw)
# golpe inicial (gancho) + transiciones suaves entre escenas
add(boom(2.2, 55) * 0.8, 0.0, 0.9, 0.5); add(whoosh(0.4), 0.0, 0.4)
for l in TL[1:]: add(whoosh(0.35), l["start"] - 0.3, 0.18, 0.1)
for x, a, b in TL[-1]["words"]:
    if clean(x) in ("a", "b"): add(pop_(), a - 0.15, 0.6); add(ping(1320 if clean(x) == "a" else 1568, 0.4), a - 0.1, 0.4)

# ---------- música por tramos ----------
t = np.arange(N) / SR
def piano(f, d=1.6):
    tt = T(d); return (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(4 * np.pi * f * tt) * np.exp(-tt * 3) + 0.2 * np.sin(6 * np.pi * f * tt) * np.exp(-tt * 5)) * env(len(tt), 0.005, 0.6)
SAD = [(220.0, 261.6, 329.6), (174.6, 220.0, 261.6), (261.6, 329.6, 392.0), (196.0, 246.9, 293.7)]
WARM = [(261.6, 329.6, 392.0), (196.0, 246.9, 293.7), (220.0, 261.6, 329.6), (174.6, 220.0, 261.6)]
secs = getattr(G, "MUSIC", {}).get(PART, [(TL[0]["scene"], "tense")])
bounds = [(S(sc) - 0.3 if i else 0.0, kind) for i, (sc, kind) in enumerate(secs)] + [(END, None)]
drone = (np.sin(2 * np.pi * 55 * t) + 0.7 * np.sin(2 * np.pi * 58.3 * t) + 0.3 * np.sin(2 * np.pi * 110.6 * t)) + lp(rng.normal(0, 1, N), 250) * 0.5
trem = (np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 443 * t)) * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * t)) * 0.25
for (a, kind), (b, _) in zip(bounds, bounds[1:]):
    ia, ib = int(a * SR), int(b * SR); fade = np.ones(ib - ia); fl = min(int(0.6 * SR), len(fade) // 3)
    fade[:fl] = np.linspace(0, 1, fl); fade[-fl:] = np.linspace(1, 0, fl)
    if kind in ("dark", "tense"):
        mus[ia:ib] += drone[ia:ib] * (0.09 if kind == "dark" else 0.07) * fade
    if kind == "tense":
        mus[ia:ib] += trem[ia:ib] * 0.05 * fade
        k = a + 0.5
        while k < b - 0.8:
            put(mus, heart() * 0.35, k); k += 0.85
    if kind in ("piano", "warm"):
        prog = SAD if kind == "piano" else WARM; beat = 60 / (70 if kind == "piano" else 80); bt = a; i = 0
        seg = np.zeros(N)
        while bt < b - 0.3:
            ch = prog[(i // 4) % 4]; put(seg, piano(ch[[0, 1, 2, 1][i % 4]] * 2, 1.4), bt, 0.16)
            if i % 4 == 0: put(seg, piano(ch[0] / 2, 3.0), bt, 0.14)
            bt += beat; i += 1
        seg[ia:ib] *= fade; seg[:ia] = 0; seg[ib:] = 0; mus += seg
        if kind == "piano": mus[ia:ib] += drone[ia:ib] * 0.025 * fade
mix_rev = rev + mus * 0.5
dip = np.ones(N)
for h in hits:
    a, b = int((h - 0.5) * SR), int(h * SR)
    if a > 0: dip[a:b] = np.minimum(dip[a:b], np.linspace(1, 0.1, b - a))
ir_t = np.arange(int(2.4 * SR)) / SR; ir = rng.normal(0, 1, len(ir_t)) * np.exp(-ir_t * 2.8); ir = lp(ir, 5000); ir /= np.abs(ir).sum() / 40
bed = (out + mus) * dip + fftconvolve(mix_rev * dip, ir)[:N] * 0.3
sr, v = wavfile.read(f"{B}/voz.wav"); v = v.astype(float) / 32768; v = np.pad(v, (0, max(0, N - len(v))))[:N]
ve = np.convolve(np.abs(v), np.ones(4410) / 4410, mode="same"); ve /= ve.max()
bed *= 1 - 0.5 * np.clip(ve * 3, 0, 1)
bed /= np.abs(bed).max() / 0.55
final = v + bed * 0.8; final /= np.abs(final).max() / 0.95
wavfile.write(f"{B}/mix.wav", SR, (final * 32767).astype(np.int16)); print(PART, "mix ok")

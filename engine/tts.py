"""Voz: Kokoro (gratis, local) con pronunciación latina (es-419).
Uso: python3 engine/tts.py stories/<historia> <parte>
Salida: stories/<historia>/build/p<parte>/voz.wav + timeline.json
"""
import sys, os, json, re, subprocess, importlib.util
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

MODELS = os.environ.get("KOKORO_DIR", "/home/claude/models")
story, part = sys.argv[1].rstrip("/"), int(sys.argv[2])
spec = importlib.util.spec_from_file_location("guion", f"{story}/guion.py"); G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)
LINES = G.PARTS[part]
OUT = f"{story}/build/p{part}"; os.makedirs(OUT, exist_ok=True)

k = Kokoro(f"{MODELS}/kokoro.onnx", f"{MODELS}/voices.bin")
V = k.get_voice_style
# Voz «C · Narrador de suspenso»: latina, más grave, pausas dramáticas
VOICES = {
    "N": (0.7 * V("em_alex") + 0.3 * V("em_santa"), 0.95, 0.95),   # (estilo, velocidad, tono)
    "G": (0.85 * V("em_alex") + 0.15 * V("am_michael"), 0.97, 0.98),
    "M": (V("ef_dora"), 0.92, 0.99),
    "P": (V("em_santa"), 0.9, 0.97),
    "K": (V("ef_dora"), 1.0, 1.28),
    "V": (V("ef_dora"), 0.85, 0.9),                                   # abuela                                   # niño/niña
    "X": (0.6 * V("em_santa") + 0.4 * V("am_onyx"), 0.82, 0.86),     # voz ronca (payaso)
}
def chain(pitch):
    return (f"rubberband=pitch={pitch}:formant=preserved,highpass=f=55,equalizer=f=120:t=q:w=1.2:g=3,"
            "equalizer=f=2800:t=q:w=1:g=1.5,equalizer=f=7000:t=q:w=1:g=-2,"
            "acompressor=threshold=-22dB:ratio=3:attack=4:release=120:makeup=3")

SR = 44100; t = 0.35; segs = []; TL = []
for sc, v, text, pause in LINES:
    st, sp, pitch = VOICES[v]
    if len(text) < 32 and not text.startswith("¿"): sp *= 0.9      # frases cortas = más dramáticas
    a, sr0 = k.create(text, voice=st, speed=sp, lang="es-419")
    sf.write("/tmp/_l.wav", a, sr0)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/_l.wav", "-af", chain(pitch), "-ar", str(SR), "-ac", "1", "/tmp/_l2.wav"], check=True)
    a, _ = sf.read("/tmp/_l2.wav")
    idx = np.where(np.abs(a) > 0.01)[0]; a = a[max(0, idx[0] - 400):idx[-1] + 5000]
    dd = len(a) / SR; spk = dd - 0.12
    words = text.split()
    w = [len(re.sub(r"[^\wáéíóúñü]", "", x, flags=re.I)) + 1.5 + (4 if re.search(r"[.?:]$", x) else (2.5 if re.search(r"[,;]$", x) else 0)) + (3 if x.endswith("...") else 0) for x in words]
    tot = sum(w); acc = t; wt = []
    for x, ww in zip(words, w):
        du = spk * ww / tot; wt.append([x, round(acc, 3), round(acc + du, 3)]); acc += du
    TL.append({"scene": sc, "voice": v, "start": round(t, 3), "end": round(t + dd, 3), "words": wt, "text": text})
    segs.append((t, a)); t += dd + pause
END = round(t + 0.3, 2)
out = np.zeros(int(END * SR) + SR)
for s, a in segs: i0 = int(s * SR); out[i0:i0 + len(a)] += a
out = out[:int(END * SR)]; out /= np.abs(out).max() / 0.9
sf.write(f"{OUT}/voz.wav", (out * 32767).astype(np.int16), SR, subtype="PCM_16")
# envolvente por cuadro (30 fps) para mover la boca
hop = SR // 30; n = len(out) // hop
amp = np.array([np.sqrt(np.mean(out[i * hop:(i + 1) * hop] ** 2)) for i in range(n)])
amp = np.clip(amp / (np.percentile(amp[amp > 0.01], 90) + 1e-6), 0, 1)
json.dump({"END": END, "lines": TL, "amp": [round(float(x), 3) for x in amp]}, open(f"{OUT}/timeline.json", "w"), ensure_ascii=False)
print(part, "END", END)

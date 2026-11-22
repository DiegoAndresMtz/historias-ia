"""Revisa que cada palabra usada en panels.py / FX / CUES / CAM exista en su línea del guion.
Uso: python3 engine/check.py stories/<historia>"""
import sys, re, importlib.util
story = sys.argv[1].rstrip("/")
spec = importlib.util.spec_from_file_location("g", f"{story}/guion.py"); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
src = open(f"{story}/panels.py").read()
def clean(x): return re.sub(r"[^\wáéíóúñü]", "", x.lower())
lines = {sc: text for p in g.PARTS.values() for sc, v, text, pa in p}
bad = []
def has(sc, tok): return any(clean(x).startswith(clean(tok)) for x in lines[sc].split())
for f in re.split(r"\ndef ", src):
    name = f.split("(")[0]
    if name in lines:
        for tok in re.findall(r'w\("([^"]+)"\)', f):
            if not has(name, tok): bad.append((name, tok))
for m in re.finditer(r'CAM\["(\w+)"\] = \[(.*)\]', src):
    for tok in re.findall(r'\("([^"]+)",', m.group(2)):
        if not has(m.group(1), tok): bad.append((m.group(1), tok))
for sc, lst in getattr(g, "FX", {}).items():
    for tok, _ in lst:
        if not has(sc, tok): bad.append((sc, tok))
for sc, lst in getattr(g, "CUES", {}).items():
    for tok, _, _ in lst:
        if not has(sc, tok): bad.append((sc, tok))
missing = [k for k in lines if f"def {k}(" not in src]
print("palabras que no existen:", bad or "ninguna"); print("escenas sin dibujar:", missing or "ninguna")
sys.exit(1 if bad or missing else 0)

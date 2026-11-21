# Historias varias

Videos de historias POV en 3 partes para TikTok, YouTube e Instagram.

## Preparar una sesión nueva
```bash
bash setup.sh   # librerías (requirements.txt), voz Kokoro y fuentes
```

## Hacer una historia
```bash
python3 engine/tts.py stories/<historia> <parte>                     # voz + tiempos de cada palabra
python3 engine/render.py stories/<historia> <parte> stills a01+1.0   # cuadros de prueba
python3 engine/render.py stories/<historia> <parte> render 2         # video por escenas
```

## Estructura
- `engine/`: motor común.
  - `tts.py`: voz «narrador de suspenso», latina y más grave.
  - `render.py`: cortes de cámara cada 1–3 s, flash, temblor, glitch, viñeta, subtítulos, boca sincronizada y tarjeta A/B.
  - `lib.py` y `povlib.py`: dibujo y personajes.
- `stories/<historia>/`:
  - `guion.py`: líneas, palabras clave, efectos, sonidos y música.
  - `panels.py`: escenas.
- `videos/<fecha>/`: videos finales. Buffer los publica desde aquí.

#!/usr/bin/env bash
# Prepara una sesión nueva: librerías, voz (Kokoro) y fuentes.
set -e
cd "$(dirname "$0")"
pip install -q --break-system-packages -r requirements.txt
command -v ffmpeg >/dev/null || (apt-get update -qq && apt-get install -y -qq ffmpeg)
# ffmpeg necesita rubberband (tono de la voz)
ffmpeg -hide_banner -filters 2>/dev/null | grep -q rubberband || echo "AVISO: ffmpeg sin rubberband"
M="${KOKORO_DIR:-/home/claude/models}"; mkdir -p "$M"
R=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s "$M/kokoro.onnx" ] || curl -sL -o "$M/kokoro.onnx" "$R/kokoro-v1.0.onnx"
[ -s "$M/voices.bin" ]  || curl -sL -o "$M/voices.bin"  "$R/voices-v1.0.bin"
# Fuentes (Montserrat para textos, Crimson Text para letra a mano)
if ! fc-list | grep -qi montserrat; then
  F=/usr/local/share/fonts/hv; mkdir -p $F; G=https://raw.githubusercontent.com/google/fonts/main/ofl
  curl -sL -o "$F/Montserrat.ttf" "$G/montserrat/Montserrat%5Bwght%5D.ttf"
  curl -sL -o "$F/CrimsonText-Italic.ttf" "$G/crimsontext/CrimsonText-Italic.ttf"
  fc-cache -f >/dev/null
fi
echo "Listo: librerías, voz y fuentes instaladas."
# Motor de animación Remotion (personajes Open Peeps, CC0)
if [ -f remo/package.json ]; then (cd remo && npm ci --silent --no-audit --no-fund) && echo "Remotion listo"; fi

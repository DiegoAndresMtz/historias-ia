#!/usr/bin/env bash
# Renderiza una parte con Remotion. Uso: engine/remo_render.sh <slug> <parte> <salida.mp4>
# (la composición se llama <slug con guiones>-p<N>; ~12 min por cada 50 s de video con 2 núcleos)
set -e
ID="$(echo $1 | tr '_' '-')-p$2"; O=$(realpath -m "$3"); mkdir -p "$(dirname "$O")"
cd remo
CH=$(command -v google-chrome || command -v chromium || true)
npx remotion render src/index.ts "$ID" "$O.tmp.mp4" ${CH:+--browser-executable=$CH} --concurrency=2 --codec=h264 --crf=20 --log=error
# Remotion deja archivos muy pesados (16 Mbps): se recomprimen para que GitHub (límite 100 MB) y Buffer los acepten
ffmpeg -v error -y -i "$O.tmp.mp4" -c:v libx264 -preset veryfast -crf 23 -maxrate 7M -bufsize 14M -pix_fmt yuv420p -c:a copy -movflags +faststart "$O"
rm -f "$O.tmp.mp4"; ls -la "$O"

#!/usr/bin/env bash
# Renderiza una parte con Remotion. Uso: engine/remo_render.sh <slug> <parte> <salida.mp4>
# (la composición se llama <slug con guiones>-p<N>; ~12 min por cada 50 s de video con 2 núcleos)
set -e
ID="$(echo $1 | tr '_' '-')-p$2"; O=$(realpath -m "$3"); mkdir -p "$(dirname "$O")"
cd remo
CH=$(command -v google-chrome || command -v chromium || true)
npx remotion render src/index.ts "$ID" "$O.tmp.mp4" ${CH:+--browser-executable=$CH} --concurrency=2 --codec=h264 --crf=20 --log=error
mv "$O.tmp.mp4" "$O"; ls -la "$O"

#!/usr/bin/env bash
# Voz + efectos + música para el motor Remotion. Uso: engine/remo_audio.sh <slug> <parte>
# Deja remo/src/data/<slug>_p<N>.json (tiempos de cada palabra) y remo/public/<slug>_p<N>.m4a (audio final, -14 LUFS).
set -e
S=stories/$1; P=$2; B=$S/build/p$P
python3 engine/tts.py $S $P
python3 engine/sfx.py $S $P
mkdir -p remo/src/data remo/public
cp $B/timeline.json remo/src/data/$1_p$P.json
ffmpeg -v error -y -i $B/mix.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100,aformat=channel_layouts=stereo" -c:a aac -b:a 192k remo/public/$1_p$P.m4a
echo "audio listo: $1 parte $P"

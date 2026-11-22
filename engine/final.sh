#!/usr/bin/env bash
# Une escenas + mezcla y codifica para redes. Uso: engine/final.sh stories/<historia> <parte> <salida.mp4>
set -e
S=$1; P=$2; O=$3; B=$S/build/p$P
python3 engine/sfx.py $S $P
ffmpeg -v error -y -f concat -safe 0 -i $B/seg/list.txt -c copy $B/video.mp4
mkdir -p "$(dirname "$O")"
VF="null"; [ -f $B/label.png ] && VF="movie=$B/label.png[l];[in][l]overlay=0:0"
ffmpeg -v error -y -i $B/video.mp4 -i $B/mix.wav -vf "$VF" -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 22 -maxrate 6M -bufsize 12M -tune animation -pix_fmt yuv420p \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100,aformat=channel_layouts=stereo" -c:a aac -b:a 192k -movflags +faststart -shortest "$O.tmp.mp4"
mv "$O.tmp.mp4" "$O"; ls -la "$O"

#!/usr/bin/env bash
# Build a finished Reel (video + original music) from a spec file.
# Usage: tools/make_reel.sh specs/2026-10-27_millet_noodles.json reels/2026-10-27_millet_noodles.mp4
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
spec="$1"; out="$2"
tmp="$(mktemp -d)"
python3 "$here/reel_maker.py" "$spec" "$tmp/silent.mp4"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$tmp/silent.mp4")
mood=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('music','warm'))" "$spec")
python3 "$here/music_maker.py" "$tmp/music.wav" "$dur" "$mood"
ffmpeg -loglevel error -y -i "$tmp/silent.mp4" -i "$tmp/music.wav" -map 0:v -map 1:a -c:v copy \
  -c:a aac -b:a 160k -af "loudnorm=I=-16:TP=-1.5" -shortest -movflags +faststart "$out"
rm -rf "$tmp"
echo "built $out"

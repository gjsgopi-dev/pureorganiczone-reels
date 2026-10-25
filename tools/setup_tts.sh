#!/usr/bin/env bash
# One-time download of the offline narration engine (Kokoro-82M + espeak-ng from piper). ~150 MB.
set -euo pipefail
C="${TTS_HOME:-$HOME/.cache/reel_tts}"; mkdir -p "$C"; cd "$C"
[ -s kokoro.onnx ] || curl -sSL -o kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx
[ -s voices.bin ] || curl -sSL -o voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
if [ ! -x piper/espeak-ng ]; then
  curl -sSL -o piper.tgz https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz
  tar -xzf piper.tgz && rm piper.tgz && chmod +x piper/espeak-ng
fi
python3 -c "import onnxruntime" 2>/dev/null || pip install -q onnxruntime --break-system-packages
echo "narration engine ready in $C"

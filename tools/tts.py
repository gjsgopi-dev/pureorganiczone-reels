"""Offline neural narration (Kokoro-82M ONNX + espeak-ng phonemes).

Usage: python3 tts.py out.wav "text to speak" [voice] [speed] [lang]
voice defaults to af_heart; lang is the espeak voice (en-us, en-gb, hi).
"""
import json, os, re, subprocess, sys
import numpy as np
import onnxruntime as ort
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("TTS_HOME", os.path.expanduser("~/.cache/reel_tts"))
PIPER = os.path.join(CACHE, "piper")
SR = 24000
VOCAB = json.load(open(os.path.join(HERE, "kokoro_config.json")))["vocab"]


def espeak_ipa(text, lang):
    env = dict(os.environ, LD_LIBRARY_PATH=PIPER)
    out = subprocess.run([os.path.join(PIPER, "espeak-ng"), f"--path={PIPER}/espeak-ng-data",
                          "-q", "--ipa", "-v", lang, text], capture_output=True, text=True, env=env).stdout
    return " ".join(out.split())


def phonemize(text, lang):
    # keep punctuation (espeak drops it) by phonemizing the pieces between marks
    parts = re.split(r"([,.!?;:—…])", text)
    ph = ""
    for p in parts:
        if not p.strip():
            continue
        if re.fullmatch(r"[,.!?;:—…]", p):
            ph = ph.rstrip() + p + " "
        else:
            ph += espeak_ipa(p, lang) + " "
    return "".join(c for c in ph.strip() if c in VOCAB)


def synth(text, voice="af_heart", speed=1.0, lang="en-us"):
    sess = ort.InferenceSession(os.path.join(CACHE, "kokoro.onnx"), providers=["CPUExecutionProvider"])
    names = {i.name: i for i in sess.get_inputs()}
    tok_name = "input_ids" if "input_ids" in names else "tokens"
    voices = np.load(os.path.join(CACHE, "voices.bin"))
    style_all = voices[voice]
    audio = []
    # sentence chunks keep each run under the 510-phoneme limit
    for sent in re.split(r"(?<=[.!?])\s+", text.strip()):
        if not sent:
            continue
        ph = phonemize(sent, lang)
        toks = [VOCAB[c] for c in ph][:508]
        style = style_all[min(len(toks), len(style_all)) - 1]
        speed_dtype = np.int32 if "int" in names["speed"].type else np.float32
        out = sess.run(None, {tok_name: np.array([[0, *toks, 0]], dtype=np.int64),
                              "style": np.asarray(style, dtype=np.float32),
                              "speed": np.array([speed], dtype=speed_dtype)})[0]
        audio.append(out.squeeze())
        audio.append(np.zeros(int(SR * 0.18), dtype=np.float32))
    return np.concatenate(audio)


if __name__ == "__main__":
    out, text = sys.argv[1], sys.argv[2]
    voice = sys.argv[3] if len(sys.argv) > 3 else "af_heart"
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    lang = sys.argv[5] if len(sys.argv) > 5 else "en-us"
    a = synth(text, voice, speed, lang)
    a = a / max(1e-6, np.max(np.abs(a))) * 0.9
    wavfile.write(out, SR, (a * 32767).astype(np.int16))
    print(f"wrote {out} {len(a)/SR:.1f}s")

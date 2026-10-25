"""Build a narrated Reel: per-scene voiceover, scenes timed to the voice, music ducked underneath.

Usage: python3 tools/make_reel.py specs/<file>.json reels/<file>.mp4

Spec extras (all optional):
  "voice": Kokoro voice id (default "af_heart"); "speed": 1.0; "lang": espeak voice ("en-us")
  scene "say": the line spoken over that scene. Scenes without "say" keep their "dur".
Run tools/setup_tts.sh once per machine before the first build.
"""
import json, os, subprocess, sys, tempfile
import numpy as np
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tts  # noqa: E402

SR = tts.SR
LEAD = 0.3   # silence before each line
TAIL = 0.45  # breathing room after each line


def main(spec_path, out_path):
    spec = json.load(open(spec_path))
    voice, speed, lang = spec.get("voice", "af_heart"), spec.get("speed", 1.0), spec.get("lang", "en-us")
    tmp = tempfile.mkdtemp()
    clips, starts, t = [], [], 0.0
    for sc in spec["scenes"]:
        if sc.get("say"):
            a = tts.synth(sc["say"], voice, speed, lang)
            a = a / max(1e-6, np.max(np.abs(a))) * 0.9
            sc["dur"] = max(sc.get("min_dur", 2.6), LEAD + len(a) / SR + TAIL)
            clips.append(a)
            starts.append(t + LEAD)
        t += sc.get("dur", 3.0)
    total = t
    voice_track = np.zeros(int(SR * (total + 0.5)), dtype=np.float32)
    for a, s in zip(clips, starts):
        i = int(SR * s)
        voice_track[i:i + len(a)] += a[: len(voice_track) - i]
    vwav = os.path.join(tmp, "voice.wav")
    wavfile.write(vwav, SR, (np.clip(voice_track, -1, 1) * 32767).astype(np.int16))

    if spec.get("avatar") is not None:
        # loudness per video frame drives the presenter's mouth
        hop = SR // 30
        n = len(voice_track) // hop
        rms = np.sqrt(np.mean(voice_track[: n * hop].reshape(n, hop) ** 2, axis=1))
        env = np.clip(rms / (np.percentile(rms[rms > 0.005], 90) if np.any(rms > 0.005) else 1), 0, 1)
        envp = os.path.join(tmp, "env.npy")
        np.save(envp, env)
        spec["avatar"] = dict(spec["avatar"] or {}, envelope=envp)

    timed = os.path.join(tmp, "timed.json")
    json.dump(spec, open(timed, "w"), ensure_ascii=False)
    silent = os.path.join(tmp, "silent.mp4")
    subprocess.run([sys.executable, os.path.join(HERE, "reel_maker.py"), timed, silent], check=True)

    mwav = os.path.join(tmp, "music.wav")
    subprocess.run([sys.executable, os.path.join(HERE, "music_maker.py"), mwav, f"{total:.2f}",
                    spec.get("music", "warm")], check=True)

    # music sits low and dips further whenever the narrator speaks (sidechain ducking)
    filt = ("[1:a]aresample=44100,volume=0.55[m];[2:a]aresample=44100,asplit=2[v][vk];"
            "[m][vk]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[md];"
            "[v][md]amix=inputs=2:duration=longest:normalize=0,loudnorm=I=-15:TP=-1.5[a]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", silent, "-i", mwav, "-i", vwav,
                    "-filter_complex", filt, "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-t", f"{total:.2f}", "-movflags", "+faststart",
                    out_path], check=True)
    print(f"built {out_path} {total:.1f}s with {len(clips)} narrated scenes")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

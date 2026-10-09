"""Makes the rendered lines sound like the game's recordings, and encodes them for the mod.

usage: python finish.py <render-dir> <speech-wav-dir> <sltool> <mod-dir> [<line>...]

The game's lines share one radio sound: a band that falls away steeply above about 5 kHz, and
heavy limiting. The renders vary in how tinny they are, because each copies the sound of its
reference. So each line gets an equalizer of its own: its third-octave spectrum is compared with
the average of its character's recorded lines, and the difference is made up. The equalizer cuts
freely but boosts at most 6 dB, so as not to raise noise. The line's leading and trailing silence
is trimmed to the game's, it's compressed as the game's lines are, and it's brought to the median
loudness of its character's recorded lines under a limiter.

Last, the line is encoded in the game's speech format and decoded again. The format overshoots full
scale on loud speech, so a line that overshoots more often than most of the game's own lines is
made 1 dB quieter until it doesn't.

A briefing is a speech file too: Enriquez speaks it over the briefing room, as she does the game's
own `enddebriefing.ut` at the campaign's end.

Each line is written to <render-dir>/final as a WAV file, and to <mod-dir> as a speech file named
after the line. finish.json records each line's loudness, its peak, and how far its spectrum still
is from its character's after the equalizer.
"""

import json
import os
import re
import statistics
import subprocess
import sys

import librosa
import numpy as np
import soundfile

import voices

render_dir, speech_dir, sltool, mod_dir = sys.argv[1:5]
only = set(sys.argv[5:])
RATE = 22050
CENTRES = [63, 100, 160, 250, 400, 630, 1000, 1600, 2500, 4000, 5000, 6300, 8000, 10000]
REFERENCE = CENTRES.index(1000)
CEILING = 0.89  # -1 dBFS
# How each voice is compressed: the radio's lines are limited hard, as the game's are, and
# Enriquez's words in person not at all, as her spoken briefing at the campaign's end isn't.
RADIO_COMPRESSOR = "acompressor=threshold=-24dB:ratio=4:attack=3:release=80:makeup=6dB"
IN_PERSON_COMPRESSOR = "anull"
IN_PERSON_VOICES = {"enriquez_spoken"}
OVERSHOOT = 0.001  # Full-scale samples a line may have, decoded: 1 a thousand.
freqs = librosa.fft_frequencies(sr=RATE, n_fft=2048)


def band_levels(paths):
    """The average third-octave levels of the speech in `paths`, relative to 1 kHz."""
    total, frames = None, 0
    for path in paths:
        wav, _ = librosa.load(path, sr=RATE)
        wav, _ = librosa.effects.trim(wav, top_db=35)
        if len(wav) < RATE // 4:
            continue
        power = np.abs(librosa.stft(wav, n_fft=2048, hop_length=512)) ** 2
        loud = power[:, power.sum(axis=0) > power.sum(axis=0).max() * 1e-3]
        total = loud.sum(axis=1) if total is None else total + loud.sum(axis=1)
        frames += loud.shape[1]
    spectrum = total / frames
    levels = []
    for centre in CENTRES:
        mask = (freqs >= centre / 2 ** (1 / 6)) & (freqs < centre * 2 ** (1 / 6))
        levels.append(10 * np.log10(spectrum[mask].mean() + 1e-12))
    levels = np.array(levels)
    return levels - levels[REFERENCE]


def equalizer(target, current, gains=None):
    """The gains that bring `current` to `target`. The first pass is smoothed across neighbouring
    bands; later passes, added to the gains so far, correct each band sharply, as the radio's band
    falls away steeply below the voice. They cut freely, but boost little, so as not to raise
    noise."""
    make_up = target - current
    if gains is None:
        total = np.convolve(np.pad(make_up, 1, mode="edge"), [0.25, 0.5, 0.25], mode="valid")
    else:
        total = gains + make_up
    return np.clip(total, -40.0, 6.0)


def entries(gains):
    """The equalizer's curve as ffmpeg's entries: dense, a sixth of an octave apart, interpolated
    between the bands on a logarithmic frequency scale, so that it bends smoothly."""
    points = []
    frequency = 40.0
    while frequency < RATE / 2:
        gain = np.interp(np.log(frequency), np.log(CENTRES), gains)
        points.append(f"entry({frequency:.0f},{gain:.2f})")
        frequency *= 2 ** (1 / 6)
    points.append(f"entry({RATE // 2},{gains[-1]:.2f})")
    return ";".join(points)


def run(source, target, chain):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", source, "-af", chain, "-ac", "1", "-ar", str(RATE),
                    "-sample_fmt", "s16", target], check=True)


def full_scale(path):
    """How many samples of a 16-bit WAV file sit at full scale."""
    wav, _ = librosa.load(path, sr=None, mono=True)
    return int(np.sum(np.abs(wav) >= 32767 / 32768))


def samples(path):
    return int(librosa.get_duration(path=path) * RATE)


def loudness(path):
    result = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=sample", "-f", "null", "-"],
                            capture_output=True, text=True)
    integrated = re.findall(r"I:\s+(-?[\d.]+) LUFS", result.stderr)
    peak = re.findall(r"Peak:\s+(-?[\d.inf]+) dBFS", result.stderr)
    return float(integrated[-1]), float(peak[-1]) if peak else None


checks = json.load(open(os.path.join(render_dir, "checks.json")))
final_dir = os.path.join(render_dir, "final")
os.makedirs(final_dir, exist_ok=True)
os.makedirs(mod_dir, exist_ok=True)
report_path = os.path.join(render_dir, "finish.json")
report = json.load(open(report_path)) if os.path.exists(report_path) else {}

by_voice = {}
for name, check in checks.items():
    if not only or name in only:
        by_voice.setdefault(check["voice"], []).append(name)

for voice, names in by_voice.items():
    originals = voices.files_of(speech_dir, voice)
    target_levels = band_levels(originals)
    # Their median loudness, but no louder than -6 LUFS, so the hottest voices aren't squashed more
    # than they need to be.
    target_loudness = min(statistics.median(loudness(f)[0] for f in originals[:: max(1, len(originals) // 30)]), -6.0)
    for name in names:
        raw = os.path.join(render_dir, "raw", f"{name}.wav")
        final = os.path.join(final_dir, f"{name}.wav")
        shaped = final + ".shaped.wav"
        # The game's lines start and end with the speech; the renders open with a pause.
        trimmed = final + ".trimmed.wav"
        wav, rate = librosa.load(raw, sr=None)
        wav, _ = librosa.effects.trim(wav, top_db=40)
        soundfile.write(trimmed, np.concatenate([np.zeros(int(0.02 * rate)), wav, np.zeros(int(0.03 * rate))]), rate)
        raw = trimmed
        # The equalizer, measured after the compressor and corrected again, four times, since
        # the compressor shifts the balance of the bands.
        compressor = IN_PERSON_COMPRESSOR if voice in IN_PERSON_VOICES else RADIO_COMPRESSOR
        gains = equalizer(target_levels, band_levels([raw]))
        for _ in range(4):
            run(raw, shaped, f"aresample={RATE},firequalizer=delay=0.1:accuracy=1:gain_entry='{entries(gains)}',{compressor}")
            gains = equalizer(target_levels, band_levels([shaped]), gains)
        # Gain into the limiter, up to four times, since limiting takes some loudness back. Then the line is
        # encoded and decoded as the game plays it. The speech codec overshoots full scale on loud
        # speech: the game's own lines do in about 1.5 samples a thousand, which OpenReliant rounds
        # off (`cbox.softClip`) and the original cuts flat. While a line overshoots in more than
        # `OVERSHOOT` of its samples, cleaner than two in three of the game's lines, it goes through
        # again 1 dB quieter.
        gain = target_loudness - loudness(shaped)[0]
        encoded = os.path.join(mod_dir, f"{name}.ut")
        decoded = final + ".decoded.wav"
        for lowered in range(0, 13):
            ceiling = CEILING * 10 ** (-lowered / 20)
            line_gain = gain - lowered
            for _ in range(4):
                run(shaped, final, f"volume={line_gain:.2f}dB,alimiter=limit={ceiling:.4f}:attack=1:release=50:level=false")
                short = (target_loudness - lowered) - loudness(final)[0]
                if short < 0.5:
                    break
                line_gain += short
            subprocess.run([sltool, "speech", "encode", final, encoded], check=True, capture_output=True)
            subprocess.run([sltool, "speech", "decode", encoded, decoded], check=True, capture_output=True)
            if full_scale(decoded) <= OVERSHOOT * samples(decoded):
                break
        os.remove(shaped)
        os.remove(trimmed)
        integrated, peak = loudness(final)
        played_loudness, played_peak = loudness(decoded)
        clipped = full_scale(decoded)
        samples_played = samples(decoded)
        os.remove(decoded)
        off = band_levels([final]) - target_levels
        report[name] = {
            "voice": voice,
            "loudness": integrated,
            "target": round(target_loudness, 1),
            "peak": peak,
            "played_peak": played_peak,
            "played_loudness": played_loudness,
            "lowered": lowered,
            "overshoot": round(1000 * clipped / samples_played, 2),
            # How far its spectrum still is from its character's, up to 5 kHz and above.
            "off_in_band": round(float(np.abs(off[1:CENTRES.index(5000)]).max()), 1),
            "off_above": round(float(np.abs(off[CENTRES.index(5000):]).max()), 1),
        }
    print(f"{voice}: {len(names)} lines, {target_loudness:.1f} LUFS", flush=True)

json.dump(report, open(report_path, "w"), indent=1)
peaks = [r["played_peak"] for r in report.values() if r.get("played_peak") is not None]
print(f"{len(report)} lines; highest peak as played {max(peaks):.2f} dBFS, "
      f"most overshoot {max(r['overshoot'] for r in report.values()):.2f} samples a thousand; "
      f"largest spectral difference left {max(r['off_in_band'] for r in report.values()):.1f} dB up to 5 kHz, "
      f"{max(r['off_above'] for r in report.values()):.1f} dB above")

"""Synthesized 120 BPM electronic track synced to the video cuts. Writes music.wav (stereo, 44.1k)."""
import wave
import numpy as np
from scipy.signal import butter, sosfilt

SR, DUR, BPM = 44100, 16.0, 120
BEAT = 60 / BPM
N = int(SR * DUR)
CUTS = [2.0, 4.0, 10.0, 12.25]            # scene changes -> impacts
WIPES = [1.6, 3.6, 9.65, 11.9]           # wipe starts -> whooshes
rng = np.random.default_rng(7)
L, R = np.zeros(N), np.zeros(N)

def add(sig, t0, gain=1.0, pan=0.0):
    s = int(t0 * SR)
    if s >= N: return
    sig = sig[: N - s] * gain
    L[s:s + len(sig)] += sig * (1 - max(0, pan))
    R[s:s + len(sig)] += sig * (1 + min(0, pan))

def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)

def lp(x, f, order=2): return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)
def hp(x, f, order=2): return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)
def saw(f, t): return 2 * ((f * t) % 1) - 1
def note(m): return 440 * 2 ** ((m - 69) / 12)

def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(45 + 140 * np.exp(-t * 35)) / SR
    return np.tanh(2 * np.sin(ph) * np.exp(-t * 7))

def clap():
    n = int(0.3 * SR); x = rng.standard_normal(n)
    e = sum(env(n, 0.001, 0.012) * (np.arange(n) >= int(k * 0.011 * SR)) for k in range(3)) + env(n, 0.001, 0.12) * 0.6
    return hp(lp(x, 4000), 900) * e

def hat(open_=False):
    n = int((0.25 if open_ else 0.06) * SR)
    return hp(rng.standard_normal(n), 7000) * env(n, 0.001, 0.08 if open_ else 0.015)

def impact():
    n = int(2.0 * SR); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(30 + 60 * np.exp(-t * 8)) / SR) * np.exp(-t * 2.2)
    noise = lp(rng.standard_normal(n), 2500) * np.exp(-t * 4) * 0.5
    return np.tanh(1.5 * (boom + noise))

def whoosh(d=0.45):
    n = int(d * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    # sweep band by blending lp of increasing cutoff
    out = np.zeros(n); seg = n // 8
    for i in range(8):
        f = 300 * 2 ** (i * 0.7)
        out[i * seg:(i + 1) * seg] = lp(x, min(f, 15000))[i * seg:(i + 1) * seg]
    return out * np.sin(np.pi * t / d) ** 2

# --- chords: Am F C G (one bar = 4 beats = 2s each) ---
PROG = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]
BASS = [45, 41, 48, 43]
t_all = np.arange(N) / SR

# sidechain envelope from kick positions
side = np.ones(N)
for b in range(int(DUR / BEAT)):
    t0 = b * BEAT
    if t0 < 2.0 or 15.0 <= t0: continue
    s = int(t0 * SR); n = int(BEAT * SR)
    tt = np.arange(min(n, N - s)) / SR
    side[s:s + len(tt)] = 1 - 0.75 * np.exp(-tt * 9)

pad = np.zeros(N)
for bar in range(8):
    s, e = int(bar * 2 * SR), min(N, int((bar + 1) * 2 * SR))
    tt = t_all[s:e]
    for m in PROG[bar % 4]:
        for det in (-0.08, 0.08):
            pad[s:e] += saw(note(m + 12) * (1 + det / 100 * 12), tt)
pad = lp(pad, 1800) * 0.06
pad *= np.clip(t_all / 1.5, 0, 1)
add(pad * side, 0, pan=-0.2); add(pad * side, 0.012, pan=0.2)

# pluck arpeggio, 16ths, from bar 2
for i in range(int(DUR / (BEAT / 4))):
    t0 = i * BEAT / 4
    if t0 < 4.0 or t0 >= 15.0: continue
    ch = PROG[int(t0 // 2) % 4]
    m = (ch + (ch[0] + 12,))[[0, 1, 2, 3, 2, 1, 2, 3][i % 8]] + 12
    n = int(0.25 * SR); tt = np.arange(n) / SR
    p = lp(saw(note(m), tt) * env(n, 0.002, 0.07), 3500) * 0.12
    add(p, t0, pan=0.35 if i % 2 else -0.35)
    add(p * 0.35, t0 + BEAT * 0.75, pan=-0.35 if i % 2 else 0.35)  # ping-pong delay

# drums + bass
for b in range(int(DUR / BEAT)):
    t0 = b * BEAT
    if 2.0 <= t0 < 15.0:
        add(kick(), t0, 0.9)
        if b % 2: add(clap(), t0, 0.35)
        add(hat(), t0 + BEAT / 2, 0.18, pan=0.3)
        if t0 >= 4.0: add(hat(), t0 + BEAT / 4, 0.07, -0.3); add(hat(), t0 + 3 * BEAT / 4, 0.07, -0.3)
        if b % 4 == 3: add(hat(True), t0 + BEAT / 2, 0.1)
        # offbeat sub bass
        n = int(BEAT / 2 * SR); tt = np.arange(n) / SR
        root = note(BASS[int(t0 // 2) % 4] - 12)
        bs = (np.sin(2 * np.pi * root * tt) + 0.3 * lp(saw(root, tt), 400)) * env(n, 0.005, 0.18)
        add(bs, t0 + BEAT / 2, 0.45)

# intro riser into first drop
n = int(2.0 * SR); tt = np.arange(n) / SR
rise = lp(rng.standard_normal(n), 6000) * (tt / 2) ** 2 * 0.25 + np.sin(2 * np.pi * np.cumsum(200 + 600 * (tt / 2) ** 2) / SR) * (tt / 2) ** 2 * 0.08
add(rise, 0.0)

for c in CUTS: add(impact(), c, 0.55)
for w in WIPES: add(whoosh(), w, 0.35)

# outro: final hit at logo, tail
add(impact(), 15.0, 0.4)

mix = np.stack([L, R], 1)
mix *= np.clip((DUR - t_all) / 0.8, 0, 1)[:, None]
mix = np.tanh(mix * 1.3)
mix /= np.abs(mix).max() / 0.9
pcm = (mix * 32767).astype(np.int16)
with wave.open("music.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("music.wav written")

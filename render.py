"""Kalmuk Media - Instagram Reels (9:16) motion graphics promo.
Render: python3 render.py  -> kalmuk_media_reels.mp4
"""
import math, subprocess, wave, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DUR = 1080, 1920, 30, 16.0
N = int(FPS * DUR)
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BG1, BG2 = (10, 8, 30), (35, 10, 70)
ACC1, ACC2 = (255, 70, 140), (0, 210, 255)
WHITE = (255, 255, 255)
_fc = {}
def F(size, bold=True):
    k = (size, bold)
    if k not in _fc: _fc[k] = ImageFont.truetype(BOLD if bold else REG, size)
    return _fc[k]

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, s, d): return clamp((t - s) / d)
def eo(x): return 1 - (1 - x) ** 3
def back(x, s=1.7): x -= 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, x): return a + (b - a) * x
def mix(c1, c2, x): return tuple(int(lerp(a, b, x)) for a, b in zip(c1, c2))

# static gradient background
gy = np.linspace(0, 1, H)[:, None, None]
BASE = (np.array(BG1) * (1 - gy) + np.array(BG2) * gy).repeat(W, 1).astype(np.uint8)
random.seed(4)
PARTS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(1, 4), random.uniform(20, 80)) for _ in range(70)]

def text_c(d, y, s, font, fill, x=W // 2):
    b = d.textbbox((0, 0), s, font=font)
    d.text((x - (b[2] - b[0]) / 2 - b[0], y), s, font=font, fill=fill)

def layer_text(s, font, fill):
    b = font.getbbox(s)
    im = Image.new("RGBA", (b[2] + 20, b[3] + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - b[0], 10), s, font=font, fill=fill)
    return im

def paste_alpha(base, im, xy, a):
    if a <= 0: return
    if a < 1:
        r, g, b_, al = im.split()
        im = Image.merge("RGBA", (r, g, b_, al.point(lambda v: int(v * a))))
    base.alpha_composite(im, (int(xy[0]), int(xy[1])))

def background(t):
    img = Image.fromarray(BASE).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    # drifting glow blobs
    for i, c in enumerate((ACC1, ACC2)):
        cx = W / 2 + math.sin(t * 0.6 + i * 3) * 380
        cy = H / 2 + math.cos(t * 0.45 + i * 2) * 650
        d.ellipse((cx - 420, cy - 420, cx + 420, cy + 420), fill=c + (70,))
    ov = ov.filter(ImageFilter.GaussianBlur(160))
    img.alpha_composite(ov)
    d = ImageDraw.Draw(img)
    # grid lines
    off = (t * 40) % 120
    for y in np.arange(-120 + off, H, 120):
        d.line((0, y, W, y), fill=(255, 255, 255, 10))
    for x in range(0, W, 120):
        d.line((x, 0, x, H), fill=(255, 255, 255, 10))
    for (x, y, r, sp) in PARTS:
        yy = (y - t * sp) % H
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=(255, 255, 255, 90))
    return img

def scene_logo(img, t):  # 0 - 3.4
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, H / 2 - 120
    # expanding rings
    for i in range(3):
        p = prog(t, 0.1 + i * 0.15, 1.2)
        if 0 < p < 1:
            r = eo(p) * (300 + i * 140)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(ACC1 if i % 2 == 0 else ACC2) + (int(255 * (1 - p)),), width=6)
    # K monogram square pops in & rotates
    p = prog(t, 0.2, 0.8)
    if p > 0:
        s = 260 * back(p)
        sq = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sq)
        sd.rounded_rectangle((200 - s / 2, 200 - s / 2, 200 + s / 2, 200 + s / 2), radius=int(s * 0.22), fill=ACC1 + (255,))
        if p > 0.4:
            text_c(sd, 200 - s * 0.38, "K", F(max(1, int(s * 0.62))), WHITE, 200)
        sq = sq.rotate(lerp(-180, 0, eo(p)), resample=Image.BICUBIC)
        img.alpha_composite(sq, (int(cx - 200), int(cy - 200)))
    # letters of name stagger up
    name = "KALMUK"
    f = F(150)
    total = sum(f.getlength(ch) for ch in name) + 8 * (len(name) - 1)
    x = W / 2 - total / 2
    for i, ch in enumerate(name):
        p = prog(t, 0.8 + i * 0.07, 0.5)
        lt = layer_text(ch, f, WHITE)
        paste_alpha(img, lt, (x - 10, cy + 200 + (1 - eo(p)) * 120), p)
        x += f.getlength(ch) + 8
    p = prog(t, 1.5, 0.6)
    lt = layer_text("M E D I A", F(70), ACC2)
    paste_alpha(img, lt, (W / 2 - lt.width / 2, cy + 390), eo(p))
    # underline sweep
    p = eo(prog(t, 1.7, 0.6))
    d = ImageDraw.Draw(img)
    d.rectangle((W / 2 - 300 * p, cy + 500, W / 2 + 300 * p, cy + 508), fill=ACC1)

def scene_head(img, t):  # 3.4 - 6.6
    lines = [("Dijital dünyada", WHITE), ("FARK", ACC1), ("yaratın.", WHITE)]
    sizes = [90, 240, 90]
    y = 620
    for i, ((s, c), sz) in enumerate(zip(lines, sizes)):
        p = eo(prog(t, i * 0.25, 0.6))
        lt = layer_text(s, F(sz), c)
        # mask wipe left to right
        w = int(lt.width * p)
        if w > 0:
            m = Image.new("L", lt.size, 0); ImageDraw.Draw(m).rectangle((0, 0, w, lt.height), fill=255)
            lt.putalpha(Image.composite(lt.split()[3], m, m))
            img.alpha_composite(lt, (int(W / 2 - lt.width / 2 + (1 - p) * -60), y))
        y += sz + 50
    p = eo(prog(t, 1.2, 0.7))
    lt = layer_text("Web Tasarım & Dijital Çözümler", F(50, False), ACC2)
    paste_alpha(img, lt, (W / 2 - lt.width / 2, y + 40 + (1 - p) * 40), p)

SERVICES = [("</>", "Web Tasarım"), ("🛒", "E-Ticaret"), ("QR", "QR Menü"),
            ("#", "Sosyal Medya"), ("☎", "Mobil Site"), ("★", "Marka Kimliği")]
def scene_services(img, t):  # 6.6 - 11.4
    p = eo(prog(t, 0, 0.5))
    lt = layer_text("HİZMETLERİMİZ", F(90), WHITE)
    paste_alpha(img, lt, (W / 2 - lt.width / 2, 260 - (1 - p) * 60), p)
    d = ImageDraw.Draw(img)
    d.rectangle((W / 2 - 120 * p, 390, W / 2 + 120 * p, 398), fill=ACC1)
    cw, ch, gx, gy0 = 440, 340, 60, 500
    for i, (ic, name) in enumerate(SERVICES):
        p = prog(t, 0.4 + i * 0.22, 0.6)
        if p <= 0: continue
        col, row = i % 2, i // 2
        x0 = W / 2 - cw - gx / 2 + col * (cw + gx)
        y0 = gy0 + row * (ch + 50)
        sc = back(p)
        card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        cd = ImageDraw.Draw(card)
        acc = ACC1 if (i % 2 == row % 2) else ACC2
        cd.rounded_rectangle((0, 0, cw - 1, ch - 1), radius=40, fill=(255, 255, 255, 22), outline=acc + (200,), width=4)
        cd.ellipse((cw / 2 - 70, 45, cw / 2 + 70, 185), fill=acc + (255,))
        icon = ic if ic not in ("🛒",) else "₺"
        text_c(cd, 72, icon, F(70 if len(icon) < 3 else 52), WHITE, cw / 2)
        text_c(cd, 225, name, F(46), WHITE, cw / 2)
        nw, nh = max(1, int(cw * sc)), max(1, int(ch * sc))
        card = card.resize((nw, nh), Image.BICUBIC)
        paste_alpha(img, card, (x0 + (cw - nw) / 2, y0 + (ch - nh) / 2), clamp(p * 2))
    # float bob after appear
def scene_stats(img, t):  # 11.4 - 13.6
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, 820
    p = eo(prog(t, 0, 1.0))
    r = 300
    d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * p, fill=ACC1, width=24)
    d.arc((cx - r + 40, cy - r + 40, cx + r - 40, cy + r - 40), 90, 90 + 360 * p, fill=ACC2, width=10)
    n = int(round(4 * p))
    text_c(d, cy - 190, f"{n}+", F(260), WHITE)
    p2 = eo(prog(t, 0.6, 0.6))
    lt = layer_text("YILLIK DENEYİM", F(80), WHITE)
    paste_alpha(img, lt, (W / 2 - lt.width / 2, cy + r + 80 + (1 - p2) * 50), p2)
    p3 = eo(prog(t, 0.9, 0.6))
    lt = layer_text("📍 Trabzon'dan tüm Türkiye'ye".replace("📍 ", ""), F(52, False), ACC2)
    paste_alpha(img, lt, (W / 2 - lt.width / 2, cy + r + 200 + (1 - p3) * 50), p3)

def scene_cta(img, t):  # 13.6 - 16
    d = ImageDraw.Draw(img)
    p = eo(prog(t, 0, 0.6))
    lt = layer_text("Projenizi", F(110), WHITE)
    paste_alpha(img, lt, (W / 2 - lt.width / 2, 560 - (1 - p) * 80), p)
    p = eo(prog(t, 0.15, 0.6))
    lt = layer_text("hayata geçirelim!", F(90), ACC1)
    paste_alpha(img, lt, (W / 2 - lt.width / 2, 700 - (1 - p) * 80), p)
    # pulsing button
    p = back(prog(t, 0.4, 0.6))
    pulse = 1 + 0.04 * math.sin(t * 8) if t > 1 else 1
    bw, bh = 620 * p * pulse, 150 * p * pulse
    if bw > 2:
        d.rounded_rectangle((W / 2 - bw / 2, 1000 - bh / 2, W / 2 + bw / 2, 1000 + bh / 2), radius=int(bh / 2), fill=ACC1)
        if p > 0.6: text_c(d, 1000 - 40, "ÜCRETSİZ TEKLİF AL", F(56), WHITE)
    p = eo(prog(t, 0.8, 0.6))
    lt = layer_text("kalmukmedia.com.tr", F(70), ACC2)
    paste_alpha(img, lt, (W / 2 - lt.width / 2, 1180 + (1 - p) * 40), p)
    p = eo(prog(t, 1.0, 0.6))
    lt = layer_text("KALMUK MEDIA", F(48, False), (255, 255, 255))
    paste_alpha(img, lt, (W / 2 - lt.width / 2, 1650), p * 0.8)

SCENES = [(0, 3.4, scene_logo), (3.4, 6.6, scene_head), (6.6, 11.4, scene_services),
          (11.4, 13.6, scene_stats), (13.6, 16.01, scene_cta)]

def frame(t):
    img = background(t)
    for s, e, fn in SCENES:
        if s <= t < e:
            fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            fn(fg, t - s)
            # scene exit: fade + zoom
            out = prog(t, e - 0.3, 0.3) if e < DUR else 0
            if out > 0:
                z = 1 + out * 0.15
                fg = fg.resize((int(W * z), int(H * z)), Image.BILINEAR)
                fg = fg.crop(((fg.width - W) // 2, (fg.height - H) // 2, (fg.width - W) // 2 + W, (fg.height - H) // 2 + H))
                fg.putalpha(fg.split()[3].point(lambda v: int(v * (1 - out))))
            img.alpha_composite(fg)
            # transition flash bar
            tp = prog(t, e - 0.25, 0.5)
            if 0 < tp < 1 and e < DUR:
                dd = ImageDraw.Draw(img)
                x = lerp(-W, W * 2, eo(tp))
                dd.polygon([(x - 200, 0), (x + 100, 0), (x - 100, H), (x - 400, H)], fill=ACC1 + (200,))
    # progress bar
    ImageDraw.Draw(img).rectangle((0, H - 10, W * t / DUR, H), fill=ACC2)
    return img.convert("RGB")

def music(path):
    sr = 44100; n = int(sr * DUR); t = np.arange(n) / sr
    bpm = 120; beat = 60 / bpm
    out = np.zeros(n)
    for k in range(int(DUR / beat)):  # kick
        s = int(k * beat * sr); L = int(0.3 * sr); tt = np.arange(L) / sr
        seg = np.sin(2 * np.pi * (50 + 120 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9)
        out[s:s + L] += seg[: n - s] * 0.8
        if k % 2:  # hat
            hs = int((k * beat + beat / 2) * sr); hl = int(0.05 * sr)
            out[hs:hs + hl] += np.random.randn(min(hl, n - hs)) * np.exp(-np.arange(min(hl, n - hs)) / sr * 80) * 0.15
    chords = [(220, 277.2, 329.6), (174.6, 220, 261.6), (196, 246.9, 293.7), (164.8, 207.7, 246.9)]
    for i in range(int(DUR / (beat * 4)) + 1):
        s = int(i * beat * 4 * sr); e = min(n, int((i + 1) * beat * 4 * sr))
        tt = t[s:e]
        for f in chords[i % 4]:
            out[s:e] += 0.07 * np.sign(np.sin(2 * np.pi * f * tt)) * 0.5 + 0.08 * np.sin(2 * np.pi * f * tt)
    out *= np.minimum(1, (DUR - t) / 1.0)
    out = np.int16(np.clip(out / np.abs(out).max() * 0.8, -1, 1) * 32767)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(out.tobytes())

if __name__ == "__main__":
    music("music.wav")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "music.wav",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                          "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                          "kalmuk_media_reels.mp4"], stdin=subprocess.PIPE)
    for i in range(N):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    print("done")

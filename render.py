"""Kalmuk Media - Instagram Reels (9:16) motion graphics promo.
Brand colors: #51a2ff (blue), #ffffff (white), #000000 (black). Font: Montserrat.
Render: python3 render.py  -> kalmuk_media_reels.mp4
"""
import math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 16.0
SUB = 2  # sub-frames per frame for motion blur
BLUE, WHITE, BLACK = (0x51, 0xA2, 0xFF), (255, 255, 255), (0, 0, 0)
FONTS = {"black": "fonts/Montserrat_900Black.ttf", "bold": "fonts/Montserrat_700Bold.ttf",
         "med": "fonts/Montserrat_500Medium.ttf"}
_fc = {}
def F(size, w="black"):
    k = (int(size), w)
    if k not in _fc: _fc[k] = ImageFont.truetype(FONTS[w], max(1, int(size)))
    return _fc[k]

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, s, d): return clamp((t - s) / d)
def expo(x): return 1 if x >= 1 else 1 - 2 ** (-10 * x)
def inout(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def back(x, s=1.6): x -= 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, x): return a + (b - a) * x

def tsize(s, font, spacing=0):
    b = font.getbbox(s)
    return b[2] - b[0] + spacing * (len(s) - 1), b[3] - b[1], b

def draw_text(d, s, font, fill, cx, y, spacing=0, stroke=0, stroke_fill=None):
    """Draw text horizontally centered at cx, top at y (ink box)."""
    w, h, b = tsize(s, font, spacing)
    x = cx - w / 2
    if spacing == 0:
        d.text((x - b[0], y - b[1]), s, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    else:
        for ch in s:
            d.text((x - b[0], y - b[1]), ch, font=font, fill=fill)
            x += font.getlength(ch) + spacing

def reveal(img, s, font, fill, cx, y, p, spacing=0, out=0.0):
    """Masked slide-up reveal: text rises from below a clip line (p 0->1); out 0->1 pushes it up and away."""
    if p <= 0 or out >= 1: return
    w, h, b = tsize(s, font, spacing)
    pad = int(h * 0.25)
    lay = Image.new("RGBA", (int(w) + 40, h + 2 * pad), (0, 0, 0, 0))
    off = (1 - expo(p)) * (h + pad) - inout(out) * (h + pad)
    draw_text(ImageDraw.Draw(lay), s, font, fill, lay.width / 2, pad + off, spacing)
    img.alpha_composite(lay, (int(cx - lay.width / 2), int(y - pad)))

def wipe(img, color, p, direction):
    """Full-screen color panel sliding in. direction: up/down/left/right."""
    if p <= 0: return
    d = ImageDraw.Draw(img)
    e = inout(p)
    if direction == "up": d.rectangle((0, H * (1 - e), W, H), fill=color)
    elif direction == "left": d.rectangle((W * (1 - e), 0, W, H), fill=color)
    elif direction == "right": d.rectangle((0, 0, W * e, H), fill=color)

def chrome(img, t, fg):
    """Persistent UI frame: brand tag, year, corner marks."""
    d = ImageDraw.Draw(img)
    a = expo(prog(t, 0.2, 0.6))
    if a <= 0: return
    f = F(30, "bold")
    d.text((70, 90 - (1 - a) * 30), "KALMUK MEDIA", font=f, fill=fg)
    d.text((W - 70 - f.getlength("©2026"), 90 - (1 - a) * 30), "©2026", font=f, fill=fg)
    L = 40 * a
    for (x, y, sx, sy) in ((50, 50, 1, 1), (W - 50, 50, -1, 1), (50, H - 50, 1, -1), (W - 50, H - 50, -1, -1)):
        d.line((x, y, x + L * sx, y), fill=fg, width=4)
        d.line((x, y, x, y + L * sy), fill=fg, width=4)

# ---------------- scenes ----------------
def s_intro(img, t):  # 0 - 2.0, black
    d = ImageDraw.Draw(img)
    cy = H / 2
    p = expo(prog(t, 0.0, 0.5))
    d.rectangle((W / 2 - 420 * p, cy - 3, W / 2 + 420 * p, cy + 3), fill=BLUE)
    f = F(170)
    reveal(img, "DİJİTAL", f, WHITE, W / 2, cy - 200, prog(t, 0.25, 0.5))
    # second word drops from the line downward (inverted reveal via mirror trick: just slide down)
    p2 = prog(t, 0.5, 0.5)
    if p2 > 0:
        w, h, b = tsize("DÜNYADA", f)
        lay = Image.new("RGBA", (int(w) + 40, h + 80), (0, 0, 0, 0))
        draw_text(ImageDraw.Draw(lay), "DÜNYADA", f, WHITE, lay.width / 2, 40 - (1 - expo(p2)) * (h + 40))
        img.alpha_composite(lay, (int(W / 2 - lay.width / 2), int(cy + 30)))
    p3 = expo(prog(t, 1.0, 0.4))
    if p3 > 0:
        draw_text(d, "BİR ADIM ÖNDE OLUN", F(44, "bold"), BLUE, W / 2, cy + 300 + (1 - p3) * 40, spacing=6)
    wipe(img, BLUE, prog(t, 1.6, 0.4), "up")

def s_fark(img, t):  # 2.0 - 4.0, blue
    img.paste(BLUE, (0, 0, W, H))
    # slow camera push
    z = 1 + 0.06 * t / 2
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    reveal(lay, "FARK", F(290), BLACK, W / 2, 640, prog(t, 0.0, 0.5))
    reveal(lay, "YARATIN.", F(150), WHITE, W / 2, 1020, prog(t, 0.2, 0.5))
    pl = expo(prog(t, 0.6, 0.5))
    ImageDraw.Draw(lay).rectangle((W / 2 - 200 * pl, 1230, W / 2 + 200 * pl, 1240), fill=BLACK)
    if z != 1:
        lay = lay.resize((int(W * z), int(H * z)), Image.BICUBIC)
        lay = lay.crop(((lay.width - W) // 2, (lay.height - H) // 2, (lay.width - W) // 2 + W, (lay.height - H) // 2 + H))
    img.alpha_composite(lay)
    # circle iris into black
    p = inout(prog(t, 1.6, 0.4))
    if p > 0:
        r = p * 1200
        ImageDraw.Draw(img).ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), fill=BLACK)

SERVICES = [("WEB", "TASARIM"), ("ÖZEL", "YAZILIM"), ("CRM", "ÇÖZÜMLERİ"), ("E-TİCARET", None),
            ("QR", "MENÜ"), ("SOSYAL", "MEDYA"), ("MOBİL", "SİTE"), ("MARKA", "KİMLİĞİ")]
SLOT = 0.75
def s_services(img, t):  # 4.0 - 10.0, black
    d = ImageDraw.Draw(img)
    a = expo(prog(t, 0, 0.5))
    draw_text(d, "HİZMETLERİMİZ", F(40, "bold"), BLUE, W / 2, 330 - (1 - a) * 30, spacing=10)
    idx = min(len(SERVICES) - 1, int(t // SLOT))
    lt = t - idx * SLOT
    # huge faint outlined number behind
    num = f"0{idx + 1}"
    np_ = expo(prog(lt, 0, 0.4))
    draw_text(d, num, F(620), BLACK, W / 2 + (1 - np_) * 120, 620, stroke=3, stroke_fill=(40, 40, 40))
    # word in/out
    pin = prog(lt, 0.0, 0.45) if idx > 0 or t > 0.1 else 0
    if idx == 0: pin = prog(t, 0.1, 0.45)
    pout = prog(lt, SLOT - 0.25, 0.25) if idx < len(SERVICES) - 1 else 0
    l1, l2 = SERVICES[idx]
    f = F(150 if len(l1) < 8 else 130)
    if l2:
        reveal(img, l1, f, WHITE, W / 2, 790, pin, out=pout)
        reveal(img, l2, F(150 if len(l2) < 8 else 130), BLUE, W / 2, 970, prog(lt, 0.08, 0.45) if idx else prog(t, 0.18, 0.45), out=pout)
    else:
        reveal(img, l1, f, BLUE, W / 2, 880, pin, out=pout)
    # counter + progress
    draw_text(d, f"0{idx + 1} / 0{len(SERVICES)}", F(36, "bold"), WHITE, W / 2, 1400, spacing=4)
    gp = clamp(t / (SLOT * len(SERVICES)))
    d.rectangle((W / 2 - 300, 1480, W / 2 + 300, 1484), fill=(50, 50, 50))
    d.rectangle((W / 2 - 300, 1480, W / 2 - 300 + 600 * gp, 1484), fill=BLUE)
    wipe(img, WHITE, prog(t, 5.65, 0.35), "right")

def s_stats(img, t):  # 10.0 - 12.25, white
    img.paste(WHITE, (0, 0, W, H))
    d = ImageDraw.Draw(img)
    n = min(6, 1 + int(prog(t, 0.0, 0.6) * 6))
    sc = back(prog(t, 0.0, 0.45))
    if sc > 0:
        draw_text(d, f"{n}+", F(560 * sc), BLACK, W / 2, 560 + (1 - sc) * 200)
    reveal(img, "YIL", F(120), BLUE, W / 2, 1150, prog(t, 0.35, 0.45))
    reveal(img, "DENEYİM", F(120), BLACK, W / 2, 1290, prog(t, 0.45, 0.45))
    p = expo(prog(t, 0.8, 0.5))
    if p > 0:
        d.rectangle((W / 2 - 160 * p, 1490, W / 2 + 160 * p, 1496), fill=BLUE)
        draw_text(d, "TRABZON", F(44, "bold"), BLACK, W / 2, 1530 + (1 - p) * 30, spacing=14)
    wipe(img, BLACK, prog(t, 1.9, 0.35), "left")

def s_outro(img, t):  # 12.25 - 16.0, black
    d = ImageDraw.Draw(img)
    cx, cy = W / 2, 700
    # brand logo: blue ring draws on, white K mark scales in
    p = prog(t, 0.0, 0.7)
    r = 190
    if p > 0:
        d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * expo(p), fill=BLUE, width=10)
    p = prog(t, 0.2, 0.6)
    if p > 0:
        sz = max(1, int(330 * back(p)))
        k = LOGO_K.resize((sz, sz), Image.LANCZOS).rotate(lerp(-25, 0, expo(p)), resample=Image.BICUBIC)
        img.alpha_composite(k, (int(cx - sz / 2), int(cy - sz / 2)))
    # name, letter stagger
    f = F(150); sp = 6
    name = "KALMUK"
    total = tsize(name, f, sp)[0]
    x = W / 2 - total / 2
    for i, ch in enumerate(name):
        cw = f.getlength(ch)
        reveal(img, ch, f, WHITE, x + cw / 2, 1000, prog(t, 0.45 + i * 0.05, 0.5))
        x += cw + sp
    reveal(img, "MEDIA", F(64, "bold"), BLUE, W / 2, 1180, prog(t, 0.8, 0.5), spacing=36)
    p = expo(prog(t, 1.2, 0.5))
    if p > 0:
        draw_text(d, "Web Tasarım • Özel Yazılım • CRM", F(38, "med"), (200, 200, 200), W / 2, 1320 + (1 - p) * 30)
    p = back(prog(t, 1.5, 0.5))
    if p > 0:
        bw, bh = 640 * p, 120 * p
        d.rounded_rectangle((W / 2 - bw / 2, 1480 - bh / 2, W / 2 + bw / 2, 1480 + bh / 2), radius=int(bh / 2), fill=BLUE)
        if p > 0.7: draw_text(d, "kalmukmedia.com.tr", F(46, "bold"), BLACK, W / 2, 1480 - 22)
    p = expo(prog(t, 1.9, 0.5))
    if p > 0:
        draw_text(d, "TEKLİF İÇİN DM'DEN YAZIN", F(32, "bold"), WHITE, W / 2, 1600 + (1 - p) * 20, spacing=6)

def _logo_k():
    """White K mark from logo.png (black disc + white K) as a transparent RGBA."""
    im = Image.open("logo.png").convert("RGBA")
    a = np.asarray(im).astype(np.float32)
    lum = a[..., :3].mean(-1)
    alpha = np.clip((lum - 60) / 140, 0, 1) * (a[..., 3] / 255)
    out = np.zeros_like(a); out[..., :3] = 255; out[..., 3] = alpha * 255
    return Image.fromarray(out.astype(np.uint8))
LOGO_K = _logo_k()

SCENES = [(0.0, 2.0, s_intro, BLACK, WHITE), (2.0, 4.0, s_fark, BLUE, BLACK),
          (4.0, 10.0, s_services, BLACK, WHITE), (10.0, 12.25, s_stats, WHITE, BLACK),
          (12.25, 99, s_outro, BLACK, WHITE)]

def frame(t):
    for s, e, fn, bg, fg in SCENES:
        if s <= t < e:
            img = Image.new("RGBA", (W, H), bg + (255,))
            fn(img, t - s)
            chrome(img, t, fg if t - s > 0.15 or s == 0 else fg)
            break
    a = np.asarray(img.convert("RGB"), dtype=np.float32)
    # fade from / to black
    k = min(prog(t, 0, 0.25), 1 - prog(t, DUR - 0.4, 0.4))
    return a * k

if __name__ == "__main__":
    subprocess.run(["python3", "music.py"], check=True)
    n = int(FPS * DUR)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", "music.wav",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow",
                          "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                          "kalmuk_media_reels.mp4"], stdin=subprocess.PIPE)
    for i in range(n):
        acc = sum(frame((i + j / SUB) / FPS) for j in range(SUB)) / SUB
        p.stdin.write(acc.astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
    print("done")

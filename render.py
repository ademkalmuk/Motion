"""Kalmuk Media - Instagram Reels (9:16) motion graphics promo.
Brand colors: #51a2ff (blue), #ffffff (white), #000000 (black). Font: Montserrat.
Render: python3 render.py  -> kalmuk_media_reels.mp4
"""
import math, subprocess, os
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 23.0
SUB = 4  # sub-frames per frame for motion blur
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

def s_web(img, t):  # 4.0 - 8.0, black: phone mockup building a website
    d = ImageDraw.Draw(img)
    reveal(img, "MARKANIZA ÖZEL", F(84), WHITE, W / 2, 230, prog(t, 0.0, 0.5))
    reveal(img, "DİJİTAL DENEYİM", F(84), BLUE, W / 2, 340, prog(t, 0.1, 0.5))
    pw, ph = 560, 1080
    p = expo(prog(t, 0.15, 0.7))
    if p <= 0: return
    x0, y0 = W / 2 - pw / 2, 560 + (1 - p) * 1400
    scr = Image.new("RGBA", (pw - 40, ph - 40), (12, 12, 14, 255))
    sd = ImageDraw.Draw(scr)
    sw = scr.width
    scroll = inout(prog(t, 2.5, 0.9)) * 520
    def y(v): return v - scroll
    # nav
    a = expo(prog(t, 0.7, 0.4))
    sd.ellipse((30, y(40), 80, y(90)), fill=BLUE)
    for i in range(3):
        sd.rounded_rectangle((sw - 70 - i * 0 , y(48 + i * 14), sw - 70 + 40 * a, y(54 + i * 14)), radius=3, fill=WHITE)
    # hero
    hp_ = expo(prog(t, 0.85, 0.5))
    sd.rounded_rectangle((24, y(120), sw - 24, y(120 + 380 * hp_)), radius=28, fill=BLUE)
    if hp_ > 0.5:
        lp_ = expo(prog(t, 1.1, 0.4))
        sd.rounded_rectangle((60, y(200), 60 + 340 * lp_, y(240)), radius=10, fill=WHITE)
        sd.rounded_rectangle((60, y(260), 60 + 240 * lp_, y(300)), radius=10, fill=WHITE)
        bp = back(prog(t, 1.3, 0.4))
        if bp > 0:
            sd.rounded_rectangle((60, y(370), 60 + 190 * bp, y(370 + 66 * bp)), radius=33, fill=BLACK)
            if bp > 0.8: sd.text((60 + 95, y(403)), "BAŞLA", font=F(24, "bold"), fill=WHITE, anchor="mm")
    # cards grid
    for i in range(6):
        cp = expo(prog(t, 1.5 + i * 0.12, 0.45))
        if cp <= 0: continue
        cx_ = 24 + (i % 2) * (sw / 2 - 12)
        cy_ = 540 + (i // 2) * 270 + (1 - cp) * 80
        w_ = sw / 2 - 36
        sd.rounded_rectangle((cx_, y(cy_), cx_ + w_, y(cy_ + 240)), radius=22, fill=(32, 32, 36))
        sd.rounded_rectangle((cx_ + 20, y(cy_ + 20), cx_ + w_ - 20, y(cy_ + 130)), radius=14, fill=BLUE if i % 3 == 0 else (60, 60, 66))
        sd.rounded_rectangle((cx_ + 20, y(cy_ + 155), cx_ + 20 + (w_ - 60) * cp, y(cy_ + 175)), radius=6, fill=WHITE)
        sd.rounded_rectangle((cx_ + 20, y(cy_ + 190), cx_ + 20 + (w_ - 110) * cp, y(cy_ + 205)), radius=6, fill=(120, 120, 128))
    # tap ripple on button
    tp = prog(t, 2.0, 0.5)
    if 0 < tp < 1:
        r = 20 + 90 * expo(tp)
        sd.ellipse((155 - r, y(403) - r, 155 + r, y(403) + r), outline=WHITE + (int(255 * (1 - tp)),), width=4)
    # phone body
    phone = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    pd = ImageDraw.Draw(phone)
    pd.rounded_rectangle((0, 0, pw - 1, ph - 1), radius=70, fill=(28, 28, 30), outline=(90, 90, 96), width=4)
    m = Image.new("L", scr.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, scr.width - 1, scr.height - 1), radius=52, fill=255)
    phone.paste(scr, (20, 20), m)
    pd.rounded_rectangle((pw / 2 - 70, 34, pw / 2 + 70, 62), radius=14, fill=BLACK)
    img.alpha_composite(phone, (int(x0), int(y0)))
    wipe(img, BLUE, prog(t, 3.6, 0.4), "left")

STEPS = [("ANALİZ", "İhtiyaç ve hedefler"), ("TASARIM", "UI/UX ve marka dili"),
         ("GELİŞTİRME", "Kodlama ve test"), ("YAYIN", "Lansman ve destek")]
def s_process(img, t):  # 14.0 - 17.0, blue
    img.paste(BLUE, (0, 0, W, H))
    d = ImageDraw.Draw(img)
    reveal(img, "NASIL", F(110), WHITE, W / 2, 230, prog(t, 0.0, 0.45))
    reveal(img, "ÇALIŞIYORUZ?", F(110), BLACK, W / 2, 360, prog(t, 0.1, 0.45))
    lx, top, gap = 230, 620, 270
    lp_ = inout(prog(t, 0.2, 1.4))
    d.rectangle((lx - 3, top, lx + 3, top + (gap * 3) * lp_), fill=BLACK)
    for i, (name, sub) in enumerate(STEPS):
        st = 0.3 + i * 0.35
        cy = top + i * gap
        p = back(prog(t, st, 0.4))
        if p > 0:
            r = 52 * p
            d.ellipse((lx - r, cy - r, lx + r, cy + r), fill=BLACK)
            if p > 0.7: d.text((lx, cy), f"0{i + 1}", font=F(38, "black"), fill=WHITE, anchor="mm")
        f = F(78)
        w_ = tsize(name, f)[0]
        reveal(img, name, f, BLACK, lx + 100 + w_ / 2, cy - 60, prog(t, st + 0.05, 0.45))
        q = expo(prog(t, st + 0.2, 0.4))
        if q > 0:
            d.text((lx + 100 + (1 - q) * 40, cy + 40), sub, font=F(40, "med"), fill=WHITE)
    wipe(img, WHITE, prog(t, 2.6, 0.4), "up")

SERVICES = [("WEB", "TASARIM"), ("ÖZEL", "YAZILIM"), ("CRM", "ÇÖZÜMLERİ"), ("E-TİCARET", None),
            ("QR", "MENÜ"), ("SOSYAL", "MEDYA"), ("MOBİL", "SİTE"), ("MARKA", "KİMLİĞİ")]
SLOT = 0.75
def s_services(img, t):  # 8.0 - 14.0, black
    d = ImageDraw.Draw(img)
    a = expo(prog(t, 0, 0.5))
    if t < 0.4:  # blue panel from previous scene exits to the right
        d.rectangle((W * inout(t / 0.4), 0, W, H), fill=BLUE)
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
    wipe(img, BLUE, prog(t, 5.65, 0.35), "right")

def s_stats(img, t):  # 17.0 - 19.0, white
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
    wipe(img, BLACK, prog(t, 1.65, 0.35), "left")

def s_outro(img, t):  # 19.0 - 23.0, black
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
          (4.0, 8.0, s_web, BLACK, WHITE), (8.0, 14.0, s_services, BLACK, WHITE),
          (14.0, 17.0, s_process, BLUE, BLACK), (17.0, 19.0, s_stats, WHITE, BLACK),
          (19.0, 99, s_outro, BLACK, WHITE)]

def _glow():
    yy, xx = np.mgrid[-700:700, -700:700]
    a = np.clip(1 - np.sqrt(xx ** 2 + yy ** 2) / 700, 0, 1) ** 2.2 * 0.22
    g = np.zeros((1400, 1400, 4), np.uint8); g[..., :3] = BLUE; g[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(g)
GLOW = _glow()

def frame(t):
    for s, e, fn, bg, fg in SCENES:
        if s <= t < e:
            img = Image.new("RGBA", (W, H), bg + (255,))
            if bg == BLACK:  # slow drifting brand-blue glow for depth
                img.alpha_composite(GLOW, (int(W / 2 - 700 + math.sin(t * 0.5) * 300), int(H * 0.62 - 700 + math.cos(t * 0.37) * 400)))
            fn(img, t - s)
            chrome(img, t, fg if t - s > 0.15 or s == 0 else fg)
            break
    a = np.asarray(img.convert("RGB"), dtype=np.float32)
    # fade from / to black
    k = min(prog(t, 0, 0.25), 1 - prog(t, DUR - 0.4, 0.4))
    return a * k

def render_frame(i):
    acc = sum(frame((i + (j + 0.5) / SUB) / FPS) for j in range(SUB)) / SUB
    return np.clip(acc + 0.5, 0, 255).astype(np.uint8).tobytes()

if __name__ == "__main__":
    subprocess.run(["python3", "music.py"], check=True)
    n = int(FPS * DUR)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", "music.wav",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "14", "-preset", "slow", "-profile:v", "high", "-tune", "animation",
                          "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart",
                          "kalmuk_media_reels.mp4"], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for buf in pool.imap(render_frame, range(n), chunksize=4):
            p.stdin.write(buf)
    p.stdin.close(); p.wait()
    print("done")

"""Kalmuk Media referans videosu: Hüner Otomatik Kapı web sitesi (Instagram Reels, 9:16).
Render: python3 referans_huner.py -> referans_huner_otomatik_kapi.mp4
"""
import json, math, os, subprocess
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw
from render import (W, H, FPS, SUB, BLUE, WHITE, BLACK, F, clamp, prog, expo, inout, back, lerp,
                    tsize, draw_text, reveal, wipe, chrome, GLOW, LOGO_K)

DUR = 21.0
GREY, DARK, MID = (32, 32, 36), (18, 18, 20), (70, 70, 78)
CLIENT_URL = "hunerotomatikkapi.com"

def door(d, x0, y0, w, h, open_p, panel=6, frame=WHITE, fill=(210, 214, 222)):
    """Sectional door: frame + horizontal panels that roll up as open_p goes 0->1."""
    d.rectangle((x0 - 10, y0 - 10, x0 + w + 10, y0 + h), outline=frame, width=6)
    ph = h / panel
    vis = h * (1 - open_p)
    for i in range(panel):
        top = y0 + vis - (panel - i) * ph
        if top + ph <= y0: continue
        a, b = max(y0, top), top + ph - 4
        if b > a:
            d.rectangle((x0, a, x0 + w, b), fill=fill)
            if b - a > ph * 0.5:
                d.line((x0 + 14, (a + b) / 2, x0 + w - 14, (a + b) / 2), fill=(170, 175, 185), width=3)

# ---------------- scenes ----------------
def s_intro(img, t):  # 0 - 2, black
    d = ImageDraw.Draw(img)
    cy = H / 2
    p = expo(prog(t, 0.0, 0.5))
    d.rectangle((W / 2 - 400 * p, cy - 3, W / 2 + 400 * p, cy + 3), fill=BLUE)
    reveal(img, "YENİ", F(190), WHITE, W / 2, cy - 230, prog(t, 0.2, 0.5))
    reveal(img, "REFERANS", F(150), BLUE, W / 2, cy + 40, prog(t, 0.4, 0.5))
    q = expo(prog(t, 0.9, 0.4))
    if q > 0:
        draw_text(d, "WEB SİTESİ PROJESİ", F(40, "bold"), WHITE, W / 2, cy + 260 + (1 - q) * 30, spacing=10)
    wipe(img, BLUE, prog(t, 1.6, 0.4), "up")

def s_client(img, t):  # 2 - 4.5, blue
    img.paste(BLUE, (0, 0, W, H))
    d = ImageDraw.Draw(img)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    draw_text(ld, "MÜŞTERİMİZ", F(40, "bold"), WHITE, W / 2, 470, spacing=12) if t > 0.1 else None
    # door icon opens behind the name
    door(ld, W / 2 - 170, 560, 340, 300, inout(prog(t, 0.3, 1.2)), frame=BLACK, fill=WHITE)
    reveal(lay, "HÜNER", F(250), BLACK, W / 2, 920, prog(t, 0.1, 0.5))
    reveal(lay, "OTOMATİK KAPI", F(96), WHITE, W / 2, 1200, prog(t, 0.25, 0.5))
    q = expo(prog(t, 0.8, 0.5))
    if q > 0:
        ld.rectangle((W / 2 - 140 * q, 1360, W / 2 + 140 * q, 1366), fill=BLACK)
        draw_text(ld, "PENDİK • İSTANBUL", F(40, "bold"), BLACK, W / 2, 1400 + (1 - q) * 20, spacing=8)
    z = 1 + 0.05 * t / 2.5
    lay = lay.resize((int(W * z), int(H * z)), Image.BICUBIC)
    lay = lay.crop(((lay.width - W) // 2, (lay.height - H) // 2, (lay.width - W) // 2 + W, (lay.height - H) // 2 + H))
    img.alpha_composite(lay)
    p = inout(prog(t, 2.1, 0.4))
    if p > 0:
        r = p * 1200
        d.ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), fill=BLACK)

def s_brief(img, t):  # 4.5 - 6.5, black
    d = ImageDraw.Draw(img)
    rows = [("SEKTÖR", "Otomatik Kapı Sistemleri"), ("PROJE", "Kurumsal Web Sitesi"),
            ("KAPSAM", "Ürün & Hizmet Sayfaları"), ("PLATFORM", "Masaüstü + Mobil")]
    reveal(img, "PROJE", F(120), WHITE, W / 2, 380, prog(t, 0.0, 0.45))
    reveal(img, "DETAYLARI", F(120), BLUE, W / 2, 520, prog(t, 0.08, 0.45))
    for i, (k, v) in enumerate(rows):
        y = 800 + i * 190
        p = expo(prog(t, 0.3 + i * 0.15, 0.45))
        if p <= 0: continue
        d.rectangle((140, y + 130, 140 + 800 * p, y + 132), fill=MID)
        d.text((140 + (1 - p) * 60, y), k, font=F(34, "bold"), fill=BLUE)
        d.text((140 + (1 - p) * 90, y + 50), v, font=F(54, "bold"), fill=WHITE)
    wipe(img, WHITE, prog(t, 1.65, 0.35), "right")

def browser(t, scroll):
    """Desktop browser showing a stylized version of the client site."""
    bw, bh = 940, 640
    b = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), radius=26, fill=(245, 246, 248), outline=(200, 200, 205), width=2)
    for i, c in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))):
        d.ellipse((24 + i * 30, 22, 42 + i * 30, 40), fill=c)
    d.rounded_rectangle((140, 16, bw - 30, 46), radius=15, fill=WHITE)
    tp = clamp((t - 0.6) / 0.8)
    url = CLIENT_URL[: int(len(CLIENT_URL) * tp)]
    d.text((160, 31), "🔒 " [0:0] + url, font=F(20, "med"), fill=(60, 60, 60), anchor="lm")
    vw, vh = bw - 20, bh - 76
    v = Image.new("RGBA", (vw, vh * 3), WHITE)
    vd = ImageDraw.Draw(v)
    # nav
    vd.rectangle((0, 0, vw, 64), fill=WHITE)
    vd.text((24, 32), "HÜNER", font=F(26), fill=BLACK, anchor="lm")
    vd.text((130, 33), "OTOMATİK KAPI", font=F(14, "bold"), fill=BLUE, anchor="lm")
    for i, n in enumerate(("Kurumsal", "Ürünler", "Servis", "İletişim")):
        vd.text((vw - 420 + i * 100, 33), n, font=F(16, "med"), fill=(50, 50, 50), anchor="lm")
    # hero
    vd.rectangle((0, 64, vw, 520), fill=(16, 18, 24))
    hp_ = expo(prog(t, 1.0, 0.6))
    vd.text((50 - (1 - hp_) * 40, 170), "Otomatik Kapı", font=F(46), fill=WHITE)
    vd.text((50 - (1 - hp_) * 60, 228), "Sistemleri", font=F(46), fill=BLUE)
    vd.text((50, 300), "Endüstriyel, ticari ve konut projeleri için", font=F(17, "med"), fill=(190, 190, 195))
    vd.text((50, 326), "güvenli ve estetik kapı çözümleri.", font=F(17, "med"), fill=(190, 190, 195))
    bp = back(prog(t, 1.4, 0.4))
    if bp > 0:
        vd.rounded_rectangle((50, 380, 50 + 200 * bp, 380 + 54 * bp), radius=27, fill=BLUE)
        if bp > 0.8: vd.text((150, 407), "Teklif Alın", font=F(18, "bold"), fill=WHITE, anchor="mm")
    # animated sectional door in hero
    op = (math.sin((t - 1.0) * 1.8) * 0.5 + 0.5) if t > 1.0 else 0
    door(vd, vw - 380, 140, 300, 320, op * 0.8, frame=(120, 125, 135))
    # product cards
    prods = ("Seksiyonel Kapı", "Sarmal Kapı", "Hızlı PVC Kapı", "Fotoselli Kapı", "Hangar Kapı", "Servis & Tamir")
    vd.text((vw / 2, 580), "Ürünlerimiz", font=F(34), fill=BLACK, anchor="mm")
    for i, n in enumerate(prods):
        cx = 30 + (i % 3) * ((vw - 60) / 3)
        cy = 640 + (i // 3) * 300
        cw = (vw - 60) / 3 - 20
        vd.rounded_rectangle((cx, cy, cx + cw, cy + 270), radius=18, fill=(242, 244, 247))
        vd.rounded_rectangle((cx + 14, cy + 14, cx + cw - 14, cy + 170), radius=12, fill=(16, 18, 24))
        door(vd, cx + cw / 2 - 60, cy + 40, 120, 115, (i * 0.17) % 0.7, panel=4, frame=(120, 125, 135))
        vd.text((cx + 20, cy + 200), n, font=F(20, "bold"), fill=BLACK)
        vd.rounded_rectangle((cx + 20, cy + 236, cx + 110, cy + 246), radius=4, fill=BLUE)
    view = v.crop((0, int(scroll), vw, int(scroll) + vh))
    m = Image.new("L", (vw, vh), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, vw - 1, vh - 1), radius=14, fill=255)
    b.paste(view, (10, 64), m)
    return b

def s_desktop(img, t):  # 6.5 - 11.5, white
    img.paste(WHITE, (0, 0, W, H))
    if t < 0.35:
        ImageDraw.Draw(img).rectangle((W * inout(t / 0.35), 0, W, H), fill=BLACK)
    reveal(img, "KURUMSAL", F(110), BLACK, W / 2, 260, prog(t, 0.1, 0.45))
    reveal(img, "WEB SİTESİ", F(110), BLUE, W / 2, 390, prog(t, 0.2, 0.45))
    p = expo(prog(t, 0.25, 0.7))
    if p <= 0: return
    scroll = inout(prog(t, 2.8, 1.4)) * 520
    b = browser(t, scroll)
    # slight 3D-ish tilt via scale + drop shadow
    sc = lerp(0.85, 1.0, p) * (1 + 0.03 * t / 5)
    bw, bh = int(b.width * sc), int(b.height * sc)
    b = b.resize((bw, bh), Image.BICUBIC)
    x, y = W / 2 - bw / 2, 760 + (1 - p) * 500
    sh = Image.new("RGBA", (bw + 80, bh + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((40, 60, bw + 40, bh + 60), radius=30, fill=(0, 0, 0, 50))
    img.alpha_composite(sh, (int(x - 40), int(y - 30)))
    img.alpha_composite(b, (int(x), int(y)))
    q = expo(prog(t, 2.0, 0.5))
    if q > 0:
        draw_text(ImageDraw.Draw(img), CLIENT_URL, F(40, "bold"), BLACK, W / 2, y + bh + 120 + (1 - q) * 30)
    wipe(img, BLACK, prog(t, 4.6, 0.4), "up")

PRODUCTS = [("SEKSİYONEL", "KAPI"), ("SARMAL", "KAPI"), ("HIZLI PVC", "KAPI"),
            ("FOTOSELLİ", "KAPI"), ("HANGAR", "KAPI")]
SLOT = 0.7
def s_products(img, t):  # 11.5 - 15, black
    d = ImageDraw.Draw(img)
    a = expo(prog(t, 0, 0.5))
    draw_text(d, "SİTEDE YER ALAN ÜRÜNLER", F(36, "bold"), BLUE, W / 2, 330 - (1 - a) * 30, spacing=8)
    idx = min(len(PRODUCTS) - 1, int(t // SLOT))
    lt = t - idx * SLOT
    # door icon cycling open/close per product
    door(d, W / 2 - 150, 520, 300, 260, inout(prog(lt, 0.0, 0.5)) * 0.85, frame=WHITE, fill=BLUE)
    pin = prog(lt, 0.0, 0.4) if idx else prog(t, 0.05, 0.4)
    pout = prog(lt, SLOT - 0.22, 0.22) if idx < len(PRODUCTS) - 1 else 0
    l1, l2 = PRODUCTS[idx]
    reveal(img, l1, F(130 if len(l1) < 9 else 112), WHITE, W / 2, 920, pin, out=pout)
    reveal(img, l2, F(130), BLUE, W / 2, 1090, prog(lt, 0.06, 0.4) if idx else prog(t, 0.12, 0.4), out=pout)
    draw_text(d, f"0{idx + 1} / 0{len(PRODUCTS)}", F(36, "bold"), WHITE, W / 2, 1400, spacing=4)
    gp = clamp(t / (SLOT * len(PRODUCTS)))
    d.rectangle((W / 2 - 300, 1480, W / 2 + 300, 1484), fill=(50, 50, 50))
    d.rectangle((W / 2 - 300, 1480, W / 2 - 300 + 600 * gp, 1484), fill=BLUE)
    wipe(img, BLUE, prog(t, 3.15, 0.35), "left")

def s_mobile(img, t):  # 15 - 17.5, blue
    img.paste(BLUE, (0, 0, W, H))
    d = ImageDraw.Draw(img)
    reveal(img, "MOBİL", F(120), WHITE, W / 2, 200, prog(t, 0.0, 0.45))
    reveal(img, "UYUMLU", F(120), BLACK, W / 2, 330, prog(t, 0.08, 0.45))
    pw, ph = 500, 1000
    p = expo(prog(t, 0.1, 0.6))
    if p <= 0: return
    scr = Image.new("RGBA", (pw - 36, ph - 36), WHITE)
    sd = ImageDraw.Draw(scr)
    sw = scr.width
    sc = inout(prog(t, 1.0, 1.1)) * 700
    def y(v): return v - sc
    sd.rectangle((0, y(0), sw, y(110)), fill=WHITE)
    sd.text((30, y(70)), "HÜNER", font=F(30), fill=BLACK, anchor="lm")
    for i in range(3): sd.rectangle((sw - 70, y(56 + i * 12), sw - 34, y(61 + i * 12)), fill=BLACK)
    sd.rectangle((0, y(110), sw, y(620)), fill=(16, 18, 24))
    sd.text((30, y(170)), "Otomatik Kapı", font=F(40), fill=WHITE)
    sd.text((30, y(220)), "Sistemleri", font=F(40), fill=BLUE)
    door(sd, sw / 2 - 120, y(330), 240, 200, (math.sin(t * 2.4) * 0.5 + 0.5) * 0.8, frame=(120, 125, 135))
    sd.rounded_rectangle((30, y(555), 230, y(605)), radius=25, fill=BLUE)
    sd.text((130, y(580)), "Teklif Alın", font=F(18, "bold"), fill=WHITE, anchor="mm")
    for i, n in enumerate(("Seksiyonel Kapı", "Sarmal Kapı", "Hızlı PVC Kapı", "Fotoselli Kapı")):
        cy = 660 + i * 230
        sd.rounded_rectangle((24, y(cy), sw - 24, y(cy + 200)), radius=18, fill=(242, 244, 247))
        sd.rounded_rectangle((40, y(cy + 16), 200, y(cy + 184)), radius=12, fill=(16, 18, 24))
        sd.text((224, y(cy + 70)), n, font=F(24, "bold"), fill=BLACK)
        sd.rounded_rectangle((224, y(cy + 120), 320, y(cy + 130)), radius=4, fill=BLUE)
    phone = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    pd = ImageDraw.Draw(phone)
    pd.rounded_rectangle((0, 0, pw - 1, ph - 1), radius=66, fill=(20, 20, 22), outline=(60, 60, 66), width=4)
    m = Image.new("L", scr.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, scr.width - 1, scr.height - 1), radius=50, fill=255)
    phone.paste(scr, (18, 18), m)
    pd.rounded_rectangle((pw / 2 - 64, 32, pw / 2 + 64, 58), radius=13, fill=BLACK)
    rot = lerp(-8, 0, p)
    phone = phone.rotate(rot, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(phone, (int(W / 2 - phone.width / 2), int(560 + (1 - p) * 1300 - (phone.height - ph) / 2)))
    wipe(img, BLACK, prog(t, 2.1, 0.4), "up")

def s_outro(img, t):  # 17.5 - 21, black
    d = ImageDraw.Draw(img)
    reveal(img, "BU PROJE", F(70, "bold"), WHITE, W / 2, 330, prog(t, 0.0, 0.45), spacing=8)
    reveal(img, "İMZAMIZI TAŞIYOR", F(70, "bold"), BLUE, W / 2, 430, prog(t, 0.1, 0.45), spacing=4)
    cx, cy = W / 2, 820
    p = prog(t, 0.2, 0.7)
    r = 170
    if p > 0: d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * expo(p), fill=BLUE, width=10)
    p = prog(t, 0.4, 0.6)
    if p > 0:
        sz = max(1, int(290 * back(p)))
        k = LOGO_K.resize((sz, sz), Image.LANCZOS).rotate(lerp(-25, 0, expo(p)), resample=Image.BICUBIC)
        img.alpha_composite(k, (int(cx - sz / 2), int(cy - sz / 2)))
    f = F(140); sp = 6; name = "KALMUK"
    x = W / 2 - tsize(name, f, sp)[0] / 2
    for i, ch in enumerate(name):
        cw = f.getlength(ch)
        reveal(img, ch, f, WHITE, x + cw / 2, 1080, prog(t, 0.6 + i * 0.05, 0.5))
        x += cw + sp
    reveal(img, "MEDIA", F(60, "bold"), BLUE, W / 2, 1250, prog(t, 0.9, 0.5), spacing=34)
    p = back(prog(t, 1.4, 0.5))
    if p > 0:
        bw, bh = 640 * p, 120 * p
        d.rounded_rectangle((W / 2 - bw / 2, 1480 - bh / 2, W / 2 + bw / 2, 1480 + bh / 2), radius=int(bh / 2), fill=BLUE)
        if p > 0.7: draw_text(d, "kalmukmedia.com.tr", F(46, "bold"), BLACK, W / 2, 1480 - 22)
    p = expo(prog(t, 1.8, 0.5))
    if p > 0:
        draw_text(d, "SIRADAKİ PROJE SİZİNKİ OLSUN", F(32, "bold"), WHITE, W / 2, 1600 + (1 - p) * 20, spacing=6)

SCENES = [(0.0, 2.0, s_intro, BLACK, WHITE), (2.0, 4.5, s_client, BLUE, BLACK),
          (4.5, 6.5, s_brief, BLACK, WHITE), (6.5, 11.5, s_desktop, WHITE, BLACK),
          (11.5, 15.0, s_products, BLACK, WHITE), (15.0, 17.5, s_mobile, BLUE, BLACK),
          (17.5, 99, s_outro, BLACK, WHITE)]
CUTS = [s for s, *_ in SCENES[1:]]
WIPES = [1.6, 4.1, 6.15, 11.1, 14.65, 17.1]

def frame(t):
    for s, e, fn, bg, fg in SCENES:
        if s <= t < e:
            img = Image.new("RGBA", (W, H), bg + (255,))
            if bg == BLACK:
                img.alpha_composite(GLOW, (int(W / 2 - 700 + math.sin(t * 0.5) * 300), int(H * 0.62 - 700 + math.cos(t * 0.37) * 400)))
            fn(img, t - s)
            chrome(img, t, fg)
            break
    a = np.asarray(img.convert("RGB"), dtype=np.float32)
    return a * min(prog(t, 0, 0.25), 1 - prog(t, DUR - 0.4, 0.4))

def render_frame(i):
    acc = sum(frame((i + (j + 0.5) / SUB) / FPS) for j in range(SUB)) / SUB
    return np.clip(acc + 0.5, 0, 255).astype(np.uint8).tobytes()

if __name__ == "__main__":
    out = "referans_huner_otomatik_kapi.mp4"
    subprocess.run(["python3", "music.py", json.dumps({"dur": DUR, "cuts": CUTS, "wipes": WIPES, "out": "music_huner.wav"})], check=True)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "music_huner.wav",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "14", "-preset", "slow",
                          "-profile:v", "high", "-tune", "animation",
                          "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    with Pool(os.cpu_count()) as pool:
        for buf in pool.imap(render_frame, range(int(FPS * DUR)), chunksize=4):
            p.stdin.write(buf)
    p.stdin.close(); p.wait()
    print("done", out)

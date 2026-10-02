"""Kalmuk Media referans videosu: Hüner Otomatik Kapı web sitesi (Instagram Reels, 9:16).
Render: python3 referans_huner.py -> referans_huner_otomatik_kapi.mp4
"""
import json, math, os, subprocess
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from render import (W, H, FPS, SUB, BLUE, WHITE, BLACK, F, clamp, prog, expo, inout, back, lerp,
                    tsize, draw_text, reveal, wipe, chrome, GLOW, LOGO_K)

DUR = 25.5
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
            ("KAPSAM", "25+ Ürün • Teklif Formu • Blog"), ("PLATFORM", "Masaüstü + Mobil")]
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

HB = (0x0B, 0x4F, 0xD1)          # Hüner theme color (meta theme-color)
HDARK = (9, 13, 24)
HTXT, HMUT = (14, 18, 28), (98, 106, 122)
SORA = {"x": "fonts/Sora_800ExtraBold.ttf", "s": "fonts/Sora_600SemiBold.ttf", "r": "fonts/Sora_400Regular.ttf"}
_sf = {}
def SF(size, w="x"):
    k = (int(size), w)
    if k not in _sf: _sf[k] = ImageFont.truetype(SORA[w], max(1, int(size)))
    return _sf[k]

MARQ = ["Seksiyonel Kapı", "PVC Hızlı Kapı", "Sarmal Kapı", "Hangar Kapısı", "Kepenk Sistemleri",
        "Fotoselli Kapı", "Yükleme Rampası", "Bariyer Sistemleri", "Yangın Kapısı"]

def photo(d, box, t, seed=0):
    """Stand-in for a site photo: dark gradient panel with an animated door."""
    x0, y0, x1, y1 = box
    for i in range(8):
        c = tuple(int(lerp(a, b, i / 7)) for a, b in zip((30, 40, 60), (12, 16, 26)))
        d.rectangle((x0, y0 + (y1 - y0) * i / 8, x1, y0 + (y1 - y0) * (i + 1) / 8), fill=c)
    w, h = (x1 - x0) * 0.55, (y1 - y0) * 0.6
    op = (math.sin(t * 1.6 + seed) * 0.5 + 0.5) * 0.75
    door(d, (x0 + x1) / 2 - w / 2, y1 - h - (y1 - y0) * 0.12, w, h, op, panel=5, frame=(140, 146, 160))

def site_desktop(t, hero_t, count_t):
    """Recreation of hunerotomatikkapi.com home page at 1280 CSS px wide (real copy & structure)."""
    pw, phh = 1280, 3000
    pg = Image.new("RGBA", (pw, phh), WHITE)
    d = ImageDraw.Draw(pg)
    # header
    d.rounded_rectangle((40, 18, 92, 70), radius=12, fill=HB)
    door(d, 54, 30, 24, 28, 0.0, panel=3, frame=WHITE, fill=WHITE)
    d.text((104, 26), "HÜNER", font=SF(26), fill=HTXT)
    d.text((104, 54), "Otomatik Kapı", font=SF(12, "r"), fill=HMUT)
    x = 360
    for n in ("Kurumsal", "Ürünlerimiz ▾", "Çalışmalarımız", "E-Katalog", "Blog", "SSS", "İletişim"):
        d.text((x, 44), n, font=SF(15, "s"), fill=HTXT, anchor="lm"); x += SF(15, "s").getlength(n) + 30
    d.rounded_rectangle((1090, 22, 1250, 66), radius=22, fill=HB)
    d.text((1170, 44), "Hemen Ara →", font=SF(15, "s"), fill=WHITE, anchor="mm")
    # hero
    d.rectangle((0, 88, pw, 820), fill=HDARK)
    for gx in range(0, pw, 64): d.line((gx, 88, gx, 820), fill=(20, 26, 40))
    for gy in range(88, 820, 64): d.line((0, gy, pw, gy), fill=(20, 26, 40))
    d.text((70, 190), "—  AUTOMATIC DOOR & AUTOMATION SYSTEMS", font=SF(13, "s"), fill=(127, 168, 255))
    lines = [("Kapınız", WHITE, None), ("akıllı, hızlı", WHITE, "akıllı,"), ("ve güvenli.", WHITE, None)]
    for i, (ln, c, acc) in enumerate(lines):
        p = expo(prog(hero_t, i * 0.12, 0.5))
        if p <= 0: continue
        y = 240 + i * 104
        lay = Image.new("RGBA", (720, 110), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        oy = (1 - p) * 110
        if acc:
            ld.text((0, oy), acc, font=SF(92), fill=(127, 168, 255))
            ld.text((SF(92).getlength(acc + " "), oy), ln[len(acc) + 1:], font=SF(92), fill=c)
        else:
            ld.text((0, oy), ln, font=SF(92), fill=c)
        pg.alpha_composite(lay, (70, y))
    q = expo(prog(hero_t, 0.4, 0.5))
    lead = ["Seksiyonel kapıdan PVC hızlı kapıya, sarmal kapıdan hangar",
            "kapısına kadar; endüstriyel, ticari ve konut projeleri için",
            "güvenli, dayanıklı ve estetik otomatik kapı çözümleri."]
    if q > 0:
        for i, l in enumerate(lead):
            d.text((70, 590 + i * 28 + (1 - q) * 20), l, font=SF(17, "r"), fill=(170, 178, 195))
        d.rounded_rectangle((70, 700, 300, 756), radius=28, fill=HB)
        d.text((185, 728), "Ücretsiz Keşif İste →", font=SF(15, "s"), fill=WHITE, anchor="mm")
        d.rounded_rectangle((316, 700, 500, 756), radius=28, outline=(90, 100, 120), width=2)
        d.text((408, 728), "Ürünleri Keşfet", font=SF(15, "s"), fill=WHITE, anchor="mm")
    # hero reel card
    r = expo(prog(hero_t, 0.2, 0.6))
    if r > 0:
        bx, by = 790 + (1 - r) * 80, 170
        photo(d, (bx, by, bx + 420, by + 540), t)
        d.rounded_rectangle((bx + 16, by + 490, bx + 250, by + 524), radius=17, fill=(0, 0, 0))
        d.ellipse((bx + 28, by + 502, bx + 38, by + 512), fill=(255, 70, 70))
        d.text((bx + 46, by + 507), "Hüner · Sarmal PVC Kapı", font=SF(13, "s"), fill=WHITE, anchor="lm")
        for j, (big, small, cy) in enumerate((("3 m/sn", "Sarmal kapı hızı", by + 60), ("20+", "Kapı & otomasyon ürünü", by + 330))):
            cx = bx - 60 if j == 0 else bx + 260
            d.rounded_rectangle((cx, cy, cx + 210, cy + 78), radius=16, fill=WHITE)
            d.text((cx + 18, cy + 12), big, font=SF(26), fill=HB)
            d.text((cx + 18, cy + 50), small, font=SF(12, "r"), fill=HMUT)
    # marquee
    d.rectangle((0, 820, pw, 900), fill=HB)
    s = "   •   ".join(MARQ * 3)
    d.text((-(t * 120) % 1400 - 1400, 860), s, font=SF(26), fill=WHITE, anchor="lm")
    # about
    photo(d, (70, 960, 560, 1560), t, 1)
    d.rounded_rectangle((330, 1460, 600, 1540), radius=16, fill=WHITE, outline=(225, 228, 235))
    d.text((350, 1474), "7/24", font=SF(28), fill=HB)
    d.text((440, 1478), "Servis & Bakım", font=SF(15, "s"), fill=HTXT)
    d.text((440, 1502), "Profesyonel montaj ekibi", font=SF(12, "r"), fill=HMUT)
    d.text((640, 980), "KURUMSAL", font=SF(13, "s"), fill=HB)
    d.text((640, 1010), "Kaliteden ödün vermeyen", font=SF(44), fill=HTXT)
    d.text((640, 1064), "kapı sistemleri.", font=SF(44), fill=HTXT)
    for i, l in enumerate(["Hüner Otomatik Kapı, sektördeki güçlü deneyimi ve kaliteli",
                           "ürünleriyle otomatik kapı sistemleri alanında öncü bir markadır."]):
        d.text((640, 1150 + i * 28), l, font=SF(16, "r"), fill=HMUT)
    for i, l in enumerate(["Ücretsiz keşif & projelendirme", "Uzman montaj ekibi", "Periyodik bakım & servis", "Uygun fiyat garantisi"]):
        d.ellipse((640, 1240 + i * 40, 662, 1262 + i * 40), fill=HB)
        d.text((674, 1251 + i * 40), l, font=SF(16, "s"), fill=HTXT, anchor="lm")
    d.rounded_rectangle((640, 1420, 860, 1474), radius=27, fill=HTXT)
    d.text((750, 1447), "Projenizi Konuşalım →", font=SF(14, "s"), fill=WHITE, anchor="mm")
    # counters
    d.rectangle((0, 1620, pw, 1860), fill=(244, 246, 250))
    for i, (n, suf, lab) in enumerate(((35, "+", "Seksiyonel kapı bileşeni"), (3, "m/s", "Sarmal kapı açılma hızı"),
                                       (20, "+", "Ürün & sistem çeşidi"), (100, "%", "Müşteri memnuniyeti odağı"))):
        cx = 70 + i * 290
        v = int(round(n * expo(clamp(count_t / 1.2))))
        d.text((cx, 1670), f"{v}", font=SF(64), fill=HTXT)
        d.text((cx + SF(64).getlength(f"{v}") + 6, 1680), suf, font=SF(24), fill=HB)
        d.text((cx, 1770), lab, font=SF(15, "r"), fill=HMUT)
    # products
    d.rectangle((0, 1860, pw, 2560), fill=HDARK)
    d.text((70, 1930), "ÜRÜNLERİMİZ", font=SF(13, "s"), fill=(127, 168, 255))
    d.text((70, 1960), "Her geçiş için", font=SF(52), fill=WHITE)
    d.text((70 + SF(52).getlength("Her geçiş için "), 1960), "doğru kapı.", font=SF(52), fill=(110, 118, 135))
    for i, n in enumerate(("Seksiyonel Kapılar", "PVC Hızlı Kapılar", "Sarmal PVC Kapı", "Hangar Kapısı")):
        cx = 70 + i * 400 - (t * 30)
        photo(d, (cx, 2080, cx + 370, 2480), t, i + 2)
        d.text((cx + 20, 2100), f"0{i + 1}", font=SF(16, "s"), fill=WHITE)
        d.text((cx + 20, 2430), n, font=SF(24), fill=WHITE)
    # process
    d.text((70, 2630), "SÜREÇ", font=SF(13, "s"), fill=HB)
    d.text((70, 2660), "Keşiften teslimata", font=SF(48), fill=HTXT)
    d.text((70 + SF(48).getlength("Keşiften teslimata "), 2660), "4 adım.", font=SF(48), fill=(150, 156, 170))
    for i, (h, p_) in enumerate((("Ücretsiz Keşif", "Alanınızı yerinde inceliyoruz."), ("Projelendirme", "Ölçü, model ve otomasyon."),
                                 ("Üretim & Montaj", "Hızlı ve temiz montaj."), ("Bakım & Servis", "Periyodik bakım ve servis."))):
        cx = 70 + i * 290
        d.rounded_rectangle((cx, 2760, cx + 270, 2940), radius=18, fill=(244, 246, 250))
        d.text((cx + 22, 2780), f"0{i + 1}", font=SF(30), fill=HB)
        d.text((cx + 22, 2840), h, font=SF(19), fill=HTXT)
        d.text((cx + 22, 2876), p_, font=SF(13, "r"), fill=HMUT)
    return pg

def preloader(size, t):
    """The site's real preloader: two door leaves, HÜNER, progress bar + percent, then doors open."""
    w, h = size
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    op = inout(prog(t, 1.0, 0.5))
    d.rectangle((-w / 2 * op, 0, w / 2 - w / 2 * op, h), fill=HDARK)
    d.rectangle((w / 2 + w / 2 * op, 0, w + w / 2 * op, h), fill=HDARK)
    if op < 0.3:
        a = int(255 * (1 - op / 0.3))
        cx, cy = w / 2, h / 2
        d.line((cx - 40, cy - 60, cx - 40, cy - 150, cx + 40, cy - 150, cx + 40, cy - 60), fill=WHITE + (a,), width=4)
        d.polygon([(cx - 22, cy - 136), (cx + 26, cy - 126), (cx + 26, cy - 66), (cx - 22, cy - 76)], fill=HB + (a,))
        d.text((cx, cy - 20), "HÜNER", font=SF(46), fill=WHITE + (a,), anchor="mm")
        d.text((cx, cy + 24), "Otomatik Kapı Sistemleri", font=SF(14, "r"), fill=(170, 178, 195, a), anchor="mm")
        pc = expo(clamp(t / 0.95))
        d.rectangle((cx - 120, cy + 60, cx + 120, cy + 63), fill=(40, 46, 60, a))
        d.rectangle((cx - 120, cy + 60, cx - 120 + 240 * pc, cy + 63), fill=HB + (a,))
        d.text((cx, cy + 92), f"{int(pc * 100)}%", font=SF(14, "s"), fill=WHITE + (a,), anchor="mm")
    return lay

def browser(t, scroll):
    bw, bh = 960, 680
    b = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), radius=24, fill=(236, 238, 242), outline=(200, 202, 208), width=2)
    for i, c in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))):
        d.ellipse((22 + i * 28, 20, 38 + i * 28, 36), fill=c)
    d.rounded_rectangle((130, 13, bw - 30, 43), radius=15, fill=WHITE)
    tp = clamp((t - 0.6) / 0.7)
    d.text((150, 28), CLIENT_URL[: int(len(CLIENT_URL) * tp)], font=F(18, "med"), fill=(60, 60, 60), anchor="lm")
    vw, vh = bw - 16, bh - 64
    pg = site_desktop(t, t - 2.0, t - 3.9)
    s = vw / pg.width
    src_h = vh / s
    view = pg.crop((0, int(scroll), pg.width, int(scroll + src_h))).resize((vw, vh), Image.LANCZOS)
    if t < 2.2:
        view.alpha_composite(preloader((vw, vh), t - 0.6) if t > 0.6 else Image.new("RGBA", (vw, vh), HDARK + (255,)))
    m = Image.new("L", (vw, vh), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, vw - 1, vh - 1), radius=14, fill=255)
    b.paste(view, (8, 56), m)
    return b

def s_desktop(img, t):  # 6.5 - 12.5, white
    img.paste(WHITE, (0, 0, W, H))
    if t < 0.35:
        ImageDraw.Draw(img).rectangle((W * inout(t / 0.35), 0, W, H), fill=BLACK)
    reveal(img, "KURUMSAL", F(110), BLACK, W / 2, 250, prog(t, 0.1, 0.45))
    reveal(img, "WEB SİTESİ", F(110), BLUE, W / 2, 380, prog(t, 0.2, 0.45))
    p = expo(prog(t, 0.2, 0.7))
    if p <= 0: return
    scroll = inout(prog(t, 2.9, 2.6)) * 2140
    b = browser(t, scroll)
    sc = lerp(0.85, 1.0, p) * (1 + 0.04 * t / 6)
    bw, bh = int(b.width * sc), int(b.height * sc)
    b = b.resize((bw, bh), Image.BICUBIC)
    x, y = W / 2 - bw / 2, 720 + (1 - p) * 500
    sh = Image.new("RGBA", (bw + 80, bh + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((40, 60, bw + 40, bh + 60), radius=30, fill=(0, 0, 0, 45))
    img.alpha_composite(sh, (int(x - 40), int(y - 30)))
    img.alpha_composite(b, (int(x), int(y)))
    q = expo(prog(t, 1.2, 0.5))
    if q > 0:
        draw_text(ImageDraw.Draw(img), CLIENT_URL, F(40, "bold"), BLACK, W / 2, y + bh + 110 + (1 - q) * 30)
    wipe(img, BLUE, prog(t, 5.6, 0.4), "up")

FEATURES = ["25+ Ürün Sayfası & Mega Menü", "Fotoğraflı Teklif Formu", "WhatsApp Entegrasyonu",
            "SEO & Schema Yapısı", "E-Katalog & Blog", "KVKK Çerez Yönetimi"]
def s_features(img, t):  # 12.5 - 15.5, blue
    img.paste(BLUE, (0, 0, W, H))
    d = ImageDraw.Draw(img)
    reveal(img, "NELER", F(130), WHITE, W / 2, 260, prog(t, 0.0, 0.45))
    reveal(img, "YAPTIK?", F(130), BLACK, W / 2, 410, prog(t, 0.08, 0.45))
    for i, f in enumerate(FEATURES):
        p = expo(prog(t, 0.35 + i * 0.16, 0.45))
        if p <= 0: continue
        y = 700 + i * 150
        x = 130 + (1 - p) * 80
        d.rounded_rectangle((x, y, W - 130, y + 118), radius=59, fill=BLACK)
        cp = back(prog(t, 0.45 + i * 0.16, 0.35))
        r = 34 * cp
        d.ellipse((x + 59 - r, y + 59 - r, x + 59 + r, y + 59 + r), fill=BLUE)
        if cp > 0.6:
            d.line((x + 44, y + 60, x + 55, y + 72, x + 76, y + 47), fill=BLACK, width=7)
        d.text((x + 120, y + 59), f, font=F(42, "bold"), fill=WHITE, anchor="lm")
    wipe(img, BLACK, prog(t, 2.6, 0.4), "left")

PRODUCTS = [("SEKSİYONEL", "KAPI"), ("PVC HIZLI", "KAPI"), ("SARMAL", "KAPI"),
            ("HANGAR", "KAPISI"), ("FOTOSELLİ", "KAPI")]
SLOT = 0.7
def s_products(img, t):  # 15.5 - 19, black
    d = ImageDraw.Draw(img)
    a = expo(prog(t, 0, 0.5))
    draw_text(d, "SİTEDE YER ALAN ÜRÜNLER", F(36, "bold"), BLUE, W / 2, 330 - (1 - a) * 30, spacing=8)
    idx = min(len(PRODUCTS) - 1, int(t // SLOT))
    lt = t - idx * SLOT
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

def site_mobile(t):
    """Mobile layout of the home page at 390 CSS px wide."""
    pw, phh = 390, 2000
    pg = Image.new("RGBA", (pw, phh), WHITE)
    d = ImageDraw.Draw(pg)
    d.rounded_rectangle((18, 18, 58, 58), radius=10, fill=HB)
    door(d, 29, 28, 18, 22, 0.0, panel=3, frame=WHITE, fill=WHITE)
    d.text((68, 22), "HÜNER", font=SF(20), fill=HTXT)
    d.text((68, 44), "Otomatik Kapı", font=SF(10, "r"), fill=HMUT)
    d.rectangle((340, 32, 368, 35), fill=HTXT); d.rectangle((346, 42, 368, 45), fill=HTXT)
    d.rectangle((0, 76, pw, 760), fill=HDARK)
    for gx in range(0, pw, 48): d.line((gx, 76, gx, 760), fill=(20, 26, 40))
    d.text((20, 110), "— AUTOMATIC DOOR & AUTOMATION", font=SF(10, "s"), fill=(127, 168, 255))
    d.text((20, 136), "Kapınız", font=SF(46), fill=WHITE)
    d.text((20, 188), "akıllı,", font=SF(46), fill=(127, 168, 255))
    d.text((20 + SF(46).getlength("akıllı, "), 188), "hızlı", font=SF(46), fill=WHITE)
    d.text((20, 240), "ve güvenli.", font=SF(46), fill=WHITE)
    for i, l in enumerate(["Seksiyonel kapıdan PVC hızlı kapıya,", "sarmal kapıdan hangar kapısına kadar",
                           "güvenli ve estetik otomatik kapı çözümleri."]):
        d.text((20, 316 + i * 22), l, font=SF(13, "r"), fill=(170, 178, 195))
    d.rounded_rectangle((20, 400, 230, 448), radius=24, fill=HB)
    d.text((125, 424), "Ücretsiz Keşif İste →", font=SF(13, "s"), fill=WHITE, anchor="mm")
    photo(d, (20, 480, 370, 700), t)
    d.text((20, 716), "3 m/sn", font=SF(22), fill=WHITE); d.text((200, 716), "20+", font=SF(22), fill=WHITE)
    d.rectangle((0, 760, pw, 812), fill=HB)
    d.text((-(t * 90) % 600 - 600, 786), "   •   ".join(MARQ * 2), font=SF(18), fill=WHITE, anchor="lm")
    photo(d, (20, 840, 370, 1140), t, 1)
    d.text((20, 1160), "KURUMSAL", font=SF(11, "s"), fill=HB)
    d.text((20, 1182), "Kaliteden ödün vermeyen", font=SF(24), fill=HTXT)
    d.text((20, 1214), "kapı sistemleri.", font=SF(24), fill=HTXT)
    for i, l in enumerate(["Ücretsiz keşif & projelendirme", "Uzman montaj ekibi", "Periyodik bakım & servis"]):
        d.ellipse((20, 1268 + i * 34, 38, 1286 + i * 34), fill=HB)
        d.text((48, 1277 + i * 34), l, font=SF(13, "s"), fill=HTXT, anchor="lm")
    d.rectangle((0, 1400, pw, 1700), fill=(244, 246, 250))
    for i, (n, lab) in enumerate((("35+", "Kapı bileşeni"), ("3 m/s", "Açılma hızı"), ("20+", "Ürün çeşidi"), ("100%", "Memnuniyet"))):
        cx, cy = 20 + (i % 2) * 185, 1430 + (i // 2) * 130
        d.text((cx, cy), n, font=SF(36), fill=HTXT)
        d.text((cx, cy + 56), lab, font=SF(12, "r"), fill=HMUT)
    d.rectangle((0, 1700, pw, phh), fill=HDARK)
    d.text((20, 1740), "Her geçiş için", font=SF(28), fill=WHITE)
    d.text((20, 1776), "doğru kapı.", font=SF(28), fill=(110, 118, 135))
    photo(d, (20, 1830, 370, 2000), t, 3)
    return pg

def s_mobile(img, t):  # 19 - 22, blue
    img.paste(BLUE, (0, 0, W, H))
    reveal(img, "MOBİL", F(120), WHITE, W / 2, 190, prog(t, 0.0, 0.45))
    reveal(img, "UYUMLU", F(120), BLACK, W / 2, 320, prog(t, 0.08, 0.45))
    pw, ph = 500, 1040
    p = expo(prog(t, 0.1, 0.6))
    if p <= 0: return
    sw, sh_ = pw - 36, ph - 36
    pg = site_mobile(t)
    s = sw / pg.width
    scroll = inout(prog(t, 0.9, 1.6)) * 1150
    scr = pg.crop((0, int(scroll), pg.width, int(scroll + sh_ / s))).resize((sw, sh_), Image.LANCZOS)
    phone = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    pd = ImageDraw.Draw(phone)
    pd.rounded_rectangle((0, 0, pw - 1, ph - 1), radius=66, fill=(20, 20, 22), outline=(60, 60, 66), width=4)
    m = Image.new("L", (sw, sh_), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, sw - 1, sh_ - 1), radius=50, fill=255)
    phone.paste(scr, (18, 18), m)
    pd.rounded_rectangle((pw / 2 - 64, 30, pw / 2 + 64, 56), radius=13, fill=BLACK)
    phone = phone.rotate(lerp(-8, 0, p), resample=Image.BICUBIC, expand=True)
    img.alpha_composite(phone, (int(W / 2 - phone.width / 2), int(540 + (1 - p) * 1300 - (phone.height - ph) / 2)))
    wipe(img, BLACK, prog(t, 2.6, 0.4), "up")

def s_outro(img, t):  # 22 - 25.5, black
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
          (4.5, 6.5, s_brief, BLACK, WHITE), (6.5, 12.5, s_desktop, WHITE, BLACK),
          (12.5, 15.5, s_features, BLUE, BLACK), (15.5, 19.0, s_products, BLACK, WHITE),
          (19.0, 22.0, s_mobile, BLUE, BLACK), (22.0, 99, s_outro, BLACK, WHITE)]
CUTS = [s for s, *_ in SCENES[1:]]
WIPES = [1.6, 4.1, 6.15, 12.1, 15.1, 18.65, 21.6]

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

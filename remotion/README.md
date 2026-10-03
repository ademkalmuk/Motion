# Kalmuk Media – Remotion videoları

```bash
cd remotion
npm install
npm run studio                 # tarayıcıda canlı önizleme / düzenleme
npm run render:huner           # out/referans_huner.mp4 (1080x1920, 30fps)
npm run render:promo           # out/kalmuk_media_reels.mp4
```

Bulut ortamında Chromium indirmek yerine hazır olanı kullanmak için:
`--browser-executable=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`

## Yapı
- `src/brand.ts` – Kalmuk (#51a2ff / #fff / #000) ve Hüner (#0b4fd1) renkleri
- `src/fonts.ts` – Montserrat + Sora (public/fonts, yerel)
- `src/components/motion.tsx` – Reveal, SplitChars, BarTransition, Grain, Glow, Chrome, Asset…
- `src/huner/` – Hüner Otomatik Kapı referans videosu (site HTML'den yeniden kurgulandı)

## Gerçek görseller
`public/huner/` klasörüne aşağıdaki adlarla dosya koyun; varsa otomatik kullanılır,
yoksa animasyonlu kapı çizimi gösterilir:

| Dosya | Sitedeki kaynak |
|---|---|
| `logo.png` | /assets/img/logo.png |
| `hero.jpg` | /uploads/2026/09/922d971f-babdoor-hizli-pvc-kapi-3.jpg |
| `seksiyonel.jpg` | /uploads/2026/09/2e048e33-seksiyonel-kapi-horizontal-banner-1.jpg |
| `pvc.jpg` | /uploads/2026/09/922d971f-babdoor-hizli-pvc-kapi-3.jpg |
| `sarmal.jpg` | /uploads/2026/09/b38233ec-garaj-kepenk-1024x576-1.jpg |
| `hangar.jpg` | /uploads/2026/09/30d67eb0-outside-aircarft-hangar-door-ct.jpg |
| `fotoselli.jpg` | /uploads/2026/09/c6261fd2-1656155054-fotosel-1.jpg |
| `about.jpg` | /uploads/2026/09/7969bd43-seksiyeonelkapi1.jpg |
| `desktop.png` | (isteğe bağlı) masaüstü tam sayfa ekran görüntüsü |

Müzik: `python3 ../music.py '{"dur":26,...,"out":"remotion/public/huner-music.wav"}'`

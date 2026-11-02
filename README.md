# Kalmuk Media – Motion

Instagram Reels (1080×1920) ve tanıtım videoları için araç zinciri.

```bash
bash scripts/setup.sh      # her şeyi kurar (ffmpeg, Blender, Remotion, HyperFrames, Motion Canvas)
```

| Araç | Klasör | Ne için | Render |
|---|---|---|---|
| **Remotion** (React) | `remotion/` | Ana videolar: tanıtım, referans, CRM | `cd remotion && npm run render:promo` (`render:huner`, `render:crm`) |
| **HyperFrames** (HTML + GSAP) | `hyperframes/` | Hızlı HTML/CSS animasyonları, web sitesi yakalama (`capture`) | `cd hyperframes/ornek && npx hyperframes render -o out.mp4` |
| **Motion Canvas** (TS, generator) | `motion-canvas/` | Kod/diyagram animasyonları, hassas zamanlama | `cd motion-canvas && npm run render` → `output/project.mp4` |
| **Blender** | `blender/` | 3D logo, ürün/cihaz sahneleri | `blender -b -P blender/test_logo.py -- out.png` |
| **ffmpeg** | – | Birleştirme, ses, format dönüştürme | `ffmpeg -i a.mp4 -i b.mp4 ...` |
| Python | `render.py`, `music.py` | İlk sürümler + müzik üretici | `python3 music.py '{"dur":25,"cuts":[...],"out":"x.wav"}'` |

## Bulut ortamı notları
- Tarayıcı: `/opt/pw-browsers/chromium` (Remotion için `--browser-executable`, Motion Canvas için `CHROME=` ile değiştirilebilir).
- CDN'ler (jsdelivr vb.) engelli olabilir: HyperFrames projelerinde `gsap.min.js` yerel dosya olarak kullanılır.
- Blender headless çalışır (`-b`), Eevee yerine `BLENDER_WORKBENCH` veya `CYCLES` (CPU) motorunu kullanın.

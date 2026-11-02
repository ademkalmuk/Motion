#!/usr/bin/env bash
# Video araç zincirini kurar: ffmpeg, Blender, Remotion, HyperFrames, Motion Canvas, Python paketleri.
# Tekrar çalıştırmak güvenlidir; kurulu olanı atlar.
set -e
cd "$(dirname "$0")/.."

if ! command -v blender >/dev/null || ! command -v ffmpeg >/dev/null; then
  apt-get update -q >/dev/null
  apt-get install -y -q ffmpeg blender libegl1 libgl1 >/dev/null
fi
python3 -c "import PIL, numpy, scipy" 2>/dev/null || pip install -q pillow numpy scipy

for d in remotion hyperframes motion-canvas; do
  [ -d "$d/node_modules" ] || (cd "$d" && npm ci --no-audit --no-fund --loglevel=error)
done
# HyperFrames: CDN'ler engelli olabilir, gsap'ı yerelden kopyala
for p in hyperframes/*/; do [ -f "$p/index.html" ] && cp -n hyperframes/node_modules/gsap/dist/gsap.min.js "$p" 2>/dev/null || true; done
echo "video toolchain ready: $(blender --version | head -1), $(ffmpeg -version | head -1 | cut -d' ' -f1-3)"

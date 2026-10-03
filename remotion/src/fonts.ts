import {continueRender, delayRender, staticFile} from 'remotion';

const FONTS: [string, string, string][] = [
  ['Montserrat', 'fonts/Montserrat_500Medium.ttf', '500'],
  ['Montserrat', 'fonts/Montserrat_700Bold.ttf', '700'],
  ['Montserrat', 'fonts/Montserrat_900Black.ttf', '900'],
  ['Sora', 'fonts/Sora_400Regular.ttf', '400'],
  ['Sora', 'fonts/Sora_600SemiBold.ttf', '600'],
  ['Sora', 'fonts/Sora_800ExtraBold.ttf', '800'],
];

let loaded = false;
export const loadFonts = () => {
  if (loaded || typeof document === 'undefined') return;
  loaded = true;
  const handle = delayRender('fonts');
  Promise.all(
    FONTS.map(([family, file, weight]) => {
      const f = new FontFace(family, `url(${staticFile(file)})`, {weight});
      document.fonts.add(f);
      return f.load();
    }),
  ).then(() => continueRender(handle), () => continueRender(handle));
};

export const MONT = 'Montserrat, sans-serif';
export const SORA = 'Sora, sans-serif';

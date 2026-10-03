import React from 'react';
import {AbsoluteFill, Audio, Img, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig, spring} from 'remotion';
import {HUNER, K} from '../brand';
import {loadFonts, MONT, SORA} from '../fonts';
import {
  BarTransition, Chrome, clamp, ease, easeInOut, Glow, Grain, hasAsset, KalmukMark, Reveal, SplitChars, useProg, useSpr,
} from '../components/motion';
import {HunerLogo, Photo, PRODUCTS, SiteDesktop, SiteMobile} from './site';

loadFonts();

// scene starts (frames @30fps)
export const CUTS = [0, 75, 165, 240, 420, 525, 600, 690];
export const HUNER_DURATION = 780;
const URL = 'hunerotomatikkapi.com';

const big: React.CSSProperties = {fontFamily: MONT, fontWeight: 900, color: K.white, textAlign: 'center', letterSpacing: -2};

// ---------- 1. intro ----------
const Intro: React.FC = () => {
  const f = useCurrentFrame();
  const line = useProg(14, 22);
  const mark = useSpr(0, 14);
  return (
    <AbsoluteFill style={{background: K.black, transform: `scale(${1 + f / 900})`}}>
      <Glow opacity={0.3} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div style={{transform: `scale(${mark}) rotate(${(1 - mark) * -40}deg)`, marginBottom: 60}}><KalmukMark size={150} /></div>
        <SplitChars text="YENİ" delay={6} style={{...big, fontSize: 210}} />
        <div style={{height: 8, width: 700 * line, background: K.blue, margin: '18px 0'}} />
        <SplitChars text="PROJE" delay={12} style={{...big, fontSize: 210, color: K.blue}} />
        <Reveal delay={30} style={{marginTop: 40}}>
          <div style={{fontFamily: MONT, fontWeight: 700, fontSize: 38, letterSpacing: 14, color: K.white}}>CASE STUDY • WEB SİTESİ</div>
        </Reveal>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------- 2. client: doors open ----------
const Leaf: React.FC<{side: 'l' | 'r'; p: number}> = ({side, p}) => (
  <div style={{
    position: 'absolute', top: 0, bottom: 0, width: '50%', [side === 'l' ? 'left' : 'right']: 0,
    transform: `translateX(${(side === 'l' ? -1 : 1) * p * 100}%)`,
    background: 'repeating-linear-gradient(#1c2333 0 118px, #0d1220 118px 128px)',
    boxShadow: side === 'l' ? 'inset -12px 0 30px #000' : 'inset 12px 0 30px #000',
  }} />
);
const Client: React.FC = () => {
  const open = useProg(8, 34, easeInOut);
  const logo = useSpr(22, 12);
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: HUNER.blue}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at 50% 45%, #2f73ff 0%, ${HUNER.blue} 40%, #062a75 100%)`}} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', transform: `scale(${1.08 - f / 1500})`}}>
        <div style={{fontFamily: MONT, fontWeight: 700, fontSize: 34, letterSpacing: 16, color: '#ffffffcc', opacity: open}}>MÜŞTERİMİZ</div>
        <div style={{margin: '60px 0 30px', transform: `scale(${logo})`, filter: `drop-shadow(0 30px 60px #0006)`}}>
          <div style={{background: '#fff', borderRadius: 48, padding: 40}}><HunerLogo size={240} dark /></div>
        </div>
        <Reveal delay={30}><div style={{fontFamily: SORA, fontWeight: 800, fontSize: 230, color: '#fff', letterSpacing: -6}}>HÜNER</div></Reveal>
        <Reveal delay={36}><div style={{fontFamily: SORA, fontWeight: 600, fontSize: 64, color: '#fff'}}>Otomatik Kapı Sistemleri</div></Reveal>
        <div style={{marginTop: 50, padding: '18px 40px', border: '3px solid #fff', borderRadius: 99, fontFamily: MONT, fontWeight: 700, fontSize: 34, letterSpacing: 6, color: '#fff', opacity: useProg(48, 14)}}>PENDİK • İSTANBUL</div>
      </AbsoluteFill>
      {/* light leaking through the opening */}
      <AbsoluteFill style={{background: `linear-gradient(90deg, transparent ${50 - open * 50 - 4}%, #ffffffaa ${50 - open * 50}%, transparent ${50 - open * 50 + 6}%)`, opacity: 1 - open}} />
      <Leaf side="l" p={open} /><Leaf side="r" p={open} />
    </AbsoluteFill>
  );
};

// ---------- 3. the site's headline, kinetic ----------
const Statement: React.FC = () => {
  const f = useCurrentFrame();
  const speed = useProg(34, 20);
  return (
    <AbsoluteFill style={{background: K.black, justifyContent: 'center', padding: '0 90px'}}>
      <Glow color={HUNER.blue} opacity={0.5} />
      {/* speed streaks */}
      {Array.from({length: 14}).map((_, i) => {
        const y = 200 + ((i * 137) % 1500);
        const x = ((f * (40 + (i % 5) * 14) + i * 300) % 2200) - 600;
        return <div key={i} style={{position: 'absolute', top: y, left: x, width: 300 + (i % 4) * 120, height: 3, background: `linear-gradient(90deg, transparent, ${K.blue})`, opacity: 0.25 + speed * 0.4}} />;
      })}
      <div style={{fontFamily: MONT, fontWeight: 700, fontSize: 30, letterSpacing: 8, color: K.blue, marginBottom: 30, opacity: useProg(0, 12)}}>SİTENİN MANŞETİ</div>
      {[['Kapınız', K.white], ['akıllı, hızlı', K.blue], ['ve güvenli.', K.white]].map(([t, c], i) => (
        <Reveal key={t} delay={4 + i * 6} dur={16}><div style={{fontFamily: SORA, fontWeight: 800, fontSize: 150, color: c, letterSpacing: -5}}>{t}</div></Reveal>
      ))}
      <div style={{marginTop: 70, display: 'flex', alignItems: 'baseline', gap: 24, transform: `translateX(${(1 - speed) * -200}px)`, opacity: speed}}>
        <span style={{fontFamily: SORA, fontWeight: 800, fontSize: 200, color: 'transparent', WebkitTextStroke: `4px ${K.white}`}}>3</span>
        <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 56, color: K.white}}>m/sn<br /><span style={{fontSize: 30, fontWeight: 500, color: '#aaa'}}>sarmal kapı hızı</span></span>
      </div>
    </AbsoluteFill>
  );
};

// ---------- 4. desktop: 3D browser ----------
const Preloader: React.FC<{t: number}> = ({t}) => {
  const pc = interpolate(t, [0, 26], [0, 100], {...clamp, easing: ease});
  const open = interpolate(t, [28, 42], [0, 1], {...clamp, easing: easeInOut});
  if (open >= 1) return null;
  const leaf = (s: number): React.CSSProperties => ({position: 'absolute', top: 0, bottom: 0, width: '50%', left: s < 0 ? 0 : '50%', background: HUNER.dark, transform: `translateX(${s * open * 100}%)`});
  return (
    <AbsoluteFill>
      <div style={leaf(-1)} /><div style={leaf(1)} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity: 1 - open * 3, color: '#fff', fontFamily: SORA}}>
        <HunerLogo size={90} />
        <div style={{fontWeight: 800, fontSize: 52, marginTop: 10}}>HÜNER</div>
        <div style={{fontSize: 15, color: '#aab'}}>Otomatik Kapı Sistemleri</div>
        <div style={{width: 260, height: 3, background: '#2a3040', marginTop: 24}}><div style={{width: `${pc}%`, height: 3, background: HUNER.blue}} /></div>
        <div style={{fontSize: 14, marginTop: 10}}>{Math.round(pc)}%</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Callout: React.FC<{x: number; y: number; delay: number; text: string; side?: 'l' | 'r'}> = ({x, y, delay, text, side = 'r'}) => {
  const s = useSpr(delay, 12);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `scale(${s})`, transformOrigin: side === 'r' ? 'left center' : 'right center', display: 'flex', alignItems: 'center', gap: 14, flexDirection: side === 'r' ? 'row' : 'row-reverse'}}>
      <div style={{width: 22, height: 22, borderRadius: 99, background: K.blue, boxShadow: `0 0 0 10px ${K.blue}44`}} />
      <div style={{background: K.black, color: '#fff', fontFamily: MONT, fontWeight: 700, fontSize: 32, padding: '14px 26px', borderRadius: 99}}>{text}</div>
    </div>
  );
};

const Desktop: React.FC = () => {
  const f = useCurrentFrame();
  const enter = useSpr(4, 20, 1);
  const rx = interpolate(enter, [0, 1], [40, 10]) - interpolate(f, [60, 170], [0, 6], clamp);
  const ry = interpolate(enter, [0, 1], [-30, -8]) + interpolate(f, [60, 170], [0, 8], clamp);
  const scroll = interpolate(f, [72, 168], [0, 1590], {...clamp, easing: easeInOut});
  const typed = Math.floor(interpolate(f, [14, 34], [0, URL.length], clamp));
  return (
    <AbsoluteFill style={{background: '#f2f4f8'}}>
      <AbsoluteFill style={{backgroundImage: 'linear-gradient(#0000000a 2px,transparent 2px),linear-gradient(90deg,#0000000a 2px,transparent 2px)', backgroundSize: '90px 90px'}} />
      <div style={{position: 'absolute', top: 190, width: '100%'}}>
        <Reveal delay={2}><div style={{...big, color: K.black, fontSize: 120}}>KURUMSAL</div></Reveal>
        <Reveal delay={6}><div style={{...big, color: K.blue, fontSize: 120}}>WEB SİTESİ</div></Reveal>
      </div>
      <AbsoluteFill style={{perspective: 2200, justifyContent: 'center', alignItems: 'center', paddingTop: 260}}>
        <div style={{
          width: 980, height: 720, borderRadius: 26, background: '#e9ecf1', overflow: 'hidden',
          transform: `translateY(${(1 - enter) * 600}px) rotateX(${rx}deg) rotateY(${ry}deg) scale(${0.92 + enter * 0.08})`,
          boxShadow: '0 80px 120px -30px #0006, 0 0 0 2px #cfd3da',
        }}>
          <div style={{height: 58, display: 'flex', alignItems: 'center', gap: 10, padding: '0 22px'}}>
            {['#ff5f57', '#febc2e', '#28c840'].map((c) => <div key={c} style={{width: 16, height: 16, borderRadius: 99, background: c}} />)}
            <div style={{marginLeft: 20, flex: 1, height: 34, borderRadius: 17, background: '#fff', display: 'flex', alignItems: 'center', padding: '0 18px', fontFamily: MONT, fontWeight: 500, fontSize: 18, color: '#444'}}>
              🔒&nbsp;{URL.slice(0, typed)}<span style={{opacity: f % 20 < 10 ? 1 : 0}}>|</span>
            </div>
          </div>
          <div style={{position: 'relative', height: 662, overflow: 'hidden', background: '#fff'}}>
            {hasAsset('huner/desktop.png') ? (
              <Img src={staticFile('huner/desktop.png')} style={{width: '100%', transform: `translateY(${-scroll * 0.75}px)`}} />
            ) : (
              <div style={{transform: `translateY(${-scroll * 0.75}px) scale(0.75)`, transformOrigin: 'top left'}}><SiteDesktop heroT={f - 52} /></div>
            )}
            <Preloader t={f - 10} />
          </div>
        </div>
      </AbsoluteFill>
      <Callout x={90} y={1500} delay={60} text="Kapı açılış preloader" />
      <Callout x={520} y={1630} delay={84} text="Mega menü • 25+ ürün" />
      <Callout x={140} y={1740} delay={112} text="Sayaçlar & ürün kartları" />
    </AbsoluteFill>
  );
};

// ---------- 5. products coverflow ----------
const Products: React.FC = () => {
  const f = useCurrentFrame();
  const pos = interpolate(f, [10, 95], [-0.6, PRODUCTS.length - 1], {...clamp, easing: easeInOut});
  const active = Math.round(Math.max(0, pos));
  return (
    <AbsoluteFill style={{background: K.black}}>
      <Glow opacity={0.35} />
      <div style={{position: 'absolute', top: 210, width: '100%'}}>
        <Reveal delay={0}><div style={{...big, fontSize: 40, fontWeight: 700, letterSpacing: 12, color: K.blue}}>SİTEDEKİ ÜRÜNLER</div></Reveal>
        <Reveal delay={4}><div style={{...big, fontSize: 110}}>HER GEÇİŞ İÇİN</div></Reveal>
        <Reveal delay={8}><div style={{...big, fontSize: 110, color: K.blue}}>DOĞRU KAPI</div></Reveal>
      </div>
      <AbsoluteFill style={{perspective: 1600, justifyContent: 'center', alignItems: 'center', paddingTop: 380}}>
        {PRODUCTS.map((p, i) => {
          const d = i - pos;
          const ad = Math.abs(d);
          return (
            <div key={p.name} style={{
              position: 'absolute', width: 620, height: 800, borderRadius: 36, overflow: 'hidden',
              transform: `translateX(${d * 520}px) translateZ(${-ad * 380}px) rotateY(${-d * 38}deg)`,
              opacity: Math.max(0, 1 - ad * 0.45), zIndex: 100 - Math.round(ad * 10),
              boxShadow: '0 50px 100px #000a',
            }}>
              <Photo img={p.img} seed={i} />
              <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(transparent 50%, #000d)'}} />
              <div style={{position: 'absolute', left: 40, top: 34, fontFamily: MONT, fontWeight: 800, fontSize: 40, color: K.blue}}>0{i + 1}</div>
              <div style={{position: 'absolute', left: 40, bottom: 50, right: 40, fontFamily: SORA, color: '#fff'}}>
                <div style={{fontSize: 54, fontWeight: 800, lineHeight: 1.05}}>{p.name}</div>
                <div style={{fontSize: 28, color: '#cfd5e0', marginTop: 10}}>{p.sub}</div>
              </div>
            </div>
          );
        })}
      </AbsoluteFill>
      <div style={{position: 'absolute', bottom: 150, width: '100%', display: 'flex', justifyContent: 'center', gap: 14}}>
        {PRODUCTS.map((_, i) => <div key={i} style={{width: i === active ? 60 : 16, height: 16, borderRadius: 99, background: i === active ? K.blue : '#444'}} />)}
      </div>
    </AbsoluteFill>
  );
};

// ---------- 6. features ----------
const FEATURES = ['25+ ürün sayfası & mega menü', 'Fotoğraflı teklif formu', 'WhatsApp entegrasyonu', 'SEO & Schema yapısı', 'E-Katalog & Blog', 'KVKK çerez yönetimi'];
const Features: React.FC = () => {
  const {fps} = useVideoConfig();
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: K.blue, padding: '220px 100px 0'}}>
      <div style={{position: 'absolute', right: -40, bottom: 80, fontFamily: MONT, fontWeight: 900, fontSize: 700, color: 'transparent', WebkitTextStroke: '4px #ffffff40', lineHeight: 1}}>06</div>
      <Reveal delay={0}><div style={{...big, textAlign: 'left', fontSize: 140}}>NELER</div></Reveal>
      <Reveal delay={4}><div style={{...big, textAlign: 'left', fontSize: 140, color: K.black}}>YAPTIK?</div></Reveal>
      <div style={{marginTop: 80}}>
        {FEATURES.map((t, i) => {
          const s = spring({frame: f - 12 - i * 5, fps, config: {damping: 15}});
          const c = spring({frame: f - 18 - i * 5, fps, config: {damping: 10}});
          return (
            <div key={t} style={{display: 'flex', alignItems: 'center', gap: 30, background: K.black, borderRadius: 99, padding: '26px 40px', marginBottom: 26, transform: `translateX(${(1 - s) * 900}px)`, opacity: s}}>
              <div style={{width: 64, height: 64, borderRadius: 99, background: K.blue, display: 'grid', placeItems: 'center', transform: `scale(${c})`, fontSize: 38, color: K.black, fontWeight: 900}}>✓</div>
              <div style={{fontFamily: MONT, fontWeight: 700, fontSize: 40, color: '#fff', whiteSpace: 'nowrap'}}>{t}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ---------- 7. mobile ----------
const Phone: React.FC<{scroll: number; tilt: number; delay: number; offset?: number}> = ({scroll, tilt, delay, offset = 0}) => {
  const f = useCurrentFrame();
  const s = useSpr(delay, 16);
  return (
    <div style={{
      width: 440, height: 920, borderRadius: 70, background: '#111', padding: 16, boxShadow: '0 60px 120px #000c, inset 0 0 0 3px #333',
      transform: `translateY(${(1 - s) * 1400 + Math.sin(f / 18 + delay) * 14}px) rotateY(${tilt}deg) rotateZ(${tilt / 6}deg)`,
    }}>
      <div style={{position: 'relative', width: '100%', height: '100%', borderRadius: 56, overflow: 'hidden', background: '#fff'}}>
        <div style={{transform: `translateY(${-(scroll + offset) * (408 / 390)}px) scale(${408 / 390})`, transformOrigin: 'top left'}}><SiteMobile /></div>
        <div style={{position: 'absolute', top: 14, left: '50%', marginLeft: -60, width: 120, height: 32, borderRadius: 99, background: '#000'}} />
      </div>
    </div>
  );
};
const Mobile: React.FC = () => {
  const f = useCurrentFrame();
  const sc = interpolate(f, [20, 85], [0, 700], {...clamp, easing: easeInOut});
  return (
    <AbsoluteFill style={{background: K.black}}>
      <Glow opacity={0.4} />
      <div style={{position: 'absolute', top: 190, width: '100%'}}>
        <Reveal delay={0}><div style={{...big, fontSize: 130}}>MOBİL</div></Reveal>
        <Reveal delay={4}><div style={{...big, fontSize: 130, color: K.blue}}>UYUMLU</div></Reveal>
      </div>
      <AbsoluteFill style={{perspective: 1800, flexDirection: 'row', justifyContent: 'center', alignItems: 'center', gap: 40, paddingTop: 420}}>
        <Phone scroll={sc} tilt={14} delay={4} />
        <div style={{marginTop: 160}}><Phone scroll={sc * 0.8} offset={900} tilt={-14} delay={10} /></div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------- 8. outro ----------
const Outro: React.FC = () => {
  const ring = useProg(4, 24);
  const mark = useSpr(10, 12);
  const pill = useSpr(44, 12);
  return (
    <AbsoluteFill style={{background: K.black, alignItems: 'center', justifyContent: 'center'}}>
      <Glow opacity={0.35} />
      <Reveal delay={0}><div style={{fontFamily: MONT, fontWeight: 700, fontSize: 40, letterSpacing: 10, color: '#fff'}}>TASARIM &amp; YAZILIM</div></Reveal>
      <div style={{position: 'relative', width: 340, height: 340, margin: '60px 0', display: 'grid', placeItems: 'center'}}>
        <svg width={340} height={340} style={{position: 'absolute', transform: 'rotate(-90deg)'}}>
          <circle cx={170} cy={170} r={160} fill="none" stroke={K.blue} strokeWidth={10} strokeDasharray={1005} strokeDashoffset={1005 * (1 - ring)} strokeLinecap="round" />
        </svg>
        <div style={{transform: `scale(${mark}) rotate(${(1 - mark) * -30}deg)`}}><KalmukMark size={300} /></div>
      </div>
      <SplitChars text="KALMUK" delay={20} style={{...big, fontSize: 170}} />
      <Reveal delay={30}><div style={{fontFamily: MONT, fontWeight: 700, fontSize: 66, letterSpacing: 40, color: K.blue, marginLeft: 40}}>MEDIA</div></Reveal>
      <div style={{marginTop: 70, padding: '30px 70px', borderRadius: 99, background: K.blue, fontFamily: MONT, fontWeight: 700, fontSize: 50, color: K.black, transform: `scale(${pill})`}}>kalmukmedia.com.tr</div>
      <Reveal delay={54} style={{marginTop: 40}}><div style={{fontFamily: MONT, fontWeight: 700, fontSize: 34, letterSpacing: 6, color: '#fff'}}>SIRADAKİ PROJE SİZİNKİ OLSUN</div></Reveal>
    </AbsoluteFill>
  );
};

const SCENES: [React.FC, string][] = [
  [Intro, K.white], [Client, K.white], [Statement, K.white], [Desktop, K.black],
  [Products, K.white], [Features, K.black], [Mobile, K.white], [Outro, K.white],
];

export const HunerReferans: React.FC = () => {
  const f = useCurrentFrame();
  const fade = interpolate(f, [0, 8, HUNER_DURATION - 14, HUNER_DURATION], [0, 1, 1, 0], clamp);
  return (
    <AbsoluteFill style={{background: K.black}}>
      <AbsoluteFill style={{opacity: fade}}>
        {SCENES.map(([Scene, chrome], i) => {
          const from = CUTS[i];
          const to = CUTS[i + 1] ?? HUNER_DURATION;
          return (
            <Sequence key={i} from={from} durationInFrames={to - from}>
              <Scene />
              <Chrome color={chrome} />
            </Sequence>
          );
        })}
        {CUTS.slice(1).map((c) => <BarTransition key={c} at={c} />)}
        <Grain />
      </AbsoluteFill>
      <Audio src={staticFile('huner-music.wav')} />
    </AbsoluteFill>
  );
};

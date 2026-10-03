import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {K} from '../brand';
import {loadFonts, MONT} from '../fonts';
import {
  BarTransition, Chrome, clamp, ease, easeInOut, Glow, Grain, KalmukMark, Reveal, SplitChars, useProg, useSpr,
} from '../components/motion';

loadFonts();

export const PROMO_CUTS = [0, 75, 150, 285, 465, 555, 630];
export const PROMO_DURATION = 750;

const big: React.CSSProperties = {fontFamily: MONT, fontWeight: 900, color: K.white, textAlign: 'center', letterSpacing: -2, lineHeight: 1};

// ---------- 1. intro ----------
const Intro: React.FC = () => {
  const f = useCurrentFrame();
  const mark = useSpr(0, 13);
  const line = useProg(10, 24);
  return (
    <AbsoluteFill style={{background: K.black, justifyContent: 'center', alignItems: 'center', transform: `scale(${1 + f / 800})`}}>
      <Glow opacity={0.3} />
      <div style={{transform: `scale(${mark}) rotate(${(1 - mark) * -60}deg)`, marginBottom: 70}}><KalmukMark size={170} /></div>
      <SplitChars text="DİJİTAL" delay={8} stagger={2} style={{...big, fontSize: 160}} />
      <div style={{height: 8, width: 760 * line, background: K.blue, margin: '26px 0'}} />
      <SplitChars text="DÜNYADA" delay={16} stagger={2} style={{...big, fontSize: 160}} />
      <Reveal delay={36} style={{marginTop: 50}}>
        <div style={{fontFamily: MONT, fontWeight: 700, fontSize: 44, letterSpacing: 14, color: K.blue}}>BİR ADIM ÖNDE OLUN</div>
      </Reveal>
    </AbsoluteFill>
  );
};

// ---------- 2. FARK slam ----------
const Fark: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const slam = spring({frame: f - 2, fps, config: {damping: 13, mass: 0.7, stiffness: 160}});
  const scale = interpolate(slam, [0, 1], [3.2, 1]);
  const impact = interpolate(f, [8, 20], [1, 0], clamp);
  const shake = Math.sin(f * 2.3) * 18 * impact;
  return (
    <AbsoluteFill style={{background: K.blue, justifyContent: 'center', alignItems: 'center', transform: `translate(${shake}px, ${shake * 0.6}px) scale(${1 + f / 1200})`}}>
      {/* outlined echoes */}
      {[3, 2, 1].map((k) => (
        <div key={k} style={{...big, position: 'absolute', fontSize: 330, color: 'transparent', WebkitTextStroke: '3px #00000030', transform: `translateY(${-k * 130 * slam}px)`, opacity: slam * 0.8}}>FARK</div>
      ))}
      <div style={{...big, fontSize: 330, color: K.black, transform: `scale(${scale})`, filter: `blur(${(1 - Math.min(1, slam)) * 20}px)`}}>FARK</div>
      <Reveal delay={12}><div style={{...big, fontSize: 150, marginTop: 10}}>YARATIN.</div></Reveal>
      <div style={{height: 12, width: 420 * useProg(22, 18), background: K.black, marginTop: 50}} />
      {/* impact flash */}
      <AbsoluteFill style={{background: '#fff', opacity: interpolate(f, [8, 14], [0.6, 0], clamp)}} />
    </AbsoluteFill>
  );
};

// ---------- 3. web build in a phone ----------
const UiBlock: React.FC<{delay: number; style: React.CSSProperties}> = ({delay, style}) => {
  const s = useSpr(delay, 14);
  return <div style={{position: 'absolute', transform: `translateY(${(1 - s) * 60}px) scale(${0.8 + s * 0.2})`, opacity: s, ...style}} />;
};
const Chip: React.FC<{text: string; x: number; y: number; delay: number; depth: number}> = ({text, x, y, delay, depth}) => {
  const f = useCurrentFrame();
  const s = useSpr(delay, 12);
  return (
    <div style={{
      position: 'absolute', left: x, top: y + Math.sin(f / 15 + depth) * 14 * depth, transform: `scale(${s})`, zIndex: 5,
      background: depth > 1 ? K.blue : '#111', color: depth > 1 ? K.black : '#fff', border: '2px solid #2a2a2a',
      fontFamily: MONT, fontWeight: 800, fontSize: 34, padding: '16px 28px', borderRadius: 20, boxShadow: '0 30px 60px #000a',
    }}>{text}</div>
  );
};
const WebBuild: React.FC = () => {
  const f = useCurrentFrame();
  const enter = useSpr(6, 18, 1);
  const scroll = interpolate(f, [80, 125], [0, 420], {...clamp, easing: easeInOut});
  const tap = interpolate(f, [62, 80], [0, 1], clamp);
  return (
    <AbsoluteFill style={{background: K.black}}>
      <Glow opacity={0.4} />
      <div style={{position: 'absolute', top: 200, width: '100%'}}>
        <Reveal delay={0}><div style={{...big, fontSize: 96}}>MARKANIZA ÖZEL</div></Reveal>
        <Reveal delay={5}><div style={{...big, fontSize: 96, color: K.blue}}>DİJİTAL DENEYİM</div></Reveal>
      </div>
      <AbsoluteFill style={{perspective: 1800, justifyContent: 'center', alignItems: 'center', paddingTop: 330}}>
        <div style={{
          width: 560, height: 1120, borderRadius: 80, background: '#111', padding: 18, boxShadow: '0 80px 140px #000, inset 0 0 0 3px #333',
          transform: `translateY(${(1 - enter) * 1400}px) rotateY(${interpolate(f, [0, 135], [-18, 10])}deg) rotateX(${interpolate(enter, [0, 1], [30, 6])}deg)`,
        }}>
          <div style={{position: 'relative', width: '100%', height: '100%', borderRadius: 64, overflow: 'hidden', background: '#0c0c0e'}}>
            <div style={{position: 'absolute', inset: 0, transform: `translateY(${-scroll}px)`}}>
              <UiBlock delay={20} style={{left: 34, top: 70, width: 56, height: 56, borderRadius: 99, background: K.blue}} />
              <UiBlock delay={22} style={{right: 34, top: 84, width: 60, height: 8, borderRadius: 4, background: '#fff', boxShadow: '0 16px 0 #fff, 0 32px 0 #fff'}} />
              <UiBlock delay={26} style={{left: 28, right: 28, top: 160, height: 420, borderRadius: 34, background: `linear-gradient(140deg, ${K.blue}, #1d5fd6)`}} />
              <UiBlock delay={32} style={{left: 64, top: 230, width: 330, height: 40, borderRadius: 10, background: '#fff'}} />
              <UiBlock delay={35} style={{left: 64, top: 290, width: 230, height: 40, borderRadius: 10, background: '#fff'}} />
              <UiBlock delay={40} style={{left: 64, top: 470, width: 200, height: 70, borderRadius: 35, background: '#000'}} />
              {Array.from({length: 6}).map((_, i) => (
                <UiBlock key={i} delay={46 + i * 4} style={{
                  left: 28 + (i % 2) * 262, top: 620 + Math.floor(i / 2) * 300, width: 236, height: 270, borderRadius: 26,
                  background: '#1c1c20', boxShadow: `inset 0 -110px 0 #1c1c20, inset 0 150px 0 ${i % 3 === 0 ? K.blue : '#3a3a42'}`,
                }} />
              ))}
            </div>
            {/* tap ripple */}
            {tap > 0 && tap < 1 && (
              <div style={{position: 'absolute', left: 164 - 100 * tap, top: 505 - 100 * tap, width: 200 * tap, height: 200 * tap, borderRadius: 999, border: `5px solid rgba(255,255,255,${1 - tap})`}} />
            )}
            <div style={{position: 'absolute', top: 18, left: '50%', marginLeft: -70, width: 140, height: 36, borderRadius: 99, background: '#000'}} />
          </div>
        </div>
      </AbsoluteFill>
      <Chip text="</>" x={60} y={720} delay={30} depth={1.5} />
      <Chip text="UI / UX" x={800} y={860} delay={38} depth={2} />
      <Chip text="SEO" x={50} y={1380} delay={46} depth={2} />
      <Chip text="⚡ Hızlı" x={790} y={1520} delay={54} depth={1.2} />
    </AbsoluteFill>
  );
};

// ---------- 4. services ----------
const SERVICES: [string, string?][] = [
  ['WEB', 'TASARIM'], ['ÖZEL', 'YAZILIM'], ['CRM', 'ÇÖZÜMLERİ'], ['E-TİCARET'],
  ['QR', 'MENÜ'], ['SOSYAL', 'MEDYA'], ['MOBİL', 'SİTE'], ['MARKA', 'KİMLİĞİ'],
];
const SLOT = 22.5;
const Services: React.FC = () => {
  const f = useCurrentFrame();
  const idx = Math.min(SERVICES.length - 1, Math.floor(f / SLOT));
  const lt = f - idx * SLOT;
  const last = idx === SERVICES.length - 1;
  const [a, b] = SERVICES[idx];
  const numS = interpolate(lt, [0, 14], [0, 1], {...clamp, easing: ease});
  const lineStyle = (txt: string, color: string): React.CSSProperties => ({...big, fontSize: txt.length > 8 ? 140 : 168, color});
  return (
    <AbsoluteFill style={{background: K.black}}>
      <Glow opacity={0.25} />
      {/* background vertical ticker */}
      <div style={{position: 'absolute', left: 60, top: -200 - f * 3, fontFamily: MONT, fontWeight: 900, fontSize: 64, color: '#ffffff0d', lineHeight: 1.3}}>
        {[...SERVICES, ...SERVICES, ...SERVICES].map((s, i) => <div key={i}>{s.join(' ')}</div>)}
      </div>
      <div style={{position: 'absolute', top: 300, width: '100%'}}>
        <div style={{fontFamily: MONT, fontWeight: 700, fontSize: 40, letterSpacing: 14, color: K.blue, textAlign: 'center', opacity: useProg(0, 12)}}>HİZMETLERİMİZ</div>
      </div>
      <div style={{...big, position: 'absolute', top: 560, width: '100%', fontSize: 680, color: 'transparent', WebkitTextStroke: '4px #262626', transform: `translateX(${(1 - numS) * 160}px)`, opacity: numS}}>
        0{idx + 1}
      </div>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        {/* key on idx so each word gets its own animation clock */}
        <Sequence key={idx} from={Math.round(idx * SLOT)} layout="none">
          <div>
            <Reveal delay={0} dur={12} out={last ? undefined : SLOT - 9}><div style={lineStyle(a, b ? K.white : K.blue)}>{a}</div></Reveal>
            {b && <Reveal delay={3} dur={12} out={last ? undefined : SLOT - 8}><div style={lineStyle(b, K.blue)}>{b}</div></Reveal>}
          </div>
        </Sequence>
      </AbsoluteFill>
      <div style={{position: 'absolute', bottom: 340, width: '100%', textAlign: 'center', fontFamily: MONT, fontWeight: 700, fontSize: 40, letterSpacing: 6, color: '#fff'}}>
        0{idx + 1} / 0{SERVICES.length}
      </div>
      <div style={{position: 'absolute', bottom: 290, left: 240, right: 240, height: 6, background: '#333'}}>
        <div style={{width: `${Math.min(100, (f / (SLOT * SERVICES.length)) * 100)}%`, height: 6, background: K.blue}} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- 5. process ----------
const STEPS = [['ANALİZ', 'İhtiyaç ve hedefler'], ['TASARIM', 'UI/UX ve marka dili'], ['GELİŞTİRME', 'Kodlama ve test'], ['YAYIN', 'Lansman ve destek']];
const Process: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const line = useProg(8, 40, easeInOut);
  return (
    <AbsoluteFill style={{background: K.blue, padding: '230px 100px'}}>
      <Reveal delay={0}><div style={{...big, textAlign: 'left', fontSize: 104}}>NASIL</div></Reveal>
      <Reveal delay={4}><div style={{...big, textAlign: 'left', fontSize: 104, color: K.black}}>ÇALIŞIYORUZ?</div></Reveal>
      <div style={{position: 'relative', marginTop: 110}}>
        <div style={{position: 'absolute', left: 52, top: 50, width: 8, height: 860 * line, background: K.black}} />
        {STEPS.map(([t, s], i) => {
          const sp = spring({frame: f - 12 - i * 10, fps, config: {damping: 12}});
          return (
            <div key={t} style={{display: 'flex', alignItems: 'center', gap: 50, height: 290}}>
              <div style={{width: 112, height: 112, borderRadius: 99, background: K.black, color: '#fff', display: 'grid', placeItems: 'center', fontFamily: MONT, fontWeight: 900, fontSize: 44, transform: `scale(${sp})`, zIndex: 1}}>0{i + 1}</div>
              <div style={{transform: `translateX(${(1 - sp) * 200}px)`, opacity: Math.min(1, sp)}}>
                <div style={{fontFamily: MONT, fontWeight: 900, fontSize: 84, color: K.black}}>{t}</div>
                <div style={{fontFamily: MONT, fontWeight: 500, fontSize: 40, color: '#fff'}}>{s}</div>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ---------- 6. stats ----------
const Stats: React.FC = () => {
  const ring = useProg(0, 36);
  const n = Math.max(1, Math.round(6 * useProg(0, 30)));
  const pop = useSpr(0, 11);
  return (
    <AbsoluteFill style={{background: K.white, justifyContent: 'center', alignItems: 'center'}}>
      <div style={{position: 'relative', width: 760, height: 760, display: 'grid', placeItems: 'center'}}>
        <svg width={760} height={760} style={{position: 'absolute', transform: 'rotate(-90deg)'}}>
          <circle cx={380} cy={380} r={360} fill="none" stroke="#eee" strokeWidth={16} />
          <circle cx={380} cy={380} r={360} fill="none" stroke={K.blue} strokeWidth={16} strokeDasharray={2262} strokeDashoffset={2262 * (1 - ring)} strokeLinecap="round" />
        </svg>
        <div style={{...big, fontSize: 470, color: K.black, transform: `scale(${pop})`}}>{n}+</div>
      </div>
      <Reveal delay={14} style={{marginTop: 70}}><div style={{...big, fontSize: 130, color: K.blue}}>YIL DENEYİM</div></Reveal>
      <div style={{marginTop: 50, display: 'flex', alignItems: 'center', gap: 18, fontFamily: MONT, fontWeight: 700, fontSize: 48, letterSpacing: 16, opacity: useProg(26, 14)}}>
        <svg width={44} height={56} viewBox="0 0 24 30"><path d="M12 0C5.4 0 0 5.4 0 12c0 9 12 18 12 18s12-9 12-18C24 5.4 18.6 0 12 0z" fill={K.blue} /><circle cx={12} cy={12} r={5} fill="#fff" /></svg>
        TRABZON
      </div>
    </AbsoluteFill>
  );
};

// ---------- 7. outro ----------
const Outro: React.FC = () => {
  const ring = useProg(4, 26);
  const mark = useSpr(10, 12);
  const pill = useSpr(44, 12);
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: K.black, alignItems: 'center', justifyContent: 'center'}}>
      <Glow opacity={0.35} />
      <div style={{position: 'relative', width: 380, height: 380, marginBottom: 60, display: 'grid', placeItems: 'center'}}>
        <svg width={380} height={380} style={{position: 'absolute', transform: `rotate(${-90 + f * 0.6}deg)`}}>
          <circle cx={190} cy={190} r={178} fill="none" stroke={K.blue} strokeWidth={10} strokeDasharray={1118} strokeDashoffset={1118 * (1 - ring)} strokeLinecap="round" />
        </svg>
        <div style={{transform: `scale(${mark}) rotate(${(1 - mark) * -30}deg)`}}><KalmukMark size={330} /></div>
      </div>
      <SplitChars text="KALMUK" delay={20} style={{...big, fontSize: 180}} />
      <Reveal delay={30}><div style={{fontFamily: MONT, fontWeight: 700, fontSize: 70, letterSpacing: 42, color: K.blue, marginLeft: 42}}>MEDIA</div></Reveal>
      <Reveal delay={38} style={{marginTop: 36}}><div style={{fontFamily: MONT, fontWeight: 500, fontSize: 40, color: '#bbb'}}>Web Tasarım • Özel Yazılım • CRM</div></Reveal>
      <div style={{marginTop: 70, padding: '30px 70px', borderRadius: 99, background: K.blue, fontFamily: MONT, fontWeight: 700, fontSize: 52, color: K.black, transform: `scale(${pill})`}}>kalmukmedia.com.tr</div>
      <Reveal delay={56} style={{marginTop: 44}}><div style={{fontFamily: MONT, fontWeight: 700, fontSize: 36, letterSpacing: 6, color: '#fff'}}>TEKLİF İÇİN DM'DEN YAZIN</div></Reveal>
    </AbsoluteFill>
  );
};

const SCENES: [React.FC, string][] = [
  [Intro, K.white], [Fark, K.black], [WebBuild, K.white], [Services, K.white],
  [Process, K.black], [Stats, K.black], [Outro, K.white],
];

export const KalmukPromo: React.FC = () => {
  const f = useCurrentFrame();
  const fade = interpolate(f, [0, 8, PROMO_DURATION - 14, PROMO_DURATION], [0, 1, 1, 0], clamp);
  return (
    <AbsoluteFill style={{background: K.black}}>
      <AbsoluteFill style={{opacity: fade}}>
        {SCENES.map(([Scene, chrome], i) => {
          const from = PROMO_CUTS[i];
          const to = PROMO_CUTS[i + 1] ?? PROMO_DURATION;
          return (
            <Sequence key={i} from={from} durationInFrames={to - from}>
              <Scene />
              <Chrome color={chrome} />
            </Sequence>
          );
        })}
        {PROMO_CUTS.slice(1).map((c) => <BarTransition key={c} at={c} />)}
        <Grain />
      </AbsoluteFill>
      <Audio src={staticFile('promo-music.wav')} />
    </AbsoluteFill>
  );
};

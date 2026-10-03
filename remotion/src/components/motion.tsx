import React from 'react';
import {
  AbsoluteFill, Easing, getStaticFiles, Img, interpolate, spring, staticFile,
  useCurrentFrame, useVideoConfig,
} from 'remotion';
import {K} from '../brand';
import {MONT} from '../fonts';

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const ease = Easing.bezier(0.16, 1, 0.3, 1); // expo-out
export const easeInOut = Easing.bezier(0.83, 0, 0.17, 1);

/** spring 0->1 starting at `delay` frames */
export const useSpr = (delay = 0, damping = 18, mass = 0.8, stiffness = 120) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: frame - delay, fps, config: {damping, mass, stiffness}});
};

export const useProg = (start: number, dur: number, e = ease) => {
  const frame = useCurrentFrame();
  return interpolate(frame, [start, start + dur], [0, 1], {...clamp, easing: e});
};

/** Masked line reveal: text slides up from behind a clip edge, with motion blur. */
export const Reveal: React.FC<{
  delay?: number; children: React.ReactNode; style?: React.CSSProperties; out?: number; dur?: number;
}> = ({delay = 0, children, style, out, dur = 18}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [delay, delay + dur], [0, 1], {...clamp, easing: ease});
  const o = out === undefined ? 0 : interpolate(frame, [out, out + 10], [0, 1], {...clamp, easing: easeInOut});
  const y = (1 - p) * 110 - o * 110;
  const blur = Math.abs((1 - p) * 8) + o * 8;
  return (
    <div style={{overflow: 'hidden', lineHeight: 1.05, padding: '0.06em 0', ...style}}>
      <div style={{transform: `translateY(${y}%)`, filter: `blur(${blur}px)`}}>{children}</div>
    </div>
  );
};

/** Per-character stagger with 3D flip + blur. */
export const SplitChars: React.FC<{text: string; delay?: number; stagger?: number; style?: React.CSSProperties}> = ({
  text, delay = 0, stagger = 2, style,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <div style={{display: 'flex', justifyContent: 'center', perspective: 800, ...style}}>
      {[...text].map((ch, i) => {
        const s = spring({frame: frame - delay - i * stagger, fps, config: {damping: 14, mass: 0.6}});
        return (
          <span key={i} style={{
            display: 'inline-block', whiteSpace: 'pre',
            transform: `translateY(${(1 - s) * 80}px) rotateX(${(1 - s) * -90}deg)`,
            opacity: Math.min(1, s * 1.5), filter: `blur(${(1 - Math.min(1, s)) * 10}px)`,
          }}>{ch}</span>
        );
      })}
    </div>
  );
};

/** Count-up number */
export const Counter: React.FC<{to: number; delay?: number; dur?: number; suffix?: string; style?: React.CSSProperties}> = ({
  to, delay = 0, dur = 30, suffix = '', style,
}) => {
  const p = useProg(delay, dur);
  return <span style={style}>{Math.round(to * p)}{suffix}</span>;
};

/** Film grain + vignette for a cinematic finish */
export const Grain: React.FC<{opacity?: number}> = ({opacity = 0.07}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <svg width="100%" height="100%" style={{opacity, mixBlendMode: 'overlay'}}>
        <filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={frame % 30} /></filter>
        <rect width="100%" height="100%" filter="url(#g)" />
      </svg>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.45) 100%)'}} />
    </AbsoluteFill>
  );
};

/** Drifting brand-blue light */
export const Glow: React.FC<{color?: string; opacity?: number}> = ({color = K.blue, opacity = 0.35}) => {
  const frame = useCurrentFrame();
  const x = 50 + Math.sin(frame / 60) * 25;
  const y = 60 + Math.cos(frame / 80) * 20;
  return (
    <AbsoluteFill style={{
      background: `radial-gradient(circle at ${x}% ${y}%, ${color} 0%, transparent 45%)`, opacity,
    }} />
  );
};

/** Bar transition centred on frame `at`: bars sweep up to cover, then continue up to reveal. */
export const BarTransition: React.FC<{at: number; colors?: string[]; bars?: number}> = ({
  at, colors = [K.blue, K.white, K.blue, K.black, K.blue], bars = 5,
}) => {
  const frame = useCurrentFrame();
  if (frame < at - 16 || frame > at + 18) return null;
  return (
    <AbsoluteFill style={{flexDirection: 'row'}}>
      {Array.from({length: bars}).map((_, i) => {
        const d = i * 1.5;
        const inP = interpolate(frame, [at - 14 + d, at - 2 + d], [0, 1], {...clamp, easing: easeInOut});
        const outP = interpolate(frame, [at + 1 + d, at + 13 + d], [0, 1], {...clamp, easing: easeInOut});
        const y = (1 - inP) * 100 - outP * 100;
        return <div key={i} style={{flex: 1, background: colors[i % colors.length], transform: `translateY(${y}%)`}} />;
      })}
    </AbsoluteFill>
  );
};

/** UI frame: brand tag + corner marks */
export const Chrome: React.FC<{color?: string; label?: string}> = ({color = K.white, label = 'KALMUK MEDIA'}) => {
  const p = useProg(6, 20);
  const L = 44 * p;
  const corner = (s: React.CSSProperties) => (
    <div style={{position: 'absolute', width: L, height: L, borderColor: color, borderStyle: 'solid', borderWidth: 0, ...s}} />
  );
  return (
    <AbsoluteFill style={{pointerEvents: 'none', color, fontFamily: MONT, fontWeight: 700, fontSize: 28, letterSpacing: 3}}>
      <div style={{position: 'absolute', top: 84, left: 76, opacity: p}}>{label}</div>
      <div style={{position: 'absolute', top: 84, right: 76, opacity: p}}>©2026</div>
      {corner({top: 50, left: 50, borderTopWidth: 4, borderLeftWidth: 4})}
      {corner({top: 50, right: 50, borderTopWidth: 4, borderRightWidth: 4})}
      {corner({bottom: 50, left: 50, borderBottomWidth: 4, borderLeftWidth: 4})}
      {corner({bottom: 50, right: 50, borderBottomWidth: 4, borderRightWidth: 4})}
    </AbsoluteFill>
  );
};

const files = () => new Set(getStaticFiles().map((f) => f.name));
export const hasAsset = (name: string) => files().has(name);

/** Image from /public if present, otherwise render the fallback. */
export const Asset: React.FC<{name: string; style?: React.CSSProperties; fallback: React.ReactNode}> = ({name, style, fallback}) =>
  hasAsset(name) ? <Img src={staticFile(name)} style={{objectFit: 'cover', ...style}} /> : <>{fallback}</>;

/** Kalmuk K mark extracted to white on transparent via CSS (logo is white K on black disc). */
export const KalmukMark: React.FC<{size: number}> = ({size}) => (
  <Img src={staticFile('kalmuk-logo.png')} style={{width: size, height: size, mixBlendMode: 'screen', borderRadius: '50%'}} />
);

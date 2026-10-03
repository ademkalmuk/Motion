// KALMUK CRM tanıtım videosu. Arayüz yapısı/metinleri gerçek panelden; veriler DEMO (gerçek müşteri bilgisi yok).
import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {K} from '../brand';
import {loadFonts, MONT} from '../fonts';
import {
  BarTransition, Chrome, clamp, easeInOut, Glow, Grain, KalmukMark, Reveal, SplitChars, useProg, useSpr,
} from '../components/motion';

loadFonts();

export const CRM_CUTS = [0, 75, 150, 330, 480, 570, 660];
export const CRM_DURATION = 750;

const F = MONT;
const big: React.CSSProperties = {fontFamily: F, fontWeight: 900, color: K.white, textAlign: 'center', letterSpacing: -2, lineHeight: 1};
const brutal = (s = 8): React.CSSProperties => ({border: `${Math.max(2, s / 3)}px solid #000`, boxShadow: `${s}px ${s}px 0 0 #000`});

const NAV = ['Dashboard', 'Müşteri Havuzu', 'Projeler', 'Proforma', 'Sözleşme', 'Ajanda', 'Hedefler', 'Başvurular', 'Raporlar', 'Şablonlar'];
const STATS: [number, string, string, string, string?][] = [
  [120, 'Toplam', '#000', '#fff'], [18, 'Yeni Kayıt', '#f3f4f6', '#000'], [64, 'İletişimde', '#dbeafe', '#1e3a8a'],
  [9, 'Teklif', '#fef9c3', '#713f12'], [29, 'Kazanıldı', '#dcfce7', '#14532d'], [3, 'Kaybedildi', '#fee2e2', '#7f1d1d'],
  [6, 'Bekleyen Görev', '#ffedd5', '#7c2d12'], [240, 'Bu Ay Ciro', '#14532d', '#fff', '₺K'],
];
const DEMO = ['Örnek Yazılım A.Ş.', 'Demo Gıda Ltd.', 'Mavi İnşaat', 'Kuzey Lojistik', 'Atlas Mobilya', 'Yıldız Tekstil'];

// ---------- 1. intro ----------
const Intro: React.FC = () => {
  const f = useCurrentFrame();
  const k = useSpr(0, 12);
  const typed = Math.floor(interpolate(f, [18, 40], [0, 10], clamp));
  return (
    <AbsoluteFill style={{background: K.black, justifyContent: 'center', alignItems: 'center'}}>
      <Glow opacity={0.25} />
      <div style={{...big, fontSize: 330, transform: `scale(${k}) rotate(${(1 - k) * -20}deg)`}}>K<span style={{color: K.blue}}>.</span></div>
      <div style={{fontFamily: F, fontWeight: 900, fontSize: 110, color: '#fff', marginTop: 30, letterSpacing: 2}}>
        {'KALMUK CRM'.slice(0, typed)}<span style={{opacity: f % 16 < 8 ? 1 : 0, color: K.blue}}>|</span>
      </div>
      <Reveal delay={42} style={{marginTop: 30}}><div style={{fontFamily: F, fontWeight: 700, fontSize: 40, letterSpacing: 16, color: '#999'}}>SATIŞ &amp; CRM</div></Reveal>
    </AbsoluteFill>
  );
};

// ---------- 2. problem → order ----------
const Problem: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const order = interpolate(f, [38, 60], [0, 1], {...clamp, easing: easeInOut});
  return (
    <AbsoluteFill style={{background: '#f8fafc'}}>
      <div style={{position: 'absolute', top: 220, width: '100%'}}>
        <Reveal delay={0}><div style={{...big, color: K.black, fontSize: 92}}>MÜŞTERİLER</div></Reveal>
        <Reveal delay={4}><div style={{...big, color: K.black, fontSize: 92}}>DAĞINIK MI?</div></Reveal>
      </div>
      {Array.from({length: 9}).map((_, i) => {
        const s = spring({frame: f - 4 - i * 2, fps, config: {damping: 11}});
        const chaosX = ((i * 397) % 760) - 380, chaosY = ((i * 271) % 700) - 250, rot = ((i * 53) % 50) - 25;
        const gx = (i % 3 - 1) * 300, gy = Math.floor(i / 3) * 230 - 160;
        const x = interpolate(order, [0, 1], [chaosX, gx]), y = interpolate(order, [0, 1], [chaosY, gy]);
        return (
          <div key={i} style={{
            position: 'absolute', left: '50%', top: 900, width: 260, height: 180, marginLeft: -130, background: i % 4 === 0 ? K.blue : '#fff', ...brutal(8),
            transform: `translate(${x}px, ${y - (1 - s) * 1500}px) rotate(${rot * (1 - order)}deg)`, padding: 20, fontFamily: F,
          }}>
            <div style={{fontWeight: 900, fontSize: 24, textTransform: 'uppercase'}}>{DEMO[i % DEMO.length]}</div>
            <div style={{marginTop: 14, height: 10, width: '70%', background: '#000'}} />
            <div style={{marginTop: 10, height: 10, width: '45%', background: '#0003'}} />
            <div style={{position: 'absolute', right: -12, top: -14, background: '#fff', ...brutal(3), fontSize: 14, fontWeight: 800, padding: '3px 10px'}}>{['YENİ', 'İLETİŞİMDE', 'KAZANILDI'][i % 3]}</div>
          </div>
        );
      })}
      <div style={{position: 'absolute', bottom: 170, width: '100%', opacity: order}}>
        <div style={{...big, fontSize: 84, color: K.blue}}>TEK PANELDE TOPLAYIN.</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- 3. dashboard in 3D browser ----------
const Dashboard: React.FC<{t: number}> = ({t}) => {
  const {fps} = useVideoConfig();
  const bars: [string, number, string][] = [['Kazanıldı', 24, '#22c55e'], ['Teklif Verildi', 8, '#facc15'], ['İletişimde', 53, '#60a5fa'], ['Yeni Kayıt', 15, '#d1d5db']];
  return (
    <div style={{display: 'flex', width: 1280, height: 860, fontFamily: F, background: '#f8fafc', color: '#000'}}>
      <div style={{width: 240, background: '#000', color: '#fff', flexShrink: 0}}>
        <div style={{padding: '22px 18px', borderBottom: '1px solid #ffffff1a', display: 'flex', gap: 12, alignItems: 'center'}}>
          <b style={{fontSize: 22, fontWeight: 900}}>K.</b>
          <div><div style={{fontWeight: 900, fontSize: 14}}>KALMUK CRM</div><div style={{fontSize: 9, color: '#999', letterSpacing: 3}}>SATIŞ &amp; CRM</div></div>
        </div>
        {NAV.map((n, i) => {
          const s = Math.min(1, Math.max(0, (t - i * 1.5) / 8));
          return (
            <div key={n} style={{padding: '12px 18px', fontSize: 11, fontWeight: 700, letterSpacing: 2, textTransform: 'uppercase', opacity: s, transform: `translateX(${(1 - s) * -30}px)`,
              background: i === 0 ? '#ffffff1f' : 'none', borderLeft: `3px solid ${i === 0 ? '#fff' : 'transparent'}`}}>{n}</div>
          );
        })}
      </div>
      <div style={{flex: 1, padding: 30}}>
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', borderBottom: '2px solid #000', paddingBottom: 12}}>
          <div><div style={{fontSize: 30, fontWeight: 900}}>DASHBOARD</div><div style={{fontSize: 11, color: '#999', letterSpacing: 3}}>03 EKİM 2026, CUMARTESİ</div></div>
          <div style={{display: 'flex', gap: 8}}>
            <div style={{background: '#000', color: '#fff', padding: '8px 16px', fontSize: 11, fontWeight: 800, letterSpacing: 2}}>+ YENİ KAYIT</div>
            <div style={{border: '2px solid #000', padding: '6px 14px', fontSize: 11, fontWeight: 800, letterSpacing: 2}}>PROJELER</div>
          </div>
        </div>
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(8, 1fr)', gap: 10, marginTop: 22}}>
          {STATS.map(([n, l, bg, c, suf], i) => {
            const s = spring({frame: t - 14 - i * 2, fps, config: {damping: 12}});
            const v = Math.round(n * Math.min(1, Math.max(0, (t - 14 - i * 2) / 30)));
            return (
              <div key={l} style={{background: bg, color: c, ...brutal(4), padding: 12, transform: `scale(${s})`}}>
                <div style={{fontSize: 24, fontWeight: 900}}>{suf === '₺K' ? `₺${v}K` : v}</div>
                <div style={{fontSize: 8, letterSpacing: 1.5, marginTop: 6, opacity: 0.7, textTransform: 'uppercase'}}>{l}</div>
              </div>
            );
          })}
        </div>
        <div style={{display: 'flex', gap: 20, marginTop: 26}}>
          <div style={{flex: 2, background: '#fff', ...brutal(4)}}>
            <div style={{padding: 12, borderBottom: '2px solid #000', fontSize: 12, fontWeight: 900, letterSpacing: 2}}>📋 SON ETKİLEŞİMLER</div>
            {DEMO.slice(0, 5).map((d, i) => {
              const s = Math.min(1, Math.max(0, (t - 40 - i * 4) / 10));
              return (
                <div key={d} style={{display: 'flex', gap: 12, padding: '12px 14px', borderBottom: '1px solid #eee', opacity: s, transform: `translateY(${(1 - s) * 20}px)`}}>
                  <span>{['💬', '📞', '🤝', '📝', '💬'][i]}</span>
                  <div style={{flex: 1}}><div style={{fontSize: 12, fontWeight: 900}}>{d.toUpperCase()}</div><div style={{fontSize: 11, color: '#666'}}>Teklif maili gönderildi, dönüş bekleniyor.</div></div>
                  <span style={{fontSize: 9, color: '#999'}}>{12 + i} EKİ</span>
                </div>
              );
            })}
          </div>
          <div style={{flex: 1, background: '#fff', ...brutal(4)}}>
            <div style={{padding: 12, borderBottom: '2px solid #000', fontSize: 12, fontWeight: 900, letterSpacing: 2}}>📊 DURUM DAĞILIMI</div>
            <div style={{padding: 14}}>
              {bars.map(([l, p, c], i) => {
                const w = p * Math.min(1, Math.max(0, (t - 50 - i * 5) / 25));
                return (
                  <div key={l} style={{marginBottom: 16}}>
                    <div style={{display: 'flex', justifyContent: 'space-between', fontSize: 10, fontWeight: 800}}><span>{l.toUpperCase()}</span><span style={{color: '#999'}}>{Math.round(w)}%</span></div>
                    <div style={{height: 10, border: '1px solid #000', background: '#f3f4f6', marginTop: 4}}><div style={{height: '100%', width: `${w}%`, background: c}} /></div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
const DashScene: React.FC = () => {
  const f = useCurrentFrame();
  const enter = useSpr(4, 20, 1);
  const zoom = interpolate(f, [110, 170], [1, 1.18], {...clamp, easing: easeInOut});
  return (
    <AbsoluteFill style={{background: K.black}}>
      <Glow opacity={0.35} />
      <div style={{position: 'absolute', top: 200, width: '100%'}}>
        <Reveal delay={0}><div style={{...big, fontSize: 110}}>HER ŞEY</div></Reveal>
        <Reveal delay={5}><div style={{...big, fontSize: 110, color: K.blue}}>TEK EKRANDA</div></Reveal>
      </div>
      <AbsoluteFill style={{perspective: 2200, justifyContent: 'center', alignItems: 'center', paddingTop: 300}}>
        <div style={{
          width: 1000, borderRadius: 22, overflow: 'hidden', background: '#e5e7eb', boxShadow: '0 80px 140px #000',
          transform: `translateY(${(1 - enter) * 900}px) rotateX(${interpolate(enter, [0, 1], [45, 8])}deg) rotateY(${interpolate(f, [0, 180], [-14, 8])}deg) scale(${zoom})`,
          transformOrigin: '50% 40%',
        }}>
          <div style={{height: 46, display: 'flex', alignItems: 'center', gap: 8, padding: '0 18px'}}>
            {['#ff5f57', '#febc2e', '#28c840'].map((c) => <div key={c} style={{width: 13, height: 13, borderRadius: 99, background: c}} />)}
            <div style={{marginLeft: 16, flex: 1, height: 26, borderRadius: 13, background: '#fff', fontFamily: F, fontSize: 14, display: 'flex', alignItems: 'center', padding: '0 14px', color: '#555'}}>🔒 crm.kalmukmedia.com.tr/Dashboard</div>
          </div>
          <div style={{width: 1000, height: 672, overflow: 'hidden'}}>
            <div style={{transform: 'scale(0.78125)', transformOrigin: 'top left'}}><Dashboard t={f - 14} /></div>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------- 4. modules ----------
const MODULES: [string, string, string][] = [
  ['MÜŞTERİ', 'HAVUZU', '👥'], ['PROFORMA', 'FATURA', '🧾'], ['DİJİTAL', 'SÖZLEŞME', '✍️'], ['AJANDA', '& GÖREV', '📅'],
  ['SATIŞ', 'HEDEFLERİ', '🎯'], ['TOPLU', 'MAİL', '✉️'],
];
const SLOT = 25;
const Modules: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const idx = Math.min(MODULES.length - 1, Math.floor(f / SLOT));
  return (
    <AbsoluteFill style={{background: K.blue}}>
      <div style={{position: 'absolute', top: 210, width: '100%', fontFamily: F, fontWeight: 800, fontSize: 40, letterSpacing: 14, textAlign: 'center', color: '#000'}}>MODÜLLER</div>
      {/* stacked brutalist cards */}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        {MODULES.slice(0, idx + 1).map(([a, b, ic], i) => {
          const s = spring({frame: f - i * SLOT, fps, config: {damping: 13, stiffness: 140}});
          const depth = idx - i;
          return (
            <div key={a} style={{
              position: 'absolute', width: 780, height: 720, background: i % 2 ? '#fff' : '#000', color: i % 2 ? '#000' : '#fff', ...brutal(18),
              transform: `translate(${depth * -26}px, ${(1 - s) * 1600 + depth * -26}px) rotate(${(1 - s) * 12 + depth * -2}deg)`,
              display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: 70, fontFamily: F,
            }}>
              <div style={{fontSize: 140}}>{ic}</div>
              <div style={{fontWeight: 900, fontSize: 110, lineHeight: 1, marginTop: 40}}>{a}</div>
              <div style={{fontWeight: 900, fontSize: 110, lineHeight: 1, color: K.blue}}>{b}</div>
              <div style={{position: 'absolute', top: 50, right: 60, fontWeight: 900, fontSize: 50, opacity: 0.4}}>0{i + 1}</div>
            </div>
          );
        })}
      </AbsoluteFill>
      <div style={{position: 'absolute', bottom: 190, width: '100%', display: 'flex', justifyContent: 'center', gap: 14}}>
        {MODULES.map((_, i) => <div key={i} style={{width: i === idx ? 70 : 20, height: 20, background: i <= idx ? '#000' : '#0003', border: '3px solid #000'}} />)}
      </div>
    </AbsoluteFill>
  );
};

// ---------- 5. pipeline ----------
const STAGES: [string, string][] = [['YENİ KAYIT', '#e5e7eb'], ['İLETİŞİMDE', '#bfdbfe'], ['TEKLİF', '#fef08a'], ['KAZANILDI', '#86efac']];
const Pipeline: React.FC = () => {
  const f = useCurrentFrame();
  const pos = interpolate(f, [16, 30, 40, 54, 64, 78], [0, 1, 1, 2, 2, 3], {...clamp, easing: easeInOut});
  const stage = Math.round(pos);
  const win = useProg(78, 10);
  return (
    <AbsoluteFill style={{background: '#f8fafc', padding: '200px 70px 0'}}>
      <Reveal delay={0}><div style={{...big, color: '#000', fontSize: 100}}>SATIŞ HUNİSİ</div></Reveal>
      <div style={{position: 'relative', marginTop: 90, display: 'flex', flexDirection: 'column', gap: 34}}>
        {STAGES.map(([n, c], i) => (
          <div key={n} style={{height: 250, background: c, ...brutal(8), display: 'flex', alignItems: 'center', padding: '0 40px', fontFamily: F, fontWeight: 900, fontSize: 44,
            opacity: useProg(i * 4, 12), outline: stage === i ? `6px solid ${K.blue}` : 'none', outlineOffset: 8}}>{n}</div>
        ))}
        {/* moving deal card */}
        <div style={{
          position: 'absolute', right: 40, top: 30 + pos * 284, width: 420, height: 190, background: '#fff', ...brutal(10),
          fontFamily: F, padding: 24, transform: `rotate(${Math.sin(f / 6) * 2}deg) scale(${1 + win * 0.08})`,
        }}>
          <div style={{fontWeight: 900, fontSize: 30}}>ÖRNEK YAZILIM A.Ş.</div>
          <div style={{fontSize: 22, color: '#555', marginTop: 8}}>Kurumsal web sitesi</div>
          <div style={{position: 'absolute', bottom: 22, left: 24, background: '#dcfce7', border: '2px solid #22c55e', fontWeight: 800, fontSize: 22, padding: '4px 14px'}}>₺50.000</div>
          <div style={{position: 'absolute', right: -18, top: -22, background: STAGES[stage][1], ...brutal(4), fontWeight: 900, fontSize: 18, padding: '6px 14px'}}>{STAGES[stage][0]}</div>
        </div>
      </div>
      {win > 0 && Array.from({length: 24}).map((_, i) => (
        <div key={i} style={{position: 'absolute', left: 540 + Math.cos(i) * 500 * win, top: 1500 + Math.sin(i * 2.3) * 400 * win - win * 200, width: 22, height: 22,
          background: [K.blue, '#22c55e', '#000', '#facc15'][i % 4], transform: `rotate(${i * 40 + f * 8}deg)`, opacity: 1 - win * 0.3}} />
      ))}
    </AbsoluteFill>
  );
};

// ---------- 6. mobile ----------
const MobileCRM: React.FC = () => {
  const f = useCurrentFrame();
  const enter = useSpr(4, 16);
  const sc = interpolate(f, [30, 85], [0, 520], {...clamp, easing: easeInOut});
  const st: [string, string, string][] = [['YENİ KAYIT', '#e5e7eb', '#000'], ['İLETİŞİMDE', '#bfdbfe', '#1e3a8a'], ['KAZANILDI', '#bbf7d0', '#14532d']];
  return (
    <AbsoluteFill style={{background: K.black}}>
      <Glow opacity={0.4} />
      <div style={{position: 'absolute', top: 190, width: '100%'}}>
        <Reveal delay={0}><div style={{...big, fontSize: 110}}>CEBİNİZDE</div></Reveal>
        <Reveal delay={5}><div style={{...big, fontSize: 110, color: K.blue}}>HER YERDE</div></Reveal>
      </div>
      <AbsoluteFill style={{perspective: 1800, justifyContent: 'center', alignItems: 'center', paddingTop: 380}}>
        <div style={{width: 500, height: 1020, borderRadius: 72, background: '#111', padding: 18, boxShadow: '0 60px 120px #000', transform: `translateY(${(1 - enter) * 1400}px) rotateY(${Math.sin(f / 30) * 10}deg)`}}>
          <div style={{width: '100%', height: '100%', borderRadius: 56, overflow: 'hidden', background: '#f8fafc', fontFamily: F, position: 'relative'}}>
            <div style={{background: '#000', color: '#fff', padding: '60px 22px 18px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', position: 'relative', zIndex: 2}}>
              <b style={{fontSize: 26, fontWeight: 900}}>KALMUK.</b><div style={{width: 40, height: 40, border: '1px solid #fff5', display: 'grid', placeItems: 'center'}}>☰</div>
            </div>
            <div style={{transform: `translateY(${-sc}px)`, padding: 20}}>
              <div style={{display: 'flex', gap: 10}}>
                <div style={{flex: 1, background: '#000', color: '#fff', padding: '18px 0', textAlign: 'center', fontWeight: 800, fontSize: 13, letterSpacing: 1}}>+ YENİ İŞLETME</div>
                <div style={{background: '#2563eb', color: '#fff', padding: '18px 16px', fontWeight: 800, fontSize: 13}}>TOPLU MAİL ✉️</div>
              </div>
              <div style={{display: 'flex', justifyContent: 'space-between', borderBottom: '2px solid #000', margin: '24px 0 22px', paddingBottom: 8}}>
                <b style={{fontSize: 22, fontWeight: 900}}>MÜŞTERİ HAVUZU</b><span style={{background: '#000', color: '#fff', fontSize: 11, padding: '4px 10px', fontWeight: 800}}>120 MÜŞTERİ</span>
              </div>
              {DEMO.map((d, i) => (
                <div key={d} style={{background: '#fff', ...brutal(5), padding: 18, marginBottom: 26, position: 'relative'}}>
                  <div style={{position: 'absolute', top: -12, right: -10, background: st[i % 3][1], color: st[i % 3][2], border: '2px solid #000', fontSize: 10, fontWeight: 800, padding: '3px 10px'}}>{st[i % 3][0]}</div>
                  <div style={{fontWeight: 900, fontSize: 20, marginTop: 4}}>{d.toUpperCase()}</div>
                  <div style={{display: 'flex', gap: 8, marginTop: 14}}>
                    <div style={{flex: 1, background: '#22c55e', border: '2px solid #000', textAlign: 'center', fontSize: 12, fontWeight: 800, padding: 8}}>WA</div>
                    <div style={{flex: 1, background: '#fff', border: '2px solid #000', textAlign: 'center', fontSize: 12, fontWeight: 800, padding: 8}}>MAIL</div>
                  </div>
                  <div style={{background: '#000', color: '#fff', textAlign: 'center', fontSize: 12, fontWeight: 800, padding: 12, marginTop: 10, letterSpacing: 1}}>DETAYLARI YÖNET →</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------- 7. outro ----------
const Outro: React.FC = () => {
  const ring = useProg(4, 26);
  const mark = useSpr(10, 12);
  const pill = useSpr(46, 12);
  return (
    <AbsoluteFill style={{background: K.black, alignItems: 'center', justifyContent: 'center'}}>
      <Glow opacity={0.35} />
      <Reveal delay={0}><div style={{...big, fontSize: 64}}>SATIŞLARINIZI</div></Reveal>
      <Reveal delay={5}><div style={{...big, fontSize: 64, color: K.blue}}>KONTROL EDİN</div></Reveal>
      <div style={{position: 'relative', width: 340, height: 340, margin: '70px 0 40px', display: 'grid', placeItems: 'center'}}>
        <svg width={340} height={340} style={{position: 'absolute', transform: 'rotate(-90deg)'}}>
          <circle cx={170} cy={170} r={160} fill="none" stroke={K.blue} strokeWidth={10} strokeDasharray={1005} strokeDashoffset={1005 * (1 - ring)} strokeLinecap="round" />
        </svg>
        <div style={{transform: `scale(${mark})`}}><KalmukMark size={300} /></div>
      </div>
      <SplitChars text="KALMUK" delay={22} style={{...big, fontSize: 170}} />
      <Reveal delay={32}><div style={{fontFamily: F, fontWeight: 700, fontSize: 60, letterSpacing: 26, color: K.blue, marginLeft: 26}}>CRM</div></Reveal>
      <div style={{marginTop: 60, padding: '28px 64px', borderRadius: 99, background: K.blue, fontFamily: F, fontWeight: 700, fontSize: 50, color: '#000', transform: `scale(${pill})`}}>kalmukmedia.com.tr</div>
      <Reveal delay={58} style={{marginTop: 40}}><div style={{fontFamily: F, fontWeight: 700, fontSize: 34, letterSpacing: 6, color: '#fff'}}>DEMO İÇİN DM'DEN YAZIN</div></Reveal>
    </AbsoluteFill>
  );
};

const SCENES: [React.FC, string][] = [
  [Intro, K.white], [Problem, K.black], [DashScene, K.white], [Modules, K.black], [Pipeline, K.black], [MobileCRM, K.white], [Outro, K.white],
];

export const KalmukCRM: React.FC = () => {
  const f = useCurrentFrame();
  const fade = interpolate(f, [0, 8, CRM_DURATION - 14, CRM_DURATION], [0, 1, 1, 0], clamp);
  return (
    <AbsoluteFill style={{background: K.black}}>
      <AbsoluteFill style={{opacity: fade}}>
        {SCENES.map(([Scene, chrome], i) => (
          <Sequence key={i} from={CRM_CUTS[i]} durationInFrames={(CRM_CUTS[i + 1] ?? CRM_DURATION) - CRM_CUTS[i]}>
            <Scene />
            <Chrome color={chrome} />
          </Sequence>
        ))}
        {CRM_CUTS.slice(1).map((c) => <BarTransition key={c} at={c} />)}
        <Grain />
      </AbsoluteFill>
      <Audio src={staticFile('crm-music.wav')} />
    </AbsoluteFill>
  );
};

// HTML recreation of hunerotomatikkapi.com (copy, structure and colours taken from the live page source).
import React from 'react';
import {useCurrentFrame} from 'remotion';
import {HUNER} from '../brand';
import {SORA} from '../fonts';
import {Asset, hasAsset} from '../components/motion';
import {Img, staticFile} from 'remotion';

export const PRODUCTS = [
  {name: 'Seksiyonel Kapılar', sub: 'Alan tasarruflu dikey hareket', img: 'huner/seksiyonel.jpg'},
  {name: 'PVC Hızlı Kapılar', sub: 'Yoğun geçişler için hızlı branda', img: 'huner/pvc.jpg'},
  {name: 'Sarmal PVC Kapı', sub: '2,5 – 3 m/sn yüksek hız', img: 'huner/sarmal.jpg'},
  {name: 'Hangar Kapısı', sub: 'Tersane, uçak ve maden sahaları', img: 'huner/hangar.jpg'},
  {name: 'Fotoselli Kapılar', sub: 'Temassız, hijyenik geçiş', img: 'huner/fotoselli.jpg'},
];
export const MARQ = ['Seksiyonel Kapı', 'PVC Hızlı Kapı', 'Sarmal Kapı', 'Hangar Kapısı', 'Kepenk Sistemleri',
  'Fotoselli Kapı', 'Yükleme Rampası', 'Bariyer Sistemleri', 'Yangın Kapısı'];

/** Placeholder "photo": an industrial sectional door that rolls up and down. */
export const DoorArt: React.FC<{seed?: number; style?: React.CSSProperties}> = ({seed = 0, style}) => {
  const f = useCurrentFrame();
  const open = (Math.sin(f / 22 + seed) * 0.5 + 0.5) * 70;
  return (
    <div style={{position: 'relative', overflow: 'hidden', background: 'linear-gradient(160deg,#28324a,#0c1120)', ...style}}>
      <div style={{position: 'absolute', left: '18%', right: '18%', top: '16%', bottom: '10%', border: '6px solid #8a93a8', borderBottom: 'none', background: '#05070d'}}>
        <div style={{
          position: 'absolute', inset: 0, transform: `translateY(-${open}%)`,
          background: 'repeating-linear-gradient(#d2d6de 0 14%, #9aa1ae 14% 16%)',
        }} />
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: '10%', background: '#1a2132'}} />
    </div>
  );
};

export const Photo: React.FC<{img: string; seed?: number; style?: React.CSSProperties}> = ({img, seed, style}) => (
  <Asset name={img} style={{width: '100%', height: '100%', ...style}} fallback={<DoorArt seed={seed} style={{width: '100%', height: '100%', ...style}} />} />
);

export const HunerLogo: React.FC<{size: number; dark?: boolean}> = ({size, dark}) =>
  hasAsset('huner/logo.png') ? (
    <Img src={staticFile('huner/logo.png')} style={{width: size, height: size, objectFit: 'contain'}} />
  ) : (
    <svg width={size} height={size} viewBox="0 0 120 140">
      <path d="M8 136V6h104v130" fill="none" stroke={dark ? HUNER.text : '#fff'} strokeWidth={9} />
      <polygon points="30,24 92,38 92,126 30,112" fill={HUNER.blue} />
    </svg>
  );

const Btn: React.FC<{children: React.ReactNode; ghost?: boolean; s?: number}> = ({children, ghost, s = 1}) => (
  <div style={{
    padding: `${14 * s}px ${26 * s}px`, borderRadius: 999, fontWeight: 600, fontSize: 15 * s,
    background: ghost ? 'transparent' : HUNER.blue, color: '#fff', border: ghost ? '2px solid #4a5468' : 'none',
  }}>{children}</div>
);

/** Desktop home page, 1280px wide. `heroT` = frames since the hero started animating. */
export const SiteDesktop: React.FC<{heroT: number}> = ({heroT}) => {
  const f = useCurrentFrame();
  const line = (i: number) => {
    const p = Math.min(1, Math.max(0, (heroT - i * 4) / 14));
    const e = 1 - Math.pow(1 - p, 4);
    return {transform: `translateY(${(1 - e) * 105}%)`};
  };
  return (
    <div style={{width: 1280, fontFamily: SORA, background: '#fff', color: HUNER.text}}>
      {/* header */}
      <div style={{height: 88, display: 'flex', alignItems: 'center', padding: '0 40px', gap: 14}}>
        <HunerLogo size={50} dark />
        <div><div style={{fontWeight: 800, fontSize: 26}}>HÜNER</div><div style={{fontSize: 12, color: HUNER.muted}}>Otomatik Kapı</div></div>
        <div style={{display: 'flex', gap: 30, marginLeft: 70, fontSize: 15, fontWeight: 600}}>
          {['Kurumsal', 'Ürünlerimiz ▾', 'Çalışmalarımız', 'E-Katalog', 'Blog', 'SSS', 'İletişim'].map((n) => <span key={n}>{n}</span>)}
        </div>
        <div style={{marginLeft: 'auto'}}><Btn>Hemen Ara →</Btn></div>
      </div>
      {/* hero */}
      <div style={{position: 'relative', height: 740, background: HUNER.dark, overflow: 'hidden', color: '#fff'}}>
        <Photo img="huner/hero.jpg" style={{position: 'absolute', inset: 0, opacity: 0.45}} />
        <div style={{position: 'absolute', inset: 0, backgroundImage: 'linear-gradient(#ffffff0d 1px,transparent 1px),linear-gradient(90deg,#ffffff0d 1px,transparent 1px)', backgroundSize: '64px 64px'}} />
        <div style={{position: 'absolute', left: 70, top: 100}}>
          <div style={{fontSize: 13, fontWeight: 600, color: HUNER.light, letterSpacing: 2}}>— AUTOMATIC DOOR &amp; AUTOMATION SYSTEMS</div>
          <div style={{fontSize: 96, fontWeight: 800, lineHeight: 1.04, marginTop: 24, letterSpacing: -2}}>
            {[<>Kapınız</>, <><em style={{color: HUNER.light}}>akıllı</em>, hızlı</>, <>ve güvenli.</>].map((c, i) => (
              <div key={i} style={{overflow: 'hidden'}}><div style={line(i)}>{c}</div></div>
            ))}
          </div>
          <div style={{width: 560, fontSize: 18, color: '#b4bccb', marginTop: 28, lineHeight: 1.55, opacity: Math.min(1, heroT / 20)}}>
            Seksiyonel kapıdan PVC hızlı kapıya, sarmal kapıdan hangar kapısına kadar; endüstriyel, ticari ve konut projeleri için güvenli, dayanıklı ve estetik otomatik kapı çözümleri.
          </div>
          <div style={{display: 'flex', gap: 14, marginTop: 30, opacity: Math.min(1, heroT / 24)}}>
            <Btn>Ücretsiz Keşif İste →</Btn><Btn ghost>Ürünleri Keşfet</Btn>
          </div>
        </div>
        <div style={{position: 'absolute', right: 70, top: 90, width: 400, height: 540, borderRadius: 24, overflow: 'hidden', transform: `translateX(${Math.max(0, 1 - heroT / 18) * 120}px)`}}>
          <Photo img="huner/sarmal.jpg" seed={1} />
          <div style={{position: 'absolute', left: 16, bottom: 16, background: '#000c', borderRadius: 99, padding: '8px 16px', fontSize: 13, fontWeight: 600}}>
            <span style={{color: '#ff4b4b'}}>● </span>Hüner · Sarmal PVC Kapı</div>
        </div>
        {[{b: '3 m/sn', s: 'Sarmal kapı hızı', x: 760, y: 150}, {b: '20+', s: 'Kapı & otomasyon ürünü', x: 1010, y: 470}].map((c, i) => (
          <div key={i} style={{position: 'absolute', left: c.x, top: c.y + Math.sin(f / 20 + i) * 8, background: '#fff', color: HUNER.text, borderRadius: 16, padding: '14px 20px', boxShadow: '0 20px 50px #0008', opacity: Math.min(1, Math.max(0, (heroT - 12 - i * 6) / 10))}}>
            <div style={{fontSize: 28, fontWeight: 800, color: HUNER.blue}}>{c.b}</div><div style={{fontSize: 12, color: HUNER.muted}}>{c.s}</div>
          </div>
        ))}
      </div>
      {/* marquee */}
      <div style={{height: 80, background: HUNER.blue, color: '#fff', overflow: 'hidden', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', fontWeight: 800, fontSize: 26}}>
        <div style={{transform: `translateX(${-((f * 4) % 1600)}px)`}}>{[...MARQ, ...MARQ, ...MARQ].map((m, i) => <span key={i} style={{marginRight: 40}}>{m} •</span>)}</div>
      </div>
      {/* about */}
      <div style={{display: 'flex', gap: 70, padding: '70px 70px'}}>
        <div style={{position: 'relative', width: 500, height: 600, borderRadius: 24, overflow: 'hidden'}}>
          <Photo img="huner/about.jpg" seed={2} />
          <div style={{position: 'absolute', right: 16, bottom: 16, background: '#fff', borderRadius: 16, padding: '14px 18px', display: 'flex', gap: 14, alignItems: 'center'}}>
            <b style={{fontSize: 30, color: HUNER.blue}}>7/24</b><div style={{fontSize: 14}}><b>Servis &amp; Bakım</b><br /><span style={{color: HUNER.muted, fontSize: 12}}>Profesyonel montaj ekibi</span></div>
          </div>
        </div>
        <div style={{flex: 1, paddingTop: 20}}>
          <div style={{color: HUNER.blue, fontWeight: 600, fontSize: 13, letterSpacing: 2}}>KURUMSAL</div>
          <div style={{fontSize: 46, fontWeight: 800, lineHeight: 1.1, marginTop: 12}}>Kaliteden ödün vermeyen kapı sistemleri.</div>
          <p style={{color: HUNER.muted, fontSize: 17, lineHeight: 1.6}}>Hüner Otomatik Kapı, sektördeki güçlü deneyimi ve kaliteli ürünleriyle otomatik kapı sistemleri alanında öncü bir markadır.</p>
          {['Ücretsiz keşif & projelendirme', 'Uzman montaj ekibi', 'Periyodik bakım & servis', 'Uygun fiyat garantisi'].map((c) => (
            <div key={c} style={{display: 'flex', gap: 12, alignItems: 'center', fontWeight: 600, fontSize: 17, margin: '14px 0'}}>
              <span style={{width: 24, height: 24, borderRadius: 99, background: HUNER.blue, color: '#fff', fontSize: 14, display: 'grid', placeItems: 'center'}}>✓</span>{c}</div>
          ))}
        </div>
      </div>
      {/* counters */}
      <div style={{display: 'flex', background: '#f4f6fa', padding: '50px 70px'}}>
        {[['35', '+', 'Seksiyonel kapı bileşeni'], ['3', 'm/s', 'Sarmal kapı açılma hızı'], ['20', '+', 'Ürün & sistem çeşidi'], ['100', '%', 'Müşteri memnuniyeti odağı']].map(([n, s, l]) => (
          <div key={l} style={{flex: 1}}><b style={{fontSize: 64, fontWeight: 800}}>{n}</b><sup style={{color: HUNER.blue, fontSize: 24, fontWeight: 800}}> {s}</sup><div style={{color: HUNER.muted}}>{l}</div></div>
        ))}
      </div>
      {/* products */}
      <div style={{background: HUNER.dark, color: '#fff', padding: '70px 0 70px 70px'}}>
        <div style={{color: HUNER.light, fontWeight: 600, fontSize: 13, letterSpacing: 2}}>ÜRÜNLERİMİZ</div>
        <div style={{fontSize: 54, fontWeight: 800}}>Her geçiş için <span style={{color: '#6e7687'}}>doğru kapı.</span></div>
        <div style={{display: 'flex', gap: 24, marginTop: 40}}>
          {PRODUCTS.slice(0, 4).map((p, i) => (
            <div key={p.name} style={{position: 'relative', width: 380, height: 440, borderRadius: 22, overflow: 'hidden', flexShrink: 0}}>
              <Photo img={p.img} seed={i + 3} />
              <div style={{position: 'absolute', left: 22, top: 18, fontWeight: 600}}>0{i + 1}</div>
              <div style={{position: 'absolute', left: 22, bottom: 22, fontSize: 24, fontWeight: 800}}>{p.name}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

/** Mobile home page, 390px wide. */
export const SiteMobile: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <div style={{width: 390, fontFamily: SORA, background: '#fff', color: HUNER.text}}>
      <div style={{height: 76, display: 'flex', alignItems: 'center', padding: '0 18px', gap: 10}}>
        <HunerLogo size={40} dark /><div><b style={{fontSize: 20, fontWeight: 800}}>HÜNER</b><div style={{fontSize: 10, color: HUNER.muted}}>Otomatik Kapı</div></div>
        <div style={{marginLeft: 'auto', width: 28}}><div style={{height: 3, background: HUNER.text, marginBottom: 7}} /><div style={{height: 3, background: HUNER.text, marginLeft: 8}} /></div>
      </div>
      <div style={{position: 'relative', background: HUNER.dark, color: '#fff', padding: '34px 20px 24px', overflow: 'hidden'}}>
        <Photo img="huner/hero.jpg" style={{position: 'absolute', inset: 0, opacity: 0.4}} />
        <div style={{position: 'relative'}}>
          <div style={{fontSize: 10, color: HUNER.light, fontWeight: 600, letterSpacing: 1.5}}>— AUTOMATIC DOOR &amp; AUTOMATION</div>
          <div style={{fontSize: 46, fontWeight: 800, lineHeight: 1.06, marginTop: 12}}>Kapınız<br /><em style={{color: HUNER.light}}>akıllı</em>, hızlı<br />ve güvenli.</div>
          <p style={{fontSize: 13, color: '#b4bccb', lineHeight: 1.6}}>Seksiyonel kapıdan PVC hızlı kapıya, sarmal kapıdan hangar kapısına kadar güvenli ve estetik çözümler.</p>
          <div style={{display: 'inline-block'}}><Btn s={0.9}>Ücretsiz Keşif İste →</Btn></div>
          <div style={{height: 220, borderRadius: 18, overflow: 'hidden', marginTop: 24}}><Photo img="huner/sarmal.jpg" seed={1} /></div>
          <div style={{display: 'flex', gap: 40, marginTop: 16, fontWeight: 800, fontSize: 22}}><span>3 m/sn</span><span>20+</span></div>
        </div>
      </div>
      <div style={{height: 52, background: HUNER.blue, color: '#fff', overflow: 'hidden', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', fontWeight: 800, fontSize: 18}}>
        <div style={{transform: `translateX(${-((f * 3) % 900)}px)`}}>{[...MARQ, ...MARQ].map((m, i) => <span key={i} style={{marginRight: 24}}>{m} •</span>)}</div>
      </div>
      <div style={{padding: 20}}>
        <div style={{height: 300, borderRadius: 18, overflow: 'hidden'}}><Photo img="huner/about.jpg" seed={2} /></div>
        <div style={{color: HUNER.blue, fontSize: 11, fontWeight: 600, marginTop: 20}}>KURUMSAL</div>
        <div style={{fontSize: 26, fontWeight: 800}}>Kaliteden ödün vermeyen kapı sistemleri.</div>
      </div>
      <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', background: '#f4f6fa', padding: 20, gap: 20}}>
        {[['35+', 'Kapı bileşeni'], ['3 m/s', 'Açılma hızı'], ['20+', 'Ürün çeşidi'], ['100%', 'Memnuniyet']].map(([n, l]) => (
          <div key={l}><b style={{fontSize: 36, fontWeight: 800}}>{n}</b><div style={{fontSize: 12, color: HUNER.muted}}>{l}</div></div>
        ))}
      </div>
      <div style={{background: HUNER.dark, color: '#fff', padding: 20}}>
        <div style={{fontSize: 28, fontWeight: 800}}>Her geçiş için <span style={{color: '#6e7687'}}>doğru kapı.</span></div>
        {PRODUCTS.slice(0, 3).map((p, i) => (
          <div key={p.name} style={{height: 240, borderRadius: 18, overflow: 'hidden', marginTop: 16, position: 'relative'}}>
            <Photo img={p.img} seed={i + 3} />
            <b style={{position: 'absolute', left: 16, bottom: 14, fontSize: 20}}>{p.name}</b>
          </div>
        ))}
      </div>
    </div>
  );
};

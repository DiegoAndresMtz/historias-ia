// «Brote zombi: atrapado en el supermercado» (formato trend TikTok nov-2026). Guion y voz en stories/zombi_super/.
import React from 'react';
import {AbsoluteFill, random} from 'remotion';
import {clamp, ease, ramp, Char, ZombieCloseup, Flash, Camera, Vignette, Meta, TL} from '../kit';
import {FLOOR, Market, Counter, Gate, ColdRoom, Skylight, Night, BackLot, Parking, Alley, Truck, Moto} from '../sets';
import p1 from '../data/zombi_super_p1.json'; import p2 from '../data/zombi_super_p2.json'; import p3 from '../data/zombi_super_p3.json';

type S = React.FC<{t: number; w: (tok: string) => number}>;
// reparto: «tú» de amarillo
const YOU = {hair: 'ShortScratch', skin: '#c68a62', clothes: '#d9a521', pose: 'ShirtPantsBW'};
const HECTOR = {hair: 'Bald', skin: '#b07a52', clothes: '#e6e1d6', pose: 'CrossedArmsWB', facialHair: 'Full'};
const MAMA = {hair: 'Long', skin: '#d49b74', clothes: '#4a6fa5', pose: 'RestingWB'};
const NINA = {hair: 'Buns', skin: '#d49b74', clothes: '#e07aa0', pose: 'WalkingWB'};
const REPA = {hair: 'HatHip', skin: '#8a5a3a', clothes: '#e8702a', pose: 'EasingWB'};
const MUCHA = {hair: 'MediumStraight', skin: '#c68a62', clothes: '#7a4a8a', pose: 'RestingBW'};
const CAJERA = {hair: 'Bun', skin: '#c68a62', clothes: '#c0392b', pose: 'ShirtPantsWB'};
const SOLD = {hair: 'BaldTop', skin: '#a8704a', clothes: '#4a5a3a', pose: 'BlazerPantsBW'};
const Z = (p: any) => <Char pose="RoboDanceOutline" zombie {...p} />;

// ---------------- Día 1 ----------------
const d01: S = ({t, w}) => { const k = w('muerde'), bit = t > k - 0.35;
  return (<Camera t={t} keys={[[0, 1.0, 540, 1100], [k, 1.55, 700, 1060]]} shake={t > k && t < k + 0.6 ? 1 : 0}>
    <Market t={t} red={bit ? ramp(t, k, 0.3) : 0} /><Counter x={600} />
    <Char t={t} x={880} y={FLOOR - 40} h={560} {...CAJERA} flip face={bit ? 'Fear' : 'Calm'} seed={3} tilt={bit ? -8 * ramp(t, k, 0.3) : 0} />
    {bit ? <Z t={t} x={640 + 70 * ramp(t, k - 0.35, 0.3)} y={FLOOR} h={640} hair="GrayBun" seed={1} />
         : <Char t={t} x={640} y={FLOOR} h={640} pose="RestingBW" hair="GrayBun" skin="#d49b74" clothes="#7b5a8a" face="Tired" seed={1} />}
    <Char t={t} x={380} y={FLOOR + 30} h={680} {...YOU} face={bit ? 'Awe' : 'Calm'} seed={5} />
    <Char t={t} x={140} y={FLOOR + 50} h={680} {...MAMA} face={bit ? 'ConcernedFear' : 'Smile'} seed={6} />
    <Flash t={t} at={k} col="255,40,40" /></Camera>); };
const d02: S = ({t, w}) => { const lv = w('levanta'), up = ramp(t, lv, 0.9), pk = w('parpadea');
  if (t > pk - 0.15) return <ZombieCloseup t={t} scale={1 + 0.06 * ease((t - pk) / 1.5)} />;
  return (<Camera t={t} keys={[[0, 1.1, 600, 1250], [lv, 1.35, 720, 1250]]}>
    <Market t={t} light={0.75} /><Counter x={620} />
    <div style={{position: 'absolute', inset: 0, transformOrigin: `760px ${FLOOR}px`, transform: `rotate(${-90 * (1 - up)}deg)`}}>
      <Char t={t} x={760} y={FLOOR} h={620} pose={up > 0 ? 'RoboDanceOutline' : 'ShirtPantsWB'} hair="Bun" zombie={up > 0} skin={CAJERA.skin} clothes={CAJERA.clothes} face="EyesClosed" seed={3} flip />
    </div>
    <Char t={t} x={300} y={FLOOR + 30} h={680} {...YOU} face="Fear" seed={5} /></Camera>); };
const Horde: React.FC<{t: number; n: number; y?: number; dim?: number; walk?: number; x0?: number; x1?: number; flip?: boolean}> = ({t, n, y = 1260, dim = 0.15, walk = 0, x0 = 80, x1 = 1000, flip}) => (<>
  {[...Array(n)].map((_, i) => <Z key={i} t={t} x={x0 + random('x' + i) * (x1 - x0)} y={y + random('y' + i) * 80} h={520 + random('h' + i) * 80}
    hair={['ShortMessy', 'Medium', 'Bald', 'Long', 'Afro'][i % 5]} seed={i + 10} flip={flip ?? random('f' + i) > 0.5} dim={dim} walk={walk} />)}</>);
const d03: S = ({t, w}) => { const g = w('golpe'), v = w('veinte');
  return (<Camera t={t} keys={[[0, 1.0, 540, 1000], [v, 1.25, 540, 900]]} shake={t > g && t < g + 0.5 ? 1 : 0}>
    <AbsoluteFill style={{background: 'linear-gradient(#07080c,#141821)'}} />
    <Horde t={t} n={t < v ? 5 : 14} />
    <Gate t={t} down={ramp(t, g - 0.5, 0.45)} shake={t > g ? 0.6 + 0.4 * Math.abs(Math.sin(t * 9)) : 0} />
    {[[YOU, 150], [HECTOR, 330], [MAMA, 510], [NINA, 650], [REPA, 800], [MUCHA, 960]].map(([c, x]: any, i) => (
      <Char key={'p' + i} t={t} x={x} y={1800} h={i === 3 ? 470 : 660} {...c} face="ConcernedFear" flip seed={20 + i} />))}
    <Vignette a={0.6} /></Camera>); };
const d04: S = ({t, w}) => { const cast: [any, string, number, number][] = [[YOU, 'tú', 150, 680], [HECTOR, 'héctor', 330, 700], [MAMA, 'mamá', 500, 680], [NINA, 'niña', 630, 470], [REPA, 'repartidor', 800, 680], [MUCHA, 'muchacha', 960, 670]];
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150]]}><Market t={t} light={0.7} />
    {cast.map(([c, tok, x, h], i) => { const k = w(tok); if (t < k - 0.3) return null; const a = ramp(t, k - 0.3, 0.45);
      return <Char key={i} t={t} x={x - 160 * (1 - a)} y={FLOOR + 40} h={h} {...c} walk={1 - a} face={['Calm', 'Serious', 'Calm', 'Cute', 'Calm', 'Concerned'][i]} seed={i * 4} />; })}
    {t > w('vendado') && <div style={{position: 'absolute', left: 900, top: 1150, width: 160, height: 160, borderRadius: 80, background: 'radial-gradient(rgba(255,30,30,.55),rgba(255,0,0,0))'}} />}
  </Camera>); };
const d05: S = ({t, w}) => { const off = clamp((t - w('apaga')) / 0.25), ad = w('adentro');
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150], [ad, 1.4, 360, 1000]]}><Market t={t} light={1 - 0.8 * off} />
    <Char t={t} x={360} y={FLOOR + 40} h={720} {...HECTOR} pose="PointingFingerWB" face="Driven" seed={2} />
    <Char t={t} x={760} y={FLOOR + 40} h={680} {...YOU} face="ConcernedFear" flip seed={5} />
    {t > ad && <div style={{position: 'absolute', inset: 0, background: `radial-gradient(circle at 360px 900px, rgba(0,0,0,0) 0, rgba(0,0,0,${0.7 * ramp(t, ad, 0.4)}) 420px)`}} />}
  </Camera>); };
const d06: S = ({t, w}) => { const s = w('sangre');
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150], [s, 1.7, 800, 1060]]}><Market t={t} light={0.32} />
    <AbsoluteFill style={{background: 'rgba(8,16,48,.35)'}} />
    <div style={{position: 'absolute', inset: 0, transformOrigin: `260px ${FLOOR}px`, transform: 'rotate(-88deg)'}}><Char t={t} x={260} y={FLOOR} h={600} {...YOU} face="EyesClosed" seed={5} /></div>
    <Char t={t} x={470} y={FLOOR + 40} h={690} {...REPA} pose="PointingFingerWB" face="ConcernedFear" seed={8} />
    <Char t={t} x={820} y={FLOOR + 40} h={680} {...MUCHA} face="Tired" flip seed={9} tilt={Math.sin(t * 12) * 2} />
    {t > s - 0.2 && <div style={{position: 'absolute', left: 700, top: 1000, width: 200, height: 200, borderRadius: 100, background: 'radial-gradient(rgba(220,0,20,.8) 0, rgba(255,0,0,0) 70%)', transform: `scale(${0.9 + 0.1 * Math.sin(t * 9)})`}} />}
  </Camera>); };
const d07: S = ({t}) => <ColdRoom t={t} knock={0} />;

// ---------------- Día 2 ----------------
const e01: S = ({t, w}) => { const g = w('golpear'), kn = t > g ? Math.abs(Math.sin(t * 6)) : 0;
  return (<Camera t={t} keys={[[0, 1.0, 540, 1100], [g, 1.25, 540, 1000]]} shake={kn * 0.3}><ColdRoom t={t} knock={kn} />
    <Char t={t} x={150} y={FLOOR + 80} h={680} {...YOU} face={kn ? 'Awe' : 'ConcernedFear'} seed={5} />
    <Char t={t} x={930} y={FLOOR + 80} h={700} {...HECTOR} face="Suspicious" flip seed={2} /></Camera>); };
const e02: S = ({t, w}) => { const k = w('techo');
  return (<Camera t={t} keys={[[0, 1.0, 540, 900], [k, 1.15, 540, 760]]}><Skylight t={t} crack={0} />
    {t > k - 0.3 && [0, 1, 2].map(i => { const a = ramp(t, k - 0.3 + i * 0.2, 0.4);
      return (<div key={i} style={{position: 'absolute', left: 70 + i * 340, top: 390, width: 280, height: 680, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: -(70 + i * 340), top: -390, width: 1080, height: 1920}}>
          <Z t={t} x={210 + i * 340} y={760 + 280 * a} h={560} hair="ShortMessy" seed={i + 2} dim={0.8} /></div></div>); })}
    <Char t={t} x={540} y={1850} h={640} {...YOU} face="Awe" seed={5} /></Camera>); };
const e03: S = ({t, w}) => { const sp = t > w('rápidos') ? 2 : 1;
  return (<Camera t={t} keys={[[0, 1.0, 640, 1000]]}><BackLot t={t} />
    {[0, 1, 2, 3, 4].map(i => { const p = (t * 0.22 * sp + i * 0.2) % 1;
      return <Z key={i} t={t} x={420 + i * 130} y={1500 - p * 900} h={440} hair={['Afro', 'Long', 'Bald', 'Medium', 'ShortMessy'][i]} seed={i + 11} walk={1} />; })}
  </Camera>); };
const e04: S = ({t, w}) => { const m = w('moto');
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150], [w('uno'), 1.3, 700, 1150]]}><Parking t={t} />
    <Moto x={760} y={FLOOR + 40} s={1.5} light={t > m ? 1 : 0} />
    <Char t={t} x={470} y={FLOOR + 50} h={690} {...REPA} pose="PointingFingerWB" face="Explaining" seed={8} />
    <Char t={t} x={170} y={FLOOR + 50} h={680} {...YOU} face="Concerned" seed={5} /></Camera>); };
const e05: S = ({t, w}) => { const f = w('fiebre');
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150], [f, 1.5, 720, 1080]]}><Market t={t} light={0.4} />
    <Char t={t} x={640} y={FLOOR + 40} h={690} {...MAMA} face="Concerned" flip seed={6} />
    <Char t={t} x={800} y={FLOOR + 40} h={470} {...NINA} pose="RestingWB" face="Tired" flip seed={4} />
    <Char t={t} x={230} y={FLOOR + 40} h={680} {...YOU} face="ConcernedFear" seed={5} />
    {t > f - 0.2 && <div style={{position: 'absolute', left: 700, top: 1000, width: 200, height: 200, borderRadius: 100, background: `radial-gradient(rgba(255,90,30,${0.35 + 0.15 * Math.sin(t * 5)}) 0, rgba(255,60,0,0) 70%)`}} />}
  </Camera>); };
const e06: S = ({t, w}) => { const k = w('raja');
  if (t > k + 0.25) return <ZombieCloseup t={t} scale={1.05} />;
  return (<Camera t={t} keys={[[0, 1.0, 540, 800], [k, 1.6, 540, 700]]} shake={t > k ? 1 : 0}><Skylight t={t} crack={ramp(t, k - 0.1, 0.3)} />
    <Flash t={t} at={k} col="230,240,255" /></Camera>); };
const e07: S = ({t}) => <Skylight t={t} crack={1} />;

// ---------------- Día 3 ----------------
const f01: S = ({t, w}) => { const k = w('caer'), x = 120 + 560 * clamp(t / Math.max(0.1, k));
  return (<Camera t={t} keys={[[0, 1.0, 540, 1100], [k, 1.35, 680, 1300]]}><Night t={t} />
    {t < k ? <><Moto x={x} y={1480} s={0.9} light={1} /><Char t={t} x={x - 20} y={1400} h={420} {...REPA} pose="ClosedLegWB" face="Fear" seed={8} /></>
           : <><Moto x={700} y={1480} s={0.9} rot={70} /><Horde t={t} n={7} y={1420} x0={520} x1={900} walk={0.4} dim={0.25} /></>}
    <Night t={t} frame /></Camera>); };
const f02: S = ({t, w}) => { const c = w('cede'), b = w('campana');
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150]]} shake={t > c && t < c + 0.6 ? 1 : 0}><Market t={t} light={0.6} />
    <Char t={t} x={860} y={FLOOR + 40} h={720} {...HECTOR} pose="PointingFingerWB" face="Rage" flip seed={2} />
    {t > b && <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
      <circle cx={760 + 12 * Math.sin(t * 14)} cy={950} r={34} fill="#e6b422" stroke="#0c0c10" strokeWidth={6} />
      {[70, 120, 170].map(r => <path key={r} d={`M${760 - r} ${950 - r * 0.6} A${r} ${r} 0 0 0 ${760 - r} ${950 + r * 0.6}`} stroke="#ffe080" strokeWidth={6} fill="none" opacity={0.6} />)}</svg>}
    <Horde t={t} n={8} y={FLOOR - 20} x0={60} x1={600} walk={t > b ? 0.9 : 0.2} dim={0.1} flip={false} />
    <Flash t={t} at={c} col="210,225,255" d={0.4} /></Camera>); };
const f03: S = ({t, w}) => { const al = w('callejón');
  if (t < al - 0.2) { const p = clamp(t / Math.max(0.1, al));
    return (<Camera t={t} keys={[[0, 1.0, 540, 1150]]}><Market t={t} light={0.45} />
      {[[YOU, 0], [MAMA, 150], [NINA, 230]].map(([c, d]: any, i) => <Char key={i} t={t} x={150 + p * 800 - d} y={FLOOR + 40} h={i === 2 ? 470 : 680} {...c} pose="WalkingBW" walk={1} face="Fear" seed={i * 5} />)}
    </Camera>); }
  return (<Camera t={t} keys={[[0, 1.0, 540, 1200], [w('ejército'), 1.15, 540, 1200]]}><Alley t={t} /><Truck x={560} y={1500} s={1.15} /></Camera>); };
const Flashlight: React.FC<{x: number; y: number; a?: number}> = ({x, y, a = 1}) => (
  <div style={{position: 'absolute', left: x, top: y - 160, width: 640, height: 320, background: 'radial-gradient(ellipse at 0% 50%, rgba(255,246,200,.45), rgba(255,246,200,0) 70%)',
    clipPath: 'polygon(0 45%, 100% 0, 100% 100%, 0 55%)', opacity: a}} />);
const f04: S = ({t, w}) => (<Camera t={t} keys={[[0, 1.0, 540, 1200], [w('pasas'), 1.2, 640, 1150]]}><Alley t={t} /><Truck x={880} y={1420} s={0.75} />
  <Char t={t} x={160} y={FLOOR + 60} h={700} {...SOLD} face="Serious" seed={30} /><Char t={t} x={300} y={FLOOR + 60} h={700} {...SOLD} hair="Short" face="Suspicious" seed={31} />
  <Flashlight x={230} y={1000} />
  <Char t={t} x={600} y={FLOOR + 60} h={680} {...YOU} face="Fear" flip seed={5} />
  <Char t={t} x={780} y={FLOOR + 60} h={690} {...MAMA} face="ConcernedFear" flip seed={6} />
  <Char t={t} x={900} y={FLOOR + 60} h={470} {...NINA} pose="RestingWB" face="Tired" flip seed={4} /></Camera>);
const f05: S = ({t, w}) => { const k = w('tobillo');
  if (t > k - 0.2) return (<AbsoluteFill style={{background: 'radial-gradient(circle at 50% 50%, #2a0a0c, #050304 70%)'}}>
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, transform: `scale(${1 + 0.05 * ease((t - k) / 2)})`}}>
      <path d="M430 0 L650 0 L640 1050 Q700 1180 860 1210 Q900 1300 800 1320 L430 1300 Q400 1200 440 1040 Z" fill="#d49b74" stroke="#0c0c10" strokeWidth={14} />
      <ellipse cx="560" cy="980" rx="120" ry="70" fill="#5e6e55" opacity={0.6} />
      {[0, 1, 2, 3, 4, 5].map(i => <ellipse key={i} cx={490 + i * 28} cy={970 + (i % 2) * 34} rx={13} ry={18} fill="#6a0010" />)}
      <path d="M520 1010 q6 80 -4 140 M600 1000 q4 60 -6 110" stroke="#5a5a3a" strokeWidth={8} fill="none" opacity={0.7} />
    </svg></AbsoluteFill>);
  return (<Camera t={t} keys={[[0, 1.0, 540, 1200], [w('niña'), 1.3, 760, 1250]]}><Alley t={t} />
    <Char t={t} x={300} y={FLOOR + 60} h={700} {...SOLD} pose="PointingFingerBW" face="Serious" seed={30} />
    <Char t={t} x={780} y={FLOOR + 60} h={480} {...NINA} pose="RestingWB" face="Tired" flip seed={4} /><Flashlight x={380} y={1200} /></Camera>); };
const f06: S = ({t, w}) => { const go = ramp(t, w('arranca'), 1.6);
  return (<Camera t={t} keys={[[0, 1.0, 540, 1200]]} shake={go > 0 && go < 0.3 ? 0.6 : 0}><Alley t={t} /><Truck x={600 + 900 * go} y={1450} s={1.0} />
    <Char t={t} x={420} y={FLOOR + 80} h={690} {...MAMA} face="Solemn" seed={6} /><Char t={t} x={520} y={FLOOR + 80} h={480} {...NINA} pose="RestingWB" face="EyesClosed" flip seed={4} /></Camera>); };
const f07: S = ({t, w}) => { const c = w('cabeza'), p = w('parpadea');
  if (t > p - 0.15) return <ZombieCloseup t={t} scale={0.95 + 0.08 * ease((t - p) / 2)} />;
  return (<AbsoluteFill><Camera t={t} keys={[[0, 1.0, 540, 1300], [c, 1.5, 560, 1250]]}>
    <Alley t={t} />
    <Char t={t} x={500} y={1420} h={480} {...MAMA} face="Solemn" seed={6} />
    {t < c ? <Char t={t} x={570} y={1420} h={330} {...NINA} pose="RestingWB" face="EyesClosed" flip seed={4} />
           : <Z t={t} x={570} y={1420} h={330} hair="Buns" clothes={NINA.clothes} seed={4} flip />}
  </Camera>
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}><path fillRule="evenodd" d="M0 0H1080V1920H0Z M180 520H900V1560H180Z" fill="#3a4a2c" />
      <rect x="170" y="510" width="740" height="1060" fill="none" stroke="#0c0c10" strokeWidth={14} /></svg></AbsoluteFill>); };
const f08: S = ({t}) => <Alley t={t} />;

const KEYS = ['uno', 'dos', 'tres', 'supermercado', 'muerde', 'cajera', 'piso', 'levanta', 'parpadea', 'reja', 'seis', 'veinte', 'tú', 'héctor', 'mamá', 'niña',
  'repartidor', 'vendado', 'cansan', 'no', 'medianoche', 'sangre', 'rascarse', 'frío', 'golpear', 'techo', 'trepar', 'rápidos', 'moto', 'fiebre', 'palabra',
  'raja', 'esquina', 'cede', 'campana', 'bodega', 'callejón', 'ejército', 'linterna', 'pasas', 'mordida', 'tobillo', 'nadie', 'suelta', 'sin', 'abrazadas', 'cabeza'];
const TITLE: [string, string] = ['Brote zombi en Bogotá:', 'atrapado en el supermercado'];
export const ZOMBI_SUPER: Record<number, Meta> = {
  1: {title: TITLE, badge: 'DÍA 1', keys: KEYS, audio: 'zombi_super_p1.m4a', tl: p1 as unknown as TL, scenes: {d01, d02, d03, d04, d05, d06, d07},
      endcard: ['¿QUÉ HACES?', 'La encierras en el cuarto frío', 'Le crees y se queda', 'EL DÍA 2 SALE HOY · SÍGUEME']},
  2: {title: TITLE, badge: 'DÍA 2', keys: KEYS, audio: 'zombi_super_p2.m4a', tl: p2 as unknown as TL, scenes: {e01, e02, e03, e04, e05, e06, e07},
      endcard: ['¿QUÉ HACES?', 'Te vas en la moto', 'Te quedas con ellas', 'EL FINAL SALE HOY · SÍGUEME']},
  3: {title: TITLE, badge: 'DÍA 3 · FINAL', keys: KEYS, audio: 'zombi_super_p3.m4a', tl: p3 as unknown as TL, scenes: {f01, f02, f03, f04, f05, f06, f07, f08},
      endcard: ['¿TE HABRÍAS SUBIDO?', 'Sí, al camión', 'Me quedo con ellas', 'SÍGUEME PARA MÁS HISTORIAS']},
};

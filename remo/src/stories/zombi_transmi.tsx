// «Brote zombi: atrapado en un TransMilenio» (formato trend TikTok nov-2026). Guion y voz en stories/zombi_transmi/.
import React from 'react';
import {AbsoluteFill, random} from 'remotion';
import {clamp, ease, ramp, Char, ZombieCloseup, Flash, Camera, Vignette, Meta, TL} from '../kit';
import {FLOOR, BusInside, DoorOutside, DoorFrame, Fuelle, GrayHand, CandyCart, Bundle, BusSide, Road, Portal, Reja, Truck} from '../sets';
import p1 from '../data/zombi_transmi_p1.json'; import p2 from '../data/zombi_transmi_p2.json'; import p3 from '../data/zombi_transmi_p3.json';

type S = React.FC<{t: number; w: (tok: string) => number}>;
// reparto: «tú» de amarillo
const YOU = {hair: 'ShortScratch', skin: '#c68a62', clothes: '#d9a521', pose: 'ShirtPantsBW'};
const GLORIA = {hair: 'GrayBun', skin: '#b07a52', clothes: '#2e8b57', pose: 'RestingWB', accessory: 'GlassRound'};
const POLI = {hair: 'Short', skin: '#a8704a', clothes: '#3d6b3a', pose: 'BlazerPantsBW'};
const COND = {hair: 'BaldTop', skin: '#c68a62', clothes: '#2a4a7a', pose: 'CrossedArmsWB', facialHair: 'MoustacheThin'};
const MUJER = {hair: 'Long', skin: '#d49b74', clothes: '#8a3a5a', pose: 'RestingBW'};
const SENOR = {hair: 'GrayShort', skin: '#b07a52', clothes: '#5a4a3a', pose: 'BlazerPantsWB'};
const MUCHA = {hair: 'MediumStraight', skin: '#d49b74', clothes: '#e07aa0', pose: 'ShirtPantsWB'};
const SOLD = {hair: 'BaldTop', skin: '#a8704a', clothes: '#4a5a3a', pose: 'BlazerPantsBW'};
const Z = (p: any) => <Char pose="RoboDanceOutline" zombie {...p} />;
const Radio: React.FC<{x: number; y: number}> = ({x, y}) => (<div style={{position: 'absolute', left: x, top: y, width: 34, height: 70, borderRadius: 8, background: '#15161a', border: '4px solid #0c0c10'}}>
  <div style={{position: 'absolute', left: 6, top: -40, width: 6, height: 40, background: '#15161a'}} /><div style={{position: 'absolute', left: 8, top: 10, width: 12, height: 8, background: '#ff3a2a'}} /></div>);
const Mom: React.FC<{t: number; x: number; y: number; h: number; face?: string; flip?: boolean; tilt?: number; walk?: number; dim?: number}> = ({t, x, y, h, face = 'Fear', flip, tilt = 0, walk = 0, dim = 0}) => (<>
  <Char t={t} x={x} y={y} h={h} {...MUJER} face={face} flip={flip} seed={7} tilt={tilt} walk={walk} dim={dim} />
  <div style={{filter: `brightness(${1 - dim})`}}><Bundle x={x + (flip ? -1 : 1) * h * 0.04} y={y - h * 0.58} s={h / 650} /></div></>);
const Crowd: React.FC<{t: number; n: number; y?: number; dim?: number; walk?: number}> = ({t, n, y = 1330, dim = 0.45, walk = 0}) => (<>
  {[...Array(n)].map((_, i) => <Char key={i} t={t} x={80 + random('cx' + i) * 920} y={y + random('cy' + i) * 40} h={500 + random('ch' + i) * 60}
    pose={['ShirtPantsWB', 'BlazerPantsBW', 'RestingBW', 'EasingWB'][i % 4]} hair={['Short', 'Long', 'Bun', 'Afro', 'Medium'][i % 5]}
    clothes={['#4a6fa5', '#7a4a8a', '#3b4a6b', '#8a5a3a', '#2e6f9e'][i % 5]} skin={['#c68a62', '#8a5a3a', '#d49b74'][i % 3]} face="Calm"
    flip={random('cf' + i) > 0.5} seed={40 + i} dim={dim} walk={walk} />)}</>);
const Horde: React.FC<{t: number; n: number; y?: number; dim?: number; walk?: number; x0?: number; x1?: number; h?: number}> = ({t, n, y = 1260, dim = 0.15, walk = 0, x0 = 80, x1 = 1000, h = 520}) => (<>
  {[...Array(n)].map((_, i) => <Z key={i} t={t} x={x0 + random('x' + i) * (x1 - x0)} y={y + random('y' + i) * 60} h={h + random('h' + i) * 80}
    hair={['ShortMessy', 'Medium', 'Bald', 'Long', 'Afro'][i % 5]} seed={i + 10} flip={random('f' + i) > 0.5} dim={dim} walk={walk} />)}</>);
const Flashlight: React.FC<{x: number; y: number; a?: number; rot?: number}> = ({x, y, a = 1, rot = 0}) => (
  <div style={{position: 'absolute', left: x, top: y - 160, width: 640, height: 320, background: 'radial-gradient(ellipse at 0% 50%, rgba(255,246,200,.5), rgba(255,246,200,0) 70%)',
    clipPath: 'polygon(0 45%, 100% 0, 100% 100%, 0 55%)', opacity: a, transform: `rotate(${rot}deg)`, transformOrigin: '0 50%'}} />);

// ---------------- Día 1 ----------------
const d01: S = ({t, w}) => { const k = w('muerde'), bit = t > k - 0.3;
  return (<Camera t={t} keys={[[0, 1.0, 540, 1100], [k, 1.5, 720, 1000]]} shake={t > k && t < k + 0.6 ? 1 : 0}>
    <BusInside t={t} sky="day" move={0.6} red={bit ? ramp(t, k, 0.3) : 0} />
    <Crowd t={t} n={6} />
    <Char t={t} x={850} y={FLOOR + 10} h={640} {...MUCHA} flip face={bit ? 'Fear' : 'Calm'} seed={3} tilt={bit ? 10 * ramp(t, k, 0.3) : 0} />
    {bit ? <Z t={t} x={600 + 90 * ramp(t, k - 0.3, 0.3)} y={FLOOR} h={680} hair="GrayShort" seed={1} />
         : <Char t={t} x={600} y={FLOOR} h={680} {...SENOR} face="Tired" seed={1} />}
    <Char t={t} x={340} y={FLOOR + 40} h={700} {...YOU} face={bit ? 'Awe' : 'Calm'} seed={5} />
    <Char t={t} x={110} y={FLOOR + 60} h={680} {...GLORIA} face={bit ? 'ConcernedFear' : 'Smile'} seed={6} />
    <Flash t={t} at={k} col="255,40,40" /></Camera>); };
const d02: S = ({t, w}) => { const lv = w('levanta'), rj = w('rojos'), m = w('muerde'), up = ramp(t, lv, 0.8);
  if (t > rj - 0.15 && t < m - 0.25) return <ZombieCloseup t={t} scale={1 + 0.06 * ease((t - rj) / 1.5)} />;
  if (t >= m - 0.25) return (<Camera t={t} keys={[[m - 0.3, 1.15, 540, 1100]]} shake={t < m + 0.5 ? 1 : 0}>
    <BusInside t={t} sky="day" move={0.3} red={0.6} /><Crowd t={t} n={5} walk={1} dim={0.35} />
    <Char t={t} x={700} y={FLOOR + 20} h={680} pose="BlazerPantsWB" hair="Afro" skin="#8a5a3a" clothes="#3b4a6b" face="Fear" flip seed={12} tilt={12} />
    <Z t={t} x={520} y={FLOOR} h={660} hair="MediumStraight" clothes={MUCHA.clothes} seed={3} />
    <Flash t={t} at={m} col="255,30,30" /></Camera>);
  return (<Camera t={t} keys={[[0, 1.2, 600, 1300], [lv, 1.3, 600, 1200]]}>
    <BusInside t={t} sky="day" move={0.2} light={0.85} /><Crowd t={t} n={7} y={1380} dim={0.3} />
    <div style={{position: 'absolute', inset: 0, transformOrigin: `620px ${FLOOR}px`, transform: `rotate(${-90 * (1 - up)}deg)`}}>
      <Char t={t} x={620} y={FLOOR} h={640} pose={up > 0 ? 'RoboDanceOutline' : MUCHA.pose} hair={MUCHA.hair} zombie={up > 0} skin={MUCHA.skin} clothes={MUCHA.clothes} face="EyesClosed" seed={3} flip />
    </div>
    <Char t={t} x={260} y={FLOOR + 40} h={700} {...YOU} face="Fear" seed={5} /></Camera>); };
const d03: S = ({t, w}) => { const f = w('frena'), at = w('atrás');
  if (t < at - 0.3) { const sp = 1 - ramp(t, f - 0.2, 0.6);
    return (<Camera t={t} keys={[[0, 1.4, 540, 1920]]} shake={t > f && t < f + 0.7 ? 1 : 0}><Road t={t} move={sp} />
      <BusSide x={540 + Math.sin(t * 20) * 3 * sp} y={1660} s={0.86} rot={t > f && t < f + 0.8 ? 2.5 * Math.sin((t - f) * 8) : 0} />
      <Flash t={t} at={f} col="255,60,40" d={0.3} /></Camera>); }
  return (<Camera t={t} keys={[[at - 0.3, 1.0, 540, 1100], [w('contigo'), 1.3, 300, 1150]]}><Fuelle t={t} eyes={1} light={0.8} />
    <Char t={t} x={190} y={FLOOR + 60} h={760} {...YOU} face="Fear" seed={5} />
    <Char t={t} x={900} y={FLOOR + 60} h={740} {...POLI} face="ConcernedFear" flip seed={9} /><Vignette a={0.5} /></Camera>); };
const d04: S = ({t, w}) => { const cast: [any, string, number, string][] = [[YOU, 'tú', 150, 'Calm'], [GLORIA, 'gloria', 370, 'Smile'], [POLI, 'policía', 760, 'Serious'], [COND, 'conductor', 950, 'Concerned']];
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150], [w('radio'), 1.35, 860, 1100]]}><BusInside t={t} light={0.75} />
    {cast.map(([c, tok, x, face], i) => { const k = w(tok); if (t < k - 0.3) return null; const a = ramp(t, k - 0.3, 0.45);
      return <Char key={i} t={t} x={x - 150 * (1 - a)} y={FLOOR + 40} h={680} {...c} walk={1 - a} face={face} flip={i === 3} seed={i * 4} />; })}
    {t > w('gloria') - 0.3 && <CandyCart x={560 - 150 * (1 - ramp(t, w('gloria') - 0.3, 0.45))} y={FLOOR + 40} s={0.8} />}
    {t > w('conductor') - 0.1 && <Radio x={870} y={FLOOR + 40 - 680 * 0.6} />}
  </Camera>); };
const d05: S = ({t, w}) => { const tr = w('trancan'), ar = w('arañar'), sc = t > ar ? Math.abs(Math.sin(t * 7)) : 0;
  return (<Camera t={t} keys={[[0, 1.0, 540, 1050], [ar, 1.3, 560, 900]]} shake={sc * 0.25}><Fuelle t={t} shake={sc * 0.5} eyes={t > ar ? 1 : 0} light={0.8} />
    {t > ar && [0, 1, 2].map(i => <div key={i} style={{position: 'absolute', left: 470 + i * 40, top: 760 + i * 10, width: 8, height: 160 * ramp(t, ar + i * 0.15, 0.3), background: '#c41a1a', transform: 'rotate(14deg)', opacity: 0.8}} />)}
    <CandyCart x={150 + 390 * ramp(t, tr - 0.2, 0.8)} y={FLOOR + 60} s={1.3} />
    <Char t={t} x={120} y={FLOOR + 80} h={720} {...YOU} face={t > ar ? 'Fear' : 'Concerned'} seed={5} />
    <Char t={t} x={960} y={FLOOR + 80} h={690} {...GLORIA} face={t > ar ? 'ConcernedFear' : 'Serious'} flip seed={6} />
    {t > ar && <Vignette a={0.55} col="60,0,0" />}</Camera>); };
const DoorScene: React.FC<{t: number; hordeT: number; knock?: boolean}> = ({t, hordeT, knock = true}) => { const kn = knock ? Math.max(0, Math.sin(t * 9)) : 0;
  return (<><DoorOutside t={t} />
    {t > hordeT && <Horde t={t} n={9} y={1240} h={300 + 160 * ramp(t, hordeT, 6)} x0={60} x1={1020} walk={0.6} dim={0.35} />}
    <Mom t={t} x={540} y={1560} h={920} face="Fear" tilt={kn * 3} />
    <DoorFrame t={t} light={0.7} /></>); };
const d06: S = ({t, w}) => { const g = w('golpea'), hd = w('horda');
  return (<Camera t={t} keys={[[0, 1.0, 540, 1050], [hd, 1.15, 540, 1000]]} shake={t > g && t < hd ? 0.25 * Math.max(0, Math.sin(t * 9)) : 0}>
    <DoorScene t={t} hordeT={hd - 0.3} knock={t > g} /><Flash t={t} at={hd} col="255,40,40" d={0.3} /></Camera>); };
const d07: S = ({t}) => <DoorScene t={t} hordeT={0} />;

// ---------------- Día 2 ----------------
const e01: S = ({t, w}) => { const ab = w('abriste'), en = w('entran'), c = w('centímetro');
  const open = ramp(t, ab - 0.2, 0.6) * (1 - ramp(t, c - 0.7, 0.6)); const inn = ramp(t, en - 0.2, 1.3);
  return (<Camera t={t} keys={[[0, 1.0, 540, 1050], [c, 1.2, 540, 950]]} shake={t > c && t < c + 0.6 ? 1 : 0}>
    <DoorOutside t={t} />
    <Horde t={t} n={9} y={1250 + 150 * ramp(t, 0, c)} h={380 + 500 * ramp(t, 0, c)} x0={100} x1={980} walk={0.9} dim={0.25} />
    {t > c - 0.1 && <Z t={t} x={540} y={1950} h={1400} hair="ShortMessy" seed={31} />}
    {inn < 0.75 && <Mom t={t} x={540 + 200 * inn} y={1560 + 400 * inn} h={920 + 700 * inn} face="Fear" walk={inn > 0 ? 1 : 0} />}
    <DoorFrame t={t} open={open} light={0.7} />
    {inn >= 0.75 && inn < 1 && <Mom t={t} x={540 + 200 * inn} y={1560 + 400 * inn} h={920 + 700 * inn} face="Fear" walk={1} />}
    <Flash t={t} at={c} col="255,40,40" /></Camera>); };
const e02: S = ({t, w}) => { const mi = w('miran'), sa = w('sacudir'), rock = t > sa ? 2.2 * Math.sin(t * 6) : 0;
  if (t > mi - 0.1 && t < mi + 1.1) return <ZombieCloseup t={t} scale={1.0 + 0.05 * ease((t - mi) / 1.2)} />;
  return (<AbsoluteFill style={{transform: `rotate(${rock}deg) scale(1.08)`}}><Camera t={t} keys={[[0, 1.0, 540, 1000]]} shake={t > sa ? 0.5 : 0}>
    <DoorOutside t={t} />
    {[...Array(8)].map((_, i) => <Z key={i} t={t} x={280 + (i % 4) * 170 + (i > 3 ? 80 : 0)} y={i > 3 ? 2140 : 1720} h={1250} hair={['ShortMessy', 'Long', 'Bald', 'Afro'][i % 4]} seed={50 + i} flip={i % 2 === 1} dim={i > 3 ? 0.1 : 0.3} />)}
    <DoorFrame t={t} light={0.6} /></Camera></AbsoluteFill>); };
const e03: S = ({t, w}) => { const pk = w('parpadean'), fl = t > pk - 0.1 ? (random('fl' + Math.floor(t * 10)) > 0.45 ? 0.85 : 0.15) : 0.75;
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150], [w('mudo'), 1.3, 830, 1100], [w('batería'), 1.0, 540, 1150]]}><BusInside t={t} sky="dawn" light={fl} />
    <Char t={t} x={130} y={FLOOR + 40} h={690} {...YOU} face="Tired" seed={5} />
    <Char t={t} x={340} y={FLOOR + 40} h={670} {...GLORIA} face="Tired" seed={6} />
    <Mom t={t} x={570} y={FLOOR + 40} h={680} face="Concerned" />
    <Char t={t} x={850} y={FLOOR + 40} h={690} {...COND} face="Concerned" flip seed={8} /><Radio x={770} y={FLOOR + 40 - 690 * 0.6} />
    <div style={{position: 'absolute', inset: 0, background: '#000', opacity: 0.5 * (1 - fl)}} /></Camera>); };
const e04: S = ({t, w}) => { const po = w('portal');
  if (t > po - 0.2) return (<Camera t={t} keys={[[po - 0.2, 1.0, 540, 1200], [w('ejército'), 1.2, 540, 1150]]}><Portal t={t} />
    <Truck x={700} y={1500} s={0.9} />
    {[0, 1, 2].map(i => <Char key={i} t={t} x={170 + i * 150} y={FLOOR + 60} h={560} {...SOLD} hair={['BaldTop', 'Short', 'Bald'][i]} face="Serious" seed={30 + i} />)}
    <Vignette a={0.4} /></Camera>);
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150], [w('arrancamos'), 1.25, 420, 1100]]}><BusInside t={t} sky="dawn" light={0.6} />
    <Char t={t} x={380} y={FLOOR + 40} h={720} {...COND} pose="PointingFingerWB" face="Driven" seed={8} />
    <Char t={t} x={800} y={FLOOR + 40} h={700} {...YOU} face="Concerned" flip seed={5} /></Camera>); };
const e05: S = ({t, w}) => { const r = w('rasgando');
  return (<Camera t={t} keys={[[0, 1.0, 540, 1100], [r, 1.25, 600, 950]]}><Fuelle t={t} tear={0.35 * ramp(t, r - 0.2, 1.5)} eyes={t > r ? 1 : 0} light={0.6} shake={t > r ? 0.3 : 0} />
    <CandyCart x={540} y={FLOOR + 60} s={1.3} />
    <Char t={t} x={160} y={FLOOR + 80} h={760} {...YOU} face="Fear" seed={5} />
    <Char t={t} x={930} y={FLOOR + 80} h={720} {...GLORIA} face="ConcernedFear" flip seed={6} /><Vignette a={0.5} col="40,0,0" /></Camera>); };
const e06: S = ({t, w}) => { const mi = w('mirar'), ho = w('hueco'), ag = w('agarra'), ap = ramp(t, 0, Math.max(0.5, mi));
  if (t > ag - 0.1) return <AbsoluteFill><ZombieCloseup t={t} scale={1.02 + 0.06 * ease((t - ag) / 1.5)} /><Flash t={t} at={ag} col="255,30,30" /></AbsoluteFill>;
  return (<Camera t={t} keys={[[0, 1.0, 540, 1100], [ho, 1.35, 520, 950]]}><Fuelle t={t} tear={0.35} eyes={1} light={0.55} />
    <Char t={t} x={160 + 230 * ap} y={FLOOR + 80} h={780} {...YOU} face={t > ho ? 'Fear' : 'Concerned'} walk={ap < 1 ? 1 : 0} seed={5} />
    {t > ho - 0.4 && <GrayHand t={t} x={600} y={900} s={0.9} rot={150} reach={ramp(t, ho - 0.4, 0.9)} />}
    <Vignette a={0.55} col="40,0,0" /></Camera>); };
const e07: S = ({t}) => (<AbsoluteFill><Fuelle t={t} tear={0.4} eyes={1} light={0.5} /><GrayHand t={t} x={600} y={900} s={0.9} rot={150} reach={1} /></AbsoluteFill>);

// ---------------- Día 3 ----------------
const ArmClose: React.FC<{t: number; k: number; scratch?: number}> = ({t, k, scratch = 1}) => (
  <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 50%, #1c2230, #05060a 70%)'}}>
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, transform: `scale(${1 + 0.05 * ease((t - k) / 2)})`}}>
      <path d="M-40 820 L420 820 L420 1120 L-40 1120 Z" fill="#d9a521" stroke="#0c0c10" strokeWidth={14} />
      <path d="M420 840 L930 880 Q1040 900 1050 980 Q1040 1070 930 1080 L420 1100 Z" fill="#c68a62" stroke="#0c0c10" strokeWidth={14} />
      <g opacity={scratch}>
        {[0, 1, 2].map(i => <path key={i} d={`M${560 + i * 40} ${900 + i * 6} L${700 + i * 40} ${1050 + i * 6}`} stroke="#5f6f5a" strokeWidth={16} strokeLinecap="round" />)}
        {[0, 1, 2, 3, 4].map(i => <path key={'v' + i} d={`M${600 + i * 30} ${960 + (i % 2) * 40} q${-40 - i * 10} ${30} ${-90 - i * 20} ${10 + i * 8}`} stroke="#4f5f4a" strokeWidth={5} fill="none" opacity={0.8} />)}
        <ellipse cx={640} cy={980} rx={170} ry={120} fill="#7f9479" opacity={0.25} />
      </g>
    </svg>
    <Flashlight x={-60} y={980} a={0.9} /></AbsoluteFill>);
const f01: S = ({t, w}) => { const cr = w('crees'), ar = w('arranca');
  if (t > ar - 0.2) return (<Camera t={t} keys={[[0, 1.4, 540, 1920]]} shake={0.35}><Road t={t} move={1.6} />
    <BusSide x={540 + Math.sin(t * 25) * 6} y={1700} s={0.86} />
    {t < ar + 0.4 && <Flash t={t} at={ar - 0.2} col="255,255,255" d={0.3} />}</Camera>);
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150], [cr, 1.9, 560, 1080]]}><BusInside t={t} light={0.55} />
    <Char t={t} x={540} y={FLOOR + 40} h={760} {...YOU} face={t > cr ? 'ConcernedFear' : 'Concerned'} seed={5} tilt={t > cr ? -6 : 0} />
    {t > cr && <div style={{position: 'absolute', left: 520, top: 1060, width: 90, height: 90, borderRadius: 45, background: 'radial-gradient(rgba(120,150,110,.7), rgba(120,150,110,0) 70%)'}} />}
    <Vignette a={0.5} /></Camera>); };
const thump = (t: number, t0: number) => t > t0 ? Math.max(0, Math.sin((t - t0) * 7.5)) ** 6 : 0;
const f02: S = ({t, w}) => { const at = w('atropella'), es = w('espalda'), th = thump(t, at - 0.1);
  return (<Camera t={t} keys={[[0, 1.0, 540, 1100], [es, 1.15, 560, 1050]]} shake={th}><Fuelle t={t} tear={0.45 + 0.15 * ramp(t, at, 3)} eyes={1} light={0.55} shake={th} />
    {t < es - 0.3 && <GrayHand t={t} x={620} y={880} s={0.8} rot={160} reach={0.8} />}
    {t > es - 0.6 && <Char t={t} x={250 + 330 * ramp(t, es - 0.6, 0.7)} y={FLOOR + 40} h={820} {...GLORIA} pose="CrossedArmsWB" face="Driven" flip seed={6} walk={1 - ramp(t, es - 0.6, 0.7)} />}
    {t > es + 0.3 && [[380, 820, 200], [800, 760, -20]].map(([x, y, r], i) => <GrayHand key={i} t={t} x={x} y={y} s={0.55} rot={r} reach={ramp(t, es + 0.3 + i * 0.3, 0.6)} />)}
    <Char t={t} x={140} y={FLOOR + 90} h={760} {...YOU} face="Fear" seed={5} />
    <Vignette a={0.55} col="40,0,0" /></Camera>); };
const f03: S = ({t, w}) => { const ro = w('rompe');
  if (t > ro - 0.15) return (<Camera t={t} keys={[[ro - 0.15, 1.2, 540, 1000], [ro + 0.6, 1.0, 540, 1100]]} shake={t < ro + 0.8 ? 1 : 0.3}>
    <Fuelle t={t} tear={1} eyes={0} light={0.5} />
    {[0, 1, 2].map(i => <Z key={i} t={t} x={420 + i * 130} y={1350 + 250 * ramp(t, ro - 0.1 + i * 0.15, 0.6)} h={620 + 260 * ramp(t, ro - 0.1 + i * 0.15, 0.6)} hair={['ShortMessy', 'Long', 'Bald'][i]} seed={60 + i} flip={i === 2} />)}
    <Flash t={t} at={ro - 0.15} col="255,40,40" d={0.35} /></Camera>);
  return (<Camera t={t} keys={[[0, 1.0, 540, 1200], [w('cien'), 1.45, 640, 1250]]} shake={0.3}><Portal t={t} /><Truck x={700} y={1500} s={0.8} />
    {[0, 1].map(i => <Char key={i} t={t} x={260 + i * 160} y={FLOOR + 40} h={520} {...SOLD} hair={['BaldTop', 'Short'][i]} face="Serious" seed={30 + i} />)}
    <Reja y0={1100} y1={1560} /><Vignette a={0.6} /></Camera>); };
const f04: S = ({t, w}) => { const en = w('encima'), al = w('alcanza');
  if (t > al - 0.25) { const red = 0.5 + 0.1 * Math.sin(t * 4);
    return (<Camera t={t} keys={[[al - 0.25, 1.0, 540, 900], [al + 2, 1.15, 540, 820]]}><AbsoluteFill style={{background: 'radial-gradient(circle at 50% 40%, #3a1418, #070203 70%)'}} />
      <Char t={t} x={560} y={2500} h={2200} {...GLORIA} face="Solemn" seed={6} tilt={-8} />
      <GrayHand t={t} x={-40} y={1300} s={1.0} rot={-20} reach={1} /><GrayHand t={t} x={1120} y={1150} s={0.9} rot={200} reach={1} />
      <Vignette a={red} col="80,0,0" /></Camera>); }
  if (t > en - 0.1) return <AbsoluteFill><ZombieCloseup t={t} scale={1.04 + 0.05 * ease((t - en) / 1.2)} /><Flash t={t} at={en - 0.1} col="255,20,20" /></AbsoluteFill>;
  return (<Camera t={t} keys={[[0, 1.0, 540, 1100], [en, 1.3, 560, 1050]]} shake={0.6}><Fuelle t={t} tear={1} light={0.45} />
    <Char t={t} x={560} y={FLOOR + 40} h={820} {...GLORIA} pose="CrossedArmsWB" face="Fear" flip seed={6} tilt={-10 * ramp(t, 0, en)} />
    {[0, 1, 2].map(i => <Z key={i} t={t} x={430 + i * 140} y={1400 + 60 * ramp(t, 0, en)} h={700} hair={['ShortMessy', 'Long', 'Bald'][i]} seed={60 + i} tilt={14 - i * 14} />)}
    <Vignette a={0.6} col="60,0,0" /></Camera>); };
const f05: S = ({t, w}) => { const es = w('estrella'), co = w('conductor'), po = w('policía');
  if (t < co - 0.3) { const p = ramp(t, 0, Math.max(0.3, es)), x = -500 + 900 * p;
    return (<Camera t={t} keys={[[0, 1.0, 540, 1300]]} shake={t > es && t < es + 0.8 ? 1.2 : 0.2}><Portal t={t} />
      <BusSide x={x} y={1640} s={0.8} rot={t > es ? -2.5 : 0} />
      <Reja y0={1050} y1={1640} bent={ramp(t, es, 0.2)} dx={0} />
      <Flash t={t} at={es} col="255,240,220" d={0.4} /></Camera>); }
  const pull = ramp(t, po, 1.6);
  return (<Camera t={t} keys={[[co - 0.3, 1.3, 330, 1150], [po, 1.0, 540, 1150]]}><BusInside t={t} light={0.35} red={0.35} />
    <div style={{position: 'absolute', inset: 0, transformOrigin: `340px ${FLOOR}px`, transform: 'rotate(-24deg)'}}>
      <Char t={t} x={340} y={FLOOR} h={600} {...COND} pose="ClosedLegWB" face="EyesClosed" seed={8} /></div>
    {t > po - 0.4 && <><Char t={t} x={620 + 320 * pull} y={FLOOR + 40} h={720} {...POLI} pose="WalkingBW" face="Driven" walk={1} seed={9} />
      <Char t={t} x={470 + 320 * pull} y={FLOOR + 40} h={700} {...YOU} pose="WalkingBW" face="Fear" walk={1} seed={5} /></>}
    <Vignette a={0.5} /></Camera>); };
const f06: S = ({t, w}) => { const ra = w('rasguño');
  if (t > ra - 0.2) return <ArmClose t={t} k={ra} scratch={ramp(t, ra - 0.2, 0.3)} />;
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150], [w('brazo'), 1.35, 640, 1100]]}><Portal t={t} />
    <Char t={t} x={230} y={FLOOR + 60} h={740} {...SOLD} pose="PointingFingerBW" face="Serious" seed={30} />
    <Flashlight x={330} y={1100} rot={4} />
    <Char t={t} x={760} y={FLOOR + 60} h={720} {...YOU} face="Fear" flip seed={5} />
    <Vignette a={0.45} /></Camera>); };
const f07: S = ({t, w}) => { const su = w('suben'), re = w('reja'), na = w('nada'), go = ramp(t, re + 0.2, 3.5), turned = t > na - 0.2;
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150], [re, 1.0, 540, 1150], [na, 1.6, 400, 1000]]} shake={turned && t < na + 0.6 ? 0.8 : 0}>
    <Portal t={t} />
    <Truck x={900 + 800 * go} y={1380} s={0.75} lights={1} />
    {t < su + 1.2 && <>
      <Char t={t} x={640 + 260 * ramp(t, su - 0.4, 1.4)} y={1390} h={460} {...POLI} pose="WalkingBW" face="Solemn" walk={1} seed={9} dim={0.2} />
      <Mom t={t} x={760 + 240 * ramp(t, su - 0.4, 1.4)} y={1390} h={450} face="Solemn" walk={1} dim={0.2} /></>}
    {turned ? <Z t={t} x={400} y={FLOOR + 160} h={980} hair={YOU.hair} clothes={YOU.clothes} seed={5} />
            : <Char t={t} x={400} y={FLOOR + 160} h={980} {...YOU} face={t > re ? 'Solemn' : 'Fear'} seed={5} tilt={t > re ? -4 : 0} />}
    <Reja y0={880} y1={1720} />
    <Flash t={t} at={na - 0.2} col="255,30,30" d={0.5} />
    {turned && <Vignette a={0.6} col="80,0,0" />}</Camera>); };
const f08: S = ({t}) => (<AbsoluteFill><Portal t={t} /><Z t={t} x={540} y={FLOOR + 160} h={980} hair={YOU.hair} clothes={YOU.clothes} seed={5} /><Reja y0={880} y1={1720} /></AbsoluteFill>);

const KEYS = ['uno', 'dos', 'tres', 'transmilenio', 'muerde', 'muchacha', 'cae', 'levanta', 'rojos', 'frena', 'puertas', 'atrás', 'contigo', 'tú', 'gloria', 'dulces',
  'policía', 'conductor', 'radio', 'fuelle', 'caucho', 'carrito', 'arañar', 'medianoche', 'bebé', 'vidrio', 'horda', 'abriste', 'centímetro', 'cuarenta',
  'sacudir', 'mudo', 'batería', 'parpadean', 'portal', 'ejército', 'rasgando', 'mano', 'gris', 'brazo', 'agarra', 'soltaste', 'crees', 'velocidad', 'atropella',
  'espalda', 'cien', 'rompe', 'encima', 'corra', 'estrella', 'reja', 'mueve', 'rasguño', 'camión', 'nada'];
const TITLE: [string, string] = ['Brote zombi en Bogotá:', 'atrapado en un TransMilenio'];
export const ZOMBI_TRANSMI: Record<number, Meta> = {
  1: {title: TITLE, badge: 'DÍA 1', keys: KEYS, audio: 'zombi_transmi_p1.m4a', tl: p1 as unknown as TL, scenes: {d01, d02, d03, d04, d05, d06, d07},
      endcard: ['¿QUÉ HACES?', 'Abres la puerta', 'La dejas cerrada', 'EL DÍA 2 SALE HOY · SÍGUEME']},
  2: {title: TITLE, badge: 'DÍA 2', keys: KEYS, audio: 'zombi_transmi_p2.m4a', tl: p2 as unknown as TL, scenes: {e01, e02, e03, e04, e05, e06, e07},
      endcard: ['¿QUÉ HACES?', 'Le gritas que arranque', 'Tapas el hueco', 'EL FINAL SALE HOY · SÍGUEME']},
  3: {title: TITLE, badge: 'DÍA 3 · FINAL', keys: KEYS, audio: 'zombi_transmi_p3.m4a', tl: p3 as unknown as TL, scenes: {f01, f02, f03, f04, f05, f06, f07, f08},
      endcard: ['¿HABRÍAS ABIERTO?', 'Sí, abro la puerta', 'No, la dejo cerrada', 'SÍGUEME PARA MÁS HISTORIAS']},
};

// Piloto: «Brote zombi: atrapado en el supermercado» — Día 1, con el motor nuevo (Remotion + Open Peeps).
import React from 'react';
import {AbsoluteFill, Audio, staticFile, random} from 'remotion';
import tl from './data/p1.json';
import {W, H, useT, clamp, ease, ramp, wordTime, Char, ZombieCloseup, Grain, Vignette, Flash, Camera, TL} from './kit';

const TLX = tl as unknown as TL;
const w = (sc: string, tok: string) => wordTime(TLX, sc, tok);
const FLOOR = 1500;
const KEY = new Set(['uno', 'supermercado', 'muerde', 'cajera', 'piso', 'levanta', 'parpadea', 'reja', 'seis', 'veinte', 'tu', 'hector',
  'mama', 'nina', 'repartidor', 'vendado', 'cansan', 'no', 'medianoche', 'sangre', 'rascarse', 'frio', 'a', 'b', 'comenta', 'sigueme']);
const norm = (s: string) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-zñ0-9]/g, '');

// reparto (Open Peeps): «tú» con gorro amarillo
const YOU = {hair: 'ShortScratch', skin: '#c68a62', clothes: '#d9a521', pose: 'ShirtPantsBW'};
const HECTOR = {hair: 'Bald', skin: '#b07a52', clothes: '#e6e1d6', pose: 'CrossedArmsWB', facialHair: 'Full'};
const MAMA = {hair: 'Long', skin: '#d49b74', clothes: '#4a6fa5', pose: 'RestingWB'};
const NINA = {hair: 'Buns', skin: '#d49b74', clothes: '#e07aa0', pose: 'WalkingWB'};
const REPA = {hair: 'HatHip', skin: '#8a5a3a', clothes: '#e8702a', pose: 'EasingWB'};
const MUCHA = {hair: 'MediumStraight', skin: '#c68a62', clothes: '#7a4a8a', pose: 'RestingBW'};
const CAJERA = {hair: 'Bun', skin: '#c68a62', clothes: '#c0392b', pose: 'ShirtPantsWB'};

// ---------------- escenario: supermercado en perspectiva ----------------
const Market: React.FC<{t: number; light?: number; red?: number}> = ({t, light = 1, red = 0}) => {
  const tubes = [0, 1, 2, 3].map(i => {
    const on = (Math.floor(t * 7 + i * 5) % 13 === 0) ? 0.25 : 0.85 + 0.15 * Math.sin(t * 50 + i);
    return on * light;
  });
  const shelf = (side: number) => [...Array(5)].map((_, r) => (
    <g key={side + 'r' + r}>
      {[...Array(9)].map((_, j) => {
        const col = ['#b03a2e', '#d4a017', '#2e6f9e', '#2e8b57', '#d9822b', '#7d3c98', '#cfd6d8'][(j + r * 2 + side) % 7];
        const x0 = side < 0 ? 40 + j * 34 : 760 + j * 34;
        return <rect key={j} x={x0} y={560 + r * 150 - 70} width={28} height={70} fill={col} opacity={0.85} />;
      })}
      <rect x={side < 0 ? 30 : 750} y={560 + r * 150} width={320} height={12} fill="#6b7280" />
    </g>));
  return (
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
      <defs>
        <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2b303b" /><stop offset="1" stopColor="#171a21" /></linearGradient>
        <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2a2d34" /><stop offset="1" stopColor="#0d0f13" /></linearGradient>
        <radialGradient id="tube"><stop offset="0" stopColor="#e8f0ff" stopOpacity="0.55" /><stop offset="1" stopColor="#e8f0ff" stopOpacity="0" /></radialGradient>
        <filter id="blur6"><feGaussianBlur stdDeviation="6" /></filter>
      </defs>
      <rect width="1080" height="1920" fill="url(#wall)" />
      <rect y="1250" width="1080" height="670" fill="url(#floor)" />
      {[...Array(13)].map((_, i) => <line key={i} x1={i * 90 - 60} y1={1920} x2={540 + (i - 6) * 26} y2={1250} stroke="#33373f" strokeWidth={3} />)}
      <g filter="url(#blur6)" opacity={0.9}>{shelf(-1)}{shelf(1)}
        <rect x="30" y="420" width="320" height="830" fill="#3a3f4a" opacity={0.35} /><rect x="750" y="420" width="320" height="830" fill="#3a3f4a" opacity={0.35} />
      </g>
      <rect x="360" y="380" width="360" height="70" rx="8" fill="#b8241c" /><text x="540" y="430" fill="#fff" fontFamily="Montserrat" fontWeight={900} fontSize="40" textAnchor="middle">SUPERMERCADO</text>
      {tubes.map((a, i) => (<g key={i}>
        <rect x={140 + i * 230} y={250} width={180} height={18} rx={6} fill={`rgba(240,246,255,${0.3 + 0.7 * a})`} />
        <ellipse cx={230 + i * 230} cy={300} rx={260} ry={220} fill="url(#tube)" opacity={a} />
      </g>))}
      <ellipse cx="540" cy="1520" rx="520" ry="90" fill="#000" opacity={0.35} />
      {red > 0 && <rect width="1080" height="1920" fill="#ff0010" opacity={0.18 * red} />}
      <rect width="1080" height="1920" fill="#000" opacity={0.55 * (1 - light)} />
    </svg>);
};
const Counter: React.FC<{x: number}> = ({x}) => (
  <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
    <rect x={x} y={FLOOR - 260} width={420} height={260} rx={10} fill="#4b5260" stroke="#0c0c10" strokeWidth={8} />
    <rect x={x} y={FLOOR - 280} width={420} height={30} fill="#6b7280" stroke="#0c0c10" strokeWidth={6} />
    <rect x={x + 290} y={FLOOR - 390} width={100} height={110} fill="#1f232b" stroke="#0c0c10" strokeWidth={6} />
    <rect x={x + 300} y={FLOOR - 380} width={80} height={60} fill="#5ad0ff" />
  </svg>);
const Gate: React.FC<{t: number; down: number; shake: number}> = ({t, down, shake}) => {
  const h = 1150 * down, dx = Math.sin(t * 40) * 8 * shake;
  return (<svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, transform: `translateX(${dx}px)`}}>
    {[...Array(31)].map((_, i) => <line key={i} x1={i * 36} y1={250} x2={i * 36} y2={250 + h} stroke="#9aa0aa" strokeWidth={7} />)}
    {[...Array(Math.floor(h / 70) + 1)].map((_, j) => <line key={'h' + j} x1={0} y1={250 + j * 70} x2={1080} y2={250 + j * 70} stroke="#b4b9c2" strokeWidth={6} />)}
    <rect x={0} y={250 + h - 20} width={1080} height={26} fill="#c8ccd4" stroke="#0c0c10" strokeWidth={4} />
  </svg>);
};

// ---------------- escenas ----------------
const D01: React.FC<{t: number}> = ({t}) => {
  const k = w('d01', 'muerde');
  const bit = t > k - 0.35;
  return (<Camera t={t} keys={[[0, 1.0, 540, 1100], [k, 1.55, 700, 1060]]} shake={t > k && t < k + 0.6 ? 1 : 0}>
    <Market t={t} red={bit ? ramp(t, k, 0.3) : 0} />
    <Counter x={600} />
    <Char t={t} x={880} y={FLOOR - 40} h={560} {...CAJERA} flip face={bit ? 'Fear' : 'Calm'} seed={3} tilt={bit ? -8 * ramp(t, k, 0.3) : 0} />
    {bit ? <Char t={t} x={640 + 70 * ramp(t, k - 0.35, 0.3)} y={FLOOR} h={640} pose="RoboDanceOutline" hair="GrayBun" zombie seed={1} />
         : <Char t={t} x={640} y={FLOOR} h={640} pose="RestingBW" hair="GrayBun" skin="#d49b74" clothes="#7b5a8a" face="Tired" seed={1} />}
    <Char t={t} x={380} y={FLOOR + 30} h={680} {...YOU} face={bit ? 'Awe' : 'Calm'} seed={5} />
    <Char t={t} x={140} y={FLOOR + 50} h={680} {...MAMA} face={bit ? 'ConcernedFear' : 'Smile'} seed={6} />
    <Flash t={t} at={k} col="255,40,40" />
  </Camera>);
};
const D02: React.FC<{t: number}> = ({t}) => {
  const up = ramp(t, w('d02', 'levanta'), 0.9), pk = w('d02', 'parpadea');
  if (t > pk - 0.15) return <ZombieCloseup t={t} k={1} scale={1 + 0.06 * ease((t - pk) / 1.5)} />;
  return (<Camera t={t} keys={[[0, 1.1, 600, 1250], [w('d02', 'levanta'), 1.35, 720, 1250]]}>
    <Market t={t} light={0.75} />
    <Counter x={620} />
    <div style={{position: 'absolute', inset: 0, transformOrigin: `760px ${FLOOR}px`, transform: `rotate(${-90 * (1 - up)}deg)`}}>
      <Char t={t} x={760} y={FLOOR} h={620} pose={up > 0 ? 'RoboDanceOutline' : 'ShirtPantsWB'} hair="Bun" zombie={up > 0} skin={CAJERA.skin} clothes={CAJERA.clothes} face="EyesClosed" seed={3} flip />
    </div>
    <Char t={t} x={300} y={FLOOR + 30} h={680} {...YOU} face="Fear" seed={5} />
  </Camera>);
};
const D03: React.FC<{t: number}> = ({t}) => {
  const g = w('d03', 'golpe'), v = w('d03', 'veinte');
  const down = ramp(t, g - 0.5, 0.45), n = t < v ? 5 : 14;
  return (<Camera t={t} keys={[[0, 1.0, 540, 1000], [v, 1.25, 540, 900]]} shake={t > g && t < g + 0.5 ? 1 : 0}>
    <AbsoluteFill style={{background: 'linear-gradient(#07080c,#141821)'}} />
    {[...Array(n)].map((_, i) => (<Char key={i} t={t} x={80 + random('x' + i) * 920} y={1260 + random('y' + i) * 80} h={520 + random('h' + i) * 80}
      pose="RoboDanceOutline" hair={['ShortMessy', 'Medium', 'Bald', 'Long', 'Afro'][i % 5]} zombie seed={i + 10} flip={random('f' + i) > 0.5} dim={0.15} />))}
    <Gate t={t} down={down} shake={t > g ? 0.6 + 0.4 * Math.abs(Math.sin(t * 9)) : 0} />
    {[[YOU, 150], [HECTOR, 330], [MAMA, 510], [NINA, 650], [REPA, 800], [MUCHA, 960]].map(([c, x]: any, i) => (
      <Char key={'p' + i} t={t} x={x} y={1800} h={i === 3 ? 470 : 660} {...c} face="ConcernedFear" flip seed={20 + i} />))}
    <Vignette a={0.6} />
  </Camera>);
};
const D04: React.FC<{t: number}> = ({t}) => {
  const cast: [any, string, number, number][] = [[YOU, 'tu', 150, 680], [HECTOR, 'hector', 330, 700], [MAMA, 'mama', 500, 680], [NINA, 'nina', 630, 470], [REPA, 'repartidor', 800, 680], [MUCHA, 'muchacha', 960, 670]];
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150]]}>
    <Market t={t} light={0.7} />
    {cast.map(([c, tok, x, h], i) => {
      const k = w('d04', tok); if (t < k - 0.3) return null;
      const a = ramp(t, k - 0.3, 0.45);
      return <Char key={i} t={t} x={x - 160 * (1 - a)} y={FLOOR + 40} h={h} {...c} walk={1 - a}
        face={i === 5 ? 'Concerned' : i === 1 ? 'Serious' : i === 3 ? 'Cute' : 'Calm'} seed={i * 4} />;
    })}
    {t > w('d04', 'vendado') && <div style={{position: 'absolute', left: 900, top: 1150, width: 160, height: 160, borderRadius: 80,
      background: 'radial-gradient(rgba(255,30,30,.55),rgba(255,0,0,0))'}} />}
  </Camera>);
};
const D05: React.FC<{t: number}> = ({t}) => {
  const off = clamp((t - w('d05', 'apaga')) / 0.25), ad = w('d05', 'adentro');
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150], [ad, 1.4, 360, 1000]]}>
    <Market t={t} light={1 - 0.8 * off} />
    <Char t={t} x={360} y={FLOOR + 40} h={720} {...HECTOR} pose="PointingFingerWB" face="Driven" seed={2} />
    <Char t={t} x={760} y={FLOOR + 40} h={680} {...YOU} face="ConcernedFear" flip seed={5} />
    {t > ad && <div style={{position: 'absolute', inset: 0, background: `radial-gradient(circle at 360px 900px, rgba(0,0,0,0) 0, rgba(0,0,0,${0.7 * ramp(t, ad, 0.4)}) 420px)`}} />}
  </Camera>);
};
const D06: React.FC<{t: number}> = ({t}) => {
  const s = w('d06', 'sangre');
  return (<Camera t={t} keys={[[0, 1.0, 540, 1150], [s, 1.7, 800, 1060]]}>
    <Market t={t} light={0.32} />
    <AbsoluteFill style={{background: 'rgba(8,16,48,.35)'}} />
    <div style={{position: 'absolute', inset: 0, transformOrigin: `260px ${FLOOR}px`, transform: 'rotate(-88deg)'}}>
      <Char t={t} x={260} y={FLOOR} h={600} {...YOU} face="EyesClosed" seed={5} />
    </div>
    <Char t={t} x={470} y={FLOOR + 40} h={690} {...REPA} pose="PointingFingerWB" face="ConcernedFear" seed={8} />
    <Char t={t} x={820} y={FLOOR + 40} h={680} {...MUCHA} face="Tired" flip seed={9} tilt={Math.sin(t * 12) * 2} />
    {t > s - 0.2 && <div style={{position: 'absolute', left: 700, top: 1000, width: 200, height: 200, borderRadius: 100,
      background: `radial-gradient(rgba(220,0,20,${0.8}) 0, rgba(255,0,0,0) 70%)`, transform: `scale(${0.9 + 0.1 * Math.sin(t * 9)})`}} />}
  </Camera>);
};
const D07: React.FC<{t: number}> = ({t}) => {
  const l = TLX.lines[TLX.lines.length - 1]; const a = ramp(t, l.start, 0.4);
  const opt = (lab: string, txt: string, i: number) => {
    const b = ramp(t, w('d07', i === 0 ? 'a' : 'b') - 0.3, 0.35);
    return (<div style={{margin: '26px 70px', padding: '34px 40px', borderRadius: 34, display: 'flex', alignItems: 'center', gap: 30, opacity: b,
      transform: `translateY(${40 * (1 - b)}px)`, background: 'rgba(18,20,28,.92)', border: `5px solid ${i === 0 ? '#f2c230' : '#5aa0ff'}`}}>
      <div style={{width: 110, height: 110, borderRadius: 55, background: i === 0 ? '#f2c230' : '#5aa0ff', color: '#111', fontSize: 70, fontWeight: 900,
        display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Montserrat'}}>{lab}</div>
      <div style={{color: '#fff', fontSize: 50, fontWeight: 800, fontFamily: 'Montserrat'}}>{txt}</div></div>);
  };
  return (<AbsoluteFill>
    <Market t={t} light={0.3} />
    <AbsoluteFill style={{background: 'rgba(0,0,0,.6)'}} />
    <div style={{position: 'absolute', top: 520, width: W, opacity: a}}>
      <div style={{textAlign: 'center', color: '#fff', fontFamily: 'Montserrat', fontWeight: 900, fontSize: 92}}>¿QUÉ HACES?</div>
      {opt('A', 'La encierras en el cuarto frío', 0)}{opt('B', 'Le crees y se queda', 1)}
      <div style={{textAlign: 'center', color: '#f2c230', fontFamily: 'Montserrat', fontWeight: 900, fontSize: 70, marginTop: 40}}>COMENTA A o B</div>
    </div>
  </AbsoluteFill>);
};
const SCENES: Record<string, React.FC<{t: number}>> = {d01: D01, d02: D02, d03: D03, d04: D04, d05: D05, d06: D06, d07: D07};

// ---------------- subtítulos y título ----------------
const Captions: React.FC<{t: number}> = ({t}) => {
  const l = TLX.lines.find(x => t >= x.start - 0.05 && t < x.end + 0.3); if (!l || l.scene === 'd07') return null;
  const ws = l.words; let i = ws.findIndex(x => t < x[2]); if (i < 0) i = ws.length - 1;
  const g0 = Math.floor(i / 3) * 3, grp = ws.slice(g0, g0 + 3);
  const pop = ramp(t, grp[0][1], 0.12);
  return (<div style={{position: 'absolute', top: 1180, width: W, textAlign: 'center', padding: '0 60px', boxSizing: 'border-box',
    transform: `scale(${0.85 + 0.15 * pop})`}}>
    {grp.map((x, j) => { const on = t >= x[1]; const key = KEY.has(norm(x[0]));
      return <React.Fragment key={j}><span style={{display: 'inline-block', fontFamily: 'Montserrat', fontWeight: 900, fontSize: 84, lineHeight: 1.1, textTransform: 'uppercase', margin: '0 12px',
        color: key && on ? '#ffd23a' : '#ffffff', opacity: on ? 1 : 0.55, WebkitTextStroke: '14px #000', paintOrder: 'stroke fill',
        textShadow: '0 8px 18px rgba(0,0,0,.6)'}}>{x[0]}</span>{' '}</React.Fragment>; })}
  </div>);
};
const Title: React.FC = () => (
  <div style={{position: 'absolute', top: 110, left: 60, right: 60, background: '#fff', borderRadius: 30, padding: '30px 30px 26px', textAlign: 'center',
    boxShadow: '0 12px 30px rgba(0,0,0,.45)'}}>
    <div style={{position: 'absolute', top: -26, left: '50%', transform: 'translateX(-50%)', background: '#e0303a', color: '#fff', fontFamily: 'Montserrat',
      fontWeight: 900, fontSize: 32, padding: '6px 22px', borderRadius: 20}}>DÍA 1</div>
    <div style={{fontFamily: 'Montserrat', fontWeight: 800, fontSize: 44, color: '#111', lineHeight: 1.25}}>Brote zombi en Bogotá:<br />atrapado en el supermercado</div>
  </div>);

export const Zombi1: React.FC = () => {
  const t = useT();
  const idx = Math.max(0, TLX.lines.findIndex((l, i) => t < (TLX.lines[i + 1]?.start ?? 1e9) - 0.4));
  const sc = TLX.lines[idx].scene, S = SCENES[sc];
  const sceneStart = idx === 0 ? 0 : TLX.lines[idx].start - 0.4;
  const cut = clamp((t - sceneStart) / 0.12);
  return (<AbsoluteFill style={{background: '#000'}}>
    <AbsoluteFill style={{opacity: idx === 0 ? 1 : cut}}><S t={t} /></AbsoluteFill>
    <Vignette a={0.7} />
    <Grain t={t} a={0.12} />
    <Title />
    <Captions t={t} />
    <Audio src={staticFile('zombi_p1.m4a')} />
  </AbsoluteFill>);
};

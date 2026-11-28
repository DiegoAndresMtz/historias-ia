// Kit de animación «cine de terror» para Remotion: personajes Open Peeps (CC0), zombis, luz, cámara, grano.
import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate, spring, Easing, random} from 'remotion';
import Peep from 'react-peeps';

export const W = 1080, H = 1920;
export const useT = () => { const f = useCurrentFrame(); const {fps} = useVideoConfig(); return f / fps; };
export const clamp = (x: number, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const ease = (x: number) => { x = clamp(x); return x * x * (3 - 2 * x); };
export const ramp = (t: number, t0: number, d: number) => ease((t - t0) / d);

// ---------- línea de tiempo (de engine/tts.py) ----------
export type Line = {scene: string; start: number; end: number; words: [string, number, number][]; text: string};
export type TL = {END: number; lines: Line[]};
const norm = (s: string) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-zñ0-9]/g, '');
export const wordTime = (tl: TL, scene: string, tok: string) => {
  const l = tl.lines.find(x => x.scene === scene); if (!l) return 0;
  const w = l.words.find(x => norm(x[0]) === norm(tok)); return w ? w[1] : l.start;
};

// ---------- personajes ----------
type CharProps = {x: number; y: number; h: number; pose?: string; face?: string; hair?: string; skin?: string; clothes?: string;
  flip?: boolean; zombie?: boolean; walk?: number; t: number; seed?: number; tilt?: number; accessory?: string; facialHair?: string; dim?: number};
const VB = {x: '-150', y: '0', width: '1300', height: '2850'} as any;
const ASPECT = 1300 / 2850;
export const Char: React.FC<CharProps> = ({x, y, h, pose = 'ShirtPantsBW', face = 'Calm', hair = 'Short', skin = '#c68a62', clothes = '#3b4a6b',
  flip = false, zombie = false, walk = 0, t, seed = 0, tilt = 0, accessory = 'None', facialHair = 'None', dim = 0}) => {
  const w = h * ASPECT;
  const ph = t * 8 + seed;
  const bob = -Math.abs(Math.sin(ph)) * h * 0.018 * walk;
  let rot = tilt + Math.sin(ph) * 1.2 * walk + Math.sin(t * 1.1 + seed) * 0.6;   // respira y se balancea apenas
  let jx = 0;
  if (zombie) {                                       // tirones de zombi: el torso se sacude, los pies quedan en el piso
    const j = Math.sin(t * 23 + seed) * Math.sin(t * 2.7 + seed * 3);
    rot += 6 + 4 * j; jx = 6 * Math.sin(t * 17 + seed);
  }
  const zs = zombie ? '#7f9479' : skin, zc = zombie ? '#4f5a4c' : clothes;
  const st = '#0c0c10';
  const filt = `drop-shadow(0 ${h * 0.02}px ${h * 0.03}px rgba(0,0,0,.55)) brightness(${1 - dim})`;
  return (
    <div style={{position: 'absolute', left: x - w / 2 + jx, top: y - h + bob, width: w, height: h,
      transform: `scaleX(${flip ? -1 : 1}) rotate(${rot}deg)`, transformOrigin: '50% 96%', filter: filt}}>
      <Peep viewBox={VB} style={{position: 'absolute', width: w, height: h}} body={pose as any} face={(zombie ? 'Blank' : face) as any}
        hair={hair as any} accessory={accessory as any} facialHair={facialHair as any} strokeColor={st} backgroundColor={zc} />
      <Peep viewBox={VB} style={{position: 'absolute', width: w, height: h}} face={(zombie ? 'Blank' : face) as any}
        hair={hair as any} accessory={accessory as any} facialHair={facialHair as any} strokeColor={st} backgroundColor={zs} />
      {zombie && <ZombieFace w={w} h={h} t={t} seed={seed} />}
    </div>);
};

// Cara de zombi encima de la cabeza (coordenadas del viewBox: ojos ≈ (480,300) y (598,295))
const ZombieFace: React.FC<{w: number; h: number; t: number; seed: number}> = ({w, h, t, seed}) => {
  const fl = 0.75 + 0.25 * Math.sin(t * 13 + seed);
  return (
    <svg viewBox="-150 0 1300 2850" style={{position: 'absolute', left: 0, top: 0, width: w, height: h}}>
      <defs>
        <radialGradient id={`g${seed}`}><stop offset="0" stopColor="#ff3a2a" stopOpacity={0.95 * fl} /><stop offset="1" stopColor="#ff0000" stopOpacity="0" /></radialGradient>
      </defs>
      <ellipse cx={540} cy={330} rx={150} ry={150} fill="#7f9479" />
      {[[478, 300], [600, 296]].map(([cx, cy], i) => (<g key={i}>
        <ellipse cx={cx} cy={cy} rx={42} ry={34} fill="#140808" />
        <circle cx={cx} cy={cy} r={60} fill={`url(#g${seed})`} />
        <circle cx={cx + 4} cy={cy} r={11} fill="#ffd0c0" />
      </g>))}
      <path d="M440 250 L520 280 M560 278 L640 258" stroke="#0c0c10" strokeWidth={14} strokeLinecap="round" />
      <path d="M500 400 Q560 370 625 395 L615 455 Q560 480 505 452 Z" fill="#1a0505" stroke="#0c0c10" strokeWidth={8} />
      {[0, 1, 2, 3, 4].map(k => <path key={k} d={`M${512 + k * 22} 398 l10 22 l10 -22`} fill="#e8dfc0" />)}
      <path d="M560 455 q4 40 -6 70" stroke="#6a0000" strokeWidth={10} fill="none" />
      <path d="M430 340 q-20 30 -10 60 M660 330 q10 30 0 55" stroke="#4f5f4a" strokeWidth={6} fill="none" />
    </svg>);
};

// Primer plano de zombi (pantalla completa)
export const ZombieCloseup: React.FC<{t: number; k?: number; scale?: number}> = ({t, k = 1, scale = 1}) => {
  const sh = Math.sin(t * 41) * 6 * k;
  const fl = 0.8 + 0.2 * Math.sin(t * 17);
  return (
    <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, transform: `translate(${sh}px,${sh * 0.5}px) scale(${scale})`}}>
      <defs>
        <radialGradient id="zc-skin" cx="0.45" cy="0.4"><stop offset="0" stopColor="#9aab92" /><stop offset="0.7" stopColor="#5f6f5a" /><stop offset="1" stopColor="#2a332a" /></radialGradient>
        <radialGradient id="zc-eye"><stop offset="0" stopColor="#ffb0a0" /><stop offset="0.25" stopColor="#ff2a1a" /><stop offset="1" stopColor="#ff0000" stopOpacity="0" /></radialGradient>
        <filter id="zc-rough"><feTurbulence baseFrequency="0.035" numOctaves="3" seed="4" /><feDisplacementMap in="SourceGraphic" scale="18" /></filter>
      </defs>
      <rect width="1080" height="1920" fill="#050304" />
      <g filter="url(#zc-rough)">
        <ellipse cx="540" cy="900" rx="430" ry="560" fill="url(#zc-skin)" stroke="#0c0c10" strokeWidth="16" />
        {[...Array(18)].map((_, i) => { const a = random('v' + i) * 6.28, r = 380; const x0 = 540 + Math.cos(a) * r, y0 = 900 + Math.sin(a) * r * 1.3;
          return <path key={i} d={`M${x0} ${y0} Q${(x0 + 540) / 2 + 40} ${(y0 + 900) / 2} ${540 + (x0 - 540) * 0.55} ${900 + (y0 - 900) * 0.55}`} stroke="#3b4a36" strokeWidth="6" fill="none" />; })}
        {[[370, 760], [710, 750]].map(([x, y], i) => (<g key={i}>
          <ellipse cx={x} cy={y} rx="120" ry="95" fill="#120606" />
          <circle cx={x} cy={y} r={150 * fl} fill="url(#zc-eye)" />
          <circle cx={x} cy={y} r="18" fill="#2a0000" />
        </g>))}
        <path d="M250 610 L470 690 M610 690 L830 600" stroke="#0c0c10" strokeWidth="34" strokeLinecap="round" />
        <path d="M300 1130 Q540 1020 790 1120 Q760 1360 540 1400 Q320 1360 300 1130 Z" fill="#140303" stroke="#0c0c10" strokeWidth="14" />
        {[...Array(9)].map((_, i) => <path key={'t' + i} d={`M${330 + i * 50} ${1110 - Math.sin(i / 8 * 3.14) * 50} l25 70 l25 -70`} fill="#e6dcbc" />)}
        {[...Array(8)].map((_, i) => <path key={'b' + i} d={`M${360 + i * 48} ${1370 - Math.sin(i / 7 * 3.14) * 20} l22 -60 l22 60`} fill="#d4c8a0" />)}
        <path d="M470 1395 q10 120 -10 230 M610 1390 q-6 90 8 170" stroke="#7a0000" strokeWidth="18" fill="none" />
      </g>
    </svg>);
};

// ---------- luz, cámara, grano ----------
export const Grain: React.FC<{t: number; a?: number}> = ({t, a = 0.14}) => {
  const seed = Math.floor(t * 24) % 50;
  return (<svg style={{position: 'absolute', inset: 0, width: W, height: H, mixBlendMode: 'overlay', opacity: a, pointerEvents: 'none'}}>
    <filter id={`gr${seed}`}><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={seed} /><feColorMatrix type="saturate" values="0" /></filter>
    <rect width="100%" height="100%" filter={`url(#gr${seed})`} />
  </svg>);
};
export const Vignette: React.FC<{a?: number; col?: string}> = ({a = 0.75, col = '0,0,0'}) => (
  <div style={{position: 'absolute', inset: 0, background: `radial-gradient(ellipse at 50% 45%, rgba(${col},0) 35%, rgba(${col},${a}) 100%)`}} />);
export const Flash: React.FC<{t: number; at: number; col?: string; d?: number}> = ({t, at, col = '255,255,255', d = 0.25}) => {
  const k = t >= at ? clamp(1 - (t - at) / d) : 0;
  return k > 0 ? <div style={{position: 'absolute', inset: 0, background: `rgba(${col},${0.85 * k})`}} /> : null;
};
export const Camera: React.FC<{t: number; keys: [number, number, number, number][]; shake?: number; children: any}> = ({t, keys, shake = 0, children}) => {
  // keys: [tiempo, zoom, cx, cy]; transición suave entre claves
  let z = keys[0][1], cx = keys[0][2], cy = keys[0][3];
  for (let i = 1; i < keys.length; i++) {
    const k = ramp(t, keys[i][0] - 0.15, 0.45);
    z = z + (keys[i][1] - z) * k; cx = cx + (keys[i][2] - cx) * k; cy = cy + (keys[i][3] - cy) * k;
  }
  const sx = shake * Math.sin(t * 53) * 14, sy = shake * Math.cos(t * 47) * 10;
  return <div style={{position: 'absolute', inset: 0, transformOrigin: `${cx}px ${cy}px`, transform: `translate(${sx}px,${sy}px) scale(${z})`}}>{children}</div>;
};

// Escenarios reutilizables (SVG 1080x1920). El piso de los personajes está en FLOOR.
import React from 'react';
import {random} from 'remotion';
export const FLOOR = 1500;
const SV: React.FC<{children: any; style?: any}> = ({children, style}) => (
  <svg viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, ...style}}>{children}</svg>);
const Defs = () => (<defs>
  <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2b303b" /><stop offset="1" stopColor="#171a21" /></linearGradient>
  <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2a2d34" /><stop offset="1" stopColor="#0d0f13" /></linearGradient>
  <linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#05070d" /><stop offset="1" stopColor="#151b2a" /></linearGradient>
  <radialGradient id="tube"><stop offset="0" stopColor="#e8f0ff" stopOpacity="0.55" /><stop offset="1" stopColor="#e8f0ff" stopOpacity="0" /></radialGradient>
  <radialGradient id="warm"><stop offset="0" stopColor="#fff2c0" stopOpacity="0.6" /><stop offset="1" stopColor="#fff2c0" stopOpacity="0" /></radialGradient>
  <filter id="blur6"><feGaussianBlur stdDeviation="6" /></filter>
  <filter id="blur3"><feGaussianBlur stdDeviation="3" /></filter>
</defs>);
const Tubes: React.FC<{t: number; light: number; y?: number; n?: number}> = ({t, light, y = 250, n = 4}) => (<>{[...Array(n)].map((_, i) => {
  const a = ((Math.floor(t * 7 + i * 5) % 13 === 0) ? 0.25 : 0.85 + 0.15 * Math.sin(t * 50 + i)) * light; const x = 140 + i * (920 / n);
  return (<g key={i}><rect x={x} y={y} width={180} height={18} rx={6} fill={`rgba(240,246,255,${0.3 + 0.7 * a})`} />
    <ellipse cx={x + 90} cy={y + 50} rx={260} ry={220} fill="url(#tube)" opacity={a} /></g>); })}</>);

export const Market: React.FC<{t: number; light?: number; red?: number}> = ({t, light = 1, red = 0}) => {
  const shelf = (side: number) => [...Array(5)].map((_, r) => (<g key={side + 'r' + r}>
    {[...Array(9)].map((_, j) => <rect key={j} x={(side < 0 ? 40 : 760) + j * 34} y={490 + r * 150} width={28} height={70}
      fill={['#b03a2e', '#d4a017', '#2e6f9e', '#2e8b57', '#d9822b', '#7d3c98', '#cfd6d8'][(j + r * 2 + side + 7) % 7]} opacity={0.85} />)}
    <rect x={side < 0 ? 30 : 750} y={560 + r * 150} width={320} height={12} fill="#6b7280" /></g>));
  return (<SV><Defs />
    <rect width="1080" height="1920" fill="url(#wall)" /><rect y="1250" width="1080" height="670" fill="url(#floor)" />
    {[...Array(13)].map((_, i) => <line key={i} x1={i * 90 - 60} y1={1920} x2={540 + (i - 6) * 26} y2={1250} stroke="#33373f" strokeWidth={3} />)}
    <g filter="url(#blur6)">{shelf(-1)}{shelf(1)}</g>
    <rect x="360" y="380" width="360" height="70" rx="8" fill="#b8241c" />
    <text x="540" y="430" fill="#fff" fontFamily="Montserrat" fontWeight={900} fontSize="40" textAnchor="middle">SUPERMERCADO</text>
    <Tubes t={t} light={light} />
    <ellipse cx="540" cy="1520" rx="520" ry="90" fill="#000" opacity={0.35} />
    {red > 0 && <rect width="1080" height="1920" fill="#ff0010" opacity={0.18 * red} />}
    <rect width="1080" height="1920" fill="#000" opacity={0.55 * (1 - light)} />
  </SV>);
};
export const Counter: React.FC<{x: number}> = ({x}) => (<SV>
  <rect x={x} y={FLOOR - 260} width={420} height={260} rx={10} fill="#4b5260" stroke="#0c0c10" strokeWidth={8} />
  <rect x={x} y={FLOOR - 280} width={420} height={30} fill="#6b7280" stroke="#0c0c10" strokeWidth={6} />
  <rect x={x + 290} y={FLOOR - 390} width={100} height={110} fill="#1f232b" stroke="#0c0c10" strokeWidth={6} />
  <rect x={x + 300} y={FLOOR - 380} width={80} height={60} fill="#5ad0ff" /></SV>);
export const Gate: React.FC<{t: number; down: number; shake: number}> = ({t, down, shake}) => {
  const h = 1150 * down, dx = Math.sin(t * 40) * 8 * shake;
  return (<SV style={{transform: `translateX(${dx}px)`}}>
    {[...Array(31)].map((_, i) => <line key={i} x1={i * 36} y1={250} x2={i * 36} y2={250 + h} stroke="#9aa0aa" strokeWidth={7} />)}
    {[...Array(Math.floor(h / 70) + 1)].map((_, j) => <line key={'h' + j} x1={0} y1={250 + j * 70} x2={1080} y2={250 + j * 70} stroke="#b4b9c2" strokeWidth={6} />)}
    <rect x={0} y={250 + h - 20} width={1080} height={26} fill="#c8ccd4" stroke="#0c0c10" strokeWidth={4} /></SV>);
};
export const ColdRoom: React.FC<{t: number; knock: number}> = ({t, knock}) => {
  const dx = Math.sin(t * 50) * 8 * knock;
  return (<SV><Defs /><rect width="1080" height="1920" fill="#1b232d" /><rect y="1320" width="1080" height="600" fill="#12161c" />
    <rect x={250 + dx} y={560} width={580} height={800} rx={14} fill="#aebac3" stroke="#0c0c10" strokeWidth={10} />
    <rect x={285 + dx} y={600} width={510} height={720} rx={8} fill="#9aa7b0" />
    {[0, 1, 2].map(i => <rect key={i} x={300 + dx} y={680 + i * 220} width={480} height={10} fill="#8a96a0" />)}
    <rect x={760 + dx} y={900} width={36} height={150} rx={8} fill="#4a545c" stroke="#0c0c10" strokeWidth={5} />
    <rect x={250} y={470} width={580} height={70} rx={8} fill="#2a6aa0" />
    <text x="540" y="520" fill="#fff" fontFamily="Montserrat" fontWeight={900} fontSize="38" textAnchor="middle">CUARTO FRÍO</text>
    {knock > 0 && <ellipse cx={540} cy={1360} rx={420} ry={60} fill="#9ad0ff" opacity={0.15 * knock} />}
    <Tubes t={t} light={0.8} y={300} n={3} /></SV>);
};
export const Skylight: React.FC<{t: number; crack: number}> = ({t, crack}) => (<SV><Defs />
  <rect width="1080" height="1920" fill="url(#night)" />
  {[0, 1, 2].map(i => <g key={i}><rect x={60 + i * 340} y={380} width={300} height={700} fill="#0d1422" stroke="#2a3446" strokeWidth={10} />
    <rect x={70 + i * 340} y={390} width={280} height={680} fill="#3a5070" opacity={0.28} /></g>)}
  {crack > 0 && [...Array(Math.floor(40 * crack))].map((_, k) => { const x0 = 420 + random('cx' + k) * 260, y0 = 450 + random('cy' + k) * 560, a = random('ca' + k) * 6.28, L = (40 + random('cl' + k) * 170) * crack;
    return <line key={k} x1={x0} y1={y0} x2={x0 + Math.cos(a) * L} y2={y0 + Math.sin(a) * L} stroke="#d8e8ff" strokeWidth={4} />; })}
</SV>);
export const Night: React.FC<{t: number; frame?: boolean}> = ({t, frame}) => frame ? (<SV>
  <rect width="1080" height="200" fill="#0a0c12" /><rect width="70" height="1920" fill="#0a0c12" /><rect x="1010" width="70" height="1920" fill="#0a0c12" />
  <rect y="1700" width="1080" height="220" fill="#0a0c12" /><line x1="540" y1="200" x2="540" y2="1700" stroke="#0a0c12" strokeWidth="26" /></SV>) : (<SV><Defs />
  <rect width="1080" height="1920" fill="url(#night)" />
  {[...Array(6)].map((_, i) => { const h = 500 + ((i * 197) % 400); return (<g key={i}><rect x={i * 190 - 40} y={1300 - h} width={170} height={h} fill="#0b0e16" />
    {[...Array(Math.floor(h / 90))].map((_, k) => (i + k) % 3 === 0 ? <rect key={k} x={i * 190 - 10 + (k % 2) * 70} y={1340 - h + k * 90} width={44} height={40} fill="#f0c060" opacity={0.35} /> : null)}</g>); })}
  <rect y="1300" width="1080" height="620" fill="#171a22" /><rect y="1520" width="1080" height="14" fill="#c8b040" opacity={0.7} />
  {frame && <g><rect width="1080" height="200" fill="#0a0c12" /><rect width="70" height="1920" fill="#0a0c12" /><rect x="1010" width="70" height="1920" fill="#0a0c12" />
    <rect y="1700" width="1080" height="220" fill="#0a0c12" /><line x1="540" y1="200" x2="540" y2="1700" stroke="#0a0c12" strokeWidth="26" /></g>}
</SV>);
export const BackLot: React.FC<{t: number}> = ({t}) => (<SV><Defs />
  <rect width="1080" height="1920" fill="url(#night)" /><rect y="1350" width="1080" height="570" fill="#15181f" />
  <rect x="0" y="560" width="1080" height="40" fill="#3a3f4a" />
  {[...Array(9)].map((_, i) => <g key={i}><rect x={430 + (i % 3) * 200} y={1350 - Math.floor(i / 3) * 190 - 190} width={190} height={180} fill="#2a5a8a" stroke="#0c0c10" strokeWidth={8} />
    {[0, 1, 2].map(k => <line key={k} x1={445 + (i % 3) * 200} y1={1350 - Math.floor(i / 3) * 190 - 150 + k * 50} x2={605 + (i % 3) * 200} y2={1350 - Math.floor(i / 3) * 190 - 150 + k * 50} stroke="#1d4268" strokeWidth={8} />)}</g>)}
  <ellipse cx="200" cy="500" rx="120" ry="120" fill="#d8dcea" opacity={0.85} />
</SV>);
export const Parking: React.FC<{t: number}> = ({t}) => (<SV><Defs />
  <rect width="1080" height="1920" fill="#10131c" /><rect y="1250" width="1080" height="670" fill="#22252e" />
  {[0, 1, 2, 3].map(i => <rect key={i} x={60 + i * 280} y={1250} width={14} height={670} fill="#e6c840" opacity={0.6} />)}
  {[0, 1, 2].map(i => <rect key={'c' + i} x={-40 + i * 400} y={300} width={60} height={950} fill="#1a1d26" />)}
  <Tubes t={t} light={0.55} y={240} n={3} /></SV>);
export const Alley: React.FC<{t: number}> = ({t}) => (<SV><Defs />
  <rect width="1080" height="1920" fill="#07080d" />
  <polygon points="0,0 300,420 300,1350 0,1920" fill="#0d0f15" /><polygon points="1080,0 780,420 780,1350 1080,1920" fill="#0d0f15" />
  <polygon points="300,1350 780,1350 1080,1920 0,1920" fill="#1a1d26" />
  <rect x="330" y="1120" width="110" height="230" fill="#24302a" stroke="#0c0c10" strokeWidth={6} />
  <rect x="640" y="1080" width="120" height="270" fill="#20242c" stroke="#0c0c10" strokeWidth={6} />
  <ellipse cx="540" cy="1400" rx="300" ry="60" fill="#fff2c0" opacity={0.06} /></SV>);
export const Truck: React.FC<{x: number; y: number; s: number; lights?: number}> = ({x, y, s, lights = 1}) => (
  <svg viewBox="-420 -420 840 460" style={{position: 'absolute', left: x - 420 * s, top: y - 420 * s, width: 840 * s, height: 460 * s, overflow: 'visible'}}>
    <rect x={-380} y={-330} width={500} height={290} fill="#4a5a3a" stroke="#0c0c10" strokeWidth={10} />
    <rect x={-380} y={-345} width={500} height={24} fill="#3a4a2c" />
    {[...Array(6)].map((_, k) => <line key={k} x1={-370 + k * 90} y1={-330} x2={-370 + k * 90} y2={-40} stroke="#3e4c30" strokeWidth={8} />)}
    <rect x={120} y={-250} width={220} height={210} fill="#55683f" stroke="#0c0c10" strokeWidth={10} /><rect x={160} y={-230} width={140} height={90} fill="#9ab0c8" />
    {[-250, 230].map(wx => <g key={wx}><circle cx={wx} cy={-30} r={62} fill="#15161a" /><circle cx={wx} cy={-30} r={24} fill="#5a5c62" /></g>)}
    {lights > 0 && <ellipse cx={380} cy={-100} rx={260} ry={160} fill="url(#warm)" opacity={lights} />}
    <defs><radialGradient id="warm"><stop offset="0" stopColor="#fff2c0" stopOpacity="0.6" /><stop offset="1" stopColor="#fff2c0" stopOpacity="0" /></radialGradient></defs>
  </svg>);
export const Moto: React.FC<{x: number; y: number; s: number; light?: number; rot?: number}> = ({x, y, s, light = 0, rot = 0}) => (
  <svg viewBox="-200 -220 400 240" style={{position: 'absolute', left: x - 200 * s, top: y - 220 * s, width: 400 * s, height: 240 * s, overflow: 'visible',
    transform: `rotate(${rot}deg)`, transformOrigin: '50% 100%'}}>
    {[-110, 110].map(wx => <g key={wx}><circle cx={wx} cy={-50} r={50} fill="#15161a" /><circle cx={wx} cy={-50} r={18} fill="#6a6c72" /></g>)}
    <path d="M-120 -90 L40 -120 L120 -90 L90 -60 L-90 -60 Z" fill="#c0392b" stroke="#0c0c10" strokeWidth={6} />
    <rect x={-10} y={-160} width={90} height={42} rx={8} fill="#e8702a" stroke="#0c0c10" strokeWidth={5} />
    <line x1={110} y1={-60} x2={90} y2={-170} stroke="#2a2a30" strokeWidth={12} />
    {light > 0 && <ellipse cx={200} cy={-110} rx={160} ry={70} fill="#fff2c0" opacity={0.3 * light} />}
  </svg>);

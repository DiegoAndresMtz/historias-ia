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

// ---------- TransMilenio (historia zombi_transmi) ----------
const TM_RED = '#b3131b';
// Edificios y postes que pasan por la ventana (move = velocidad del bus)
const Outside: React.FC<{t: number; sky: string; move: number; y0: number; y1: number}> = ({t, sky, move, y0, y1}) => {
  const c = sky === 'day' ? ['#8fa9c4', '#d9c7a0'] : sky === 'dawn' ? ['#33405e', '#c9875a'] : ['#04060b', '#141a28'];
  const lit = sky === 'day' ? 0 : 1;
  return (<g>
    <defs><linearGradient id={`sk-${sky}`} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={c[0]} /><stop offset="1" stopColor={c[1]} /></linearGradient></defs>
    <rect x={0} y={y0} width={1080} height={y1 - y0} fill={`url(#sk-${sky})`} />
    {[...Array(9)].map((_, i) => { const x = ((i * 190 - t * move * 420) % 1710 + 1710) % 1710 - 300, h = 180 + ((i * 137) % 230);
      return (<g key={i}><rect x={x} y={y1 - h} width={160} height={h} fill={sky === 'day' ? '#6d7684' : '#0b0e16'} />
        {lit ? [...Array(Math.floor(h / 60))].map((_, k) => (i + k) % 2 === 0 ? <rect key={k} x={x + 20 + (k % 2) * 70} y={y1 - h + 20 + k * 60} width={36} height={28} fill="#f0c060" opacity={0.4} /> : null) : null}</g>); })}
    {[...Array(4)].map((_, i) => { const x = ((i * 380 - t * move * 900) % 1520 + 1520) % 1520 - 200;
      return (<g key={'p' + i}><rect x={x} y={y0 + 40} width={14} height={y1 - y0} fill="#1a1d24" />
        {lit ? <circle cx={x + 7} cy={y0 + 50} r={90} fill="url(#warm)" opacity={0.6} /> : null}</g>); })}
  </g>);
};
export const BusInside: React.FC<{t: number; light?: number; red?: number; sky?: string; move?: number}> = ({t, light = 1, red = 0, sky = 'night', move = 0}) => (
  <SV><Defs />
    <rect width="1080" height="1920" fill="#262a33" />
    <Outside t={t} sky={sky} move={move} y0={430} y1={970} />
    {[0, 1, 2].map(i => <rect key={i} x={30 + i * 360} y={430} width={300} height={540} fill="none" stroke="#14161b" strokeWidth={14} rx={10} />)}
    {[0, 1, 2].map(i => <rect key={'w' + i} x={40 + i * 360} y={440} width={140} height={520} fill="#ffffff" opacity={0.05} />)}
    <rect x="0" y="430" width="30" height="540" fill={TM_RED} /><rect x="330" y="430" width="60" height="540" fill={TM_RED} />
    <rect x="690" y="430" width="60" height="540" fill={TM_RED} /><rect x="1050" y="430" width="30" height="540" fill={TM_RED} />
    <rect y="0" width="1080" height="430" fill="#b9bec7" /><rect y="330" width="1080" height="100" fill={TM_RED} />
    <rect y="970" width="1080" height="290" fill={TM_RED} /><rect y="1250" width="1080" height="670" fill="#4d5159" />
    {[...Array(6)].map((_, i) => <path key={'s' + i} d={`M${20 + i * 180} 1270 q0 -190 30 -210 h110 q30 20 30 210 Z`} fill="#2f4f7a" stroke="#0c0c10" strokeWidth={6} />)}
    <rect y="1270" width="1080" height="12" fill="#e6c840" opacity={0.7} />
    {[...Array(40)].map((_, i) => <circle key={'d' + i} cx={(i * 97) % 1080} cy={1320 + ((i * 53) % 560)} r={4} fill="#3b3f47" />)}
    <rect y="300" width="1080" height="16" fill="#cfd4db" stroke="#0c0c10" strokeWidth={3} />
    {[...Array(8)].map((_, i) => <g key={'h' + i}><line x1={70 + i * 135} y1={316} x2={70 + i * 135} y2={380} stroke="#2a2d34" strokeWidth={6} />
      <ellipse cx={70 + i * 135} cy={400} rx={20} ry={24} fill="none" stroke="#e6c840" strokeWidth={8} /></g>)}
    {[110, 970].map(x => <rect key={x} x={x - 11} y={300} width={22} height={1220} fill="#c7ccd3" stroke="#0c0c10" strokeWidth={4} />)}
    <Tubes t={t} light={light} y={120} n={4} />
    {red > 0 && <rect width="1080" height="1920" fill="#ff0010" opacity={0.2 * red} />}
    <rect width="1080" height="1920" fill="#000" opacity={0.6 * (1 - light)} />
  </SV>);
// Afuera de la puerta (estación/troncal de noche)
export const DoorOutside: React.FC<{t: number}> = ({t}) => (<SV><Defs />
  <rect width="1080" height="1920" fill="url(#night)" />
  <Outside t={t} sky="night" move={0} y0={0} y1={1250} />
  <rect y="1250" width="1080" height="670" fill="#1b1e26" /><rect y="1250" width="1080" height="40" fill="#5a5e66" />
  <ellipse cx="800" cy="1300" rx="420" ry="120" fill="#ffb060" opacity={0.08} /></SV>);
// Marco de la puerta de vidrio (se pone ENCIMA de lo que hay afuera). open: 0 cerrada · 1 abierta
export const DoorFrame: React.FC<{t: number; open?: number; light?: number}> = ({t, open = 0, light = 1}) => {
  const L = 220, R = 860, T = 380, B = 1560, m = 540, d = open * 300;
  return (<SV><Defs />
    <path fillRule="evenodd" d={`M0 0H1080V1920H0Z M${L} ${T}H${R}V${B}H${L}Z`} fill="#262a33" />
    <path fillRule="evenodd" d={`M0 0H1080V330H0Z`} fill="#b9bec7" /><rect y="330" width="1080" height="50" fill={TM_RED} />
    <rect x={0} y={380} width={L} height={1180} fill={TM_RED} /><rect x={R} y={380} width={1080 - R} height={1180} fill={TM_RED} />
    <rect y={B} width="1080" height={1920 - B} fill="#4d5159" /><rect y={B} width="1080" height="14" fill="#e6c840" opacity={0.75} />
    {[[L - d, m - d], [m + d, R + d]].map(([a, b], i) => (<g key={i}>
      <rect x={a} y={T} width={b - a} height={B - T} fill="#9ec4e0" opacity={0.13} stroke="#111317" strokeWidth={18} />
      <line x1={a + 40} y1={T + 300} x2={a + 160} y2={T + 120} stroke="#ffffff" strokeWidth={10} opacity={0.12} />
      <line x1={a + 60} y1={T + 520} x2={a + 230} y2={T + 280} stroke="#ffffff" strokeWidth={6} opacity={0.1} />
      <rect x={i === 0 ? b - 40 : a + 22} y={T + 80} width={18} height={150} rx={8} fill="#c7ccd3" stroke="#0c0c10" strokeWidth={4} /></g>))}
    <rect x={L - 30} y={T - 30} width={R - L + 60} height={30} fill="#111317" />
    <rect x={L - 30} y={T - 30} width={30} height={B - T + 30} fill="#111317" /><rect x={R} y={T - 30} width={30} height={B - T + 30} fill="#111317" />
    <Tubes t={t} light={light} y={150} n={3} />
    <rect width="1080" height="1920" fill="#000" opacity={0.6 * (1 - light)} />
  </SV>);
};
// Fuelle de caucho entre los dos vagones. tear 0..1 = hueco rasgado; eyes = ojos rojos del otro lado; broken = roto del todo
export const Fuelle: React.FC<{t: number; tear?: number; eyes?: number; shake?: number; light?: number}> = ({t, tear = 0, eyes = 0, shake = 0, light = 1}) => {
  const dx = Math.sin(t * 47) * 10 * shake, cx = 540, cy = 860;
  return (<SV><Defs />
    <rect width="1080" height="1920" fill="#262a33" /><rect y="0" width="1080" height="300" fill="#b9bec7" />
    <g transform={`translate(${dx},0)`}>
      {[...Array(9)].map((_, k) => <rect key={k} x={cx - 500 + k * 44} y={cy - 620 + k * 52} width={1000 - k * 88} height={1240 - k * 104} rx={90 - k * 6}
        fill={k % 2 ? '#34353c' : '#26272d'} stroke="#111216" strokeWidth={14} />)}
      <rect x={cx - 104} y={cy - 152} width={208} height={304} rx={30} fill="#3a0c10" />
      <rect x={cx - 104} y={cy - 152} width={208} height={304} rx={30} fill="#000" opacity={0.55} />
      {tear > 0 && (<g>
        <circle cx={cx + 60} cy={cy + 40} r={300 * tear} fill="#ff1a1a" opacity={0.12} />
        <path d={[...Array(14)].map((_, i) => { const a = i / 14 * 6.283, r = (150 + 70 * random('tr' + i)) * tear * 1.6;
          return `${i ? 'L' : 'M'}${cx + 60 + Math.cos(a) * r} ${cy + 40 + Math.sin(a) * r * 1.3}`; }).join(' ') + 'Z'} fill="#070203" stroke="#15161a" strokeWidth={10} />
        {[...Array(6)].map((_, i) => { const a = i / 6 * 6.283 + 0.3, r = 230 * tear * 1.5;
          return <path key={i} d={`M${cx + 60 + Math.cos(a) * r} ${cy + 40 + Math.sin(a) * r * 1.3} l${Math.cos(a) * 60} ${Math.sin(a) * 90 + 30}`} stroke="#2c2d33" strokeWidth={22} strokeLinecap="round" />; })}
      </g>)}
      {eyes > 0 && [...Array(6)].map((_, i) => { const ex = cx - 60 + (i % 3) * 70 + 60 * tear, ey = cy - 60 + Math.floor(i / 3) * 120 + 40 * tear, f = 0.6 + 0.4 * Math.sin(t * 9 + i);
        return <g key={'e' + i} opacity={eyes * f}><circle cx={ex} cy={ey} r={9} fill="#ff2a1a" /><circle cx={ex + 26} cy={ey - 2} r={9} fill="#ff2a1a" />
          <circle cx={ex + 13} cy={ey} r={34} fill="#ff0000" opacity={0.18} /></g>; })}
    </g>
    <rect y="1380" width="1080" height="540" fill="#4d5159" />
    <ellipse cx="540" cy="1470" rx="470" ry="90" fill="#7a7f88" stroke="#0c0c10" strokeWidth={8} />
    {[0, 1, 2, 3].map(i => <ellipse key={i} cx="540" cy="1470" rx={400 - i * 90} ry={74 - i * 16} fill="none" stroke="#5f646c" strokeWidth={5} />)}
    <Tubes t={t} light={light} y={150} n={3} />
    <rect width="1080" height="1920" fill="#000" opacity={0.6 * (1 - light)} />
  </SV>);
};
// Brazo gris de zombi que sale de un hueco (apunta hacia la derecha-abajo; reach 0..1)
export const GrayHand: React.FC<{x: number; y: number; s?: number; rot?: number; reach?: number; t: number}> = ({x, y, s = 1, rot = 0, reach = 1, t}) => {
  const tw = Math.sin(t * 19) * 3;
  return (<svg viewBox="-40 -120 520 240" style={{position: 'absolute', left: x - 40 * s, top: y - 120 * s, width: 520 * s, height: 240 * s, overflow: 'visible',
    transform: `rotate(${rot + tw}deg) translateX(${-260 * (1 - reach) * s}px)`, transformOrigin: `${40 * s}px ${120 * s}px`}}>
    <path d="M-40 -34 L300 -40 Q330 -42 340 -30 L420 -60 Q440 -66 444 -50 L380 -14 L470 -30 Q488 -30 486 -14 L392 6 L462 22 Q478 28 470 42 L384 34 L430 70 Q438 86 422 88 L340 44 Q320 50 300 40 L-40 40 Z"
      fill="#7f9479" stroke="#0c0c10" strokeWidth={9} strokeLinejoin="round" />
    <path d="M60 -20 q30 10 60 -4 M140 10 q40 14 80 0 M220 -24 q20 8 40 0" stroke="#4f5f4a" strokeWidth={6} fill="none" />
    <path d="M180 -36 q10 30 -6 70" stroke="#5a0a0a" strokeWidth={8} fill="none" opacity={0.8} />
    <path d="M-40 -34 L100 -38 L100 40 L-40 40 Z" fill="#3e3a44" stroke="#0c0c10" strokeWidth={9} />
  </svg>);
};
export const CandyCart: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <svg viewBox="-160 -300 320 300" style={{position: 'absolute', left: x - 160 * s, top: y - 300 * s, width: 320 * s, height: 300 * s, overflow: 'visible'}}>
    <rect x={-140} y={-230} width={280} height={170} rx={10} fill="#d9822b" stroke="#0c0c10" strokeWidth={8} />
    <rect x={-140} y={-170} width={280} height={14} fill="#a85f1a" />
    {[...Array(10)].map((_, i) => <rect key={i} x={-130 + (i % 5) * 52} y={-290 + Math.floor(i / 5) * 32} width={44} height={28} rx={6}
      fill={['#e0303a', '#f2c230', '#2e8b57', '#5aa0ff', '#e07aa0'][i % 5]} stroke="#0c0c10" strokeWidth={4} />)}
    <line x1={140} y1={-200} x2={190} y2={-280} stroke="#2a2d34" strokeWidth={10} strokeLinecap="round" />
    {[-100, 100].map(wx => <circle key={wx} cx={wx} cy={-30} r={30} fill="#15161a" stroke="#0c0c10" strokeWidth={6} />)}
  </svg>);
export const Bundle: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <svg viewBox="-110 -80 220 160" style={{position: 'absolute', left: x - 110 * s, top: y - 80 * s, width: 220 * s, height: 160 * s, overflow: 'visible'}}>
    <ellipse cx={0} cy={0} rx={100} ry={62} fill="#a9c7e8" stroke="#0c0c10" strokeWidth={7} />
    <path d="M-60 -30 q40 30 100 10 M-70 20 q50 20 120 -6" stroke="#7a9cc4" strokeWidth={6} fill="none" />
    <circle cx={-55} cy={-12} r={30} fill="#e8b898" stroke="#0c0c10" strokeWidth={6} />
    <path d="M-66 -14 q5 4 9 0 M-50 -16 q5 4 9 0" stroke="#0c0c10" strokeWidth={4} fill="none" />
  </svg>);
// Bus articulado rojo visto de lado (va hacia la derecha)
export const BusSide: React.FC<{x: number; y: number; s?: number; lights?: number; rot?: number}> = ({x, y, s = 1, lights = 1, rot = 0}) => (
  <svg viewBox="-620 -330 1240 340" style={{position: 'absolute', left: x - 620 * s, top: y - 330 * s, width: 1240 * s, height: 340 * s, overflow: 'visible',
    transform: `rotate(${rot}deg)`, transformOrigin: '50% 100%'}}>
    {[[-600, -30], [30, 600]].map(([a, b], i) => (<g key={i}>
      <rect x={a} y={-300} width={b - a} height={250} rx={i ? 40 : 24} fill={TM_RED} stroke="#0c0c10" strokeWidth={10} />
      <rect x={a + 20} y={-270} width={b - a - 40} height={100} rx={10} fill="#1d2633" stroke="#0c0c10" strokeWidth={6} />
      {[...Array(5)].map((_, k) => <rect key={k} x={a + 34 + k * ((b - a - 60) / 5)} y={-262} width={(b - a - 60) / 5 - 14} height={84} fill="#f3d98a" opacity={0.28 * lights} />)}
      <rect x={a + (b - a) / 2 - 50} y={-160} width={100} height={110} fill="#8a96a0" stroke="#0c0c10" strokeWidth={6} />
      <rect x={a} y={-90} width={b - a} height={16} fill="#e8e8e8" opacity={0.85} /></g>))}
    {[...Array(6)].map((_, k) => <rect key={'f' + k} x={-30 + k * 10} y={-280} width={8} height={220} fill={k % 2 ? '#26272d' : '#3a3b42'} />)}
    <rect x={560} y={-280} width={40} height={140} fill="#9ab0c8" stroke="#0c0c10" strokeWidth={6} />
    {[-480, -150, 170, 480].map(wx => <g key={wx}><circle cx={wx} cy={-40} r={48} fill="#15161a" /><circle cx={wx} cy={-40} r={18} fill="#5a5c62" /></g>)}
    {lights > 0 && <ellipse cx={760} cy={-90} rx={220} ry={80} fill="#fff2c0" opacity={0.3 * lights} />}
  </svg>);
// Troncal de noche (move = velocidad: las rayas y los edificios corren a la izquierda)
export const Road: React.FC<{t: number; move?: number}> = ({t, move = 0}) => (<SV><Defs />
  <rect width="1080" height="1920" fill="url(#night)" />
  <Outside t={t} sky="night" move={move * 0.4} y0={300} y1={1250} />
  <rect y="1250" width="1080" height="80" fill="#4a4e57" stroke="#0c0c10" strokeWidth={6} />
  <rect y="1330" width="1080" height="590" fill="#1c1f27" />
  {[...Array(8)].map((_, i) => { const x = ((i * 260 - t * move * 1400) % 2080 + 2080) % 2080 - 300; return <rect key={i} x={x} y={1640} width={150} height={18} fill="#e8e8e8" opacity={0.6} />; })}
</SV>);
// Portal de llegada (techo de estación, reflectores del ejército)
export const Portal: React.FC<{t: number}> = ({t}) => (<SV><Defs />
  <rect width="1080" height="1920" fill="url(#night)" />
  <path d="M-40 640 L1120 560 L1120 640 L-40 720 Z" fill="#20242e" stroke="#0c0c10" strokeWidth={8} />
  {[80, 400, 720, 1000].map(x => <rect key={x} x={x} y={620} width={34} height={700} fill="#1a1d24" />)}
  {[[160, 360], [920, 330]].map(([x, y], i) => <g key={i}><circle cx={x} cy={y} r={30 + 4 * Math.sin(t * 5 + i)} fill="#fffbe8" />
    <circle cx={x} cy={y} r={260} fill="#fff6d0" opacity={0.12} /></g>)}
  <polygon points="160,360 -100,1500 500,1500" fill="#fff6d0" opacity={0.06} /><polygon points="920,330 600,1500 1180,1500" fill="#fff6d0" opacity={0.06} />
  <rect y="1300" width="1080" height="620" fill="#1c1f27" />
</SV>);
// Reja (barrotes) para poner delante de los personajes
export const Reja: React.FC<{y0?: number; y1?: number; dx?: number; bent?: number}> = ({y0 = 820, y1 = 1560, dx = 0, bent = 0}) => (<SV>
  {[...Array(19)].map((_, i) => { const x = 20 + i * 58 + dx, b = bent * Math.max(0, 1 - Math.abs(i - 9) / 5) * 120;
    return <path key={i} d={`M${x} ${y0} Q${x + b * 0.5} ${(y0 + y1) / 2} ${x} ${y1}`} stroke="#8d939c" strokeWidth={12} fill="none" />; })}
  {[y0 + 20, y1 - 60].map(y => <rect key={y} x={0} y={y} width={1080} height={16} fill="#a3a9b2" stroke="#0c0c10" strokeWidth={3} />)}
</SV>);

import React from 'react';
import {AbsoluteFill} from 'remotion';
import Peep from 'react-peeps';
export const Measure: React.FC = () => (
  <AbsoluteFill style={{background: '#fff'}}>
    <div style={{position:'absolute',left:0,top:0}}>
      <Peep viewBox={{x:'-150',y:'0',width:'1300',height:'1600'} as any} style={{width:1080,height:1330}} body={'RoboDanceOutline' as any} face="Blank" hair="ShortMessy" strokeColor="#111" backgroundColor="#8a9e84"/>
      <svg viewBox="-150 0 1300 1600" style={{position:'absolute',left:0,top:0,width:1080,height:1330}}>
        {Array.from({length:14}).map((_,i)=>(<g key={i}><line x1={-150+i*100} y1={0} x2={-150+i*100} y2={1600} stroke="red" strokeWidth={2}/><text x={-145+i*100} y={30} fontSize={24} fill="red">{-150+i*100}</text></g>))}
        {Array.from({length:16}).map((_,i)=>(<g key={'h'+i}><line x1={-150} y1={i*100} x2={1150} y2={i*100} stroke="blue" strokeWidth={2}/><text x={-140} y={i*100-4} fontSize={24} fill="blue">{i*100}</text></g>))}
      </svg>
    </div>
  </AbsoluteFill>);

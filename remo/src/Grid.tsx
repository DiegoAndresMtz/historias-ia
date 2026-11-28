import React from 'react';
import {AbsoluteFill} from 'remotion';
import Peep from 'react-peeps';
const P = ['BlazerBW','BlazerPantsBW','BlazerPantsWB','BlazerWB','CrossedArmsBW','CrossedArmsWB','Doc','DocProtectiveClothe','DocStethoscope','EasingBW','EasingWB','PointingFingerBW','PointingFingerWB','PolkaDots','RestingBW','RestingWB','RoboDanceBW','RoboDanceOutline','RoboDanceWB','ShirtBW','ShirtPantsBW','ShirtPantsWB','ShirtWB','WalkingBW','WalkingFilled','WalkingWB'];
export const Grid: React.FC = () => (
  <AbsoluteFill style={{background: '#556'}}>
    {P.map((b,i)=>(<div key={b} style={{position:'absolute', left:(i%7)*154, top: Math.floor(i/7)*470, width:150, height:470}}>
      <Peep viewBox={{x:'-150',y:'0',width:'1300',height:'3200'} as any} style={{width:150,height:370}} body={b as any} face="Calm" hair="Short" strokeColor="#111" backgroundColor="#e03030"/>
      <div style={{color:'#fff',fontSize:16}}>{b}</div></div>))}
  </AbsoluteFill>);

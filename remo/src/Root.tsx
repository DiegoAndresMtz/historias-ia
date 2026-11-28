import React from 'react';
import {Composition, AbsoluteFill} from 'remotion';
import Peep from 'react-peeps';
import {Grid} from './Grid';
import {Measure} from './Measure';
import {Zombi1} from './Zombi1';
const Test: React.FC = () => (
  <AbsoluteFill style={{background: 'linear-gradient(#2a2e38,#101218)'}}>
    {[['WalkingBW','Fear','Short','#f2c230'],['PointingFingerBW','Angry','Bald','#e8e4dc'],['RestingWB','ConcernedFear','Long','#9ad'],['ShirtPantsBW','Monster','ShortMessy','#8a9e84']].map(([b,f,h,c],i)=>(
      <div key={i} style={{position:'absolute', left: 20+i*260, top: 700, width: 300, height: 600}}>
        <Peep viewBox={{x:'-150',y:'0',width:'1300',height:'3200'} as any} style={{width: 300, height: 740}} body={b as any} face={f as any} hair={h as any} strokeColor="#111" backgroundColor={c as any} />
      </div>))}
    {[['bust','Shirt'],].map(()=>null)}
    <div style={{position:'absolute', left: 200, top: 100, width: 700, height: 600}}>
      <Peep style={{width:700,height:600}} body="Hoodie" face="Monster" hair="ShortScratch" strokeColor="#0a0a0a" backgroundColor="#7c8f78" />
    </div>
  </AbsoluteFill>
);
export const Root: React.FC = () => (<>
  <Composition id="Test" component={Test} width={1080} height={1920} fps={30} durationInFrames={30} />
  <Composition id="Grid" component={Grid} width={1080} height={1920} fps={30} durationInFrames={30} />
  <Composition id="Measure" component={Measure} width={1080} height={1400} fps={30} durationInFrames={30} />
  <Composition id="Zombi1" component={Zombi1} width={1080} height={1920} fps={30} durationInFrames={1408} />
</>);

import React from 'react';
import {Composition} from 'remotion';
import {Episode, Meta} from './kit';
import {STORIES} from './stories';
// Una composición por historia y parte: <historia con guiones>-p<N>  (ej. zombi-super-p1).
// Las escenas son funciones: no se pasan como props (Remotion las serializa), se buscan en STORIES.
const LIST = Object.entries(STORIES).flatMap(([id, parts]) => Object.entries(parts).map(([n, m]) => {
  const C: React.FC = () => <Episode m={m as Meta} />;
  return {id: `${id.replace(/_/g, '-')}-p${n}`, C, frames: Math.ceil((m as Meta).tl.END * 30)};
}));
export const Root: React.FC = () => (<>
  {LIST.map(x => <Composition key={x.id} id={x.id} component={x.C} width={1080} height={1920} fps={30} durationInFrames={x.frames} />)}
</>);

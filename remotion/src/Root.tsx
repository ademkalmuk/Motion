import React from 'react';
import {Composition} from 'remotion';
import {FPS, H, W} from './brand';
import {HunerReferans, HUNER_DURATION} from './huner/HunerReferans';

export const Root: React.FC = () => (
  <>
    <Composition id="HunerReferans" component={HunerReferans} durationInFrames={HUNER_DURATION} fps={FPS} width={W} height={H} />
  </>
);

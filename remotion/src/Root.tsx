import React from 'react';
import {Composition} from 'remotion';
import {FPS, H, W} from './brand';
import {HunerReferans, HUNER_DURATION} from './huner/HunerReferans';
import {KalmukPromo, PROMO_DURATION} from './promo/KalmukPromo';

export const Root: React.FC = () => (
  <>
    <Composition id="KalmukPromo" component={KalmukPromo} durationInFrames={PROMO_DURATION} fps={FPS} width={W} height={H} />
    <Composition id="HunerReferans" component={HunerReferans} durationInFrames={HUNER_DURATION} fps={FPS} width={W} height={H} />
  </>
);

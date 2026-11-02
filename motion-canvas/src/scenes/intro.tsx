// Kalmuk Media test scene: logo text + blue line, 1080x1920.
import {makeScene2D, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, easeOutExpo, waitFor} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
  view.fill('#000');
  const title = createRef<Txt>();
  const line = createRef<Rect>();
  view.add(
    <>
      <Txt ref={title} text="KALMUK" fill="#fff" fontSize={180} fontWeight={900} fontFamily="Montserrat" opacity={0} y={60} />
      <Rect ref={line} width={0} height={10} fill="#51a2ff" y={180} />
    </>,
  );
  yield* all(title().opacity(1, 0.6), title().y(0, 0.6, easeOutExpo), line().width(700, 0.8, easeOutExpo));
  yield* waitFor(1);
});

import React from 'react';
import { Composition, AbsoluteFill, Sequence } from 'remotion';
import { Intro } from './Intro';
import { History } from './History';
import { Principles } from './Principles';
import { Formula } from './Formula';
import { Example } from './Example';
import { Summary } from './Summary';

export const PositionManagement: React.FC = () => {
  return (
    <Composition
      id="PositionManagement"
      component={PositionManagementVideo}
      durationInFrames={1530} // 约 51 秒 (30fps)
      width={1920}
      height={1080}
      fps={30}
    />
  );
};

const PositionManagementVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#1a1a2e' }}>
      {/* 开场 */}
      <Sequence from={0} durationInFrames={180}>
        <Intro />
      </Sequence>

      {/* 历史起源 */}
      <Sequence from={180} durationInFrames={300}>
        <History />
      </Sequence>

      {/* 核心原理 */}
      <Sequence from={480} durationInFrames={360}>
        <Principles />
      </Sequence>

      {/* 凯利公式 */}
      <Sequence from={840} durationInFrames={300}>
        <Formula />
      </Sequence>

      {/* 实战计算 */}
      <Sequence from={1140} durationInFrames={300}>
        <Example />
      </Sequence>

      {/* 总结 */}
      <Sequence from={1440} durationInFrames={90}>
        <Summary />
      </Sequence>
    </AbsoluteFill>
  );
};

export default PositionManagementVideo;
import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { motion } from 'framer-motion';

export const Formula: React.FC = () => {
  return (
    <AbsoluteFill style={{ padding: '80px' }}>
      <h2
        style={{
          fontSize: '60px',
          fontWeight: 'bold',
          color: '#10b981',
          margin: '0 0 60px 0',
          fontFamily: 'Noto Sans SC, sans-serif',
        }}
      >
        凯利公式
      </h2>

      {/* 公式展示 */}
      <Sequence from={0} durationInFrames={100}>
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          style={{
            textAlign: 'center',
            fontSize: '80px',
            color: '#10b981',
            fontFamily: 'Noto Sans SC, sans-serif',
            margin: '0 0 40px 0',
          }}
        >
          f* = (bp − q) / b
        </motion.div>
      </Sequence>

      {/* 公式说明 */}
      <Sequence from={50} durationInFrames={100}>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          style={{ fontSize: '40px', color: '#e5e7eb', fontFamily: 'Noto Sans SC, sans-serif', margin: '0 0 40px 0' }}
        >
          <p style={{ margin: '0 0 20px 0' }}>f* = 最优投入比例</p>
          <p style={{ margin: '0 0 20px 0' }}>b = 赔率（平均盈利 ÷ 平均亏损）</p>
          <p style={{ margin: '0 0 20px 0' }}>p = 胜率</p>
          <p style={{ margin: '0' }}>q = 亏损率（= 1 − p）</p>
        </motion.div>
      </Sequence>

      {/* 示例 */}
      <Sequence from={100} durationInFrames={100}>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          style={{
            backgroundColor: '#374151',
            padding: '40px',
            borderRadius: '12px',
            textAlign: 'center',
          }}
        >
          <h3
            style={{
              fontSize: '40px',
              color: '#f59e0b',
              margin: '0 0 20px 0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            示例
          </h3>
          <p
            style={{
              fontSize: '30px',
              color: '#e5e7eb',
              margin: '0 0 20px 0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            胜率 60% · 赔率 2:1
          </p>
          <p
            style={{
              fontSize: '40px',
              color: '#10b981',
              margin: '0 0 20px 0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            f* = 25%
          </p>
          <p
            style={{
              fontSize: '25px',
              color: '#9ca3af',
              margin: '0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            提示：实际操作常用 1/4 凯利或 1/2 凯利
          </p>
        </motion.div>
      </Sequence>
    </AbsoluteFill>
  );
};
import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { motion } from 'framer-motion';

export const History: React.FC = () => {
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
        历史起源
      </h2>

      {/* 凯利 */}
      <Sequence from={0} durationInFrames={100}>
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          style={{ marginBottom: '40px' }}
        >
          <h3
            style={{
              fontSize: '40px',
              color: '#f59e0b',
              margin: '0 0 20px 0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            1956 · 约翰·凯利
          </h3>
          <p
            style={{
              fontSize: '30px',
              color: '#e5e7eb',
              margin: '0 0 20px 0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            贝尔实验室科学家
          </p>
          <p
            style={{
              fontSize: '30px',
              color: '#e5e7eb',
              margin: '0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            顺手发明了一个公式：<b>凯利公式</b>
          </p>
        </motion.div>
      </Sequence>

      {/* 索普 */}
      <Sequence from={100} durationInFrames={100}>
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          style={{ marginBottom: '40px' }}
        >
          <h3
            style={{
              fontSize: '40px',
              color: '#f59e0b',
              margin: '0 0 20px 0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            1960s · 爱德华·索普
          </h3>
          <p
            style={{
              fontSize: '30px',
              color: '#e5e7eb',
              margin: '0 0 20px 0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            用凯利公式在赌场算牌
          </p>
          <p
            style={{
              fontSize: '30px',
              color: '#e5e7eb',
              margin: '0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            赚了→黑名单→华尔街连续30年盈利
          </p>
        </motion.div>
      </Sequence>

      {/* 丹尼斯 */}
      <Sequence from={200} durationInFrames={100}>
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h3
            style={{
              fontSize: '40px',
              color: '#f59e0b',
              margin: '0 0 20px 0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            1983 · 理查德·丹尼斯
          </h3>
          <p
            style={{
              fontSize: '30px',
              color: '#e5e7eb',
              margin: '0 0 20px 0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            海龟交易实验
          </p>
          <p
            style={{
              fontSize: '30px',
              color: '#e5e7eb',
              margin: '0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            只教仓位管理→4年回报80%
          </p>
        </motion.div>
      </Sequence>
    </AbsoluteFill>
  );
};
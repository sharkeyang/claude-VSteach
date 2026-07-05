import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { motion } from 'framer-motion';

export const Principles: React.FC = () => {
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
        核心原理
      </h2>

      {/* 三个关键数字 */}
      <Sequence from={0} durationInFrames={100}>
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          style={{
            display: 'flex',
            justifyContent: 'space-around',
            marginBottom: '40px',
          }}
        >
          <div style={{ textAlign: 'center', flex: 1 }}>
            <h3
              style={{
                fontSize: '50px',
                color: '#f59e0b',
                margin: '0 0 20px 0',
                fontFamily: 'Noto Sans SC, sans-serif',
              }}
            >
              胜率
            </h3>
            <p
              style={{
                fontSize: '30px',
                color: '#e5e7eb',
                margin: '0',
                fontFamily: 'Noto Sans SC, sans-serif',
              }}
            >
              赚钱的交易占比
            </p>
          </div>
          <div style={{ textAlign: 'center', flex: 1 }}>
            <h3
              style={{
                fontSize: '50px',
                color: '#f59e0b',
                margin: '0 0 20px 0',
                fontFamily: 'Noto Sans SC, sans-serif',
              }}
            >
              赔率
            </h3>
            <p
              style={{
                fontSize: '30px',
                color: '#e5e7eb',
                margin: '0',
                fontFamily: 'Noto Sans SC, sans-serif',
              }}
            >
              赚多少 ÷ 亏多少
            </p>
          </div>
          <div style={{ textAlign: 'center', flex: 1 }}>
            <h3
              style={{
                fontSize: '50px',
                color: '#f59e0b',
                margin: '0 0 20px 0',
                fontFamily: 'Noto Sans SC, sans-serif',
              }}
            >
              破产成本
            </h3>
            <p
              style={{
                fontSize: '30px',
                color: '#e5e7eb',
                margin: '0',
                fontFamily: 'Noto Sans SC, sans-serif',
              }}
            >
              亏光就出局
            </p>
          </div>
        </motion.div>
      </Sequence>

      {/* 核心问题 */}
      <Sequence from={100} durationInFrames={100}>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          style={{ textAlign: 'center' }}
        >
          <p
            style={{
              fontSize: '40px',
              color: '#e5e7eb',
              margin: '0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            <b>在不确定的情况下，该投入多少？</b>
          </p>
        </motion.div>
      </Sequence>
    </AbsoluteFill>
  );
};
import React from 'react';
import { AbsoluteFill, useCurrentFrame, spring } from 'remotion';
import { motion } from 'framer-motion';

export const Intro: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        style={{ textAlign: 'center' }}
      >
        <h1
          style={{
            fontSize: '80px',
            fontWeight: 'bold',
            color: '#10b981',
            margin: '0 0 40px 0',
            fontFamily: 'Noto Sans SC, sans-serif',
          }}
        >
          仓位管理
        </h1>
        <p
          style={{
            fontSize: '40px',
            color: '#e5e7eb',
            margin: '0 0 20px 0',
            fontFamily: 'Noto Sans SC, sans-serif',
          }}
        >
          决定你能赚多少钱的——不是选股
        </p>
        <p
          style={{
            fontSize: '40px',
            color: '#e5e7eb',
            margin: '0 0 40px 0',
            fontFamily: 'Noto Sans SC, sans-serif',
          }}
        >
          而是<b style={{ color: '#f59e0b' }}>买多少</b>
        </p>
        <p
          style={{
            fontSize: '30px',
            color: '#9ca3af',
            margin: '0',
            fontFamily: 'Noto Sans SC, sans-serif',
          }}
        >
          专业交易者的核心秘密
        </p>
      </motion.div>
    </AbsoluteFill>
  );
};
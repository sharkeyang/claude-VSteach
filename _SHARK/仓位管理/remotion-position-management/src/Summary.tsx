import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { motion } from 'framer-motion';

export const Summary: React.FC = () => {
  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: '80px' }}>
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        style={{ textAlign: 'center' }}
      >
        <h2
          style={{
            fontSize: '60px',
            fontWeight: 'bold',
            color: '#10b981',
            margin: '0 0 40px 0',
            fontFamily: 'Noto Sans SC, sans-serif',
          }}
        >
          记住三件事
        </h2>

        <div style={{ fontSize: '40px', color: '#e5e7eb', fontFamily: 'Noto Sans SC, sans-serif' }}>
          <p style={{ margin: '0 0 30px 0' }}>
            <span style={{ color: '#f59e0b', fontWeight: 'bold' }}>1.</span> 仓位比选股重要
          </p>
          <p style={{ margin: '0 0 30px 0' }}>
            <span style={{ color: '#f59e0b', fontWeight: 'bold' }}>2.</span> 凯利公式是数学最优解<br/>
            <span style={{ fontSize: '30px', color: '#9ca3af' }}>但实践中要保守（用1/4或1/2凯利）</span>
          </p>
          <p style={{ margin: '0' }}>
            <span style={{ color: '#f59e0b', fontWeight: 'bold' }}>3.</span> 2%原则是底线<br/>
            <span style={{ fontSize: '30px', color: '#9ca3af' }}>单笔不超过2%，让你永远有翻盘的机会</span>
          </p>
        </div>
      </motion.div>
    </AbsoluteFill>
  );
};
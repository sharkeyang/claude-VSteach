import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { motion } from 'framer-motion';

export const Example: React.FC = () => {
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
        实战计算
      </h2>

      {/* 公式 */}
      <Sequence from={0} durationInFrames={100}>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          style={{
            textAlign: 'center',
            fontSize: '50px',
            color: '#10b981',
            fontFamily: 'Noto Sans SC, sans-serif',
            margin: '0 0 40px 0',
          }}
        >
          仓位 = 可承受亏损 ÷ 每股止损幅度
        </motion.div>
      </Sequence>

      {/* 例子 */}
      <Sequence from={100} durationInFrames={100}>
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          style={{
            backgroundColor: '#374151',
            padding: '40px',
            borderRadius: '12px',
          }}
        >
          <h3
            style={{
              fontSize: '40px',
              color: '#f59e0b',
              margin: '0 0 30px 0',
              fontFamily: 'Noto Sans SC, sans-serif',
            }}
          >
            实例
          </h3>
          <div style={{ fontSize: '30px', color: '#e5e7eb', fontFamily: 'Noto Sans SC, sans-serif' }}>
            <p style={{ margin: '0 0 20px 0' }}>• 总资金：<span style={{ color: '#10b981' }}>10万</span></p>
            <p style={{ margin: '0 0 20px 0' }}>• 单笔最大亏损：<span style={{ color: '#10b981' }}>2000元（2%）</span></p>
            <p style={{ margin: '0 0 20px 0' }}>• 股票：<span style={{ color: '#10b981' }}>10元买入，止损9.5元</span></p>
            <p style={{ margin: '0 0 20px 0' }}>• 每股亏损：<span style={{ color: '#10b981' }}>0.5元</span></p>
            <p style={{ margin: '0 0 30px 0' }}>• 能买股数：<span style={{ color: '#10b981' }}>2000 ÷ 0.5 = 4000股</span></p>
            <p style={{ margin: '0', fontSize: '40px', color: '#f59e0b' }}>• 对应仓位：<span style={{ color: '#10b981' }}>4万元（总资金的40%）</span></p>
          </div>
          <p
            style={{
              fontSize: '30px',
              color: '#9ca3af',
              margin: '30px 0 0 0',
              fontFamily: 'Noto Sans SC, sans-serif',
              fontStyle: 'italic',
            }}
          >
            这不是"赌"——这是你计算过的风险
          </p>
        </motion.div>
      </Sequence>
    </AbsoluteFill>
  );
};
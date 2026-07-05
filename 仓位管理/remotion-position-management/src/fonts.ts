import { registerFont } from '@remotion/fonts';

// 注册字体（可选，使用系统字体也可以）
registerFont({
  family: 'Noto Sans SC',
  source: [
    {
      format: 'woff2',
      url: 'https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap',
    },
  ],
});

export const DEFAULT_FONT = 'Noto Sans SC, sans-serif';
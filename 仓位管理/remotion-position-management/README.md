# 仓位管理视频 - Remotion 项目

基于仓位管理课程内容的视频项目，使用 Remotion 生成。

## 项目结构

```
remotion-position-management/
├── package.json          # 项目依赖
├── tsconfig.json         # TypeScript 配置
├── .gitignore            # Git 忽略文件
├── src/
│   ├── index.tsx         # 主入口，定义视频结构
│   ├── Intro.tsx         # 开场动画
│   ├── History.tsx       # 历史起源
│   ├── Principles.tsx    # 核心原理
│   ├── Formula.tsx       # 凯利公式
│   ├── Example.tsx       # 实战计算
│   └── Summary.tsx       # 总结
```

## 视频规格

- **分辨率**: 1920×1080 (1080p)
- **帧率**: 30 fps
- **时长**: 约 51 秒
- **总帧数**: 1530 帧

## 快速开始

### 方法 1：使用批处理脚本（推荐）

1. 双击 `start.bat` 安装依赖并启动 Remotion Studio
2. 双击 `build.bat` 渲染视频

### 方法 2：手动运行

```bash
# 安装依赖
npm install

# 启动 Remotion Studio（预览）
npm start

# 渲染视频
npm run build
```

## 自定义

### 修改时长

在 `src/index.tsx` 中修改 `durationInFrames` 和 `from` 属性。

### 修改颜色

在组件中修改颜色值：
- 主色: `#10b981` (绿色)
- 强调色: `#f59e0b` (橙色)
- 文字色: `#e5e7eb` (浅灰)

### 添加配音

Remotion 支持文本转语音。参考 [Remotion TTS 文档](https://www.remotion.dev/docs/tts)。

## 导出视频到抖音/小红书

1. 渲染生成 MP4 文件
2. 上传到抖音/小红书
3. 添加字幕和背景音乐（可选）

## 参考资源

- 凯利公式
- 海龟交易法则
- 《仓位控制与资金管理集萃》
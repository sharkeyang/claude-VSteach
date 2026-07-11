---
name: calligraphy
description: 生成 Chris 字帖 PDF — 输入古文名，自动生成含描红+临写的字帖 PDF
---

# 字帖生成 · Calligraphy Generator

> 调用方式：`/calligraphy 古文名` 或用户在 VSteach 项目中说"生成字帖"

## 用法

```
/calligraphy 陋室铭        → 生成《陋室铭》字帖 PDF
/calligraphy -l            → 列出所有可用的古文
/calligraphy 自定义文本     → 超出古文库范围的，手写自定义文本
```

## 原理

1. 调用 `_CHRIS/__temp/gen_calligraphy.py` 脚本
2. 该脚本内置古文全文数据库，生成 HTML 字帖
3. 用 Edge headless 打印为 PDF
4. PDF 保存在 `_CHRIS/字帖_古文名.pdf`

## 可用古文

包括但不限于：
- 陋室铭、爱莲说、两小儿辩日、论语六章
- 劝学、师说、岳阳楼记、醉翁亭记
- 桃花源记、生于忧患死于安乐、鱼我所欲也
- 出师表、赤壁赋、曹刿论战
- 学而第一、为政第二、八佾第三、里仁第四 等

完整列表运行：`python _CHRIS/__temp/gen_calligraphy.py -l`

## 字帖格式

- 每字 4 格：描红×2 + 临写×2
- 红框米字格（含对角线辅助线）
- 页脚标注练字要点
- A4 竖版，自动分页

## 注意事项

- 需要 Edge 浏览器（用于 PDF 转换）
- 自定义文本：直接说内容，AI 将其传入脚本
- 生成后告知用户 PDF 路径
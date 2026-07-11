# -*- coding: utf-8 -*-
import re

with open('_CHRIS/Chris · 2026年暑假深度方案（优化版）.md', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('拍照步骤→豆包评估', '拍照 → Chris-数学-考试官'),
    ('| Dx-05 | ✍️ 练字（第1次·工整） | 拍照→豆包评估', '| Dx-05 | ✍️ 练字（第1次·工整） | 拍照 → Chris-练字-考试官'),
    ('| Dx-09 | ✍️ 练字（第2次·工整） | 拍照→豆包评估', '| Dx-09 | ✍️ 练字（第2次·工整） | 拍照 → Chris-练字-考试官'),
    ('| Dx-07 | 📖 古文背诵（新篇） | 费曼法复述+默写', '| Dx-07 | 📖 古文背诵（新篇） | 语音 → Chris-古文-考试官'),
    ('| Dx-08 | 📘 新概念英语3复习 | 背诵检测+发音', '| Dx-08 | 📘 新概念英语3复习 | 语音 → Chris-新概念背诵-考试官'),
    ('| Dx-10 | 🗣️ 英语发音/口语 | 录音→豆包评估', '| Dx-10 | 🗣️ 英语发音/口语 | 录音 → Chris-英语发音-考试官'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f'OK: replaced "{old[:20]}..."')
    else:
        print(f'WARN: not found "{old[:20]}..."')

with open('_CHRIS/Chris · 2026年暑假深度方案（优化版）.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
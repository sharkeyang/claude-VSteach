# -*- coding: utf-8 -*-
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

path = r'd:\@VSwork\VSteach\_CHRIS\学而思秘籍 2022版《 小学数学思维培养》电子书.txt'

with open(path, 'rb') as f:
    raw = f.read()

text = raw.decode('gbk', errors='replace')
lines = text.split('\n')

# Extract all levels
level_data = {}
current_level = 0

for line in lines:
    line = line.strip()
    if not line:
        continue
    # Level header: e.g. "第9级-2022版 小学数学思维培养"
    m = re.search(r'第(\d+)级', line)
    if m:
        current_level = int(m.group(1))
        if current_level not in level_data:
            level_data[current_level] = []
        continue
    # Lecture entry: "第1讲 名称"
    m = re.search(r'第(\d+)讲[\s-]*([^\d].*?)(?:\.pdf|\d+\.\d+M)', line)
    if m and current_level > 0:
        lecture_name = m.group(2).strip().rstrip('.')
        level_data[current_level].append((int(m.group(1)), lecture_name))

# Also try alternative pattern for entries without file size
for line in lines:
    line = line.strip()
    if not line:
        continue
    m = re.search(r'第(\d+)级', line)
    if m:
        current_level = int(m.group(1))
        continue
    if current_level > 0:
        m = re.search(r'第(\d+)讲\s+(.*)', line)
        if m:
            num = int(m.group(1))
            name = m.group(2).strip()
            # Avoid duplicates
            existing = [x for x in level_data.get(current_level, []) if x[0] == num]
            if not existing:
                if current_level not in level_data:
                    level_data[current_level] = []
                level_data[current_level].append((num, name))

# Sort and deduplicate
for lv in level_data:
    seen = set()
    unique = []
    for num, name in level_data[lv]:
        key = (num, name)
        if key not in seen:
            seen.add(key)
            unique.append((num, name))
    level_data[lv] = sorted(unique)

# Print all levels
output = []
for lv in sorted(level_data.keys()):
    output.append(f'\n## 第{lv}级')
    for num, name in level_data[lv]:
        output.append(f'- 讲{num}：{name}')

result = '\n'.join(output)
print(result)

# Save
outpath = r'd:\@VSwork\VSteach\_CHRIS\学而思秘籍全级别目录.md'
with open(outpath, 'w', encoding='utf-8') as f:
    f.write('# 学而思秘籍 2022版《小学数学思维培养》全级别目录\n')
    f.write(result)
print(f'\n\nSaved to: {outpath}')
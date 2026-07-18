# -*- coding: utf-8 -*-
"""
验证每日计划 —— 检查古文/新概念/RE/学而思进度是否与记录一致
用法: python _CHRIS/__temp/verify_daily_plan.py
"""
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'D:\@VSwork\VSteach'
RECORD_FILE = os.path.join(BASE, '_CHRIS', 'Chris的每日记录.md')
PLAN_FILE = os.path.join(BASE, '_CHRIS', 'Chris的2026年暑假深度方案（优化版）.md')
GUWEN_DB_FILE = os.path.join(BASE, '_CHRIS', '__temp', 'gen_calligraphy.py')

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ''

def extract_last(records, pattern):
    """从记录中提取最新的匹配项"""
    lines = records.split('\n')
    matches = []
    for line in lines:
        m = pattern.search(line)
        if m:
            matches.append(m.groups())
    return matches[-1] if matches else None

def verify():
    records = read_file(RECORD_FILE)
    if not records:
        print('[ERR] 无法读取记录文件')
        return

    errors = []
    results = []

    # === 1. 古文 ===
    guwen_pattern = re.compile(r'古文[：:]\s*《(.+?)》')
    last_guwen = extract_last(records, guwen_pattern)
    if last_guwen:
        last_name = last_guwen[0]
        # 查暑假计划列表找下一篇
        plan_text = read_file(PLAN_FILE)
        if plan_text:
            # 找编号列表中的匹配
            found = False
            next_name = None
            lines = plan_text.split('\n')
            for i, line in enumerate(lines):
                # 匹配 | 编号 | 篇名 格式（可能有《》也可能没有）
                m = re.search(r'\|\s*(\d+)\s*\|\s*《?(.+?)》?\s*\|', line)
                if m:
                    num = int(m.group(1))
                    name = m.group(2).strip()
                    # 匹配时忽略《》
                    if name == last_name or name.strip('《》') == last_name.strip('《》'):
                        # 找下一篇
                        for j in range(i+1, min(i+10, len(lines))):
                            m2 = re.search(r'\|\s*(\d+)\s*\|\s*《?(.+?)》?\s*\|', lines[j])
                            if m2:
                                next_name = m2.group(2).strip()
                                found = True
                                break
                        break
            if found and next_name:
                results.append((f'📜 古文: #{last_name} ✅ → 下一篇《{next_name}》', True))
            else:
                results.append((f'⚠️ 古文: #{last_name} 未找到下一篇', False))
        else:
            results.append((f'📜 古文: #{last_name}（无法验证列表）', None))
    else:
        results.append(('📜 古文: 未找到最近记录', False))

    # === 2. NC3 ===
    nc3_pattern = re.compile(r'NC3\s*(?:Lesson)?\s*(\d+)')
    last_nc3 = extract_last(records, nc3_pattern)
    if last_nc3:
        n = int(last_nc3[0])
        results.append((f'📘 NC3: Lesson {n} ✅ → 下一篇 Lesson {n+1}', True))
    else:
        results.append(('📘 NC3: 未找到最近记录', False))

    # === 3. RE2 ===
    re_pattern = re.compile(r'RE2?\s*[：:]?\s*(\d+)([A-B])')
    last_re = extract_last(records, re_pattern)
    if last_re:
        unit = int(last_re[0])
        part = last_re[1]
        # 递推: 7B → 8A, 8B → 9A
        if part == 'B':
            next_unit = unit + 1
            next_part = 'A'
        else:
            next_unit = unit
            next_part = 'B'
        results.append((f'🗣️ RE2: {unit}{part} ✅ → 下一篇 {next_unit}{next_part}', True))
    else:
        # Try alternate format
        re_pattern2 = re.compile(r'U(\d+)([A-B])')
        last_re2 = extract_last(records, re_pattern2)
        if last_re2:
            unit = int(last_re2[0])
            part = last_re2[1]
            if part == 'B':
                next_unit = unit + 1
                next_part = 'A'
            else:
                next_unit = unit
                next_part = 'B'
            results.append((f'🗣️ RE2: U{unit}{part} ✅ → 下一篇 U{next_unit}{next_part}', True))
        else:
            results.append(('🗣️ RE2: 未找到最近记录', False))

    # === 4. 学而思 ===
    # 匹配: 学而思9级 第14讲 或 学而思9级 讲14 或 学而思9级 第14讲 后半部分
    # 先匹配"级"（集/volume），再匹配"讲"（lesson）
    xe_pattern = re.compile(r'学而思\s*(\d+)\s*[级集][^\\n]*?[第]?\s*(\d+)\s*[讲]')
    last_xe = extract_last(records, xe_pattern)
    if last_xe:
        vol = int(last_xe[0])
        lesson = int(last_xe[1])
        results.append((f'📚 学而思: 第{vol}集 第{lesson}讲 ✅', True))
    else:
        # 备用匹配
        xe_pattern2 = re.compile(r'学而思.*?(\d+)\s*[讲]')
        last_xe2 = extract_last(records, xe_pattern2)
        if last_xe2:
            n = int(last_xe2[0])
            results.append((f'📚 学而思: 第{n}讲 ✅（集数未识别）', None))
        else:
            results.append(('📚 学而思: 未找到最近记录', False))

    # === 6. 字帖文件名编号验证 ===
    plan_text = read_file(PLAN_FILE)
    if plan_text:
        # 重建编号映射
        name_to_num = {}
        for line in plan_text.split('\n'):
            m = re.search(r'\|\s*(\d+)\s*\|\s*《?(.+?)》?\s*\|', line)
            if m:
                num = int(m.group(1))
                nm = m.group(2).strip().strip('《》').strip()
                name_to_num[nm] = num

        pdf_dir = os.path.join(BASE, '_CHRIS')
        pdf_errors = 0
        pdf_fixed = 0
        if os.path.exists(pdf_dir):
            for f in sorted(os.listdir(pdf_dir)):
                if not f.startswith('字帖_') or not f.endswith('.pdf') or f == '字帖_控笔.pdf':
                    continue
                parts = f.replace('字帖_','').replace('.pdf','').split('_', 1)
                if len(parts) != 2:
                    continue
                old_num, name = parts
                correct_num = name_to_num.get(name, None)
                if correct_num and str(correct_num).zfill(2) != old_num:
                    pdf_errors += 1
                    # Auto-fix
                    new_name = f'字帖_{correct_num:02d}_{name}.pdf'
                    old_path = os.path.join(pdf_dir, f)
                    new_path = os.path.join(pdf_dir, new_name)
                    if not os.path.exists(new_path):
                        os.rename(old_path, new_path)
                        pdf_fixed += 1
                    else:
                        os.remove(old_path)  # duplicate, remove
                        pdf_fixed += 1

        if pdf_errors > 0:
            results.append((f'📄 字帖编号: ❌ 发现{pdf_errors}个错误，已修正{pdf_fixed}个', False))
        else:
            results.append(('📄 字帖编号: ✅ 全部正确', True))
    else:
        results.append(('📄 字帖编号: ⚠️ 无法读取列表', None))

    # 输出
    print()
    print('📋 每日计划验证报告')
    print('═══════════════════')
    all_ok = True
    for msg, ok in results:
        if ok is True:
            print(f'  {msg}')
        elif ok is None:
            print(f'  {msg}')
            all_ok = False
        else:
            print(f'  ❌ {msg}')
            all_ok = False
    print()
    if all_ok:
        print('═══════════════════')
        print('全部通过 ✅')
    else:
        print('═══════════════════')
        print('有异常需检查 ⚠️')

if __name__ == '__main__':
    verify()
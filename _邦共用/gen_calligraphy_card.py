# -*- coding: utf-8 -*-
"""
通用 · 古文背诵理解字帖生成器
============================
格式：描红原文 → 白话解释 → 场景举例 → 针对提醒
由 gen_zgxw_calligraphy.py 泛化而来，支持任意古文/英语材料

用法：
  python gen_calligraphy_card.py "文件名.md"         # 从 Markdown 文件读数据
  python gen_calligraphy_card.py "篇目名" "原文" ...   # 直接传参（待实现）

输入格式要求（Markdown）：
  ## 分类名1
  - 原文|解释|场景|提醒
  - 原文|解释|场景|提醒
  ## 分类名2
  ...

输出：
  @背诵库/@中文/{篇目}/{篇目}_字帖N_分类名.pdf

输出目录：
  _邦共用/@背诵库/@中文/{篇目}/
"""

import os, sys, subprocess, re

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '@背诵库', '@中文')


def gen_html(book_name, chapter, title, items):
    """生成描红字帖 HTML"""
    blocks = ''
    for i, (text, expl, scene, remind) in enumerate(items, 1):
        blocks += f'''
        <div class="card">
            <div class="seq">{i}</div>
            <div class="trace">{text}</div>
            <div class="expl">{expl}</div>
            <div class="scene">🏠 {scene}</div>
            <div class="remind">💡 {remind}</div>
        </div>'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#f5f0eb; font-family: "微软雅黑", "PingFang SC", sans-serif; }}
.a4-page {{ width:210mm; min-height:297mm; padding:6mm 10mm 4mm 10mm; margin:0 auto; background:#fff; position:relative; page-break-after:always; }}
.title {{ font-size:15px; font-weight:700; color:#2D3E50; text-align:center; padding-bottom:3px; border-bottom:2px solid #B78B4A; margin-bottom:2px; }}
.chapter {{ font-size:11px; color:#B78B4A; text-align:center; margin-bottom:2px; }}
.subtitle {{ font-size:8px; color:#999; text-align:center; margin-bottom:4px; }}
.card {{ padding:3px 0 3px 0; border-bottom:1px dashed #e8e0d8; page-break-inside:avoid; }}
.card .seq {{ font-size:7px; color:#ccc; float:left; width:20px; text-align:right; margin-right:6px; line-height:34px; }}
.card .trace {{ font-size:26px; font-weight:500; color:#E0B0B0; font-family:"KaiTi","STKaiti","SimSun",serif; letter-spacing:1px; padding-left:26px; line-height:1.35; }}
.card .expl {{ font-size:10px; color:#666; padding-left:26px; line-height:1.3; }}
.card .scene {{ font-size:9px; color:#888; padding-left:26px; line-height:1.3; }}
.card .remind {{ font-size:8.5px; color:#B78B4A; padding-left:26px; line-height:1.3; }}
@media print {{ body {{ background:#fff; }} .a4-page {{ box-shadow:none; margin:0; padding:5mm 8mm 3mm 8mm; width:100%; min-height:100vh; }} @page {{ margin:0; size:A4 portrait; }} }}
</style>
</head>
<body>
<div class="a4-page">
    <div class="title">{book_name} · 描红字帖</div>
    <div class="chapter">第{chapter}章 · {title}</div>
    <div class="subtitle">描红一遍 → 读解释 → 想场景 → 记提醒</div>
    {blocks}
</div>
</body>
</html>'''
    return html


def save_pdf(book_name, out_dir, chapter, title, items):
    """生成 HTML 并转 PDF"""
    safe = re.sub(r'[\\/:*?"<>| ]', '_', title)
    pdf_name = f'{book_name}_字帖{chapter}_{safe}.pdf'
    html_name = f'_temp_ch{chapter}.html'

    html_path = os.path.join(out_dir, html_name)
    pdf_path = os.path.join(out_dir, pdf_name)

    html = gen_html(book_name, chapter, title, items)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    edge_paths = [
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    ]
    browser = None
    for p in edge_paths:
        if os.path.exists(p):
            browser = p
            break
    if not browser:
        print(f'[WARN] 未找到 Edge/Chrome，请打开 {html_path} 手动打印')
        return

    abs_html = os.path.abspath(html_path)
    abs_pdf = os.path.abspath(pdf_path)
    cmd = f'"{browser}" --headless=new --disable-gpu --no-margins --print-to-pdf-no-header --print-to-pdf="{abs_pdf}" "file://{abs_html}"'
    subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)

    if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 1000:
        print(f'  [OK] {pdf_name}  ({os.path.getsize(abs_pdf)//1024} KB)')
        if os.path.exists(html_path):
            os.remove(html_path)
    else:
        print(f'  [WARN] 请打开 {html_path} 手动打印')


def parse_md(filepath):
    """从 Markdown 文件解析数据，格式见文件头说明"""
    chapters = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by ## headings
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)
    ch_num = 0
    for section in sections:
        if not section.strip():
            continue
        lines = section.strip().split('\n')
        title = lines[0].strip()
        items = []
        for line in lines[1:]:
            line = line.strip()
            if line.startswith('- '):
                parts = [p.strip() for p in line[2:].split('|')]
                if len(parts) >= 4:
                    items.append(tuple(parts[:4]))
                elif len(parts) == 3:
                    items.append(tuple(parts) + ('',))
        if items:
            ch_num += 1
            chapters.append((ch_num, title, items))
    return chapters


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0)

    # 从 Markdown 文件读取
    md_path = args[0]
    book_name = os.path.splitext(os.path.basename(md_path))[0]
    # 去掉末尾的 _分类、_原文 等后缀
    for suffix in ['_分类', '_原文', '_归类分析']:
        if book_name.endswith(suffix):
            book_name = book_name[:-len(suffix)]
            break

    out_dir = os.path.join(BASE_DIR, book_name)
    os.makedirs(out_dir, exist_ok=True)

    chapters = parse_md(md_path)
    for ch, title, items in chapters:
        save_pdf(book_name, out_dir, ch, title, items)

    print(f'\n全部生成完毕！输出目录：{out_dir}')
    print(f'共 {len(chapters)} 章，{sum(len(i) for _,_,i in chapters)} 条')
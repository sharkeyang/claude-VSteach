# -*- coding: utf-8 -*-
"""增广贤文 · 描红字帖生成器 - 完整版"""
import os, sys, subprocess, re
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r'D:\@VSwork\VSteach\_邦共用\@背诵库\@中文\增广贤文'

with open(os.path.join(OUT_DIR, '增广贤文_分类.md'),'r',encoding='utf-8') as f: md=f.read()
hdrs={'说话之道':'说话之道','处世智慧':'处世智慧','人际关系':'人际关系','勤奋/认真':'勤奋认真','家庭/亲情':'家庭亲情','金钱/财富观':'金钱财富','时间/人生感悟':'时间人生'}
cats={v:[] for v in hdrs.values()};cc=None
for line in md.split('\n'):
    l=line.strip()
    if l.startswith('## '):
        if any(x in l for x in ['排除','无意义','数据统计','分类归属']): cc=None;continue
        for hk,cn in hdrs.items():
            if hk in l: cc=cn;break
        continue
    if l.startswith('| **') and '|' in l and cc and '**原文**' not in l:
        parts=[p.strip() for p in l.split('|') if p.strip()]
        if len(parts)>=2:
            t=parts[0].replace('**','').replace('<small>','').replace('</small>','').strip()
            e=parts[1].replace('**','').replace('<small>','').replace('</small>','').strip()
            r=parts[2].replace('**','').replace('<small>','').replace('</small>','').strip() if len(parts)>=3 else ''
            if t and len(t)>4: cats[cc].append((t,e,r))
cat_labels={'说话之道':'说话之道','处世智慧':'处世智慧','人际关系':'人际关系','勤奋认真':'勤奋/认真','家庭亲情':'家庭/亲情','金钱财富':'金钱/财富观','时间人生':'时间/人生感悟'}
cat_order=['说话之道','处世智慧','人际关系','勤奋认真','家庭亲情','金钱财富','时间人生']
CHAPTERS=[(cat_order.index(cn)+1,cat_labels[cn],cats[cn]) for cn in cat_order if cn in cats and cats[cn]]

def get_scene(text,expl):
    s={'好言一句':'同学考试没考好，你说没事下次努力 vs 你说你太笨了','伤身事莫做':'同学穿新衣服你说好丑','过头饭好吃':'你说考100分结果没考到','好话不在多说':'你越激动越大声别人越不听','蚊虫遭扇打':'你在班上笑同学下次他不跟你玩了','祸从口出':'你跟同学说老师坏话传到他耳朵里','一言既出':'你答应了又反悔人家再也不信你','说长说短':'你跟A说B的坏话A转头告诉B','好言难得':'说句你真棒要勇气说句你真笨脱口而出','伤人一语':'你说你妈妈不要了这话让人哭','来说是非者':'同学跑来传话他也会说你别信他'}
    for kw,sc in s.items():
        if kw in text: return sc
    return expl[:15]+'的例子'

def gen_html(ch,title,items):
    b=''
    for i,(t,e,r) in enumerate(items,1):
        s=get_scene(t,e)
        b+=f'<div class="card"><div class="seq">{i}</div><div class="trace">{t}</div><div class="expl">{e}</div><div class="scene">\U0001f3e0 {s}</div><div class="remind">\U0001f4a1 {r}</div></div>\n'
    return f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><style>*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#f5f0eb;font-family:"微软雅黑","PingFang SC",sans-serif}}.a4-page{{width:210mm;min-height:297mm;padding:6mm 10mm 4mm 10mm;margin:0 auto;background:#fff;position:relative;page-break-after:always}}.title{{font-size:15px;font-weight:700;color:#2D3E50;text-align:center;padding-bottom:3px;border-bottom:2px solid #B78B4A;margin-bottom:2px}}.chapter{{font-size:11px;color:#B78B4A;text-align:center;margin-bottom:2px}}.subtitle{{font-size:8px;color:#999;text-align:center;margin-bottom:4px}}.card{{padding:3px 0 3px 0;border-bottom:1px dashed #e8e0d8;page-break-inside:avoid}}.card .seq{{font-size:7px;color:#ccc;float:left;width:20px;text-align:right;margin-right:6px;line-height:34px}}.card .trace{{font-size:26px;font-weight:500;color:#E0B0B0;font-family:"KaiTi","STKaiti","SimSun",serif;letter-spacing:1px;padding-left:26px;line-height:1.35}}.card .expl{{font-size:10px;color:#666;padding-left:26px;line-height:1.3}}.card .scene{{font-size:9px;color:#888;padding-left:26px;line-height:1.3}}.card .remind{{font-size:8.5px;color:#B78B4A;padding-left:26px;line-height:1.3}}@media print{{body{{background:#fff}}.a4-page{{box-shadow:none;margin:0;padding:5mm 8mm 3mm 8mm;width:100%;min-height:100vh}}@page{{margin:0;size:A4 portrait}}}}</style></head><body><div class="a4-page"><div class="title">增广贤文 · 描红字帖</div><div class="chapter">第{ch}章 · {title}</div><div class="subtitle">描红一遍 -> 读解释 -> 想场景 -> 记提醒</div>{b}</div></body></html>'

def save_pdf(ch,title,items):
    safe=re.sub(r'[\\/:*?"<>| ]','',title)
    fn=f'增广贤文_字帖{ch}_{safe}.pdf'
    hp=os.path.join(OUT_DIR,f'_temp_ch{ch}.html')
    pp=os.path.join(OUT_DIR,fn)
    with open(hp,'w',encoding='utf-8') as f: f.write(gen_html(ch,title,items))
    br=None
    for p in [r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',r'C:\Program Files\Google\Chrome\Application\chrome.exe']:
        if os.path.exists(p): br=p;break
    if not br: print(f'No browser');return
    cmd=f'"{br}" --headless=new --disable-gpu --no-margins --print-to-pdf-no-header --print-to-pdf="{os.path.abspath(pp)}" "file://{os.path.abspath(hp)}"'
    subprocess.run(cmd,shell=True,capture_output=True,text=True,timeout=60)
    if os.path.exists(pp) and os.path.getsize(pp)>1000:
        print(f'  [OK] {fn}');os.remove(hp)
    else: print(f'  [WARN] {hp}')

if __name__=='__main__':
    os.makedirs(OUT_DIR,exist_ok=True)
    for ch,ti,it in CHAPTERS:
        save_pdf(ch,ti,it)
    print('\n全部生成完毕！')
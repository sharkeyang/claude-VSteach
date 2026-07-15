# -*- coding: utf-8 -*-
"""Regenerate gen_zgxw_calligraphy.py with clean data"""
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

# Read data from md
with open(r'D:\@VSwork\VSteach\_邦共用\@背诵库\@中文\增广贤文\增广贤文_分类.md','r',encoding='utf-8') as f:
    md=f.read()

hdrs={'说话之道':'说话之道','处世智慧':'处世智慧','人际关系':'人际关系',
      '勤奋/认真':'勤奋认真','家庭/亲情':'家庭亲情','金钱/财富观':'金钱财富','时间/人生感悟':'时间人生'}
cats={v:[] for v in hdrs.values()}
cc=None
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
            e=parts[1].replace('**','').replace('<small>','').replace('</small>','').strip() if len(parts)>=2 else ''
            r=parts[2].replace('**','').replace('<small>','').replace('</small>','').strip() if len(parts)>=3 else ''
            if t and len(t)>4:
                cats[cc].append((t,e,r))

# Build scene examples
scenes={
    '好言一句':'同学考试没考好，你说没事下次努力',
    '伤身事莫做':'同学穿新衣服，你笑说好丑',
    '过头饭好吃':'你说这次一定考100分，结果没考到',
    '好话不在多说':'你越激动越大声，别人反而越不听',
    '蚊虫遭扇打':'你在班上笑同学，下次他不跟你玩了',
    '祸从口出':'你跟同学说老师坏话，传到他耳朵里',
    '口开神气散':'上课你总接话茬，老师烦同学也烦',
    '一言既出':'你答应了又反悔，人家再也不信你',
    '说长说短':'你跟A说B的坏话，A转头告诉B',
    '平生只会说人短':'你笑别人字写得丑，自己也好不到哪去',
    '当面论人惹恨最大':'你当着全班批评班长，班长从此记恨你',
    '好言难得':'说一句你真棒要鼓起勇气，说一句你真笨脱口而出',
    '伤人一语':'你说你妈妈不要你了，这句话让人哭一整天',
    '是非只为多开口':'不该你插嘴的时候插嘴，最后都是你的错',
    '会说说都是':'同样要妈妈买东西，说给我买vs说妈妈辛苦了',
    '知事少时烦恼少':'你偷听大人聊天，听到不好的事瞎担心',
    '言轻莫劝人':'你比同学小两岁去教他做题，他根本不理你',
    '能言不是真君子':'你说得天花乱坠但什么都做不成',
    '贵人语少':'班上最厉害的同学一般话都不多',
    '一字入公门':'你在网上乱说话被人截图举报了',
    '事非亲见，切莫乱谈':'你听别人说小明偷东西就到处传，结果是假的',
    '打人莫打脸':'吵架时你揭人伤疤，那是结死仇',
    '宁在人前全不会':'你只会一点就举手说会了，结果背不下去',
    '酒中不语真君子':'喝了饮料激动乱说话，第二天后悔来不及',
    '知音说与知音听':'你跟不喜欢恐龙的人大讲恐龙，他不感兴趣',
    '逢人且说三分话':'你刚认识新同学就把秘密全告诉他，他转头告诉别人',
    '莫道坐中安乐少':'你嫌作业多，想想那些没书读的孩子',
    '来说是非者，便是是非人':'同学跑来传话，他也会在别人面前说你',
    '力微休负重':'你比同学小两岁去劝和，没人听你的',
    '来说是非者':'跑来跟你说别人是非的人，自己就是是非人',
    '酒中不语':'喝了酒不乱说话才是真君子',
    '会说':'会说话的人怎么说都有理',
    '会说说都是':'会说话怎么说都有理，不会说有理也变没理',
}

# Read existing script header
with open(r'D:\@VSwork\VSteach\_邦共用\gen_zgxw_calligraphy.py','r',encoding='utf-8') as f:
    old_script=f.read()

# Find the script header (before CHAPTERS)
header_end=old_script.find('CHAPTERS = [')
header=old_script[:header_end] if header_end>0 else old_script[:old_script.find('import')]

# Get footer (after CHAPTERS section)
footer_start=old_script.find('if __name__')
footer=old_script[footer_start:] if footer_start>0 else ''

# Build new CHAPTERS
cat_labels={
    '说话之道':'说话之道','处世智慧':'处世智慧','人际关系':'人际关系',
    '勤奋认真':'勤奋/认真','家庭亲情':'家庭/亲情','金钱财富':'金钱/财富观','时间人生':'时间/人生感悟'
}
cat_order=['说话之道','处世智慧','人际关系','勤奋认真','家庭亲情','金钱财富','时间人生']

chapters=[]
for cn in cat_order:
    items=cats[cn]
    if not items:continue
    label=cat_labels[cn]
    entries=[]
    for idx,(text,expl,remind) in enumerate(items):
        # Get scene
        scene=''
        for kw,sc in scenes.items():
            if kw in text:
                scene=sc
                break
        if not scene:
            scene=expl[:15]+'的例子'
        # Clean any problematic characters
        text=text.replace('"',' ').replace('"',' ')
        expl=expl.replace('"',' ').replace('"',' ')
        scene=scene.replace('"',' ').replace('"',' ')
        remind=remind.replace('"',' ').replace('"',' ')
        entries.append(f'        ("{text}", "{expl}", "{scene}", "{remind}")')
    chapter_code=f'    ({cat_order.index(cn)+1}, "{label}", [\n' + ',\n'.join(entries) + '\n    ])'
    chapters.append(chapter_code)

new_script=header+'CHAPTERS = [\n' + ',\n'.join(chapters) + '\n]\n\n\n'+footer

with open(r'D:\@VSwork\VSteach\_邦共用\gen_zgxw_calligraphy.py','w',encoding='utf-8') as f:
    f.write(new_script)

# Verify syntax
try:
    compile(new_script,'gen_zgxw_calligraphy.py','exec')
    print('Syntax OK')
    print(f'Chapters: {len(chapters)}')
    total=sum(len(v) for v in cats.values())
    print(f'Total: {total}')
except SyntaxError as e:
    print(f'Syntax error: {e}')
    # Find the problematic line
    for i,line in enumerate(new_script.split('\n')):
        if '同学' in line and ('\"' in line or '"' in line):
            print(f'Line {i}: {line[:100]}')
            break
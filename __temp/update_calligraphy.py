# -*- coding: utf-8 -*-
"""更新 gen_zgxw_calligraphy.py 的 CHAPTERS 数据并生成字帖"""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

# 1. Read data from classification md
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

# 2. Generate scene examples from reminders
def make_scene(text, remind):
    """Generate a scene example from the text"""
    scenes = {
        '好言一句':'同学考试没考好，你说"没事下次努力" vs 你说"你太笨了"',
        '伤身事莫做':'同学穿新衣服，你笑"好丑"——你随口一说他记一整天',
        '过头饭好吃':'你说"我肯定考100分"结果考了80——别人笑话你',
        '好话不在多说':'你越激动越大声说"你不对"，别人反而越不听',
        '蚊虫遭扇打':'你在班上笑同学"你连这都不会"，下次他不跟你玩了',
        '祸从口出':'你跟同学说"老师坏话"传到他耳朵里你就倒霉了',
        '口开神气散':'上课你总接话茬老师烦同学也烦',
        '一言既出':'你答应周末去同学家又反悔说"我不去了"——人家再也不信你',
        '说长说短':'你跟A说B的坏话，A转头告诉B——你两个朋友都丢了',
        '平生只会说人短':'你笑别人字写得丑你自己的字也好不到哪去',
        '当面论人惹恨最大':'你当着全班说"班长选错了"——班长从此记恨你',
        '好言难得':'说一句"你真棒"要鼓起勇气说一句"你真笨"脱口而出',
        '伤人一语':'你说"你妈妈不要你了"——这句话可能让人哭一整天',
        '是非只为多开口':'你不该插嘴的时候插嘴不该管的事去管——最后都是你的错',
        '会说说都是':'同样要妈妈买东西你说"给我买" vs "妈妈辛苦了能帮我买吗"',
        '知事少时烦恼少':'你偷听大人聊天听到不好的事自己瞎担心',
        '言轻莫劝人':'你比同学小两岁去教他做题他根本不理你',
        '能言不是真君子':'你说得天花乱坠但什么事都没做成——大家觉得你吹牛',
        '贵人语少':'你看班上最厉害的同学一般话都不多',
        '一字入公门':'你在网上乱说话被人截图举报了',
        '事非亲见，切莫乱谈':'你听别人说"小明偷东西"就到处传——结果发现是假的',
        '打人莫打脸':'吵架时你说"你爸爸不在你是个没人管的"——这句话结死仇',
        '宁在人前全不会':'你只背了第一段就举手说"我会了"结果背不下去更丢人',
        '酒中不语真君子':'你喝饮料激动了乱说话第二天后悔也来不及',
        '知音说与知音听':'你跟不喜欢恐龙的人大讲恐龙人家根本不感兴趣',
        '逢人且说三分话':'你刚认识新同学就把家里秘密全告诉他——他转头告诉别人',
        '莫道坐中安乐少':'你嫌作业多想想那些没书读的孩子',
        '来说是非者，便是是非人':'同学跑来跟你说"老师骂你了"他也会在别人面前说你坏话',
    }
    for kw, sc in scenes.items():
        if kw in text:
            return sc
    # Generate from the text
    return f'比如：{remind[:20]}……'

# 3. Build new CHAPTERS data
cat_labels = {
    '说话之道':'说话之道','处世智慧':'处世智慧','人际关系':'人际关系',
    '勤奋认真':'勤奋/认真','家庭亲情':'家庭/亲情','金钱财富':'金钱/财富观','时间人生':'时间/人生感悟'
}
cat_order = ['说话之道','处世智慧','人际关系','勤奋认真','家庭亲情','金钱财富','时间人生']

chapters = []
for cn in cat_order:
    items = cats[cn]
    if not items: continue
    label = cat_labels[cn]
    entries = []
    for text, expl, remind in items:
        scene = make_scene(text, remind)
        entries.append(f'        ("{text}", "{expl}", "{scene}", "{remind}")')
    chapter_text = f'    ({cat_order.index(cn)+1}, "{label}", [\n' + ',\n'.join(entries) + '\n    ])'
    chapters.append(chapter_text)

# 4. Read existing script and update CHAPTERS
with open(r'D:\@VSwork\VSteach\_邦共用\gen_zgxw_calligraphy.py','r',encoding='utf-8') as f:
    script = f.read()

# Find the CHAPTERS section and replace it
start = script.find('CHAPTERS = [')
end = script.find('\n\n\nif __name__')
if start > 0 and end > 0:
    new_chapters = 'CHAPTERS = [\n' + ',\n'.join(chapters) + '\n]\n\n\n'
    new_script = script[:start] + new_chapters + script[end:]
    with open(r'D:\@VSwork\VSteach\_邦共用\gen_zgxw_calligraphy.py','w',encoding='utf-8') as f:
        f.write(new_script)
    print('Script updated')
else:
    print(f'Could not find CHAPTERS: start={start}, end={end}')

# 5. Generate PDFs
print('\nGenerating PDFs...')
os.system('python "' + os.path.join(os.path.dirname(r'D:\@VSwork\VSteach\_邦共用\gen_zgxw_calligraphy.py'),'gen_zgxw_calligraphy.py') + '" all 2>&1')

print('\nDone!')
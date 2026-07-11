# -*- coding: utf-8 -*-
"""
Chris 字帖生成器 — 根据古文名自动生成字帖 PDF
用法：python gen_calligraphy.py <古文名称>
      python gen_calligraphy.py            # 列出所有古文
"""

import sys, os, glob, subprocess, shutil

# ====== 古文库（全文 — 小升初范围 + Chris 已学 + 常见篇目） ======
GUWEN_DB = {
    "陋室铭": "山不在高，有仙则名。水不在深，有龙则灵。斯是陋室，惟吾德馨。苔痕上阶绿，草色入帘青。谈笑有鸿儒，往来无白丁。可以调素琴，阅金经。无丝竹之乱耳，无案牍之劳形。南阳诸葛庐，西蜀子云亭。孔子云：何陋之有？",
    "爱莲说": "水陆草木之花，可爱者甚蕃。晋陶渊明独爱菊。自李唐来，世人甚爱牡丹。予独爱莲之出淤泥而不染，濯清涟而不妖，中通外直，不蔓不枝，香远益清，亭亭净植，可远观而不可亵玩焉。予谓菊，花之隐逸者也；牡丹，花之富贵者也；莲，花之君子者也。噫！菊之爱，陶后鲜有闻。莲之爱，同予者何人？牡丹之爱，宜乎众矣。",
    "两小儿辩日": "孔子东游，见两小儿辩日，问其故。一儿曰：我以日始出时去人近，而日中时远也。一儿曰：我以日初出远，而日中时近也。一儿曰：日初出大如车盖，及日中则如盘盂，此不为远者小而近者大乎？一儿曰：日初出沧沧凉凉，及其日中如探汤，此不为近者热而远者凉乎？孔子不能决也。两小儿笑曰：孰为汝多知乎？",
    "论语六章": "子曰：学而时习之，不亦说乎？有朋自远方来，不亦乐乎？人不知而不愠，不亦君子乎？子曰：温故而知新，可以为师矣。子曰：学而不思则罔，思而不学则殆。子曰：三人行，必有我师焉。择其善者而从之，其不善者而改之。子曰：知之者不如好之者，好之者不如乐之者。子曰：默而识之，学而不厌，诲人不倦，何有于我哉？",
    "学而第一": "子曰：学而时习之，不亦说乎？有朋自远方来，不亦乐乎？人不知而不愠，不亦君子乎？有子曰：其为人也孝悌而好犯上者，鲜矣。不好犯上而好作乱者，未之有也。君子务本，本立而道生。孝悌也者，其为仁之本与？子曰：巧言令色，鲜矣仁。曾子曰：吾日三省吾身，为人谋而不忠乎？与朋友交而不信乎？传不习乎？",
    "为政第二": "子曰：为政以德，譬如北辰，居其所而众星共之。子曰：诗三百，一言以蔽之，曰思无邪。子曰：道之以政，齐之以刑，民免而无耻。道之以德，齐之以礼，有耻且格。子曰：吾十有五而志于学，三十而立，四十而不惑，五十而知天命，六十而耳顺，七十而从心所欲，不逾矩。",
    "八佾第三": "孔子谓季氏，八佾舞于庭，是可忍也，孰不可忍也？三家者以雍彻。子曰：相维辟公，天子穆穆，奚取于三家之堂？子曰：人而不仁，如礼何？人而不仁，如乐何？林放问礼之本。子曰：大哉问！礼，与其奢也，宁俭。丧，与其易也，宁戚。子曰：夷狄之有君，不如诸夏之亡也。季氏旅于泰山。子谓冉有曰：女弗能救与？对曰：不能。子曰：呜呼！曾谓泰山不如林放乎？",
    "里仁第四": "子曰：里仁为美。择不处仁，焉得知？子曰：不仁者不可以久处约，不可以长处乐。仁者安仁，知者利仁。子曰：唯仁者能好人，能恶人。子曰：苟志于仁矣，无恶也。子曰：富与贵是人之所欲也，不以其道得之，不处也。贫与贱是人之所恶也，不以其道得之，不去也。君子去仁，恶乎成名？君子无终食之间违仁，造次必于是，颠沛必于是。",
    "公冶长第五": "子谓公冶长，可妻也。虽在缧绁之中，非其罪也。以其子妻之。子谓南容，邦有道不废，邦无道免于刑戮。以其兄之子妻之。子谓子贱，君子哉若人！鲁无君子者，斯焉取斯？子贡问曰：赐也何如？子曰：女器也。曰：何器也？曰：瑚琏也。或曰：雍也仁而不佞。子曰：焉用佞？御人以口给，屡憎于人。不知其仁，焉用佞？",
    "雍也第六": "子曰：雍也可使南面。仲弓问子桑伯子。子曰：可也简。仲弓曰：居敬而行简，以临其民，不亦可乎？居简而行简，无乃大简乎？子曰：雍之言然。哀公问：弟子孰为好学？孔子对曰：有颜回者好学，不迁怒，不贰过。不幸短命死矣。今也则亡，未闻好学者也。子曰：贤哉回也！一箪食，一瓢饮，在陋巷，人不堪其忧，回也不改其乐。贤哉回也！",
    "述而第七": "子曰：述而不作，信而好古，窃比于我老彭。子曰：默而识之，学而不厌，诲人不倦，何有于我哉？子曰：德之不修，学之不讲，闻义不能徙，不善不能改，是吾忧也。子曰：志于道，据于德，依于仁，游于艺。子曰：不愤不启，不悱不发。举一隅不以三隅反，则不复也。子曰：饭疏食饮水，曲肱而枕之，乐亦在其中矣。不义而富且贵，于我如浮云。",
    "劝学": "君子曰：学不可以已。青，取之于蓝，而青于蓝；冰，水为之，而寒于水。木直中绳，輮以为轮，其曲中规。虽有槁暴，不复挺者，輮使之然也。故木受绳则直，金就砺则利，君子博学而日参省乎己，则知明而行无过矣。吾尝终日而思矣，不如须臾之所学也。吾尝跂而望矣，不如登高之博见也。登高而招，臂非加长也，而见者远。顺风而呼，声非加疾也，而闻者彰。",
    "师说": "古之学者必有师。师者，所以传道受业解惑也。人非生而知之者，孰能无惑？惑而不从师，其为惑也，终不解矣。生乎吾前，其闻道也固先乎吾，吾从而师之。生乎吾后，其闻道也亦先乎吾，吾从而师之。吾师道也，夫庸知其年之先后生于吾乎？是故无贵无贱，无长无少，道之所存，师之所存也。嗟乎！师道之不传也久矣，欲人之无惑也难矣。",
    "岳阳楼记": "庆历四年春，滕子京谪守巴陵郡。越明年，政通人和，百废具兴。乃重修岳阳楼，增其旧制，刻唐贤今人诗赋于其上。属予作文以记之。予观夫巴陵胜状，在洞庭一湖。衔远山，吞长江，浩浩汤汤，横无际涯。朝晖夕阴，气象万千。此则岳阳楼之大观也，前人之述备矣。然则北通巫峡，南极潇湘，迁客骚人，多会于此，览物之情，得无异乎？若夫淫雨霏霏，连月不开。阴风怒号，浊浪排空。日星隐曜，山岳潜形。商旅不行，樯倾楫摧。薄暮冥冥，虎啸猿啼。登斯楼也，则有去国怀乡，忧谗畏讥，满目萧然，感极而悲者矣。至若春和景明，波澜不惊。上下天光，一碧万顷。沙鸥翔集，锦鳞游泳。岸芷汀兰，郁郁青青。而或长烟一空，皓月千里。浮光跃金，静影沉璧。渔歌互答，此乐何极！登斯楼也，则有心旷神怡，宠辱偕忘，把酒临风，其喜洋洋者矣。嗟夫！予尝求古仁人之心，或异二者之为。何哉？不以物喜，不以己悲。居庙堂之高则忧其民，处江湖之远则忧其君。是进亦忧，退亦忧。然则何时而乐耶？其必曰：先天下之忧而忧，后天下之乐而乐乎！噫！微斯人，吾谁与归？",
    "醉翁亭记": "环滁皆山也。其西南诸峰，林壑尤美。望之蔚然而深秀者，琅琊也。山行六七里，渐闻水声潺潺，而泻出于两峰之间者，酿泉也。峰回路转，有亭翼然临于泉上者，醉翁亭也。作亭者谁？山之僧智仙也。名之者谁？太守自谓也。太守与客来饮于此，饮少辄醉，而年又最高，故自号曰醉翁也。醉翁之意不在酒，在乎山水之间也。山水之乐，得之心而寓之酒也。若夫日出而林霏开，云归而岩穴暝，晦明变化者，山间之朝暮也。野芳发而幽香，佳木秀而繁阴，风霜高洁，水落而石出者，山间之四时也。朝而往，暮而归，四时之景不同，而乐亦无穷也。",
    "曹刿论战": "十年春，齐师伐我。公将战，曹刿请见。其乡人曰：肉食者谋之，又何间焉？刿曰：肉食者鄙，未能远谋。乃入见。问：何以战？公曰：衣食所安，弗敢专也，必以分人。对曰：小惠未遍，民弗从也。公曰：牺牲玉帛，弗敢加也，必以信。对曰：小信未孚，神弗福也。公曰：小大之狱，虽不能察，必以情。对曰：忠之属也，可以一战。战则请从。公与之乘，战于长勺。公将鼓之。刿曰：未可。齐人三鼓。刿曰：可矣。齐师败绩。公将驰之。刿曰：未可。下视其辙，登轼而望之，曰：可矣。遂逐齐师。既克，公问其故。对曰：夫战，勇气也。一鼓作气，再而衰，三而竭。彼竭我盈，故克之。",
    "桃花源记": "晋太元中，武陵人捕鱼为业。缘溪行，忘路之远近。忽逢桃花林，夹岸数百步，中无杂树，芳草鲜美，落英缤纷。渔人甚异之，复前行，欲穷其林。林尽水源，便得一山。山有小口，仿佛若有光。便舍船，从口入。初极狭，才通人。复行数十步，豁然开朗。土地平旷，屋舍俨然，有良田美池桑竹之属。阡陌交通，鸡犬相闻。其中往来种作，男女衣着，悉如外人。黄发垂髫，并怡然自乐。见渔人，乃大惊，问所从来。具答之。便要还家，设酒杀鸡作食。村中闻有此人，咸来问讯。自云先世避秦时乱，率妻子邑人来此绝境，不复出焉，遂与外人间隔。问今是何世，乃不知有汉，无论魏晋。",
    "生于忧患死于安乐": "舜发于畎亩之中，傅说举于版筑之间，胶鬲举于鱼盐之中，管夷吾举于士，孙叔敖举于海，百里奚举于市。故天将降大任于是人也，必先苦其心志，劳其筋骨，饿其体肤，空乏其身，行拂乱其所为，所以动心忍性，曾益其所不能。人恒过，然后能改。困于心，衡于虑，而后作。征于色，发于声，而后喻。入则无法家拂士，出则无敌国外患者，国恒亡。然后知生于忧患而死于安乐也。",
    "鱼我所欲也": "鱼，我所欲也。熊掌，亦我所欲也。二者不可得兼，舍鱼而取熊掌者也。生，亦我所欲也。义，亦我所欲也。二者不可得兼，舍生而取义者也。生亦我所欲，所欲有甚于生者，故不为苟得也。死亦我所恶，所恶有甚于死者，故患有所不辟也。如使人之所欲莫甚于生，则凡可以得生者，何不用也？使人之所恶莫甚于死者，则凡可以辟患者，何不为也？由是则生而有不用也，由是则可以辟患而有不为也。是故所欲有甚于生者，所恶有甚于死者。非独贤者有是心也，人皆有之，贤者能勿丧耳。",
    "出师表": "先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。然侍卫之臣不懈于内，忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也。诚宜开张圣听，以光先帝遗德，恢弘志士之气，不宜妄自菲薄，引喻失义，以塞忠谏之路也。宫中府中，俱为一体。陟罚臧否，不宜异同。若有作奸犯科及为忠善者，宜付有司论其刑赏，以昭陛下平明之理，不宜偏私，使内外异法也。亲贤臣，远小人，此先汉所以兴隆也。亲小人，远贤臣，此后汉所以倾颓也。先帝在时，每与臣论此事，未尝不叹息痛恨于桓灵也。臣本布衣，躬耕于南阳，苟全性命于乱世，不求闻达于诸侯。先帝不以臣卑鄙，猥自枉屈，三顾臣于草庐之中，咨臣以当世之事，由是感激，遂许先帝以驱驰。",
    "赤壁赋": "壬戌之秋，七月既望，苏子与客泛舟游于赤壁之下。清风徐来，水波不兴。举酒属客，诵明月之诗，歌窈窕之章。少焉，月出于东山之上，徘徊于斗牛之间。白露横江，水光接天。纵一苇之所如，凌万顷之茫然。浩浩乎如冯虚御风，而不知其所止。飘飘乎如遗世独立，羽化而登仙。于是饮酒乐甚，扣舷而歌之。歌曰：桂棹兮兰桨，击空明兮溯流光。渺渺兮予怀，望美人兮天一方。客有吹洞箫者，倚歌而和之。其声呜呜然，如怨如慕，如泣如诉，余音袅袅，不绝如缕。舞幽壑之潜蛟，泣孤舟之嫠妇。苏子愀然，正襟危坐而问客曰：何为其然也？",
}

# 别名映射
ALIASES = {
    "论语": "论语六章",
    "论语六则": "论语六章",
}

OUT_DIR = r'D:\@VSwork\VSteach\_CHRIS'

def gen_html(text, cols=3):
    """生成古文字帖 HTML（不包含 UI，直接渲染网格）"""
    # 只保留汉字
    chars = [c for c in text if '一' <= c <= '鿿']
    if not chars:
        return None, None

    cells_per_char = 4
    grid_cols = cols * cells_per_char
    cells_per_row = grid_cols
    rows_per_page = 15

    # flat cells
    all_cells = []
    for ch in chars:
        for _ in range(2):
            all_cells.append((ch, True))   # trace
        for _ in range(2):
            all_cells.append((ch, False))  # empty

    while len(all_cells) % cells_per_row != 0:
        all_cells.append(('', None))  # empty placeholder

    total_cells = len(all_cells)
    total_cell_rows = total_cells // cells_per_row
    total_pages = (total_cell_rows + rows_per_page - 1) // rows_per_page

    def make_svg():
        return ('<svg viewBox="0 0 100 100">'
                '<line x1="0" y1="0" x2="100" y2="100" stroke="#f0d0d0" stroke-width="0.5"/>'
                '<line x1="100" y1="0" x2="0" y2="100" stroke="#f0d0d0" stroke-width="0.5"/>'
                '<line x1="50" y1="0" x2="50" y2="100" stroke="#f0d0d0" stroke-width="0.4"/>'
                '<line x1="0" y1="50" x2="100" y2="50" stroke="#f0d0d0" stroke-width="0.4"/>'
                '<rect x="1" y="1" width="98" height="98" fill="none" stroke="#e0c0c0" stroke-width="0.6"/>'
                '</svg>')

    pages_html = []
    for pi in range(0, total_cell_rows, rows_per_page):
        page_cells = all_cells[pi * cells_per_row : (pi + rows_per_page) * cells_per_row]
        rows_in_page = (len(page_cells) + cells_per_row - 1) // cells_per_row

        page_num = pi // rows_per_page + 1
        grid = ''
        for ri in range(rows_in_page):
            start = ri * cells_per_row
            end = min(start + cells_per_row, len(page_cells))
            grid += f'<div class="sheet" style="grid-template-columns:repeat({grid_cols},1fr)">'
            for ci in range(start, end):
                ch, mode = page_cells[ci]
                if mode is None:
                    grid += '<div class="cell empty"></div>'
                else:
                    is_end = ((ci - start) % cells_per_char == cells_per_char - 1)
                    cls = 'cell block-end' if is_end else 'cell'
                    svg = make_svg()
                    if mode:  # trace
                        grid += f'<div class="{cls}">{svg}<span class="char" style="color:#d0d0d0">{ch}</span></div>'
                    else:     # empty
                        grid += f'<div class="{cls}">{svg}</div>'
            # fill rest of row
            for _ in range(end, start + cells_per_row):
                grid += '<div class="cell empty"></div>'
            grid += '</div>'
        # blank rows to fill page
        for _ in range(rows_in_page, rows_per_page):
            grid += f'<div class="sheet" style="grid-template-columns:repeat({grid_cols},1fr)">'
            for _ in range(cells_per_row):
                grid += '<div class="cell empty"></div>'
            grid += '</div>'

        pages_html.append((page_num, total_pages, grid))

    html = f'''<!DOCTYPE html>
<html lang="zh-CN"><head>
<meta charset="UTF-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#fff;}}
.a4-page{{
  background:#fff;padding:12mm 10mm 5mm 10mm;
  width:210mm;min-height:297mm;position:relative;
  display:flex;flex-direction:column;page-break-after:always;
}}
.sheet-header{{display:flex;justify-content:space-between;align-items:baseline;padding:0 2px 4px 2px;border-bottom:2px solid #c0392b;margin-bottom:3px;}}
.sheet-header .title{{font-size:14px;font-weight:700;color:#c0392b;font-family:"KaiTi","STKaiti","SimSun",serif;}}
.sheet-header .info{{font-size:9px;color:#999;}}
.grid-area{{flex:1;display:flex;flex-direction:column;gap:0;}}
.sheet{{display:grid;gap:0;width:100%;}}
.cell{{position:relative;aspect-ratio:1;border:0.5px solid #e8d0d0;display:flex;align-items:center;justify-content:center;background:#fff;}}
.cell svg{{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;}}
.cell .char{{font-size:50px;position:relative;z-index:1;font-family:"KaiTi","STKaiti","SimSun",serif;user-select:none;line-height:1;pointer-events:none;font-weight:500;}}
.cell.empty{{background:#fafafa;}}
.cell.block-end{{border-right:2px solid #c0392b;}}
.footer-tips{{margin-top:auto;padding:4px 6px 2px 6px;border-top:1px solid #e0e0e0;font-size:10px;color:#666;line-height:1.5;text-align:left;}}
.footer-tips strong{{color:#c0392b;}}
.footer-tips .row{{margin:0;}}
@media print{{body{{background:#fff;}}.a4-page{{box-shadow:none;margin:0;padding:10mm 8mm 4mm 8mm;width:100%;min-height:100vh;page-break-after:always;}}.cell .char{{font-size:50px;}}@page{{margin:0;size:A4 portrait;}}}}
</style>
</head><body>
'''
    for pn, tp, grid in pages_html:
        tips = ('<div class="row">1. <strong>中线对齐</strong> -- 字的重心在格子中央</div>'
                '<div class="row">2. <strong>大小一致</strong> -- 每个字占格子70%-80%</div>'
                '<div class="row">3. <strong>笔画力度</strong> -- 笔画清晰可见，不要过轻</div>')
        html += f'<div class="a4-page">'
        html += f'<div class="sheet-header"><span class="title">古文练字 - 描红x2 + 临写x2</span><span class="info">第 {pn} 页 / 共 {tp} 页 - 共{len(chars)}字</span></div>'
        html += f'<div class="grid-area">{grid}</div>'
        html += f'<div class="footer-tips"><strong>练字要点：</strong>{tips}</div>'
        html += '</div>'
    html += '</body></html>'
    return html, len(chars)

def save_to_pdf(title, text):
    """生成 HTML 并用 Edge 打印为 PDF"""
    html, char_count = gen_html(text)
    if not html:
        print(f'[WARN] 古文《{title}》没有汉字内容')
        return None

    # 保存 HTML
    safe = title.replace('《','').replace('》','').replace(' ','')
    html_path = os.path.join(OUT_DIR, f'__temp/字帖_{safe}.html')
    pdf_path  = os.path.join(OUT_DIR, f'字帖_{safe}.pdf')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'HTML: {html_path}')

    # 用 Edge headless 打印为 PDF
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
        print(f'[WARN] 未找到 Edge/Chrome，无法自动转 PDF')
        print(f'   请打开 {html_path} -> Ctrl+P -> 另存为 PDF')
        return html_path

    abs_html = os.path.abspath(html_path)
    abs_pdf  = os.path.abspath(pdf_path)
    abs_out  = os.path.dirname(abs_pdf)
    os.makedirs(abs_out, exist_ok=True)

    cmd = f'"{browser}" --headless=new --disable-gpu --no-margins --print-to-pdf-no-header --print-to-pdf="{abs_pdf}" "file://{abs_html}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)

    if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 1000:
        print(f'[OK] PDF: {abs_pdf} ({os.path.getsize(abs_pdf)//1024} KB)')
        print(f'   共 {char_count} 汉字')
        # 删除临时 HTML
        os.remove(html_path)
        return abs_pdf
    else:
        print(f'[WARN] PDF 生成可能失败 ({result.stderr[:200]})')
        print(f'   请打开 {html_path} -> Ctrl+P -> 另存为 PDF')
        # 保留 HTML 供手动打印
        return html_path

def list_guwen():
    print('可用的古文：')
    for name in sorted(GUWEN_DB):
        text = GUWEN_DB[name]
        chars = sum(1 for c in text if '一' <= c <= '鿿')
        print(f'  - {name} ({chars}字)')
    print(f'\n共 {len(GUWEN_DB)} 篇')

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or args[0] in ('-l', '--list', '-h', '--help'):
        list_guwen()
        sys.exit(0)

    name = ' '.join(args)
    name = ALIASES.get(name, name)
    text = GUWEN_DB.get(name)
    if not text:
        print(f'未找到《{name}》，可用古文：')
        list_guwen()
        sys.exit(1)

    result = save_to_pdf(name, text)
    if result:
        print(f'\n已保存到: {result}')
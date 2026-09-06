#!/usr/bin/env python3
"""把 FOGG 官方等级表编成 _build/curriculum/*.json(单一真源)。
只在等级表变化时重跑: python _build/curriculum/_make_curriculum.py
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))


def W(name, obj):
    open(os.path.join(HERE, name + '.json'), 'w', encoding='utf8', newline='\n').write(
        json.dumps(obj, ensure_ascii=False, indent=1) + '\n')


# ---------- CW 创意写作 ----------
cw_levels = [
    (0, '8-9', '掌握基本故事结构、塑造人物和场景、激发表达欲',
     [('my-first-story', '我的第一个故事', 'My First Story'), ('book-of-hopes', '希望之书', 'The Book of Hopes')]),
    (1, '9-10', '写短篇故事、从民间故事与名著中汲取灵感、建立描写语言',
     [('year-full-of-stories', '一年的故事', 'A Year Full of Stories'), ('just-so-stories', '动物起源故事', 'Just So Stories (Animal Creation Story)')]),
    (2, '9-10', '生动描写、Show not tell、独特视角',
     [('painting-with-words', '写出画面感', 'Painting with Words'), ('travel-writing', '旅行故事', 'Travel Writing')]),
    (3, '10-11', '扎实的故事结构、冲突与解决、主题',
     [('how-to-write-a-good-story', '如何写出好故事', 'How to Write a Good Story'), ('brave-new-world', '打造新世界', 'Brave New World')]),
    (4, '10-11', '节奏与氛围、对话、把想象力和技巧结合起来',
     [('engaging-story', '让故事吸引人', 'How to Make Your Story Engaging'), ('fantasy-story', '创作奇幻故事', 'Write Your Own Fantasy Story')]),
    (5, '11-12', '张力、象征、人物动机',
     [('spooky-story', '创作恐怖故事', 'Write Your Own Spooky Story'), ('myth', '创作你的神话', 'Write Your Own Myth')]),
    (6, '11-12', '关键故事结构、塑造情节、想象力与创造力',
     [('seven-basic-plots', '7 个经典故事线', 'The 7 Basic Plots'), ('adventure-story', '创作冒险故事', 'Write Your Own Adventure Story')]),
    (7, '12-14', '向名著学习、发展人物与主题、英雄之旅',
     [('classic-modern-authors', '向经典与现代作家学习', 'Learn from Classic and Modern Authors'), ('heros-journey', '英雄之旅', "Hero's Journey")]),
    (8, '12-14', '悬念与反转、结构、锋利的语言与有力的表达',
     [('crime-story', '创作侦探故事', 'Write Your Own Crime Story'), ('short-writing-challenge', '短篇故事挑战', 'Short Writing Challenge')]),
    (9, '13-15', '融合事实与想象、调研、作者声音',
     [('historical-story', '创作历史小说', 'Write Your Own Historical Story'), ('life-writing', '纪实文学', 'Life Writing')]),
    (10, '13-15', '含蓄与声音、拓展想象、世界观构建',
     [('unreliable-narrators', '不靠谱的叙述人', 'Unreliable Narrators'), ('speculative-futures', '幻想未来 / 架空历史', 'Speculative Futures or Alternative Histories')]),
    (11, '14-16', '不同形式、节奏与细节、打破习惯换个角度思考',
     [('writing-across-media', '跨媒介写作', 'Writing Across Media'), ('constraint-based-writing', '被限制的写作', 'Constraint-Based Writing')]),
]
W('fogg-cw', {
    'id': 'fogg-cw', 'org': 'FOGG', 'code': 'CW', 'name': '创意写作', 'en': 'Creative Writing', 'accent': '#C0603A',
    'desc': 'FOGG 创意写作能力进阶:L0–L11,每级两个单元,每单元 10 周(= 一个学期)。',
    'levels': [{'level': l, 'age': a, 'goal': g,
                'units': [{'id': f'l{l:02d}-u{i + 1}-{s}', 'n': i + 1, 'title': z, 'en': e} for i, (s, z, e) in enumerate(us)]}
               for l, a, g, us in cw_levels]})

# ---------- EN 英文文学精读 ----------
en_levels = [
    (1, '9-10', '320L-680L', '开启多元化的基础阅读', '故事结构 | 识别观点 | 图文阅读 | 诗歌修辞',
     [("Charlotte's Web", '夏洛的网'), ('Who Was Leonardo da Vinci', '谁是达·芬奇'), ('New Kid', '新来的孩子'), ('A Light in the Attic', '阁楼上的光')]),
    (2, '9-10', '600L-790L', '学会读懂文字背后的深意', '归纳主题 | 多视角 | 观点论述 | 叙事写作',
     [('Coraline', '鬼妈妈'), ('Horrible Histories: Groovy Greeks', '恐怖的历史:古希腊人'), ('Wonder', '奇迹男孩'), ('Pushing Up the Sky', '顶天立地')]),
    (3, '10-11', '400L-810L', '开启批判性阅读', '社会背景分析 | 概括信息 | 同理心 | 诗歌象征',
     [('The Giver', '记忆传授人'), ('Science Comics: Plagues', '科学漫画:瘟疫'), ('Bridge to Terabithia', '通往泰瑞比西亚的桥'), ('Overheard in a Tower Block', '')]),
    (4, '10-11', '500L-890L', '读懂复杂、多层次的文字', '多线情节 | 作者意图 | 理解潜台词 | 对比手法',
     [('Where the Mountain Meets the Moon', '月夜仙踪'), ('I Am Malala', '我是马拉拉'), ('Shiloh', '喜乐与我'), ('Harry Potter and the Cursed Child', '哈利·波特与被诅咒的孩子')]),
    (5, '11-12', '530L-950L', '掌握经典结构,深度理解主题', '英雄之旅 | 隐喻理解 | 主题分析 | 诗歌解读',
     [('Percy Jackson and the Lightning Thief', '波西·杰克逊与神火之盗'), ('When Stars Are Scattered', '当星星散落'), ('Bud, Not Buddy', '巴德,不是巴迪'), ('Cast Away: Poems for Our Time', '')]),
    (6, '11-12', '720L-1040L', '深度分析结构、逻辑、手法', '复杂叙事 | 短篇的特点 | 说理逻辑 | 戏剧元素',
     [('The Blossom and the Firefly', '花与萤火虫'), ('Lincoln: A Photobiography', '林肯:摄影传记'), ('Ten Sorry Tales', ''), ('Our Town', '我们的小镇')]),
    (7, '12-14', '680L-1110L', '学会文学阅读与批判性阅读', '文学评论 | 议论文写作 | 深层含义理解 | 诗歌叙事',
     [('The Martian', '火星救援'), ('Chew On This', '快餐的恐怖真相'), ('The Boy in the Striped Pyjamas', '穿条纹衣的男孩'), ('The Crossover (Graphic Novel)', '')]),
    (8, '12-14', '1000L-1090L', '学会解构复杂文本,培养批判力', '深刻主题 | 图像解读 | 复杂叙事 | 高级戏剧技巧',
     [('The Hobbit', '霍比特人'), ('Sapiens: A Graphic History', '人类简史:图像版'), ('The Curious Incident of the Dog in the Night-Time', '深夜小狗神秘事件'), ('Twelve Angry Men', '十二怒汉')]),
    (9, '14-16', '870L-1000L', '学习文学评论式阅读,驾驭复杂文本', '整本书分析 | 观点提炼 | 诗歌演变 | 回答论文式问题',
     [('To Kill a Mockingbird', '杀死一只知更鸟'), ('Bobby', '芭比'), ('100 Poets', '100 位诗人')]),
    (10, '14-16', '590L-990L', '为文学类考试(IB / A Level)准备阅读与学术写作', '多重叙事 | 多个短篇综合阅读 | 莎剧解读 | 回答论文式问题',
     [('Maus', '鼠族'), ('The Illustrated Man', '插图人'), ('Macbeth', '麦克白')]),
]


def slug(en):
    words = [re.sub(r'[^a-z0-9]+', '', w.lower()) for w in en.split(' ')]
    words = [w for w in words if w and w not in ('the', 'a', 'and', 'of', 'in', 'for')]
    return '-'.join(words[:3]) or 'book'


W('fogg-en', {
    'id': 'fogg-en', 'org': 'FOGG', 'code': 'EN', 'name': '英文文学精读', 'en': 'English Literature Reading', 'accent': '#2E5A66',
    'desc': 'FOGG 英文文学精读:L1–L10,每级 4 本书(每本书一个单元)。基础阅读 → 深度理解 → 批判思维 → 学术表达。建议选择比当前年龄段低 1-2 级;蓝思值仅作参考。',
    'levels': [{'level': l, 'age': a, 'lexile': lx, 'goal': g, 'skills': sk,
                'units': [{'id': f'l{l:02d}-u{i + 1}-{slug(e)}', 'n': i + 1, 'title': z or e, 'en': e} for i, (e, z) in enumerate(bs)]}
               for l, a, lx, g, sk, bs in en_levels]})

# ---------- CN 中文阅读 ----------
cn_levels = [
    (1, '7-9', '500字+', '养成中文阅读兴趣和习惯', '建立习惯 / 读懂故事 / 说出想法', ['一古拉:可怕的练胆大会', '电饭锅参加运动会', '谁在床下养了一朵云'], 10),
    (2, '8-9', '700字+', '逐步走向中文自主阅读', '整本阅读 / 把握情节 / 读懂人物', ['青蛙和蟾蜍', '父与子漫画成语', '穿内裤的狼'], 10),
    (3, '8-10', '900字+', '夯实中文自主阅读能力', '阅读积累 / 抓住重点 / 拓展题材', ['我是罗莎·帕克斯', '胡椒罐大楼的秘密', '昨天晚上爸爸回来晚了,那是因为……'], 9),
    (4, '9-10', '1200字+', '从桥梁书走向纯文字书', '大段文字阅读 / 读懂结构 / 用阅读获取信息', ['趣玩小西游记', '用两万年修厕所', '兔子屋的秘密'], 8),
    (5, '10-11', '1500字+', '读懂更复杂、多元的中文书', '多类型阅读 / 独立思考 / 形成观点', ['福尔摩斯大侦探', '问个不停', '如果历史是一群喵'], 8),
    (6, '10-12', '1800字+', '进入中文长篇儿童文学阅读', '初步文学赏析 / 表达自己的观点 / 调研分享', ['把日记藏起来的日子', '向着明亮那方', '我在明朝做消防员'], 8),
    (7, '11-12', '2000字+', '提升中文阅读的深度', '读懂深意 / 比较分析 / 有理有据的表达', ['天蓝色的彼岸', '最美最美中国童话', '法布尔老师的昆虫教室'], 7),
    (8, '11-12', '2200字+', '走向更成熟、深入的中文阅读', '阅读经典 / 读懂科普 / 探讨深度议题', ['草房子', '罗大里的戏剧乐园', '动物的底事'], 8),
]
W('fogg-cn', {
    'id': 'fogg-cn', 'org': 'FOGG', 'code': 'CN', 'name': '中文阅读', 'en': 'Chinese Reading', 'accent': '#8A5A2B',
    'desc': 'FOGG 中文阅读成长阶梯:Lv1–Lv8 分级泛读。Lv1-4 中文自主阅读起步;Lv5-8 成熟与深度中文阅读。单元按书目建立,书目数据待补。',
    'levels': [{'level': l, 'age': a, 'vocab': v, 'goal': g, 'skills': sk, 'books': bs, 'bookCount': n, 'units': []}
               for l, a, v, g, sk, bs, n in cn_levels]})

# ---------- EW 议论文写作(暂无官方等级表)----------
W('fogg-ew', {
    'id': 'fogg-ew', 'org': 'FOGG', 'code': 'EW', 'name': '议论文写作', 'en': 'Essay Writing', 'accent': '#7A6A9E',
    'desc': 'FOGG 议论文写作:目前没有官方等级表(仅 4 个班)。等级与单元先按报名等级暂放,以后补齐。',
    'levels': [{'level': l, 'age': '', 'goal': '(等级表待补)',
                'units': [{'id': f'l{l:02d}-u1-tbd', 'n': 1, 'title': '单元 1(名称待定)', 'en': 'Unit 1 (TBD)'},
                          {'id': f'l{l:02d}-u2-tbd', 'n': 2, 'title': '单元 2(名称待定)', 'en': 'Unit 2 (TBD)'}]}
               for l in (1, 2, 3, 4, 5, 6)]})
print('ok')

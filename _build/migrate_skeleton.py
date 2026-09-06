# -*- coding: utf-8 -*-
"""一次性迁移:courses/<old-unit>/ → courses/<program>/<level-unit>/<class>/ ,key 不变。"""
import os, re, json, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def read(p): return open(p, encoding='utf8').read()
def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf8', newline='\n').write(s)
def git(*a): subprocess.check_call(['git', *a])

ALEX_OUTLINE = [
 "W1 观察与推理 deduce", "W2 玩弄读者怀疑(一级/二级、frame 嫁祸、审问问题、打造侦探)",
 "W3 分享侦探 + 开头五种方式 + 视角代词", "W4 开头反馈、看图写场景、作者的选择、反派档案",
 "W5 连环杀手、侦探即凶手、三法则、red herring、先写结局", "W6 逆向工程、Cluedo 群戏、动机+alibi",
 "W7 逐句精修、克里斯蒂视频、人物层次、奖杯失窃案", "W8 工坊互评、解谜、riddle vs story", "W9 从谜题到故事"]

CLASSES = {
 '2026s2-cw-l7-8-alex-mon': dict(program='fogg-cw', unit='l08-u1-crime-story', cls='2026s2-alex-mon',
    json={"id":"2026s2-alex-mon","year":2026,"term":"2026 S2","teacher":"Alex","weekday":"周一",
          "zoom":"CW_26_S2_MON_L7-8_Alex","enroll":"L7-8","standard":True,
          "style":"节奏快、以提问推进,大量即兴小练习;每周先聊作业再进入新技巧,爱用真实侦探小说与影视做例子。",
          "students":"Alice · Kaelyn · xuanying · Chen Yuhan",
          "speaker":"Teacher Alex","length":"约60分钟 · 周一","outline":ALEX_OUTLINE},
    sub='创意写作 · Level 8 · 创作侦探故事 · 2026 · Alex', eyebrow='FOGG 创意写作 · Level 8 · 创作侦探故事 · 2026 S2 · Teacher Alex', level='8'),
 '2026s2-cw-l1-2-tim-mon': dict(program='fogg-cw', unit='l02-u1-painting-with-words', cls='2026s2-tim-mon',
    json={"id":"2026s2-tim-mon","year":2026,"term":"2026 S2","teacher":"Tim","weekday":"周一",
          "zoom":"CW_26_S2_MON_L1-2_Tim","enroll":"L1-2","standard":True,
          "style":"(待补充)","students":"","speaker":"Teacher Tim","length":"约60分钟 · 周一","outline":[]},
    sub='创意写作 · Level 2 · 写作即绘画 · 2026 · Tim', eyebrow='FOGG 创意写作 · Level 2 · 写作即绘画 · 2026 S2 · Teacher Tim', level='2'),
 '2026s2-ew-l3-4-alex-mon': dict(program='fogg-ew', unit='l04-u1-tbd', cls='2026s2-alex-mon',
    json={"id":"2026s2-alex-mon","year":2026,"term":"2026 S2","teacher":"Alex","weekday":"周一",
          "zoom":"EW_26_S2_MON_L3-4_Alex","enroll":"L3-4","standard":True,
          "style":"(待补充)","students":"","speaker":"Teacher Alex","length":"约60分钟 · 周一","outline":[]},
    sub='议论文写作 · Level 4 · 单元 1 · 2026 · Alex', eyebrow='FOGG 议论文写作 · Level 4 · 单元 1 · 2026 S2 · Teacher Alex', level='4'),
}

# 表情清理表(课页 UI 文案)
EMOJI = [
 ('>📒 生词本 · 划线 · 笔记<', '>生词本 · 划线 · 笔记<'),
 ('☁️ 同步</button>', '同步</button>'),
 ('>📌 钉这里<', '>钉这里<'), ('>🔖 回书签<', '>回书签<'), ('>🔊 朗读<', '>朗读<'), ('>⋯ 更多<', '>更多<'),
 ('>📤 导出学习笔记<', '>导出学习笔记<'),
 ('>🖍 高亮<', '>高亮<'), ('>📖 查词<', '>查词<'), ('>📝 高亮+笔记<', '>高亮+笔记<'),
 ('>📝 写/改笔记<', '>写/改笔记<'), ('>📖 查这个词<', '>查这个词<'), ('>🗑 删除这条高亮<', '>删除这条高亮<'),
 ('>📸 截图保存<', '>截图保存<'), ('>📖 生词本<', '>生词本<'), ('>🖍 划线笔记<', '>划线笔记<'), ('>📝 总笔记<', '>总笔记<'),
 ('>☁️ 多设备同步设置<', '>多设备同步设置<'),
 ('💡 选中英文', '选中英文'), ('「📤 导出」', '「导出」'),
]

def migrate_page(old, new, c, depth_fix):
    s = read(old)
    fn = os.path.basename(new)
    wk = int(re.match(r'wk(\d+)', fn).group(1))
    # 1 资源路径 & 目录链接
    s = s.replace('href="../../app.css"', 'href="../../../../app.css"')
    s = s.replace('src="../../app.js"', 'src="../../../../app.js"')
    s = s.replace('href="../../index.html">🏠 回到目录</a>', 'href="../../../../index.html">回到目录</a>')
    s = s.replace('href="index.html">📚 本单元总览</a>', 'href="../index.html">本单元总览</a>')
    # 2 page-meta:unit → 新 id,加 program/class
    def fix_meta(m):
        meta = json.loads(m.group(1))
        out = {'key': meta['key'], 'kind': 'lesson', 'program': c['program'], 'unit': c['unit'], 'class': c['cls']}
        for k, v in meta.items():
            if k in ('key', 'kind', 'unit'): continue
            out[k] = v
        return '<script type="application/json" id="page-meta">\n' + json.dumps(out, ensure_ascii=False, indent=1) + '\n</script>'
    s, n = re.subn(r'<script type="application/json" id="page-meta">\s*(\{.*?\})\s*</script>', fix_meta, s, count=1, flags=re.S)
    assert n == 1, old
    # 3 文案
    s = re.sub(r'<div class="map-sub">[^<]*</div>', lambda m: f'<div class="map-sub">{c["sub"]} · Week {wk}</div>', s, count=1)
    s = re.sub(r'<div class="eyebrow ui">[^<]*</div>', lambda m: f'<div class="eyebrow ui">{c["eyebrow"]}</div>', s, count=1)
    s = re.sub(r'<span>Level [\d-]+ · Week', lambda m: f'<span>Level {c["level"]} · Week', s, count=1)
    s = re.sub(r'整理自 FOGG Level [\d-]+ ', lambda m: f'整理自 FOGG Level {c["level"]} ', s, count=1)
    if depth_fix:  # 标准页:更多菜单瘦身 + 侧栏底部按钮 + 去表情
        s = re.sub(r'<a href="\.\./\.\./\.\./\.\./index\.html">回到目录</a>\s*<a href="\.\./index\.html">本单元总览</a>\s*', '', s, count=1)
        s = s.replace('  </nav>\n</aside>', '  </nav>\n  <div class="map-foot"><a href="../index.html">本单元总览</a><a href="../../../../index.html">回到目录</a></div>\n</aside>', 1)
        assert 'map-foot' in s, old
        for a, b in EMOJI:
            s = s.replace(a, b)
    write(new, s)

for old_dir, c in CLASSES.items():
    new_dir = f"courses/{c['program']}/{c['unit']}/{c['cls']}"
    os.makedirs(new_dir, exist_ok=True)
    write(f'{new_dir}/class.json', json.dumps(c['json'], ensure_ascii=False, indent=1) + '\n')
    for fn in sorted(os.listdir(f'courses/{old_dir}')):
        if not fn.startswith('wk'): continue
        old = f'courses/{old_dir}/{fn}'; new = f'{new_dir}/{fn}'
        git('mv', old, new)
        src = read(new)
        migrate_page(new, new, c, depth_fix='href="../../app.css"' in src)
        print('moved', new)
    git('rm', '-q', f'courses/{old_dir}/unit.json', f'courses/{old_dir}/index.html')
    if os.path.isdir(f'courses/{old_dir}'):
        os.rmdir(f'courses/{old_dir}')
print('done')

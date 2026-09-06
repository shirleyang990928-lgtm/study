#!/usr/bin/env python3
"""
assemble.py — 用 Week1 页做外壳,拼出一堂新课页(含 page-meta、../../ 资源路径)。
用法:
  python _build/assemble.py wkN_meta.json wkN_nav.html wkN_body.html wkN_preset.json
meta.json 字段(与 page-meta 一致):
  unit, week, date, key, title, en, desc, status(默认 draft), students(可选), length(可选)
输出到 courses/<unit>/wkNN-YYYY-MM-DD.html;完成后请运行 python _build/build_site.py。
"""
import re, json, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHELL = os.path.join(ROOT, 'courses', '2026s2-cw-l7-8-alex-mon', 'wk01-2026-06-29.html')

if len(sys.argv) != 5:
    print(__doc__); sys.exit(1)
metafile, navfile, bodyfile, presetfile = sys.argv[1:5]
meta = json.load(open(metafile, encoding='utf-8'))
for k in ('unit', 'week', 'date', 'key', 'title', 'en'):
    if not meta.get(k):
        sys.exit(f'meta.json 缺少 {k}')
unit = json.load(open(os.path.join(ROOT, 'courses', meta['unit'], 'unit.json'), encoding='utf-8'))
wk = int(meta['week']); date = meta['date']
title_en = meta['en']; title_zh = meta['title']
students = meta.get('students', 'Alice · Kaelyn · xuanying · Chen Yuhan')
length = meta.get('length', '约60分钟')
teacher = unit['teacher']; level = unit['level']; tname = {'cw': '创意写作', 'ew': '议论文', 'cn': '中文阅读', 'en': '英文精读'}.get(unit['type'], unit['type'])

def R(pat, rep, s):
    return re.sub(pat, lambda m: rep, s, count=1)

shell = open(SHELL, encoding='utf-8').read()
shell = R(r'<title>[\s\S]*?</title>', f'<title>{teacher} {tname}课 Week {wk} · 学习笔记本 | {title_zh}</title>', shell)
pm = {
    'key': meta['key'], 'kind': 'lesson', 'unit': meta['unit'], 'week': wk,
    'status': meta.get('status', 'draft'), 'date': date,
    'title': title_zh, 'en': title_en, 'desc': meta.get('desc', ''),
    'speaker': unit.get('speaker', f'Teacher {teacher}'), 'length': unit.get('length', length), 'tags': meta.get('tags', []),
}
shell = R(r'<script type="application/json" id="page-meta">[\s\S]*?</script>',
          '<script type="application/json" id="page-meta">\n' + json.dumps(pm, ensure_ascii=False, indent=1) + '\n</script>', shell)
shell = R(r'<h1>[\s\S]*?</h1>', f'<h1>{title_en}<span class="zh-t">Week {wk} {tname}课 —— {title_zh}</span></h1>', shell)
shell = R(r'<div class="map-sub">[\s\S]*?</div>', f'<div class="map-sub">Teacher {teacher} · {tname} L{level} · Week {wk}</div>', shell)
shell = R(r'<span>学生：[^<]*</span>', f'<span>学生：{students}</span>', shell)
shell = R(r'<span>Level [^<]*</span>', f'<span>Level {level} · Week {wk} · {length}</span>', shell)
shell = R(r'  <nav class="map" id="map">[\s\S]*?</nav>', open(navfile, encoding='utf-8').read().rstrip('\n'), shell)
body = open(bodyfile, encoding='utf-8').read()
s = shell.index('<!-- S1 -->'); e = shell.index('<footer')
shell = shell[:s] + body + '\n' + shell[e:]
shell = R(r'整理自 FOGG[\s\S]*?供学习参考', f'整理自 FOGG Level {level} {tname}课 Week {wk} 课堂录音({length},全程) · 英文原文经口语清理 · 中文翻译供学习参考', shell)
preset = open(presetfile, encoding='utf-8').read().strip()
new_cfg = ("window.PAGE_CONFIG={\n  key:'" + meta['key'] + "',\n  title:'" + f"{teacher} {tname}课 Week {wk}" +
           "',\n  exportTitle:'" + f"{teacher} {tname}课 Week {wk} · 我的学习笔记" + "',\n  preset:" + preset + "\n};")
shell = R(r'window\.PAGE_CONFIG=\{[\s\S]*?\};', new_cfg, shell)
assert 'href="../../app.css"' in shell and 'src="../../app.js"' in shell
out = os.path.join(ROOT, 'courses', meta['unit'], f'wk{wk:02d}-{date}.html')
open(out, 'w', encoding='utf-8', newline='\n').write(shell)
print(f'✓ 写出 {os.path.relpath(out, ROOT)} ({len(shell)} 字符)。下一步: python _build/build_site.py')

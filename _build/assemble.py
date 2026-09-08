# -*- coding: utf-8 -*-
"""把 meta.json + nav.html + body.html + preset.json 装进 _build/templates/lesson.html,
写出 courses/<program>/<unit>/<class>/wkNN-YYYY-MM-DD.html。

用法: python _build/assemble.py wkN_meta.json wkN_nav.html wkN_body.html wkN_preset.json

meta.json 必填: program, unit, class, week, date, key, title, en, desc, status
可选: students, length, tags(list), speaker
其余(老师/学期/单元名/课程名)从 class.json 与 _build/curriculum/*.json 自动取。
"""
import sys, os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def rd(p):
    with open(p, encoding='utf-8') as f:
        return f.read()

def main():
    if len(sys.argv) != 5:
        print(__doc__); sys.exit(2)
    meta = json.loads(rd(sys.argv[1]))
    nav = rd(sys.argv[2]).rstrip('\n')
    if 'class="map"' not in nav:
        nav = '  <nav class="map" id="map">' + chr(10) + nav + chr(10) + '  </nav>'
    body = rd(sys.argv[3]).rstrip('\n')
    preset = rd(sys.argv[4]).strip()
    json.loads(preset)  # 校验

    need = ['program', 'unit', 'class', 'week', 'date', 'key', 'title', 'en', 'desc', 'status']
    miss = [k for k in need if k not in meta]
    if miss:
        sys.exit('meta.json 缺字段: ' + ', '.join(miss))
    prog_id, unit_id, cls_id = meta['program'], meta['unit'], meta['class']
    week = int(meta['week']); date = meta['date']
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        sys.exit('date 格式应为 YYYY-MM-DD')
    if not re.match(r'^cls-\d{8}-[a-z]+-[a-z]+-l[\d-]+-wk\d+$', meta['key']):
        print('提示: key 不是标准格式 cls-YYYYMMDD-<type>-<teacher>-l<level>-wk<week>:', meta['key'])

    prog = json.loads(rd(os.path.join(ROOT, '_build', 'curriculum', prog_id + '.json')))
    unit = None; level = None
    for lv in prog['levels']:
        for u in lv['units']:
            if u['id'] == unit_id:
                unit, level = u, lv
    if not unit:
        sys.exit(f'单元 {unit_id} 不在 {prog_id} 课程表里')
    cdir = os.path.join(ROOT, 'courses', prog_id, unit_id, cls_id)
    cjson = os.path.join(cdir, 'class.json')
    if not os.path.exists(cjson):
        sys.exit(f'找不到 {cjson},先建 class.json')
    cls = json.loads(rd(cjson))

    teacher = cls['teacher']; term = cls['term']; L = level['level']
    pname = prog['name']; org = prog.get('org', 'FOGG')
    length = meta.get('length') or cls.get('length', '约60分钟')
    students = meta.get('students') or cls.get('students', '')
    speaker = meta.get('speaker') or cls.get('speaker', f'Teacher {teacher}')
    tags = meta.get('tags', [])

    page_meta = {
        'key': meta['key'], 'kind': 'lesson', 'program': prog_id, 'unit': unit_id, 'class': cls_id,
        'week': week, 'status': meta['status'], 'date': date,
        'title': meta['title'], 'en': meta['en'], 'desc': meta['desc'],
        'speaker': speaker, 'length': length, 'tags': tags,
    }

    def js1(s):  # 放进 JS 单引号字符串
        return str(s).replace('\\', '\\\\').replace("'", "\\'")

    fill = {
        'TITLE_TAG': f"{meta['title']} · {teacher} {pname}课 Week {week} · Level {L} {unit['title']}",
        'ROOT': '../../../../',
        'META_JSON': json.dumps(page_meta, ensure_ascii=False, indent=1),
        'MAP_SUB': f"{pname} · Level {L} · {unit['title']} · {cls['year']} · {teacher} · Week {week}",
        'NAV': nav,
        'UNIT_INDEX': '../index.html',
        'EYEBROW': f"{org} {pname} · Level {L} · {unit['title']} · {term} · Teacher {teacher}",
        'H1_EN': meta['en'],
        'H1_ZH': meta['title'],
        'SPEAKER': speaker,
        'STUDENTS': students,
        'LEVEL_LINE': f"Level {L} · Week {week} · {length}",
        'BODY': body,
        'FOOTER': f"整理自 {org} Level {L} {pname}课 Week {week} 课堂录音({length.split(' · ')[0]},全程) · 英文原文经口语清理 · 中文翻译供学习参考",
        'KEY': js1(meta['key']),
        'PC_TITLE': js1(f"{teacher} {pname}课 Week {week}"),
        'EXPORT_TITLE': js1(f"{teacher} {pname}课 Week {week} · {meta['title']} · 我的学习笔记"),
        'PRESET': preset,
    }
    tpl = rd(os.path.join(ROOT, '_build', 'templates', 'lesson.html'))
    out = re.sub(r'\{\{(\w+)\}\}', lambda m: fill[m.group(1)], tpl)
    left = re.findall(r'\{\{\w+\}\}', out)
    if left:
        sys.exit('模板占位符没填完: ' + ' '.join(left))

    fname = f'wk{week:02d}-{date}.html'
    dst = os.path.join(cdir, fname)
    with open(dst, 'w', encoding='utf-8', newline='\n') as f:
        f.write(out)
    rel = os.path.relpath(dst, ROOT).replace('\\', '/')
    print(f'写出 {rel} ({len(out)//1024} KB) · key={meta["key"]}')
    print('下一步: python _build/build_site.py && node _build/testwkX.js ' + rel)

if __name__ == '__main__':
    main()

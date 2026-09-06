#!/usr/bin/env python3
"""
build_site.py — 扫描全站页面,校验并生成 catalog.js / search/*.js / 各单元总览页。
用法: python _build/build_site.py        (任何目录都行)
数据来源(单一真源):
  _build/curriculum/<program>.json                               课程体系(Level → 单元)
  courses/<program>/<unit>/<class>/class.json                    某年某老师的班级信息
  courses/<program>/<unit>/<class>/wkNN-YYYY-MM-DD.html          课页(<script id="page-meta">)
  talks/<year>/*.html, internal/<year>/*.html                    讲座/内部页(同样用 page-meta)
index.html 只读 catalog.js,不需要手改。
"""
import json, os, re, sys, html, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

META_RE = re.compile(r'<script type="application/json" id="page-meta">\s*(\{.*?\})\s*</script>', re.S)
H2_RE = re.compile(r'<h2[^>]*>(.*?)</h2>', re.S)
TAG_RE = re.compile(r'<[^>]+>')
BOX_RE = re.compile(r'<div class="(?:keypoints|explain)[^"]*"[^>]*>(.*?)</div>', re.S)
PRESET_RE = re.compile(r'preset\s*:\s*(\[.*?\])', re.S)
WORD_RE = re.compile(r'''(?:word|zh)\s*["']?\s*:\s*['"]([^'"]+)['"]''')
STATUS = {'ok': ('已达标', 'ok'), 'redo': ('待重做', 'redo'), 'draft': ('草稿', 'draft')}
WEEKS = 10


def strip(s):
    s = TAG_RE.sub(' ', s)
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def read(p):
    return open(p, encoding='utf8').read()


def write(p, s):
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
    open(p, 'w', encoding='utf8', newline='\n').write(s)


def E(s):
    return html.escape(str(s if s is not None else ''))


errors = []


def err(msg):
    errors.append(msg)


# ---------- 课程体系 ----------
programs = {}
for pj in sorted(glob.glob('_build/curriculum/*.json')):
    pr = json.loads(read(pj))
    pr['levelMap'] = {}
    for lv in pr['levels']:
        for u in lv['units']:
            u['level'] = lv['level']
            u['classes'] = []
        pr['levelMap'][lv['level']] = lv
    pr['unitMap'] = {u['id']: u for lv in pr['levels'] for u in lv['units']}
    programs[pr['id']] = pr
PROGRAM_ORDER = ['fogg-cw', 'fogg-en', 'fogg-cn', 'fogg-ew']
PROGRAM_ORDER += [p for p in programs if p not in PROGRAM_ORDER]

# ---------- 班级 ----------
classes = {}
for cj in sorted(glob.glob('courses/*/*/*/class.json')):
    cj = cj.replace('\\', '/')
    _, prog, uid, cid, _ = cj.split('/')
    c = json.loads(read(cj))
    if prog not in programs:
        err(f'{cj}: 课程 {prog} 不在 _build/curriculum/ 里')
        continue
    unit = programs[prog]['unitMap'].get(uid)
    if not unit:
        err(f'{cj}: 单元 {uid} 不在 {prog}.json 的单元表里')
        continue
    if c.get('id') != cid:
        err(f'{cj}: id "{c.get("id")}" 与文件夹名 "{cid}" 不一致')
    for k in ('year', 'term', 'teacher'):
        if k not in c:
            err(f'{cj}: 缺少字段 {k}')
    c.update(program=prog, unit=uid, level=unit['level'], unitTitle=unit['title'], unitEn=unit.get('en', ''),
             accent=programs[prog]['accent'], dir=f'courses/{prog}/{uid}/{cid}', lessons=[])
    c['cid'] = f'{prog}/{uid}/{cid}'
    classes[c['cid']] = c
    unit['classes'].append(c)

# ---------- 页面 ----------
pages = []
keys = {}
files = sorted(glob.glob('courses/*/*/*/wk*.html')) + sorted(glob.glob('talks/*/*.html')) + sorted(glob.glob('internal/*/*.html'))
for p in files:
    p = p.replace('\\', '/')
    if os.path.basename(p) == 'index.html':
        continue
    kind = 'lesson' if p.startswith('courses/') else ('talk' if p.startswith('talks/') else 'internal')
    depth = p.count('/')
    root = '../' * depth
    src = read(p)
    m = META_RE.search(src)
    if not m:
        err(f'{p}: 没有 page-meta 块')
        continue
    try:
        meta = json.loads(m.group(1))
    except Exception as e:
        err(f'{p}: page-meta 不是合法 JSON: {e}')
        continue
    for k in ('key', 'date', 'title'):
        if not meta.get(k):
            err(f'{p}: page-meta 缺少 {k}')
    key = meta.get('key', '')
    if key in keys:
        err(f'{p}: key "{key}" 与 {keys[key]} 重复')
    keys[key] = p
    if 'PAGE_CONFIG' in src and not re.search(r'''["']?key["']?\s*:\s*['"]''' + re.escape(key) + r'''['"]''', src):
        err(f'{p}: PAGE_CONFIG.key 与 page-meta.key 不一致 ({key})')
    if 'app.css' in src and f'href="{root}app.css"' not in src:
        err(f'{p}: app.css 路径应为 {root}app.css')
    if 'app.js' in src and f'src="{root}app.js"' not in src:
        err(f'{p}: app.js 路径应为 {root}app.js')
    if f'href="{root}index.html"' not in src:
        err(f'{p}: 缺少回到目录链接 href="{root}index.html"')
    meta['kind'] = kind
    meta['file'] = p
    meta['year'] = int(meta['date'][:4])
    if kind == 'lesson':
        _, prog, uid, cid, fn = p.split('/')
        c = classes.get(f'{prog}/{uid}/{cid}')
        if not c:
            err(f'{p}: 找不到 {prog}/{uid}/{cid}/class.json')
            continue
        for k, v in (('program', prog), ('unit', uid), ('class', cid)):
            if meta.get(k) and meta[k] != v:
                err(f'{p}: page-meta.{k}={meta[k]} 与所在文件夹 {v} 不一致')
            meta[k] = v
        mw = re.match(r'wk(\d+)-(\d{4}-\d{2}-\d{2})\.html$', fn)
        if not mw:
            err(f'{p}: 课页文件名应为 wkNN-YYYY-MM-DD.html')
        else:
            if int(mw.group(1)) != int(meta.get('week', -1)):
                err(f'{p}: 文件名周次与 page-meta.week 不一致')
            if mw.group(2) != meta['date']:
                err(f'{p}: 文件名日期与 page-meta.date 不一致')
        if 'href="../index.html"' not in src:
            err(f'{p}: 缺少本单元总览链接 href="../index.html"')
        meta.update(teacher=c['teacher'], term=c['term'], level=c['level'], accent=c['accent'],
                    programCode=programs[prog]['code'], programName=programs[prog]['name'],
                    unitTitle=c['unitTitle'], unitEn=c['unitEn'])
        meta.setdefault('speaker', c.get('speaker', ''))
        meta.setdefault('length', c.get('length', ''))
        meta['tagText'] = f"{programs[prog]['code']} L{c['level']} · Wk{meta.get('week')}"
        c['lessons'].append(meta)
    else:
        for k in ('type', 'teacher', 'accent'):
            if not meta.get(k):
                err(f'{p}: page-meta 缺少 {k}')
        meta.setdefault('level', '')
        meta.setdefault('tagText', '')
    meta.setdefault('status', 'ok')
    meta.setdefault('tags', [])
    meta['sections'] = [s for s in (strip(h) for h in H2_RE.findall(src)) if s]
    body = ' '.join(meta['sections'])
    body += ' ' + ' '.join(strip(b) for b in BOX_RE.findall(src))
    mp = PRESET_RE.search(src)
    if mp:
        body += ' ' + ' '.join(WORD_RE.findall(mp.group(1)))
    meta['_text'] = re.sub(r'\s+', ' ', body)[:8000]
    pages.append(meta)

if errors:
    print('检查未通过:')
    for e in errors:
        print('  -', e)
    sys.exit(1)

pages.sort(key=lambda m: m['date'], reverse=True)
for c in classes.values():
    c['lessons'].sort(key=lambda m: (m.get('week', 0), m['date']))
    c['count'] = len(c['lessons'])
    c['done'] = sum(1 for l in c['lessons'] if l.get('status') == 'ok')
    c['weeks'] = {l['week']: l for l in c['lessons']}
for pr in programs.values():
    for u in pr['unitMap'].values():
        u['classes'].sort(key=lambda c: (-c['year'], c['term'], c['teacher']))
        u['count'] = sum(c['count'] for c in u['classes'])
        u['done'] = max([c['done'] for c in u['classes']] or [0])
        u['years'] = sorted({c['year'] for c in u['classes']}, reverse=True)


# ---------- catalog.js ----------
def slim_class(c):
    return {k: c[k] for k in ('id', 'cid', 'program', 'unit', 'level', 'unitTitle', 'year', 'term', 'teacher', 'weekday',
                              'style', 'standard', 'count', 'done', 'dir') if k in c}


catalog = {
    'generated': datetime.date.today().isoformat(),
    'programs': [{
        'id': pr['id'], 'org': pr.get('org', ''), 'code': pr['code'], 'name': pr['name'], 'en': pr.get('en', ''),
        'accent': pr['accent'], 'desc': pr.get('desc', ''),
        'levels': [{**{k: v for k, v in lv.items() if k != 'units'},
                    'units': [{k: u.get(k) for k in ('id', 'n', 'title', 'en', 'level', 'count', 'done', 'years')} for u in lv['units']]}
                   for lv in pr['levels']],
    } for pid in PROGRAM_ORDER for pr in [programs[pid]]],
    'classes': [slim_class(c) for c in classes.values()],
    'pages': [{k: v for k, v in m.items() if not k.startswith('_')} for m in pages],
}
write('catalog.js',
      '// 自动生成,不要手改。运行 python _build/build_site.py\n'
      'window.CATALOG=' + json.dumps(catalog, ensure_ascii=False, separators=(',', ':')) + ';\n')

# ---------- search/<year>.js ----------
for f in glob.glob('search/*.js'):
    os.remove(f)
years = sorted({m['year'] for m in pages})
for y in years:
    part = [{'key': m['key'], 'text': m['_text']} for m in pages if m['year'] == y]
    write(f'search/{y}.js',
          'window.SEARCH_PARTS=window.SEARCH_PARTS||{};window.SEARCH_PARTS["%d"]=' % y
          + json.dumps(part, ensure_ascii=False, separators=(',', ':')) + ';\n')

# ---------- 单元总览页 courses/<program>/<unit>/index.html ----------
tpl = read('_build/templates/unit.html')
for pr in programs.values():
    for u in pr['unitMap'].values():
        if not u['classes']:
            continue
        lv = pr['levelMap'][u['level']]
        year_blocks = []
        for y in u['years']:
            cards = []
            for c in [c for c in u['classes'] if c['year'] == y]:
                rows = []
                for w in range(1, WEEKS + 1):
                    l = c['weeks'].get(w)
                    if l:
                        st, cls = STATUS.get(l.get('status', 'ok'), ('', ''))
                        href = f"{c['id']}/{os.path.basename(l['file'])}"
                        secs = ''.join(f'<li>{E(s)}</li>' for s in l['sections'])
                        rows.append(
                            f'<div class="lesson {cls}" data-key="{E(l["key"])}">'
                            f'<a class="wk" href="{href}">Wk {w}</a><div class="body">'
                            f'<div class="top"><a href="{href}">{E(l["title"])}</a><span class="st {cls}">{st}</span></div>'
                            f'<div class="en">{E(l.get("en", ""))}</div>'
                            f'<div class="desc">{E(l.get("desc", ""))}</div>'
                            f'<details><summary>章节 {len(l["sections"])} 节</summary><ol>{secs}</ol></details>'
                            f'<div class="meta"><span class="date">{l["date"].replace("-", ".")}</span>'
                            f'<span>{E(l.get("length", ""))}</span><span class="last"></span></div>'
                            f'</div></div>\n')
                    else:
                        rows.append(f'<div class="lesson todo"><span class="wk">Wk {w}</span>'
                                    f'<div class="body"><span class="todo-t">待整理</span></div></div>\n')
                outline = c.get('outline', [])
                outline_html = ''
                if outline:
                    outline_html = (f'<details class="outline"><summary>{len(outline)} 周脉络</summary><ol>'
                                    + ''.join(f'<li>{E(o)}</li>' for o in outline) + '</ol></details>')
                badge = '<span class="badge">标准底本</span>' if c.get('standard') else ''
                cards.append(
                    f'<div class="cls" id="{E(c["id"])}">'
                    f'<div class="cls-head">'
                    f'<div class="who"><b>{E(c["teacher"])}</b>{badge}<span class="sub">{E(c["term"])} · {E(c.get("weekday", ""))} · 报名 {E(c.get("enroll", ""))}</span></div>'
                    f'<div class="style">{E(c.get("style", ""))}</div>'
                    f'<div class="prog">已整理 {c["count"]} / {WEEKS} 课 · 达标 {c["done"]}<span class="caret">▾</span></div>'
                    f'</div><div class="cls-body">{outline_html}{"".join(rows)}</div></div>\n')
            year_blocks.append(f'<h2>{y} 年</h2>\n' + ''.join(cards))
        others = []
        for x in lv['units']:
            if x['id'] == u['id']:
                continue
            if x['classes']:
                others.append(f'<a href="../{x["id"]}/index.html">{E(x["title"])}</a>')
            else:
                others.append(f'<span class="dim">{E(x["title"])}(未整理)</span>')
        out = tpl
        for k, v in {
            'TITLE': E(u['title']), 'EN': E(u.get('en', '')), 'PROGRAM': E(pr['name']), 'CODE': E(pr['code']),
            'ORG': E(pr.get('org', '')), 'LEVEL': str(u['level']), 'UNIT_N': str(u['n']),
            'AGE': E(lv.get('age', '')), 'GOAL': E(lv.get('goal', '')),
            'SKILLS': E(lv.get('skills', '') or lv.get('lexile', '')),
            'OTHER_UNITS': ' · '.join(others) or '—',
            'ACCENT': pr['accent'], 'COUNT': str(u['count']), 'DONE': str(u['done']),
            'CLASSES': ''.join(year_blocks), 'UNIT_ID': u['id'], 'PROGRAM_ID': pr['id'],
        }.items():
            out = out.replace('{{' + k + '}}', v)
        write(f'courses/{pr["id"]}/{u["id"]}/index.html', out)

print(f'OK 课程 {len(programs)} 个,班级 {len(classes)} 个,页面 {len(pages)} 个,年份 {years}')
for c in classes.values():
    print(f'  {c["cid"]}: {c["count"]} 课 (达标 {c["done"]})')

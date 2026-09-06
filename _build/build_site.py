#!/usr/bin/env python3
"""
build_site.py — 扫描全站页面,生成 catalog.js / search/*.js / 各单元总览页。
用法: python _build/build_site.py        (在仓库根目录运行,或任何目录)
数据来源(单一真源):
  courses/<unit-id>/unit.json                      单元信息
  courses/<unit-id>/wkNN-YYYY-MM-DD.html  <script id="page-meta">  课页信息
  talks/<year>/*.html, internal/<year>/*.html      讲座/内部页信息(同样用 page-meta)
index.html 只读 catalog.js,不需要手改。
"""
import json, os, re, sys, html, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

TYPE_NAMES = {'cw': 'CW 创意写作', 'ew': 'EW 议论文', 'cn': '中文阅读', 'en': '英文精读', 'lr': 'LR 文学阅读'}
KIND_DIRS = {'courses': 'lesson', 'talks': 'talk', 'internal': 'internal'}

META_RE = re.compile(r'<script type="application/json" id="page-meta">\s*(\{.*?\})\s*</script>', re.S)
H2_RE = re.compile(r'<h2[^>]*>(.*?)</h2>', re.S)
TAG_RE = re.compile(r'<[^>]+>')
BOX_RE = re.compile(r'<div class="(?:keypoints|explain)[^"]*"[^>]*>(.*?)</div>', re.S)
PRESET_RE = re.compile(r'preset\s*:\s*(\[.*?\])', re.S)
WORD_RE = re.compile(r'''(?:word|zh)\s*:\s*['"]([^'"]+)['"]''')


def strip(s):
    s = TAG_RE.sub(' ', s)
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def read(p):
    return open(p, encoding='utf8').read()


def write(p, s):
    os.makedirs(os.path.dirname(p) or '.', exist_ok=True)
    open(p, 'w', encoding='utf8', newline='\n').write(s)


errors = []


def err(msg):
    errors.append(msg)


# ---------- 单元 ----------
units = {}
for uj in sorted(glob.glob('courses/*/unit.json')):
    u = json.loads(read(uj))
    d = os.path.basename(os.path.dirname(uj))
    if u.get('id') != d:
        err(f'{uj}: id "{u.get("id")}" 与文件夹名 "{d}" 不一致')
    for k in ('year', 'term', 'type', 'level', 'teacher', 'title', 'accent'):
        if k not in u:
            err(f'{uj}: 缺少字段 {k}')
    u['dir'] = f'courses/{d}'
    u['file'] = f'courses/{d}/index.html'
    u['lessons'] = []
    units[d] = u

# ---------- 页面 ----------
pages = []
keys = {}
for top, kind in KIND_DIRS.items():
    for p in sorted(glob.glob(f'{top}/*/*.html')):
        p = p.replace('\\', '/')
        if os.path.basename(p) == 'index.html':
            continue
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
        if 'href="app.css"' in src or 'src="app.js"' in src or 'href="index.html">🏠' in src:
            err(f'{p}: 资源路径还是根目录写法,应为 ../../app.css 等')
        meta['kind'] = kind
        meta['file'] = p
        meta['year'] = int(meta['date'][:4])
        if kind == 'lesson':
            uid = os.path.basename(os.path.dirname(p))
            u = units.get(uid)
            if not u:
                err(f'{p}: 找不到单元 {uid}/unit.json')
                continue
            if meta.get('unit') and meta['unit'] != uid:
                err(f'{p}: page-meta.unit={meta["unit"]} 与所在文件夹 {uid} 不一致')
            meta['unit'] = uid
            fn = os.path.basename(p)
            mw = re.match(r'wk(\d+)-(\d{4}-\d{2}-\d{2})\.html$', fn)
            if not mw:
                err(f'{p}: 课页文件名应为 wkNN-YYYY-MM-DD.html')
            else:
                if int(mw.group(1)) != int(meta.get('week', -1)):
                    err(f'{p}: 文件名周次与 page-meta.week 不一致')
                if mw.group(2) != meta['date']:
                    err(f'{p}: 文件名日期与 page-meta.date 不一致')
            for k in ('type', 'level', 'teacher', 'accent', 'term'):
                meta.setdefault(k, u[k])
            meta.setdefault('speaker', u.get('speaker', ''))
            meta.setdefault('length', u.get('length', ''))
            meta.setdefault('tagText', f"{u['type'].upper()} L{u['level']} · Wk{meta.get('week')}")
            u['lessons'].append(meta)
        else:
            for k in ('type', 'teacher', 'accent'):
                if not meta.get(k):
                    err(f'{p}: page-meta 缺少 {k}')
            meta.setdefault('level', '')
            meta.setdefault('tagText', '')
        meta.setdefault('status', 'ok')
        meta.setdefault('tags', [])
        meta['sections'] = [s for s in (strip(h) for h in H2_RE.findall(src)) if s]
        # 搜索正文:章节标题 + 黄框/绿框 + 生词表
        body = ' '.join(meta['sections'])
        body += ' ' + ' '.join(strip(b) for b in BOX_RE.findall(src))
        mp = PRESET_RE.search(src)
        if mp:
            body += ' ' + ' '.join(WORD_RE.findall(mp.group(1)))
        meta['_text'] = re.sub(r'\s+', ' ', body)[:8000]
        pages.append(meta)

if errors:
    print('❌ 检查未通过:')
    for e in errors:
        print('  -', e)
    sys.exit(1)

pages.sort(key=lambda m: m['date'], reverse=True)
for u in units.values():
    u['lessons'].sort(key=lambda m: (m.get('week', 0), m['date']))
    u['count'] = len(u['lessons'])
    u['redo'] = sum(1 for l in u['lessons'] if l.get('status') == 'redo')

# ---------- catalog.js ----------
catalog = {
    'generated': datetime.date.today().isoformat(),
    'typeNames': TYPE_NAMES,
    'units': [{k: v for k, v in u.items() if k != 'lessons'} for u in units.values()],
    'pages': [{k: v for k, v in m.items() if not k.startswith('_')} for m in pages],
}
write('catalog.js',
      '// 自动生成,不要手改。运行 python _build/build_site.py\n'
      'window.CATALOG=' + json.dumps(catalog, ensure_ascii=False, separators=(',', ':')) + ';\n')

# ---------- search/<year>.js(按年分片,搜索时才加载)----------
for f in glob.glob('search/*.js'):
    os.remove(f)
years = sorted({m['year'] for m in pages})
for y in years:
    part = [{'key': m['key'], 'text': m['_text']} for m in pages if m['year'] == y]
    write(f'search/{y}.js',
          'window.SEARCH_PARTS=window.SEARCH_PARTS||{};window.SEARCH_PARTS["%d"]=' % y
          + json.dumps(part, ensure_ascii=False, separators=(',', ':')) + ';\n')

# ---------- 单元总览页 ----------
tpl = read('_build/templates/unit.html')
STATUS = {'ok': ('✓ 已达标', 'ok'), 'redo': ('待重做', 'redo'), 'draft': ('草稿', 'redo')}
for uid, u in units.items():
    rows = []
    for l in u['lessons']:
        st, cls = STATUS.get(l.get('status', 'ok'), ('', ''))
        secs = ''.join(f'<li>{html.escape(s)}</li>' for s in l['sections'])
        en = f'<div class="en">{html.escape(l["en"])}</div>' if l.get('en') else ''
        rows.append(f'''<div class="lesson" data-key="{html.escape(l['key'])}" style="--accent:{l['accent']}">
  <a class="wk" href="{os.path.basename(l['file'])}">Wk {l.get('week', '')}</a>
  <div class="body">
    <div class="top"><span class="date">{l['date'].replace('-', '.')}</span><span class="st {cls}">{st}</span></div>
    <h3><a href="{os.path.basename(l['file'])}">{html.escape(l['title'])}</a></h3>
    {en}
    <div class="desc">{html.escape(l.get('desc', ''))}</div>
    <details><summary>章节 {len(l['sections'])} 节</summary><ol>{secs}</ol></details>
    <div class="meta"><span>🎙 {html.escape(l.get('speaker', ''))}</span><span>⏱ {html.escape(l.get('length', ''))}</span><span class="last">📖 …</span></div>
  </div>
</div>''')
    outline = ''.join(f'<li>{html.escape(o)}</li>' for o in u.get('outline', []))
    out = tpl
    for k, v in {
        'TITLE': html.escape(u['title']), 'EN': html.escape(u.get('en', '')), 'DESC': html.escape(u.get('desc', '')),
        'TERM': html.escape(u['term']), 'TYPE': TYPE_NAMES.get(u['type'], u['type']), 'LEVEL': f"L{u['level']}",
        'TEACHER': html.escape(u['teacher']), 'WEEKDAY': html.escape(u.get('weekday', '')),
        'ACCENT': u['accent'], 'COUNT': str(u['count']), 'DONE': str(u['count'] - u['redo']),
        'OUTLINE': outline, 'LESSONS': ''.join(rows), 'UNIT_ID': uid,
        'ZOOM': html.escape(u.get('zoom', '')), 'YEAR': str(u['year']),
    }.items():
        out = out.replace('{{' + k + '}}', v)
    write(u['file'], out)

print(f'✓ 单元 {len(units)} 个,页面 {len(pages)} 个,年份 {years}')
for uid, u in units.items():
    print(f'  {uid}: {u["count"]} 课 (待重做 {u["redo"]})')

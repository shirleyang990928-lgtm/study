# -*- coding: utf-8 -*-
"""把 meta.json + nav.html + body.html + preset.json 装进 _build/templates/source.html,
写出 library/<discipline>/<slug>.html(大脑库来源页)。

用法: python _build/assemble_source.py meta.json nav.html body.html preset.json

meta.json 必填: key, type, discipline, slug, author, source, length, date, title, en, desc
可选: tags(list), status(默认 ok), book, chapter(数字), quiz([{q,a}]), sourceName(来源显示名)
key 格式: lib-<type>-<slug>;discipline / type 必须在 _build/library.json 里。
"""
import sys, os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def rd(p):
    with open(p, encoding='utf-8') as f:
        return f.read()

def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;'))

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

    need = ['key', 'type', 'discipline', 'slug', 'author', 'source', 'length', 'date', 'title', 'en', 'desc']
    miss = [k for k in need if not meta.get(k)]
    if miss:
        sys.exit('meta.json 缺字段: ' + ', '.join(miss))
    lib = json.loads(rd(os.path.join(ROOT, '_build', 'library.json')))
    discs = {d['id']: d for d in lib['disciplines']}
    types = lib['types']
    disc, typ, slug = meta['discipline'], meta['type'], meta['slug']
    if disc not in discs:
        sys.exit(f'discipline {disc} 不在 _build/library.json 里')
    if typ not in types:
        sys.exit(f'type {typ} 不在 _build/library.json 里')
    if not re.match(r'^[a-z0-9-]+$', slug):
        sys.exit('slug 只能用小写字母、数字、连字符')
    if meta['key'] != f'lib-{typ}-{slug}':
        sys.exit(f"key 应为 lib-{typ}-{slug},现在是 {meta['key']}")
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', meta['date']):
        sys.exit('date 格式应为 YYYY-MM-DD')
    quiz = meta.get('quiz', [])
    if not isinstance(quiz, list) or any(not (isinstance(q, dict) and q.get('q') and q.get('a')) for q in quiz):
        sys.exit('quiz 应为 [{q,a}] 列表,每条都要有 q 和 a')
    status = meta.get('status', 'ok')
    if status not in ('ok', 'redo', 'draft'):
        sys.exit('status 只能是 ok / redo / draft')
    if 'chapter' in meta and not isinstance(meta['chapter'], int):
        sys.exit('chapter 应为数字')

    dname = discs[disc]['name']; tname = types[typ]
    accent = meta.get('accent') or discs[disc]['accent']
    tags = meta.get('tags', [])

    page_meta = {
        'key': meta['key'], 'kind': 'source', 'type': typ, 'discipline': disc,
        'author': meta['author'], 'source': meta['source'], 'length': meta['length'],
        'date': meta['date'], 'title': meta['title'], 'en': meta['en'], 'desc': meta['desc'],
        'accent': accent, 'tags': tags, 'status': status,
    }
    for k in ('book', 'chapter'):
        if k in meta:
            page_meta[k] = meta[k]
    page_meta['quiz'] = quiz

    def js1(s):  # 放进 JS 单引号字符串
        return str(s).replace('\\', '\\\\').replace("'", "\\'")

    src = meta['source']
    src_name = meta.get('sourceName') or (re.sub(r'^https?://(www\.)?', '', src).split('/')[0] if src.startswith('http') else src)
    source_line = f'<a href="{esc(src)}" target="_blank" rel="noopener">{esc(src_name)}</a>' if src.startswith('http') else esc(src)
    book_part = f" · {meta['book']}" + (f" 第{meta['chapter']}章" if 'chapter' in meta else '') if meta.get('book') else ''

    fill = {
        'TITLE_TAG': f"{meta['title']} · {meta['en']}",
        'ROOT': '../../',
        'META_JSON': json.dumps(page_meta, ensure_ascii=False, indent=1),
        'MAP_SUB': f"{dname} · {tname}{book_part}",
        'NAV': nav,
        'EYEBROW': f"大脑库 · {tname} · {dname}{book_part}",
        'H1_EN': meta['en'],
        'H1_ZH': meta['title'],
        'AUTHOR': esc(meta['author']),
        'SOURCE_LINE': source_line,
        'LENGTH': esc(meta['length']),
        'BODY': body,
        'FOOTER': '大脑库 · 学习笔记,非原文转录 · 来源见页首',
        'KEY': js1(meta['key']),
        'PC_TITLE': js1(f"大脑库 · {meta['title']}"),
        'EXPORT_TITLE': js1(f"大脑库 · {meta['title']} · {meta['author']} · 我的学习笔记"),
        'PRESET': preset,
    }
    tpl = rd(os.path.join(ROOT, '_build', 'templates', 'source.html'))
    out = re.sub(r'\{\{(\w+)\}\}', lambda m: fill[m.group(1)], tpl)
    left = re.findall(r'\{\{\w+\}\}', out)
    if left:
        sys.exit('模板占位符没填完: ' + ' '.join(left))

    ddir = os.path.join(ROOT, 'library', disc)
    os.makedirs(ddir, exist_ok=True)
    dst = os.path.join(ddir, slug + '.html')
    with open(dst, 'w', encoding='utf-8', newline='\n') as f:
        f.write(out)
    rel = os.path.relpath(dst, ROOT).replace('\\', '/')
    print(f'写出 {rel} ({len(out)//1024} KB) · key={meta["key"]}')
    print('下一步: python _build/build_site.py && node _build/testwkX.js ' + rel)

if __name__ == '__main__':
    main()

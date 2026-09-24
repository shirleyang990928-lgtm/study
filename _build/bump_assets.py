"""Add/refresh ?v=<stamp> on app.css / app.js links in every page so browsers refetch after a change.
Usage: python _build/bump_assets.py   (run after editing app.css/app.js, before build_site.py)
"""
import re, glob, datetime, io
stamp = datetime.datetime.now().strftime('%Y%m%d%H%M')
files = ['index.html'] + glob.glob('courses/*/*/*/*.html') + glob.glob('library/*/*.html') \
      + glob.glob('talks/*/*.html') + glob.glob('internal/*/*.html') + glob.glob('_build/templates/*.html') \
      + glob.glob('samples/*.html')
pat = re.compile(r'((?:\.\./)*app\.(?:css|js))(?:\?v=[\w.]+)?(")')
n = 0
for f in files:
    s = io.open(f, encoding='utf-8').read()
    t = pat.sub(lambda m: m.group(1) + '?v=' + stamp + m.group(2), s)
    if t != s:
        io.open(f, 'w', encoding='utf-8', newline='').write(t); n += 1
print('stamp', stamp, 'files updated', n)

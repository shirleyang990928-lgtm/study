# 通用规则 · 教学还原版(每个 agent 只做一堂课)

仓库根: C:/Users/shirl/Desktop/Study Web  (以下相对路径都相对仓库根)
<SP> = C:/Users/shirl/AppData/Local/Temp/claude/C--Users-shirl-Desktop-Study-Web/9b0fc7a4-0d50-48f1-aa48-fdf7cf1a747f/scratchpad
样板页(严格照版式,只有文字不同): samples/harriet-l6-wk07-lite.html
  - 版式只看: `sed -n '40,54p'`(nav 内容)、`sed -n '85,112p'`(一个完整 section)、`grep -n 'PAGE_CONFIG\|page-meta' | head`。不要整份读。
  - 样板 nav.html / meta.json 原文件: <SP>/lite_wk7/nav.html、<SP>/lite_wk7/meta.json(直接 cat,很短)。

## 目标
读者 Shirley 是中文母语的课程运营,不上课;她要「看完就懂这节课教了什么、怎么教的、好在哪坏在哪」,并能照着自己练。不是逐句转录。

## 格式(硬性)
- 6–8 个 `<section id="sN">`,按教学环节顺序,每节:
  1. `<div class="sec-head"><span class="sec-num">01</span><h2>标题</h2></div>`
  2. `<div class="sec-time ui">MM:SS – MM:SS · 一句话环节性质</div>`
  3. 叙述段 3–6 个 `<p class="narr">…</p>`,**每段 ≤130 个汉字**,一段一个意思:老师讲了什么、举了什么例、学生怎么答、哪里卡住。像懂行的人复述,不要空话。
  4. 原话引文 3–5 条:`<div class="para dialog"><p class="en"><span class="sent"><span class="se"><b>Name:</b> EN</span><span class="sz"><b>Name:</b> ZH</span></span>…</p></div>`。只选真正承载教学的话(老师关键解释/比喻/纠错、学生有代表性的回答)。老师名只写名字(如 Will),学生写名字。
  5. `<div class="keypoints ui"><b>要点</b><ul><li>…</li></ul></div>`(3–5 条,课堂实际发生了什么)
  6. `<div class="explain ui"><b>💡 这节在教什么</b><ul><li>…</li></ul></div>`(教学道理、为什么这样教、外人想自己练怎么做)
- 每个教学环节都不能跳:静默写作/技术排障/寒暄各一句话带过即可。
- 学生自己写的作品原文、老师当堂改稿前后对比:逐字保留(中英)。出版书原文长段只中英概括并注书名。
- 最后一节「专业课程评析 · 以世界级课程分析师的视角」:好不好 / 到底教了什么 / 我怎样才能学会 / 能应用在哪 / 设计逻辑 / 一句话总结引文 / 「留给你的一步:自己写一段」。**必含单独一条「哪里不好、可以做得更好」**:具体到某环节/某学生/时间分配/讲解含糊处 + 可操作建议。只夸不达标。
- nav.html: 必须有外层 `<nav class="map" id="map">` … `</nav>` 包裹(没有则侧边栏完全不显示，testwkX 导航=0)；里面是 `<div class="part">Part 1 · …</div>` + `<a href="#s1"><span class="dot"></span>标题</a>` 行，分 Part 1/2/3 + 课后(评析)。照抄 <SP>/lite_wk7/nav.html 的写法。
- preset.json:本课术语约 10 个 `[{"word","zh","def"}]`。
- meta.json:{"program","unit","class","week"(整数),"date":"YYYY-MM-DD","key","title"(中文题),"en"(EN Title),"desc"(一句话),"status":"ok","speaker","length":"约60分钟","students":"名字, 名字","tags":[…]}。key 必须完全按班级 brief 的格式。
- 中文字符串里不要用 ASCII 双引号(用「」或中文引号);不要 emoji(💡 除外);不要自创新 class 名。

## 做法(省 token)
1. `mkdir -p <SP>/out/<tag>_wkN`。压缩转录已生成(班级 brief 表里的文件),`wc -l` 后用 `sed -n 'A,Bp'` 每次 ≤200 行**全部读完**(不能只读开头;后半段常有学生作品和总结)。
2. 不写 Python 生成脚本。直接用 Write 工具写 <SP>/out/<tag>_wkN/ 下的 body.html、nav.html、preset.json、meta.json。
3. `cd "C:/Users/shirl/Desktop/Study Web" && export PYTHONIOENCODING=utf-8 && python _build/assemble.py <meta> <nav> <body> <preset>` → 写出 courses/…/wkNN-YYYY-MM-DD.html。
4. `node _build/testwkX.js <输出页>`,要求 乱码 0 / 键 OK / 侧栏底部 2 / 双框 N/N;报错就修到过。
5. 不 git、不跑 build_site.py(主会话统一跑)。

## 回报 ≤20 行
输出页路径;testwkX 那一行;节数、引文条数、narr 段数;每节标题+时间段(一行);评析「哪里不好」一句话;若发现代课老师/老师讲错周/录音异常也报。

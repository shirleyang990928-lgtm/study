# study — FOGG 学习笔记本知识库(交接说明)

Shirley 的交互式 HTML 学习笔记本库,GitHub Pages 托管:
https://shirleyang990928-lgtm.github.io/study/
仓库:github.com/shirleyang990928-lgtm/study(Public)。只有 Shirley 一个人用。
用途:公司不培训老师,她靠这个库自己学会每门课、并能回答家长。目标规模上千页。

## 你的任务

把每堂课的 Zoom VTT 转录做成一个课堂页 HTML,放进对应班级文件夹,跑 `python _build/build_site.py`,`git push` 上线。
**现行做法(2026-09-08 起):教学还原版,每堂课一个 Sonnet subagent,一批 8–10 堂并行,主会话统一 build + push(见下「课堂页标准 · 教学还原版」)。** 主会话自己不写课页(一次做多堂会滑标准)。
每堂课页设计完全一样(只有文字不同),不要自创新版式;能省 token 就省,质量不能降。

## 当前状态(2026-09-08)

- 骨架:课程 → Level → 单元 → 年份 → 老师班级 → 周课页;总目录 index.html 是单页应用(课程 tab、等级卡、单元卡、全文搜索、筛选)。
- **2026 S2 全部班级已上线**:21 个班、189 个页面。周一/周二/周三各班为逐句版;周四/周五 10 个班共 82 堂已按「教学还原版」由 Sonnet subagent 批量做完并 push(Louise CW L1 周四、Will CW L1 周四、Fran CW L4 周四、George EN L1 周四、Alex EW L2 周四 7pm、Alex EW L4 周四 8pm、Tim CW L4 周五 7pm/8pm、Ben EW L6 周五、Alex CW L3 周五)。82 堂共花 subagent token 约 651 万,平均每堂约 7.9 万。
- 待 Shirley 确认:这 10 个班 class.json 的 `style` 仍是「(待补充)」;EW 三个单元名仍是占位(`l02-u1-tbd`/`l04-u1-tbd`/`l06-u1-tbd`);Tim 周五 7pm 某学生的名字(EJ / Joshua / Iger,说话人标 YIZHE,现统一写 EJ)。
- **Alex CW Level 3 周五 4pm 班是 1对2 试课,不算正常体系**,只有 08-21 一堂录音;class.json 已 `standard:false`,`style` 写明,Wk2-10 的 outline 写明原因。
- **缺周原因已全部写进各班 class.json 的 `outline`**(单元页上代替「尚未整理」显示):
  - 录音截断/只有几十秒,做不了:Tim CW L2 周一 W2(07-06)、W5(07-27);Louise CW L6 周二8pm W4(07-21);Harriet CW L9 周二 W6(08-04);Louise CW L11 周三 W3(07-15);Alex EW L4 周一 W3(07-13)、W4(07-20);Alex EW L4 周四8pm W3(07-16);Ben EW L6 周五 W2(07-10)、W5(07-31)。
  - Zoom 当周根本没有录音文件:Fran CW L4 周三 W4(07-22);Ben CW L6 周一 W9(08-24);George EN L7 周二 W10(09-01)。
  - 本来就没上满 10 周:Will CW L1 周四 07-09 开课,只有 9 周;George EN L1 周四 08-06 开课,只有 5 周。
- Alex EW Level 4 Wk9、Fran CW L4 周三有 1 堂:旧版杂烩页,标 redo,以后重做。
- 等级表:CW 12 级、EN 10 级、EW 6 级已录入(`_build/curriculum/`);CN 8 级只有级别、单元待 Shirley 给资料。
- 之后:2025 年全部班级数据导入(同单元跨年比较课程设计);其它公司课程作为新 org 加入。

## 分类原则(Shirley 定的,不要改)

- 按 FOGG 教材等级分类,不按 Zoom 班级名。Zoom 文件夹里的 "L7-8" 是招生范围,Alex 这个班上的教材是 **Level 8**。只按教材等级标注。
- 每级每单元 10 周,每级两个单元 = 两个学期 = 20 课。
- 每个单元只要**一套标准笔记**(选一个老师的班做底本,10 页);其他老师只有讲法明显不同才另做。同一单元同一年多个老师 → 单元页上一人一张老师卡(名字 + 风格一句话),点开看该老师的课表。
- 组织写 "FOGG"(以后会加其它公司的课)。空的 Level / 单元也要显示(灰色"尚未整理")。

## 目录结构(不要改;新增内容只往这些文件夹里放)

```
index.html                 总目录(静态单页应用,读 catalog.js;不用手改内容,改 UI 才动它)
catalog.js                 自动生成:全站索引 {generated, programs, classes, pages}
search/<year>.js           自动生成:按年分片的全文搜索数据(搜索时才加载)
app.css / app.js           全站共用样式与交互(生词本/划线/笔记/同步/朗读/书签)
_build/curriculum/<program>.json   课程等级表:fogg-cw / fogg-en / fogg-cn / fogg-ew
courses/<program>/<unit-id>/       一个单元一个文件夹
   index.html                      自动生成:单元总览页(回到目录按钮、年份、老师卡、Wk1-10 清单)
   <class-id>/class.json           班级信息(见下)
   <class-id>/wkNN-YYYY-MM-DD.html 课页,例 wk02-2026-07-06.html
talks/<year>/<date>-<slug>.html      外部讲座
internal/<year>/<date>-<slug>.html   内部会议/教学大纲
_build/                    构建脚本与样板(见流水线)
```

- program id:`fogg-cw`(创意写作) `fogg-en`(英文精读) `fogg-cn`(中文阅读) `fogg-ew`(议论文)。
- unit-id 格式:`l<level 两位>-u<1|2>-<slug>`,例 `l08-u1-crime-story`。必须与 curriculum json 里 `levels[].units[].id` 一致。
- class-id 格式:`<year><term>-<teacher>-<weekday>`,例 `2026s2-alex-mon`。
- class.json 字段:`id, year, term, teacher, weekday, zoom(Zoom 文件夹名), enroll(招生范围), standard(是否底本), style(风格一句话), students, speaker, length, outline[]`。
- 新班级 = 新建 `courses/<program>/<unit-id>/<class-id>/class.json`(照抄现有的改字段),课页放进去,目录自动出现。新单元 = 先在 curriculum json 里有条目。
- 课页深度都是 4 层,资源路径一律 `../../../../app.css`、`../../../../app.js`,回到目录 `../../../../index.html`,本单元总览 `../index.html`。
- 每页 `<head>` 里有 `<script type="application/json" id="page-meta">{key,kind:"lesson",program,unit,class,week,status,date,title,en,desc,speaker,length,tags}</script>`,这是目录/搜索的唯一数据源。status:ok / redo / draft。
- `python _build/build_site.py` 会校验(key 重复、文件名与 meta 不一致、路径写法错、unit/class 是否存在)并生成 catalog.js、search/、各单元 index.html。**改了任何页面、class.json 或 curriculum 都要重跑,再 push。**
- 总目录 hash 路由:`#fogg-cw` 选课程,`#fogg-cw/l8` 跳到 Level 8 卡片,`#?q=词&t=老师&y=年&s=状态&o=排序&all=1` 是搜索/列表状态。

## 页面架构(不要改)

- 每页 = 内容 HTML + `<link rel="stylesheet" href="../../../../app.css">` + `window.PAGE_CONFIG={key,title,exportTitle,preset}` + `<script src="../../../../app.js"></script>`
- **工具栏/菜单/弹窗的 HTML 写在每页里(由 `_build/templates/lesson.html` 提供),app.js 按元素 id 绑定行为。** 改功能只改 app.js/app.css + 模板一处;老页面要同步改就用脚本批量替换。
- 左侧栏底部固定「回到目录」「本单元总览」两个按钮;「更多」里只留 显示全部中文 + 导出笔记。不要加 emoji。
- 对白段必须用 `<div class="para dialog">`(app.css 里 `.para.dialog .sent{display:block}`)。
- 云同步靠 Gist(用户浏览器 localStorage 里存 id/token,不进仓库),存储键来自 PAGE_CONFIG.key,**同一课的 key 不能变,且必须与 page-meta.key 一致**(否则用户笔记丢失)。
- PAGE_CONFIG.key 格式:`cls-YYYYMMDD-<type>-<teacher>-l<level>-wk<week>`,例 `cls-20260706-cw-alex-l8-wk2`(老页面沿用旧 key,不改)。

## VTT 来源(不要复制进仓库!含学生姓名,仓库是 Public)

`C:\Users\shirl\Desktop\FOGG Skill Work\Zoom_Transcripts\<账号>\2026_S2\<班级名称>\<VTT>`
账号:camp / siyanci / zoom1 / zoom3。Alex CW 周一班在 `…\2026_S2\CW_26_S2_MON_L7-8_Alex\`(class.json 的 zoom 字段)。
文件名 = 日期 + Zoom 课程标题 + 录制 ID。同步脚本 `FOGG Skill Work/zoom-api/sync-zoom-transcripts.ps1`,日志 `Zoom_Transcripts/_sync-index.jsonl`。
中间产物(blocks/body/nav/preset/meta)放在 scratchpad 或仓库根目录(已 .gitignore),不要提交。

## 课堂页标准 · 教学还原版(2026-09-08 起的现行标准)

Shirley 2026-09-08 定:以后所有课页按「教学还原版」做,样板 `samples/harriet-l6-wk07-lite.html`(版式只有文字不同)。规则全文在 `_build/COMMON_BRIEF_LITE.md`,要点:

- 目标读者是不上课的中文运营,要「看完就懂这节教了什么、怎么教、好在哪坏在哪」,不是逐句转录。
- 6–8 个 section,每节:`.sec-head`(编号+标题)→ `.sec-time`(时间段+环节性质)→ 3–6 段 `<p class="narr">` 旁白(每段 ≤130 字,一段一个意思,可高亮)→ 3–5 条中英原话引文(`.para.dialog`)→ 黄框 `.keypoints` → 墨绿框 `.explain`。
- 每个教学环节都不能跳;学生作品原文、老师当堂改稿前后逐字保留;出版书原文长段只中英概括并注书名。
- 最后一节「专业课程评析」必含单独一条「哪里不好、可以做得更好」(具体到环节/学生/时间分配 + 可操作建议),只夸不达标。
- preset 约 10 个术语;key 格式 `cls-YYYYMMDD-<type>-<seg>-l<level>-wkN`(同一老师两个班用 seg 区分,如 tim7/tim8、alex/alex8;代课周 key 仍用原老师 seg)。
- 每页约 1.2–2 万 token 产出;逐句版(下文)只用于 Shirley 点名要逐句的课。

### 流水线(教学还原版,多堂并行)

```
python _build/vtt2lite.py "<VTT>" <SP>/lite/<tag>/wkNN.txt     # 压缩转录(去填充词/合并同说话人),放 scratchpad,绝不进仓库
# 每个班一份 BRIEF_<tag>.md(周→压缩转录→输出页名表 + key 格式 + program/unit/class),生成脚本见 scratchpad gen_briefs.py 的思路
# 每堂课一个 Sonnet subagent(model "sonnet"),prompt:先读 COMMON_BRIEF_LITE.md + BRIEF_<tag>.md,只做 W<N>
#   subagent 自己:读完压缩转录 → Write body/nav/preset/meta → assemble.py → testwkX.js,不 git 不 build_site
python _build/build_site.py && node _build/testwkX.js <本批所有页>   # 主会话每批统一跑,然后 commit + push
```

主会话不做重活,只发 agent、校验、提交。一批 8–10 个 agent 并行。

## 课堂页质量标准 · 逐句版(旧标准,仅按需使用)

以 `_build/TEMPLATE-week1-standard.html`(= courses/fogg-cw/l08-u1-crime-story/2026s2-alex-mon/wk01-2026-06-29.html)为样板,逐条对照:

1. **逐句还原师生对白(最重要,Shirley 反复纠正过 3 次)**
   - 除了纯寒暄(吃了什么/去哪玩)可压成要点,**一进入任何教学内容就逐句还原成中英对照对白**,老师和学生的话都要。
   - 不要自行判断"哪句重要"去删或概括。不要把 20 分钟的教学压成 5 条要点。
   - 判断标准:一个 section 跨 20+ 分钟教学,却只有几条要点、一两段引文 = 不达标。
   - 对白格式:`<div class="para dialog"><p class="en">` 内每轮一个
     `<span class="sent"><span class="se"><b>Alex:</b> EN</span><span class="sz"><b>Alex:</b> ZH</span></span>`
   - 老师的整段讲解可用引文框 `.quote`(带 tag),但不能只挑一两句。
2. **Part 结构**:sidebar nav 用 `<div class="part">Part 1 · …</div>` 分组,按教学阶段分 Part 1/2/3 + 课后。
3. **8-11 个 section**,铺开完整时间线,不合并。每节有 `.sec-time`。
4. **每节双框**:黄色 `.keypoints`(课堂实际发生了什么)+ 墨绿 `.explain`(💡这节在教什么:教学道理、为什么重要、常以"如果你是外人、想自己练:"结尾)。绝不省略黄框。
5. **必有最后一节「专业课程评析 · 以世界级课程分析师的视角」**:这堂课好不好 / 到底教了什么 / 我怎样才能学会 / 能应用在哪 + 设计逻辑 + 一句话总结引文 + "留给你的一步:自己写一段"。
   - **必须有批评(Shirley 2026-09-06 要求)**:除了说好在哪,还要单独写"哪里不好 / 哪里可以做得更好"(具体到课堂里的某个环节:时间分配、某个学生没被照顾到、讲解含糊、练习没落地等),给出可操作的改进建议。只说好话 = 不达标。之前已上线的页面不用回改。
6. 保留真实课堂细节(学生名字 Alice/Kaelyn/xuanying/Chen Yuhan、他们的原话、小插曲)。
7. PAGE_CONFIG.preset:本课术语 10 个左右 `{word,zh,def}`。
8. 页面目标:一个外人能跟着学会、并能输出自己的作品。

## 流水线(做一堂课)

```
export PYTHONIOENCODING=utf-8
python _build/vtt2blocks.py "<VTT 完整路径>" wkN_blocks.txt      # 按说话人合并
# 完整读 wkN_blocks.txt(分段读,不要只读开头),规划 Part/section
# 写 build_wkN.py(仿 _build/build_wk1_v3.py):D()/DIALOG()/Q()/KP()/EX()/sec() → wkN_body.html
# 写 wkN_nav.html、wkN_preset.json、wkN_meta.json
#   meta.json 必填: {"program":"fogg-cw","unit":"l08-u1-crime-story","class":"2026s2-alex-mon",
#                    "week":N,"date":"YYYY-MM-DD","key":"cls-…","title":"中文题","en":"EN Title",
#                    "desc":"一句话","status":"ok"}   可选: tags, length, speaker, students
#   老师/学期/单元名/课程名由 class.json + curriculum json 自动填
python _build/assemble.py wkN_meta.json wkN_nav.html wkN_body.html wkN_preset.json
#   → 用 _build/templates/lesson.html 写出 courses/<program>/<unit>/<class>/wkNN-YYYY-MM-DD.html
python _build/build_site.py                                      # 校验 + 生成目录/搜索/单元页
node _build/testwkX.js courses/<program>/<unit>/<class>/wkNN-YYYY-MM-DD.html   # 可一次传多个文件
#   检查:章节/导航/双框/对白段/句对/紫词/朗读/键/乱码/侧栏底部
```
需要 `npm install jsdom` 一次(node_modules 已 .gitignore)。测试输出里"乱码"必须为 0,"键: OK","侧栏底部: 2"。

本地预览:Browser 面板用 `.claude/launch.json` 里的 `study-site`(python http.server 8765),打开 http://localhost:8765/。file:// 打开没有 JS,不要用。

上线:`git add -A && git commit -m "Week N" && git push`,等 1-2 分钟,用 `?v=N` 打开线上验证。

## 已知的坑

- Python `str.replace()` 替换串里有 `$` 会出错 → 用 `re.sub(..., lambda m: content, ...)`。
- f-string 里不能出现裸 `};` → 拼接字符串。
- Windows 上 Python 的 open() 要用 `C:\...` 路径,`/c/...` 会找不到文件;Bash/node 两种都行。
- Bash heredoc 会吞掉反斜杠(即使 `<<'EOF'`)。含反斜杠的内容用 Python `chr(92)` 拼,或用 Write 工具。
- 跑 python 前一定 `export PYTHONIOENCODING=utf-8`,否则中文输出乱码。
- 中文标点/引号混入 JS 单引号字符串会破坏页面 → 改完跑 build_site.py + testwkX.js。
- Alex 的教学脉络以 VTT 为准,不要靠周次标题猜内容(Week 3 实际讲的是"开头五种方式",不只是角色)。
- 改了 app.css/app.js 要一起 push,否则页面样式不生效。
- 不要手改 catalog.js、search/*.js、courses/*/*/index.html,它们是生成物。

## 侦探单元 9 周脉络(Alex · CW Level 8 · 2026 S2 · 周一)

W1 观察与推理 deduce → W2 玩弄读者怀疑(一级/二级、frame 嫁祸、审问问题、打造侦探) → W3 分享侦探 + 开头五种方式 + 视角代词 → W4 开头反馈、看图写场景、作者的选择、反派档案 → W5 连环杀手、侦探即凶手、三法则、red herring、先写结局 → W6 逆向工程、Cluedo 群戏、动机+alibi → W7 逐句精修、克里斯蒂视频、人物层次、奖杯失窃案 → W8 工坊互评、解谜、riddle vs story → W9 从谜题到故事(已上线)

## 之后的规划

- 补 Alex L8 Week 10;并行做 Tim CW L2 等其它班(可多个 subagent 同时各做一堂,主会话统一 build + push)。
- 之后重做 Tim CW Level 2 Wk9、Alex EW Level 4 Wk9(旧版杂烩页)。
- 导入 2025 数据(新 class.json 放同一 unit 文件夹下),CN 单元表、EW 单元名等 Shirley 给资料再补。

## 和 Shirley 协作的方式

- 中文沟通,她用语音转文字,可能有错字,按意思理解。
- 她要一次做对,不要来回挤牙膏。不确定就先问,别自作主张。
- 做错了直接承认并修,不要过度道歉。
- 每做完一堂:报告章节数/句对数/测试结果,给出线上链接,等她验收。

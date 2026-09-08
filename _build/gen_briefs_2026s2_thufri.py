import os, json, re, sys, glob
sys.path.insert(0, r'C:\Users\shirl\Desktop\Study Web\_build')
import vtt2lite
SP = os.path.dirname(os.path.abspath(__file__))
REPO = r'C:\Users\shirl\Desktop\Study Web'
ZT = r'C:\Users\shirl\Desktop\FOGG Skill Work\Zoom_Transcripts'
THU = ['07-02','07-09','07-16','07-23','07-30','08-06','08-13','08-20','08-27','09-03']
FRI = ['07-03','07-10','07-17','07-24','07-31','08-07','08-14','08-21','08-28','09-04']
CL = [
 dict(tag='alexl3', program='fogg-cw', unit='l03-u1-how-to-write-a-good-story', cls='2026s2-alex-fri', teacher='Alex', weekday='周五 4pm',
      acct='camp', zoom='CW_26_S2_Alex_L3_FRI_4-5PM', enroll='L3', standard=True, seg='alex', type='cw', level=3,
      dates=['08-21'], skip=[], students='Aiden, Clayton', unitname='How to Write a Good Story', note='只有一次录音(08-21),按 Week 1 做。'),
 dict(tag='tim7', program='fogg-cw', unit='l04-u1-engaging-story', cls='2026s2-tim-fri-7pm', teacher='Tim', weekday='周五 7pm',
      acct='camp', zoom='CW_26_S2_FRI_L3-4_Tim_7-8PM', enroll='L3-4', standard=False, seg='tim7', type='cw', level=4,
      dates=FRI, skip=[], students='', unitname='Engaging Story', note='key teacher 段用 tim7(区分 8pm 班)。'),
 dict(tag='tim8', program='fogg-cw', unit='l04-u1-engaging-story', cls='2026s2-tim-fri-8pm', teacher='Tim', weekday='周五 8pm',
      acct='camp', zoom='CW_26_S2_FRI_L3-4_Tim_8-9PM', enroll='L3-4', standard=False, seg='tim8', type='cw', level=4,
      dates=FRI, skip=[], students='', unitname='Engaging Story', note='key teacher 段用 tim8(区分 7pm 班)。'),
 dict(tag='fran', program='fogg-cw', unit='l04-u1-engaging-story', cls='2026s2-fran-thu', teacher='Fran', weekday='周四 6pm',
      acct='siyanci', zoom='CW_26_S2_THU_L3-4_Fran_6-7PM', enroll='L3-4', standard=False, seg='fran', type='cw', level=4,
      dates=THU, skip=[], students='', unitname='Engaging Story', note=''),
 dict(tag='louise', program='fogg-cw', unit='l01-u1-year-full-of-stories', cls='2026s2-louise-thu', teacher='Louise', weekday='周四 7pm',
      acct='camp', zoom='CW_26_S2_THU_L1-3_Louise_7-8PM', enroll='L1-3', standard=False, seg='louise', type='cw', level=1,
      dates=THU, skip=[], students='', unitname='A Year Full of Stories', note=''),
 dict(tag='will', program='fogg-cw', unit='l01-u1-year-full-of-stories', cls='2026s2-will-thu', teacher='Will', weekday='周四 7pm',
      acct='zoom1', zoom='CW_26_S2_THU_L1_Will_7-8PM', enroll='L1', standard=True, seg='will', type='cw', level=1,
      dates=THU[1:], skip=[], students='', unitname='A Year Full of Stories', note='07-09 是第一课(Week 1),到 09-03 共 9 周。07-16(W2)是代课老师 Ben(Benedict),页面说话人写 Ben,meta.speaker 写 Teacher Ben(代课),key 仍用 will 段。'),
 dict(tag='george', program='fogg-en', unit='l01-u1-charlottes-web', cls='2026s2-george-thu', teacher='George', weekday='周四 7pm',
      acct='zoom3', zoom='LR_26_S2_THU_L1_George_7-8PM', enroll='L1', standard=True, seg='george', type='en', level=1,
      dates=THU[5:], skip=[], students='', unitname="Charlotte's Web", note='08-06 是第一课(Week 1),到 09-03 共 5 周。英文精读课:出版书原文长段只中英概括并注书名,不整段照抄。'),
 dict(tag='alexew7', program='fogg-ew', unit='l02-u1-tbd', cls='2026s2-alex-thu-7pm', teacher='Alex', weekday='周四 7pm',
      acct='siyanci', zoom='EW_26_S2_THU_L1-2_Alex_7-8PM', enroll='L1-2', standard=True, seg='alex', type='ew', level=2,
      dates=THU, skip=[], students='', unitname='(单元名待定)', note='议论文课。'),
 dict(tag='alexew8', program='fogg-ew', unit='l04-u1-tbd', cls='2026s2-alex-thu-8pm', teacher='Alex', weekday='周四 8pm',
      acct='siyanci', zoom='EW_26_S2_THU_L3-4_Alex_8-9PM', enroll='L3-4', standard=False, seg='alex8', type='ew', level=4,
      dates=THU, skip=['07-16'], students='', unitname='(单元名待定)', note='议论文课。key teacher 段用 alex8。W3(07-16)录音截断不做。'),
 dict(tag='ben', program='fogg-ew', unit='l06-u1-tbd', cls='2026s2-ben-fri', teacher='Ben', weekday='周五 8pm',
      acct='siyanci', zoom='EW_26_S2_FRI_L5-6_Ben_8-9PM', enroll='L5-6', standard=True, seg='ben', type='ew', level=6,
      dates=FRI, skip=['07-10','07-31'], students='', unitname='(单元名待定)', note='议论文课。W2(07-10)、W5(07-31)录音截断不做。'),
]
unitnames = {}
for p in ['fogg-cw','fogg-en','fogg-ew']:
    j = json.load(open(os.path.join(REPO,'_build','curriculum',p+'.json'),encoding='utf-8'))
    for L in j['levels']:
        for u in L['units']: unitnames[(p,u['id'])] = u.get('name') or u.get('title') or u['id']
tmpl = json.load(open(os.path.join(REPO,'courses','fogg-cw','l04-u1-engaging-story','2026s2-fran-wed','class.json'),encoding='utf-8'))
summary = []
for c in CL:
    d = os.path.join(REPO,'courses',c['program'],c['unit'],c['cls']); os.makedirs(d,exist_ok=True)
    cj = dict(tmpl); cj.update(id=c['cls'], year=2026, term='S2', teacher=c['teacher'], weekday=c['weekday'], zoom=c['zoom'],
        enroll=c['enroll'], standard=c['standard'], style='(待补充)', students=c['students'] or '(待补充)',
        speaker='Teacher '+c['teacher'], length='约60分钟 · '+c['weekday'], outline=[])
    json.dump(cj, open(os.path.join(d,'class.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=2)
    vdir = os.path.join(ZT,c['acct'],'2026_S2',c['zoom'])
    files = sorted(os.listdir(vdir))
    rows=[]; litedir=os.path.join(SP,'lite',c['tag']); os.makedirs(litedir,exist_ok=True)
    for i,md in enumerate(c['dates'],1):
        if md in c['skip']: continue
        m=[f for f in files if f.startswith('2026-'+md) and f.endswith('.vtt')]
        if not m: print('MISSING',c['tag'],md); continue
        out=f'wk{i:02d}-2026-{md}.html'; lite=f'wk{i:02d}.txt'
        n,w,_=vtt2lite.process(os.path.join(vdir,m[0]),os.path.join(litedir,lite))
        rows.append((i,md,m[0],out,lite,w))
        summary.append((c['tag'],i,md,w))
    uname = unitnames.get((c['program'],c['unit']), c['unitname'])
    L=[f"# {c['teacher']} {c['type'].upper()} Level {c['level']}「{uname}」· {c['weekday']}",
       "先读同目录 COMMON_BRIEF_LITE.md(格式+质量+收尾),严格照做。",
       f"压缩转录目录: {SP}/lite/{c['tag']}/   (由 VTT 生成,含学生姓名,绝不复制进仓库)",
       f"输出目录: courses/{c['program']}/{c['unit']}/{c['cls']}/",
       f"meta.key 格式: cls-YYYYMMDD-{c['type']}-{c['seg']}-l{c['level']}-wkN  (日期无横线; date 字段有横线; N 不补零)",
       f"说话人 Teacher {c['teacher']},页面写 {c['teacher']}。program={c['program']} unit={c['unit']} class={c['cls']}。{c['note']}",
       "", "## 周 → 压缩转录 → 输出文件 (只做下表列出的周)", "| 周 | 日期 | 压缩转录 | 英文词数 | 输出页 |", "|---|---|---|---|---|"]
    for i,md,f,out,lite,w in rows: L.append(f"| W{i} | 2026-{md} | {lite} | {w} | {out} |")
    open(os.path.join(SP,f"BRIEF_{c['tag']}.md"),'w',encoding='utf-8').write('\n'.join(L)+'\n')
json.dump(summary, open(os.path.join(SP,'lessons.json'),'w'), indent=0)
print(len(summary),'lessons')
for t in CL: print(t['tag'], [s[1] for s in summary if s[0]==t['tag']])

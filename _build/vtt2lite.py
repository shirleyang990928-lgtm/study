"""VTT -> condensed blocks for 教学还原版 (cheaper to read than vtt2blocks output).
Usage: python _build/vtt2lite.py <vtt> <out.txt>
- merges consecutive same-speaker cues
- strips filler (um/uh/er/hmm/you know), stutters, immediate word repeats
- drops pure-ack blocks (yeah/ok/mm...) unless answering a question
- timestamps as [MM:SS]
"""
import re, sys
FILL=re.compile(r"\b(um+|uh+|uhm|er+|erm|hmm+|mm+|mhm|ah+|oh+|like,|you know,|I mean,|sort of,|kind of,)\s*",re.I)
REP=re.compile(r"\b(\w+(?:\s\w+)?)[,.]?\s+\1\b[,.]?\s*",re.I)
ACK=set("yes yeah yep yup ok okay mm mhm right sure good great thanks thank you bye hi hello alright fine cool nice mm-hmm uh-huh no nope".split())
def cues(src):
    txt=open(src,encoding='utf-8',errors='ignore').read().replace('\r','')
    for block in re.split(r'\n{2,}',txt):
        ls=block.strip('\n').split('\n')
        if len(ls)>=2 and '-->' in ls[1]:
            ts=ls[1].split(' --> ')[0][:8]; body=' '.join(ls[2:]).strip()
            if body: yield ts,body
def clean(t):
    t=FILL.sub('',t)
    for _ in range(2): t=REP.sub(lambda m:m.group(1)+' ',t)
    t=re.sub(r"\b(\w+)-\s+(?=\1\b)",'',t)            # "st- start"
    t=re.sub(r"\s+([,.?!])",r"\1",t); t=re.sub(r"\s{2,}",' ',t)
    t=re.sub(r"([,.!?])\s*\1+",r"\1",t)
    return t.strip()
def process(src,out):
    blocks=[];cur=None;acc=[];cts=None
    for ts,body in cues(src):
        m=re.match(r'^([^:]+):\s*(.*)$',body)
        s,b=(m.group(1),m.group(2)) if m else ('?',body)
        if s==cur: acc.append(b)
        else:
            if cur is not None: blocks.append((cts,cur,' '.join(acc)))
            cur=s;acc=[b];cts=ts
    if cur is not None: blocks.append((cts,cur,' '.join(acc)))
    outl=[];prev='';nw=0;dropped=0
    for ts,sp,tx in blocks:
        c=clean(tx)
        words=re.findall(r"[A-Za-z'-]+",c.lower())
        if not words: continue
        if len(words)<=3 and all(w in ACK for w in words) and not prev.endswith('?'):
            dropped+=1; prev=c; continue
        h,mn,sc=ts.split(':'); mm=int(h)*60+int(mn)
        outl.append(f"[{mm:02d}:{sc}] {sp}: {c}"); prev=c; nw+=len(words)
    open(out,'w',encoding='utf-8').write('\n'.join(outl)+'\n')
    return len(outl),nw,dropped
if __name__=='__main__':
    n,w,d=process(sys.argv[1],sys.argv[2]); print(f"{n} blocks, {w} words, {d} acks dropped")

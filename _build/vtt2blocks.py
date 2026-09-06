import re, sys
def process(src, out):
    txt=open(src,encoding='utf-8',errors='ignore').read().replace('\r','')
    segs=[]
    for block in txt.split('\n\n'):
        lines=block.split('\n')
        if len(lines)>=2 and '-->' in (lines[1] if len(lines)>1 else ''):
            ts=lines[1].split(' --> ')[0][:8]
            body=' '.join(lines[2:]).strip()
            if body: segs.append((ts,body))
        elif len(lines)>=3 and '-->' in lines[1]:
            pass
    # merge consecutive same speaker
    def spk(t):
        m=re.match(r'^([^:]+):\s*(.*)$',t)
        return (m.group(1),m.group(2)) if m else (None,t)
    blocks=[];cur=None;acc=[];cts=None
    for ts,body in segs:
        s,b=spk(body)
        if s==cur: acc.append(b)
        else:
            if cur is not None: blocks.append((cts,cur,' '.join(acc)))
            cur=s;acc=[b];cts=ts
    if cur is not None: blocks.append((cts,cur,' '.join(acc)))
    with open(out,'w',encoding='utf-8') as f:
        for ts,sp,tx in blocks:
            f.write(f"[{ts}] {sp}: {tx}\n\n")
    return len(blocks)
n=process(sys.argv[1],sys.argv[2])
print(f"{n} blocks")

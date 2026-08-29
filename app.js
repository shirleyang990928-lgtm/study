// ===== 公共 UI 自动注入：若页面缺少这些元素，app.js 自己补上（保证所有页一致）=====
(function(){
  var CHROME="<div id=\"sel-pop\" class=\"ui\">\n  <button id=\"pop-hl\">🖍 高亮</button><div class=\"sep\"></div><button id=\"pop-dict\">📖 查词</button><div class=\"sep\"></div><button id=\"pop-note\">📝 高亮+笔记</button>\n</div>\n<div id=\"dict-card\" class=\"ui\">\n  <button class=\"close-x\" id=\"dc-close\">✕</button>\n  <span class=\"dw\" id=\"dc-word\">…</span><span class=\"dp\" id=\"dc-ph\"></span><button class=\"say\" id=\"dc-say\" title=\"朗读\">🔊</button>\n  <div class=\"zh-big loading\" id=\"dc-zh-big\">翻译中…</div>\n  <div class=\"dd\" id=\"dc-def\"></div>\n  <div class=\"dc-row\"><button class=\"add\" id=\"dc-add\">＋ 存入生词本</button><button class=\"add mine\" id=\"dc-mine\" style=\"display:none\">✓ 设为我的生词</button></div>\n</div>\n<div id=\"note-modal\" class=\"ui\">\n  <div class=\"box\">\n    <div class=\"quote-ref\" id=\"nm-quote\"></div>\n    <textarea id=\"nm-text\" placeholder=\"写下你的想法…\"></textarea>\n    <div class=\"row\"><button class=\"ok\" id=\"nm-ok\">保存笔记</button><button class=\"no\" id=\"nm-cancel\">取消</button></div>\n  </div>\n</div>\n<div id=\"drawer\" class=\"ui\">\n  <div class=\"tabs\">\n    <button data-tab=\"vocab\" class=\"on\">📖 生词本</button>\n    <button data-tab=\"hl\">🖍 划线笔记</button>\n    <button data-tab=\"note\">📝 总笔记</button>\n  </div>\n  <div class=\"pane on\" data-pane=\"vocab\">\n    <div class=\"vocab-stats\">还不会 <b id=\"vc-unknown\">0</b> ・ 已掌握 <b class=\"ok-n\" id=\"vc-known\">0</b> ・ 共 <span id=\"vc-total\">0</span> 词　<span style=\"margin-left:auto;font-size:11px;color:#A8B8B4\">点 ⭕ = 已掌握</span></div>\n    <div id=\"vocab-list\"><p class=\"empty\">还没有生词。选中英文单词 → 点「📖 查词收藏」。</p></div>\n  </div>\n  <div class=\"pane\" data-pane=\"hl\">\n    <div id=\"hl-list\"><p class=\"empty\">还没有划线。开启划线模式后选中英文文字试试。</p></div>\n  </div>\n  <div class=\"pane\" data-pane=\"note\">\n    <textarea id=\"global-note\" style=\"width:100%;min-height:60vh;height:auto;border:1.5px solid #DDE6E3;border-radius:12px;padding:14px;font-size:14.5px;line-height:1.8;background:#FFFEF8;resize:vertical;box-sizing:border-box;overflow:hidden\" placeholder=\"整场讲座的总结、想放进 course map 的点、要转述给家长的话术……\"></textarea>\n  </div>\n</div>\n<div id=\"share-modal\" class=\"ui\">\n  <div id=\"share-card\">\n    <button class=\"sc-x\" id=\"sc-x\">✕</button>\n    <div class=\"sc-quote\" id=\"sc-quote\"></div>\n    <div class=\"sc-note\" id=\"sc-note\" style=\"display:none\"></div>\n    <div class=\"sc-src\"><span id=\"sc-src-txt\"></span><span class=\"sc-brand\">FOGG 学习笔记</span></div>\n    <div id=\"share-actions\"><button class=\"cap\" id=\"sc-cap\">📸 截图保存</button><button class=\"cls\" id=\"sc-close\">关闭</button></div>\n  </div>\n</div>\n<div id=\"sync-modal\" class=\"ui\">\n  <div class=\"box\">\n    <h3 style=\"color:var(--teal);margin-bottom:6px\">☁️ 多设备同步设置</h3>\n    <p style=\"font-size:12.5px;color:#6B8480;line-height:1.7;margin-bottom:12px\">填入你的 <b>Gist ID</b> 和 <b>GitHub Token</b>，划线/笔记就会存到云端。在每台设备上填同一组，就能看到相同内容。（留空 = 只用本机保存）</p>\n    <label style=\"font-size:12px;color:#8CA19D\">Gist ID</label>\n    <input id=\"sync-gist\" class=\"sync-inp\" placeholder=\"例如 3a1b...（那串字母数字）\">\n    <label style=\"font-size:12px;color:#8CA19D;margin-top:8px;display:block\">GitHub Token</label>\n    <input id=\"sync-token\" class=\"sync-inp\" type=\"password\" placeholder=\"ghp_ 或 github_pat_ 开头\">\n    <div id=\"sync-status\" style=\"font-size:12.5px;margin-top:10px;min-height:18px\"></div>\n    <div class=\"row\" style=\"margin-top:12px\">\n      <button class=\"ok\" id=\"sync-save\">连接并同步</button>\n      <button class=\"no\" id=\"sync-clear\">断开（只用本机）</button>\n      <button class=\"no\" id=\"sync-close2\">关闭</button>\n    </div>\n  </div>\n</div>\n<div class=\"tts-bar ui\" id=\"tts-bar\">\n  <button class=\"close\" id=\"tts-x\" title=\"关闭朗读\">✕</button>\n  <div class=\"lang\" id=\"tts-lang\">\n    <button data-lang=\"en\" class=\"on\">EN</button>\n    <button data-lang=\"zh\">中文</button>\n  </div>\n  <div class=\"seg\" id=\"tts-scope\">\n    <button data-scope=\"para\" class=\"on\">整篇</button>\n    <button data-scope=\"from\">从这句起</button>\n  </div>\n  <button id=\"tts-prev\" title=\"上一句\">⏮</button>\n  <button class=\"play\" id=\"tts-play\" title=\"播放/暂停\">▶</button>\n  <button id=\"tts-next\" title=\"下一句\">⏭</button>\n  <div class=\"rate\">\n    <button id=\"tts-slow\" title=\"减速\">−</button>\n    <span class=\"rv\" id=\"tts-rate\">1.0×</span>\n    <button id=\"tts-fast\" title=\"加速\">+</button>\n  </div>\n</div>";
  // 统一公共 UI：先移除页面里可能存在的旧版 chrome，再注入标准版，保证所有页完全一致
  var CHROME_IDS=['sel-pop','dict-card','note-modal','drawer','share-modal','sync-modal','tts-bar'];
  CHROME_IDS.forEach(function(id){ var old=document.getElementById(id); if(old&&old.parentNode) old.parentNode.removeChild(old); });
  var holder=document.createElement('div'); holder.innerHTML=CHROME;
  while(holder.firstChild){ document.body.appendChild(holder.firstChild); }
})();

(function(){
// ===== 从页面的 PAGE_CONFIG 读取本页配置（每个课页在 HTML 里定义）=====
var CFG=(window.PAGE_CONFIG||{});
var KEYBASE=CFG.key||'default-page';
const NOTE_KEY=KEYBASE+'-notes', HL_KEY=KEYBASE+'-highlights', VC_KEY=KEYBASE+'-vocab';
var LAST_READ_KEY='__last_read_'+KEYBASE;
let notes={}, highlights=[], vocab=[], saveTimer=null;

// ===== 云端同步（GitHub Gist）+ 本地兜底 =====
const CFG_GIST='__cfg_gist_id', CFG_TOKEN='__cfg_gist_token';
let gistId=localStorage.getItem(CFG_GIST)||'', gistToken=localStorage.getItem(CFG_TOKEN)||'';
let cloudCache=null, pushTimer=null, cloudOn=false;

function gistHeaders(){return {'Authorization':'token '+gistToken,'Accept':'application/vnd.github+json'}}
async function cloudPull(){
  if(!gistId||!gistToken)return null;
  const r=await fetch('https://api.github.com/gists/'+gistId,{headers:gistHeaders()});
  if(!r.ok)throw new Error('pull '+r.status);
  const j=await r.json();
  const f=j.files&&j.files['data.json'];
  cloudCache=f&&f.content?JSON.parse(f.content):{};
  return cloudCache;
}
async function cloudPush(obj){
  if(!gistId||!gistToken)return;
  const r=await fetch('https://api.github.com/gists/'+gistId,{
    method:'PATCH',headers:gistHeaders(),
    body:JSON.stringify({files:{'data.json':{content:JSON.stringify(obj)}}})
  });
  if(!r.ok)throw new Error('push '+r.status);
}

const store={
  async get(k){
    if(cloudOn&&cloudCache&&(k in cloudCache))return cloudCache[k];
    try{return localStorage.getItem(k)}catch(e){return null}
  },
  async set(k,v){
    try{localStorage.setItem(k,v)}catch(e){}
    if(cloudOn){
      if(!cloudCache)cloudCache={};
      cloudCache[k]=v;
      clearTimeout(pushTimer);
      pushTimer=setTimeout(async()=>{
        try{await cloudPush(cloudCache);cloudBadge('✓ 已同步到云端 '+nowT())}
        catch(e){cloudBadge('⚠ 云端同步失败，已存本地')}
      },900);
    }
  }
};
function nowT(){return new Date().toLocaleTimeString('zh-CN',{hour:'2-digit',minute:'2-digit'})}
function cloudBadge(t){const s=document.getElementById('save-state');if(s)s.textContent=t}

const state=document.getElementById('save-state');
const sections=[...document.querySelectorAll('section')];

function autoGrow(t){if(!t)return;t.style.height='auto';t.style.height=Math.max(t.scrollHeight,window.innerHeight*0.6)+'px';}

// —— 分享卡片 & 工具 ——
let vocabKnownOpen=false;
const SHARE_EN=''; // 占位
function escapeHtml(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function openShareCard(o){
  const q=document.getElementById('sc-quote');
  q.className='sc-quote'+(o.en==='word'||/[a-zA-Z]/.test(o.quote)&&o.en!=='' ? ' sc-en':'');
  q.innerHTML=escapeHtml(o.quote)+(o.zh?'<div class="sc-zh">'+escapeHtml(o.zh)+'</div>':'');
  const n=document.getElementById('sc-note');
  if(o.note){n.style.display='';n.textContent=o.note}else{n.style.display='none'}
  document.getElementById('sc-src-txt').textContent=o.src||'';
  document.getElementById('share-modal').classList.add('open');
}
(function(){
  const m=document.getElementById('share-modal');
  const close=()=>m.classList.remove('open');
  const x=document.getElementById('sc-x'),c=document.getElementById('sc-close');
  if(x)x.onclick=close;if(c)c.onclick=close;
  m.addEventListener('click',e=>{if(e.target===m)close()});
  const cap=document.getElementById('sc-cap');
  if(cap)cap.onclick=async()=>{
    const card=document.getElementById('share-card');
    const actions=document.getElementById('share-actions');
    if(typeof html2canvas==='undefined'){
      // 动态载入截图库
      await new Promise((res,rej)=>{const s=document.createElement('script');s.src='https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';s.onload=res;s.onerror=rej;document.head.appendChild(s)}).catch(()=>{});
    }
    if(typeof html2canvas==='undefined'){setState('⚠ 截图组件需要联网，可手动系统截图');return}
    actions.style.visibility='hidden';
    try{
      const canvas=await html2canvas(card,{backgroundColor:null,scale:2});
      actions.style.visibility='';
      canvas.toBlob(blob=>{
        const url=URL.createObjectURL(blob);
        const a=document.createElement('a');a.href=url;a.download=(CFG.key||'FOGG')+'-笔记卡片.png';a.click();
        setTimeout(()=>URL.revokeObjectURL(url),1000);
        setState('📸 卡片已保存为图片');
      });
    }catch(err){actions.style.visibility='';setState('⚠ 截图失败，可手动系统截图')}
  };
})();

function setState(t){state.textContent=t}
function scheduleSave(){setState('保存中…');try{localStorage.setItem(LAST_READ_KEY,Date.now())}catch(e){}clearTimeout(saveTimer);saveTimer=setTimeout(saveAll,700)}
async function saveAll(){
  try{
    await store.set(NOTE_KEY,JSON.stringify(notes));
    await store.set(HL_KEY,JSON.stringify(highlights));
    await store.set(VC_KEY,JSON.stringify(vocab));
    setState(cloudOn?'✓ 已保存（同步中…）':'✓ 已保存 '+nowT());
  }catch(e){setState('⚠ 保存失败，稍后自动重试');setTimeout(saveAll,3000)}
}
async function load(){
  if(gistId&&gistToken){try{await cloudPull();cloudOn=true}catch(e){cloudOn=false}}
  try{const v=await store.get(NOTE_KEY);if(v)notes=JSON.parse(v)}catch(e){}
  try{const v=await store.get(HL_KEY);if(v)highlights=JSON.parse(v)}catch(e){}
  try{const v=await store.get(VC_KEY);if(v)vocab=JSON.parse(v)}catch(e){}
  // 老师预置术语（紫色虚线；点开可「设为我的生词」升级成蓝色）
  const PRESET_VOCAB=(CFG.preset||[]);
  // 合并：用户没有的才补进来，并打上 preset 标记
  (function(){
    const have={}; vocab.forEach(v=>have[v.word.toLowerCase()]=1);
    PRESET_VOCAB.forEach(p=>{ if(!have[p.word.toLowerCase()]) vocab.push({word:p.word,zh:p.zh,def:p.def,phonetic:'',known:false,preset:true,sec:''}); });
  })();
  const g=document.getElementById('global-note');if(notes.__global)g.value=notes.__global;autoGrow(g);
  highlights.forEach((h,i)=>{if(!h.id)h.id='h'+Date.now()+'_'+i;applyHighlight(h.sec,h.text,h.id)});refreshMarkNoteStyles();
  renderHlList();renderVocab();markVocabWords();
  setState(cloudOn?('☁️ 已从云端载入 '+nowT()):(highlights.length||vocab.length||Object.keys(notes).length?'✓ 已恢复你的笔记 · 划线 · 术语':'已就绪'));
  if(typeof updateCloudBtn==='function')updateCloudBtn();
}

// notes events
document.addEventListener('input',e=>{
  if(e.target.id==='global-note'){notes.__global=e.target.value;autoGrow(e.target);scheduleSave()}
});

// 把每段的逐句中文合并成一个整齐的翻译块
document.querySelectorAll('.para,.quote').forEach(p=>{
  const szs=[...p.querySelectorAll('.sz')];
  if(!szs.length)return;
  const normal=szs.filter(s=>!s.classList.contains('comment')).map(s=>s.textContent).join('');
  const comment=szs.filter(s=>s.classList.contains('comment')).map(s=>s.textContent).join('');
  const d=document.createElement('div');d.className='zh-block';
  d.textContent=normal;
  if(comment){const c=document.createElement('span');c.className='comment-line';c.textContent=comment;d.appendChild(c)}
  p.appendChild(d);
});

// per-paragraph 中文 toggle buttons
document.querySelectorAll('.para,.quote').forEach(p=>{
  if(!p.querySelector('.zh-block'))return;
  const b=document.createElement('button');
  b.className='zh-btn';b.textContent='中';b.title='显示/隐藏本段中文';
  b.onclick=e=>{e.stopPropagation();p.classList.toggle('zh-open');b.classList.toggle('on',p.classList.contains('zh-open'))};
  p.appendChild(b);
});

// zh toggles
const zhBtn=document.getElementById('zh-toggle');
if(zhBtn){zhBtn.onclick=()=>{document.body.classList.toggle('show-zh');zhBtn.textContent=document.body.classList.contains('show-zh')?'隐藏全部中文':'显示全部中文';zhBtn.classList.toggle('primary')};}
// per-section: dblclick on section title toggles that section
sections.forEach(s=>{const h=s.querySelector('h2');h.style.cursor='pointer';h.title='点击：切换本节中文';h.onclick=()=>s.classList.toggle('show-zh')});

// ---- selection popup ----
const pop=document.getElementById('sel-pop'),dictCard=document.getElementById('dict-card'),markMenu=document.getElementById('mark-menu');
let curSel=null,curMark=null,curDict=null,suppressClickUntil=0;
const IS_TOUCH = ('ontouchstart' in window) || navigator.maxTouchPoints>0;
function placeAt(el,rect){
  el.style.display=(el.id==='sel-pop')?'flex':'block';
  const vw=document.documentElement.clientWidth,vh=document.documentElement.clientHeight;
  const w=el.offsetWidth,h=el.offsetHeight;
  // 触屏设备：菜单固定在屏幕底部中央，避免被 iPad 系统选择菜单（拷贝/翻译…）挡住
  if(IS_TOUCH && (el.id==='sel-pop' || el.id==='mark-menu')){
    el.style.left=Math.max(8,(vw-w)/2)+'px';
    el.style.top=(vh-h-24)+'px';
    el.classList.add('touch-dock');
    return;
  }
  el.style.left=Math.max(8,Math.min(rect.left+rect.width/2-w/2,vw-w-8))+'px';
  let top=rect.bottom+10;               // 默认贴在选区正下方
  if(top+h>vh-8)top=rect.top-h-10;      // 下方放不下才翻到上方
  el.style.top=Math.max(8,top)+'px';
}
// 滚动时收起浮层，避免错位
window.addEventListener('scroll',()=>{pop.style.display='none';markMenu.style.display='none'},{passive:true});
function showSelPopup(){
  const sel=window.getSelection();
  if(!sel||sel.isCollapsed){pop.style.display='none';return}
  const text=sel.toString().replace(/\s+/g,' ').trim();
  const node=sel.anchorNode;const anchor=node&&(node.nodeType===3?node.parentElement:node);
  const en=anchor&&anchor.closest?anchor.closest('.en,.keypoints,.explain,.sec-head'):null;
  if(!en||text.length<2){pop.style.display='none';return}
  // 中文译文区不参与（避免和 .sz 冲突）
  if(anchor.closest&&anchor.closest('.sz,.zh-block')){pop.style.display='none';return}
  const sec=en.closest('section');
  let rect;try{rect=sel.getRangeAt(0).getBoundingClientRect()}catch(e){return}
  curSel={text:text,sec:sec?sec.id:'',rect:rect,range:sel.getRangeAt(0).cloneRange()};
  placeAt(pop,curSel.rect);
}
document.addEventListener('mouseup',e=>{
  if(pop.contains(e.target)||dictCard.contains(e.target)||markMenu.contains(e.target))return;
  setTimeout(showSelPopup,10);
});
let touchSelTimer=null,isTouch=false;
document.addEventListener('touchstart',()=>{isTouch=true},{passive:true});
document.addEventListener('selectionchange',()=>{
  if(!isTouch)return;
  clearTimeout(touchSelTimer);
  touchSelTimer=setTimeout(showSelPopup,450);
});
document.addEventListener('touchend',e=>{
  if(!isTouch)return;
  if(pop.contains(e.target)||dictCard.contains(e.target)||markMenu.contains(e.target))return;
  clearTimeout(touchSelTimer);
  touchSelTimer=setTimeout(showSelPopup,350);
},{passive:true});
function wrapRange(range,hid){
  // 用真实选区包裹，支持任意长度/跨段落。收集选区内的文本节点后逐个包裹。
  try{
    const root=range.commonAncestorContainer;
    const rootEl=root.nodeType===1?root:root.parentElement;
    const walker=document.createTreeWalker(rootEl,NodeFilter.SHOW_TEXT,{acceptNode:n=>{
      if(n.parentElement&&n.parentElement.closest('.sz,.zh-block'))return NodeFilter.FILTER_REJECT;
      if(!range.intersectsNode(n))return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    }});
    const targets=[];
    while(walker.nextNode())targets.push(walker.currentNode);
    if(!targets.length)return false;
    let wrapped=false;
    for(const node of targets){
      let s=0,e=node.data.length;
      if(node===range.startContainer)s=range.startOffset;
      if(node===range.endContainer)e=range.endOffset;
      if(s>=e)continue;
      let t=node;
      if(s>0)t=t.splitText(s);
      if(e-s<t.data.length)t.splitText(e-s);
      const mk=document.createElement('mark');mk.dataset.hid=hid;
      t.parentNode.insertBefore(mk,t);mk.appendChild(t);
      wrapped=true;
    }
    return wrapped;
  }catch(err){return false}
}
function doHighlight(withNote){
  if(!curSel)return;
  const savedRange=curSel.range;
  window.getSelection().removeAllRanges();
  pop.style.display='none';
  suppressClickUntil=Date.now()+450;
  const hid='h'+Date.now();
  // 优先用真实选区包裹（任意长度都行），失败再退回文本匹配
  let ok=savedRange?wrapRange(savedRange,hid):false;
  if(!ok)ok=applyHighlight(curSel.sec,curSel.text,hid);
  if(ok){
    const h={id:hid,sec:curSel.sec,text:curSel.text,note:''};
    highlights.push(h);
    refreshMarkNoteStyles();renderHlList();scheduleSave();
    if(withNote){
      openNoteModal(h.text,'',val=>{h.note=val;refreshMarkNoteStyles();renderHlList();scheduleSave()});
    }
  }else{
    setState('⚠ 这段没能高亮，换个选法再试一次');
  }
}
document.getElementById('pop-hl').onclick=()=>doHighlight(false);
document.getElementById('pop-note').onclick=()=>doHighlight(true);
document.getElementById('pop-dict').onclick=()=>{
  if(!curSel)return;
  const rect=curSel.rect,t=curSel.text,s=curSel.sec;
  window.getSelection().removeAllRanges();pop.style.display='none';
  openDict(t,s,rect);
};

// ---- dictionary card: 中文翻译优先 ----
async function translateZh(text){
  try{
    const r=await fetch('https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q='+encodeURIComponent(text));
    if(!r.ok)throw 0;
    const j=await r.json();
    return (j[0]||[]).map(x=>x[0]).join('');
  }catch(e){
    try{
      const r=await fetch('https://api.mymemory.translated.net/get?q='+encodeURIComponent(text)+'&langpair=en|zh-CN');
      const j=await r.json();
      return j.responseData&&j.responseData.translatedText||'';
    }catch(e2){return ''}
  }
}
async function openDict(text,sec,rect){
  const clean=text.trim();
  const isLong=clean.length>120;
  const isPhrase=/\s/.test(clean);
  const word=isLong?clean:(isPhrase?clean:(clean.match(/[a-zA-Z][a-zA-Z'\-]*/)||[clean])[0].toLowerCase());
  curDict={word:word,sec:sec,phonetic:'',def:'',audio:'',zh:'',long:isLong};
  const dw=document.getElementById('dc-word');
  dw.className=isLong?'dw long':'dw';
  dw.textContent=isLong?'📖 选段翻译':word;
  document.getElementById('dc-ph').textContent='';
  document.getElementById('dc-say').style.display=isLong?'none':'';
  document.getElementById('dc-add').style.display=isLong?'none':'';
  const dd=document.getElementById('dc-def');
  dd.className=isLong?'orig-small':'dd';
  dd.textContent=isLong?clean:'';
  const zhBig=document.getElementById('dc-zh-big');
  zhBig.className='zh-big loading';zhBig.textContent='翻译中…';
  placeAt(dictCard,rect);
  const q=clean.slice(0,450);
  const jobs=[translateZh(q).then(zh=>{
    if(curDict&&curDict.word===word){
      curDict.zh=zh;
      zhBig.className='zh-big';
      zhBig.textContent=zh||'⚠ 翻译服务连不上（需要联网）';
    }
  })];
  if(!isPhrase&&!isLong){
    jobs.push((async()=>{
      try{
        const res=await fetch('https://api.dictionaryapi.dev/api/v2/entries/en/'+encodeURIComponent(word));
        if(!res.ok)return;
        const e0=(await res.json())[0]||{};
        if(!curDict||curDict.word!==word)return;
        curDict.phonetic=e0.phonetic||((e0.phonetics||[]).find(p=>p.text)||{}).text||'';
        curDict.audio=((e0.phonetics||[]).find(p=>p.audio)||{}).audio||'';
        const defs=[];
        (e0.meanings||[]).slice(0,2).forEach(m=>{
          const d=m.definitions&&m.definitions[0];
          if(d)defs.push(m.partOfSpeech+'. '+d.definition);
        });
        curDict.def=defs.join('　');
        document.getElementById('dc-ph').textContent=curDict.phonetic;
        document.getElementById('dc-def').textContent=curDict.def;
      }catch(e){}
    })());
  }
  await Promise.all(jobs);
}
function openDictStored(v,rect){
  curDict={word:v.word,sec:v.sec,phonetic:v.phonetic||'',def:v.def||'',audio:'',zh:v.zh||'',long:false,preset:v.preset||false};
  const dw=document.getElementById('dc-word');
  dw.className='dw';dw.textContent=v.word;
  document.getElementById('dc-ph').textContent=v.phonetic||'';
  document.getElementById('dc-say').style.display='';
  document.getElementById('dc-add').style.display='none';
  document.getElementById('dc-mine').style.display=v.preset?'':'none';
  const dd=document.getElementById('dc-def');
  dd.className='dd';dd.textContent=v.def||'';
  const zhBig=document.getElementById('dc-zh-big');
  zhBig.className='zh-big';zhBig.textContent=v.zh||'（未填中文，可在生词本里补）';
  placeAt(dictCard,rect);
}
document.getElementById('dc-say').onclick=e=>{
  e.stopPropagation();
  if(curDict&&curDict.audio){new Audio(curDict.audio).play().catch(()=>{})}
  else if(curDict&&window.speechSynthesis){const u=new SpeechSynthesisUtterance(curDict.word);u.lang='en-GB';speechSynthesis.speak(u)}
};
document.getElementById('dc-add').onclick=e=>{
  e.stopPropagation();
  if(!curDict)return;
  const ex=vocab.find(v=>v.word===curDict.word);
  if(ex){ex.zh=curDict.zh||ex.zh;ex.def=curDict.def||ex.def;ex.phonetic=curDict.phonetic||ex.phonetic}
  else vocab.unshift({word:curDict.word,phonetic:curDict.phonetic,def:curDict.def,zh:curDict.zh,known:false,sec:curDict.sec,ts:Date.now()});
  renderVocab();markVocabWords();scheduleSave();
  dictCard.style.display='none';
  setState('✓ 已存入生词本');
};
document.getElementById('dc-mine').onclick=e=>{
  e.stopPropagation();
  if(!curDict)return;
  const it=vocab.find(v=>v.word===curDict.word);
  if(it){it.preset=false;}
  renderVocab();markVocabWords();scheduleSave();
  dictCard.style.display='none';
  setState('✓ 已设为你的生词');
};
document.getElementById('dc-close').onclick=()=>dictCard.style.display='none';

// ---- note modal (centered) ----
const noteModal=document.getElementById('note-modal');
let noteCb=null;
function openNoteModal(quote,initial,cb){
  document.getElementById('nm-quote').textContent='“'+quote+'”';
  const ta=document.getElementById('nm-text');
  ta.value=initial||'';
  noteCb=cb;
  noteModal.classList.add('open');
  setTimeout(()=>ta.focus(),50);
}
document.getElementById('nm-ok').onclick=()=>{
  noteModal.classList.remove('open');
  if(noteCb)noteCb(document.getElementById('nm-text').value);
  noteCb=null;
};
document.getElementById('nm-cancel').onclick=()=>{noteModal.classList.remove('open');noteCb=null};
noteModal.addEventListener('click',e=>{if(e.target===noteModal){noteModal.classList.remove('open');noteCb=null}});

// ---- click on a highlight => menu ----
document.addEventListener('click',e=>{
  // 来自弹出菜单自身的点击（如「查词」按钮）不算“点外面”，否则刚打开的卡片会被同一下点击关掉
  if(pop.contains(e.target)||markMenu.contains(e.target)||dictCard.contains(e.target))return;
  if(e.target.classList&&e.target.classList.contains('vocab-mark')){
    const v=vocab.find(x=>x.word.toLowerCase()===e.target.textContent.toLowerCase());
    if(v){openDictStored(v,e.target.getBoundingClientRect());return}
  }
  if(e.target.tagName==='MARK'){
    if(Date.now()<suppressClickUntil)return;
    curMark=e.target;
    placeAt(markMenu,e.target.getBoundingClientRect());
    return;
  }
  // 点空白处：全部收起
  markMenu.style.display='none';
  dictCard.style.display='none';
  const drawer=document.getElementById('drawer');
  if(drawer.classList.contains('open')&&!drawer.contains(e.target)&&e.target.id!=='drawer-btn'&&!e.target.closest('#drawer-btn'))drawer.classList.remove('open');
});
function findHl(markEl){
  return highlights.find(h=>h.id===markEl.dataset.hid);
}
document.getElementById('mm-note').onclick=()=>{
  markMenu.style.display='none';
  const h=curMark&&findHl(curMark);if(!h)return;
  openNoteModal(h.text,h.note,val=>{h.note=val;refreshMarkNoteStyles();renderHlList();scheduleSave()});
};
document.getElementById('mm-dict').onclick=()=>{
  markMenu.style.display='none';
  if(!curMark)return;
  const sec=curMark.closest('section');
  openDict(curMark.textContent,sec?sec.id:'',curMark.getBoundingClientRect());
};
document.getElementById('mm-del').onclick=()=>{
  markMenu.style.display='none';
  const h=curMark&&findHl(curMark);
  if(h){removeHighlightMarks(h.id);highlights.splice(highlights.indexOf(h),1)}
  else if(curMark){curMark.outerHTML=curMark.textContent}
  renderHlList();scheduleSave();
};
function refreshMarkNoteStyles(){
  document.querySelectorAll('mark[data-hid]').forEach(m=>{
    const h=findHl(m);m.classList.toggle('has-note',!!(h&&h.note));
  });
}


// ---- 在原文中标出已收藏的生词（蓝色） ----
function markVocabWords(){
  document.querySelectorAll('span.vocab-mark').forEach(s=>{s.replaceWith(document.createTextNode(s.textContent))});
  document.querySelectorAll('.en').forEach(en=>en.normalize());
  const list=vocab.filter(v=>!v.known&&!/\s/.test(v.word));
  if(!list.length)return;
  const presetSet={}; list.forEach(v=>{presetSet[v.word.toLowerCase()]=v.preset?1:0});
  const words=list.map(v=>v.word);
  const re=new RegExp('\\b('+words.map(w=>w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+')\\b','gi');
  document.querySelectorAll('.en').forEach(en=>{
    const parts=en.innerHTML.split(/(<[^>]+>)/);
    let changed=false;
    for(let i=0;i<parts.length;i++){
      if(parts[i].startsWith('<'))continue;
      if(re.test(parts[i])){
        parts[i]=parts[i].replace(re,function(m,w){
          var cls=presetSet[w.toLowerCase()]? 'vocab-mark preset':'vocab-mark';
          var tip=presetSet[w.toLowerCase()]? '老师预置的术语，点开可「设为我的生词」':'已在生词本，点击复习';
          return '<span class="'+cls+'" title="'+tip+'">'+w+'</span>';
        });
        changed=true;
      }
      re.lastIndex=0;
    }
    if(changed)en.innerHTML=parts.join('');
  });
}

// ---- vocabulary drawer: compact rows ----
function renderVocab(){
  const box=document.getElementById('vocab-list');
  const unknownArr=vocab.filter(v=>!v.known);
  const knownArr=vocab.filter(v=>v.known);
  document.getElementById('vc-total').textContent=vocab.length;
  document.getElementById('vc-unknown').textContent=unknownArr.length;
  document.getElementById('vc-known').textContent=knownArr.length;
  if(!vocab.length){box.innerHTML='<p class="empty">还没有术语。选中关键词 → 点「📖 收藏」。</p>';return}
  function row(v){
    const gi=vocab.indexOf(v);
    return '<div class="vocab-item'+(v.known?' known':'')+'" data-i="'+gi+'">'
      +'<div class="main"><span class="w" data-i="'+gi+'" title="点开看卡片">'+escapeHtml(v.word)+'</span><span class="ph">'+escapeHtml(v.phonetic||'')+'</span>'
      +'<input class="zh-inline" data-i="'+gi+'" placeholder="中文…" value="'+String(v.zh||'').replace(/"/g,'&quot;')+'"></div>'
      +'<button class="kbtn'+(v.known?' on':'')+'" data-i="'+gi+'" title="'+(v.known?'点击取消已掌握':'标记为已掌握')+'">'+(v.known?'✅':'⭕')+'</button>'
      +'<button class="rm" data-i="'+gi+'" title="删除">✕</button>'
      +'</div>';
  }
  let html=unknownArr.map(row).join('');
  if(knownArr.length){
    html+='<div class="known-head'+(vocabKnownOpen?' open':'')+'" id="known-head"><span class="caret">▸</span>已掌握 '+knownArr.length+' 个'+(vocabKnownOpen?'（点击收起）':'（点击展开）')+'</div>';
    if(vocabKnownOpen)html+='<div id="known-wrap">'+knownArr.map(row).join('')+'</div>';
  }
  box.innerHTML=html;
  const kh=document.getElementById('known-head');
  if(kh)kh.onclick=()=>{vocabKnownOpen=!vocabKnownOpen;renderVocab()};
  box.querySelectorAll('.kbtn').forEach(b=>b.onclick=(e)=>{e.stopPropagation();vocab[+b.dataset.i].known=!vocab[+b.dataset.i].known;renderVocab();markVocabWords();scheduleSave()});
  box.querySelectorAll('.rm').forEach(b=>b.onclick=(e)=>{e.stopPropagation();vocab.splice(+b.dataset.i,1);renderVocab();markVocabWords();scheduleSave()});
  box.querySelectorAll('.zh-inline').forEach(inp=>{inp.onclick=(e)=>e.stopPropagation();inp.oninput=()=>{vocab[+inp.dataset.i].zh=inp.value;scheduleSave()}});
  // 点词 → 分享卡片
  box.querySelectorAll('.w').forEach(w=>w.onclick=(e)=>{
    e.stopPropagation();
    const v=vocab[+w.dataset.i];
    const title=document.querySelector('#'+v.sec+' h2');
    const speaker=SHARE_EN;
    openShareCard({quote:v.word, zh:v.zh||'', note:'', src:'§ '+(title?title.textContent:(v.sec||'')), en:'word'});
  });
}

// ---- drawer tabs ----
function switchTab(name){
  if(name==='note')setTimeout(()=>autoGrow(document.getElementById('global-note')),20);
  document.querySelectorAll('#drawer .tabs button').forEach(b=>b.classList.toggle('on',b.dataset.tab===name));
  document.querySelectorAll('#drawer .pane').forEach(p=>p.classList.toggle('on',p.dataset.pane===name));
}
document.querySelectorAll('#drawer .tabs button').forEach(b=>b.onclick=()=>switchTab(b.dataset.tab));

function applyHighlight(secId,text,hid){
  const sec=document.getElementById(secId);if(!sec)return false;
  const target=text.replace(/\s+/g,' ').trim();
  const esc=target.replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replace(/ /g,'[\\s\\u00a0]+');
  const re=new RegExp(esc);
  for(const en of sec.querySelectorAll('.en,.keypoints,.explain,.sec-head')){
    // 收集英文文本节点（跳过隐藏的中文 .sz）
    const walker=document.createTreeWalker(en,NodeFilter.SHOW_TEXT,{acceptNode:n=>{
      return n.parentElement&&n.parentElement.closest('.sz,.zh-block')?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT;
    }});
    const nodes=[];let full='';
    while(walker.nextNode()){nodes.push({node:walker.currentNode,start:full.length});full+=walker.currentNode.data}
    const m=re.exec(full);
    if(!m)continue;
    const s0=m.index,e0=m.index+m[0].length;
    // 找出每个文本节点内需要包裹的区间
    const segs=[];
    for(const rec of nodes){
      const ns=rec.start,ne=rec.start+rec.node.data.length;
      const s=Math.max(s0,ns),e=Math.min(e0,ne);
      if(s<e)segs.push({node:rec.node,s:s-ns,e:e-ns});
    }
    // 倒序包裹，避免 splitText 影响后续偏移
    for(let i=segs.length-1;i>=0;i--){
      const g=segs[i];
      let t=g.node;
      if(g.s>0)t=t.splitText(g.s);
      if(g.e-g.s<t.data.length)t.splitText(g.e-g.s);
      const mk=document.createElement('mark');
      mk.dataset.hid=hid;
      t.parentNode.insertBefore(mk,t);
      mk.appendChild(t);
    }
    return true;
  }
  return false;
}
function removeHighlightMarks(hid){
  document.querySelectorAll('mark[data-hid="'+hid+'"]').forEach(mk=>{
    const p=mk.parentNode;
    while(mk.firstChild)p.insertBefore(mk.firstChild,mk);
    p.removeChild(mk);p.normalize();
  });
}
function renderHlList(){
  const box=document.getElementById('hl-list');
  if(!highlights.length){box.innerHTML='<p class="empty">还没有划线。选中文字 → 点「🖍 高亮」。</p>';return}
  box.innerHTML=highlights.map((h,i)=>{
    const title=document.querySelector('#'+h.sec+' h2');
    const src=title?title.textContent:h.sec;
    let inner='<span class="del" data-i="'+i+'" title="删除">✕</span>';
    inner+='<span class="htext">'+escapeHtml(h.text)+'</span>';
    if(h.note){inner+='<span class="hnote">'+escapeHtml(h.note)+'</span>';}
    else{inner+='<button class="addnote" data-i="'+i+'">➕ 写笔记</button>';}
    inner+='<span class="src">§ '+escapeHtml(src)+'</span>';
    return '<div class="hl-item" data-i="'+i+'">'+inner+'</div>';
  }).join('');
  // 点整条 → 分享卡片
  box.querySelectorAll('.hl-item').forEach(el=>{
    el.onclick=(e)=>{
      if(e.target.closest('.del')||e.target.closest('.addnote')||e.target.closest('.hnoteinp'))return;
      const i=+el.dataset.i;const h=highlights[i];
      const title=document.querySelector('#'+h.sec+' h2');
      openShareCard({quote:h.text, zh:'', note:h.note||'', src:'§ '+(title?title.textContent:h.sec), en:''+SHARE_EN});
    };
  });
  box.querySelectorAll('.del').forEach(d=>d.onclick=(e)=>{
    e.stopPropagation();
    const h=highlights[+d.dataset.i];
    if(h.id)removeHighlightMarks(h.id);
    highlights.splice(+d.dataset.i,1);renderHlList();scheduleSave();
  });
  box.querySelectorAll('.addnote').forEach(b=>b.onclick=(e)=>{
    e.stopPropagation();
    const i=+b.dataset.i;
    const item=b.closest('.hl-item');
    b.outerHTML='<input class="hnoteinp" data-i="'+i+'" placeholder="写下你的想法…" value="">';
    const inp=item.querySelector('.hnoteinp');inp.focus();
    inp.onclick=(ev)=>ev.stopPropagation();
    inp.oninput=()=>{highlights[i].note=inp.value;refreshMarkNoteStyles();scheduleSave()};
    inp.onblur=()=>{if(inp.value.trim())renderHlList()};
  });
}

// ---- export study notes ----
document.getElementById('export-btn').onclick=async()=>{
  const lines=['# '+(CFG.exportTitle||CFG.title||'我的学习笔记'),'','导出时间：'+new Date().toLocaleString('zh-CN'),''];
  if(notes.__global){lines.push('## 总笔记','',notes.__global,'')}
  const bySec={};
  highlights.forEach(h=>{(bySec[h.sec]=bySec[h.sec]||[]).push(h)});
  sections.forEach(s=>{
    const t=s.querySelector('h2').textContent;
    const hs=bySec[s.id]||[],n=notes[s.id];
    if(!hs.length&&!n)return;
    lines.push('## '+t,'');
    hs.forEach(h=>{
      lines.push('- 🖍 “'+h.text+'”');
      if(h.note)lines.push('  - 📝 '+h.note);
    });
    if(n)lines.push('','📝 本节笔记：'+n);
    lines.push('');
  });
  if(vocab.length){
    lines.push('## 生词本（还不会 '+vocab.filter(v=>!v.known).length+' / 共 '+vocab.length+'）','');
    vocab.forEach(v=>lines.push('- **'+v.word+'** '+(v.phonetic||'')+' — '+(v.zh||String(v.def||'').split('\n')[0])+(v.known?'　✅已掌握':'　❌还不会')));
    lines.push('');
  }
  const md=lines.join('\n');
  let copied=false;
  try{await navigator.clipboard.writeText(md);copied=true}catch(e){}
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([md],{type:'text/markdown'}));
  a.download='cls-20260824-cw-alex-l8-wk9-my-notes.md';a.click();
  setState(copied?'✓ 已复制到剪贴板 + 下载 .md，可直接丢给 Claude':'✓ 已下载 .md，可直接丢给 Claude');
};

// drawer
document.getElementById('drawer-btn').onclick=()=>document.getElementById('drawer').classList.toggle('open');

// scroll spy
const links=[...document.querySelectorAll('.map a')];
if(window.IntersectionObserver){
const obs=new IntersectionObserver(es=>{es.forEach(en=>{if(en.isIntersecting){links.forEach(l=>l.classList.toggle('active',l.getAttribute('href')==='#'+en.target.id))}})},{rootMargin:'-20% 0px -70% 0px'});
sections.forEach(s=>obs.observe(s));
}


// ---- 同步设置 UI 逻辑 ----
const syncModal=document.getElementById('sync-modal');
function openSync(){
  document.getElementById('sync-gist').value=gistId;
  document.getElementById('sync-token').value=gistToken;
  document.getElementById('sync-status').innerHTML=cloudOn?'<span class="cloud-dot on"></span>已连接云端':'<span class="cloud-dot"></span>当前仅本机保存';
  syncModal.classList.add('open');
}
document.getElementById('sync-btn').onclick=openSync;
document.getElementById('sync-close2').onclick=()=>syncModal.classList.remove('open');
syncModal.addEventListener('click',e=>{if(e.target===syncModal)syncModal.classList.remove('open')});
document.getElementById('sync-clear').onclick=()=>{
  localStorage.removeItem(CFG_GIST);localStorage.removeItem(CFG_TOKEN);
  gistId='';gistToken='';cloudOn=false;cloudCache=null;
  updateCloudBtn();
  document.getElementById('sync-status').innerHTML='<span class="cloud-dot"></span>已断开，改用本机保存';
};
document.getElementById('sync-save').onclick=async()=>{
  const gid=document.getElementById('sync-gist').value.trim();
  const tok=document.getElementById('sync-token').value.trim();
  const st=document.getElementById('sync-status');
  if(!gid||!tok){st.textContent='请把两个都填上';return}
  st.textContent='正在连接…';
  gistId=gid;gistToken=tok;
  try{
    const cloud=await cloudPull();          // 试着拉云端
    cloudOn=true;
    localStorage.setItem(CFG_GIST,gid);localStorage.setItem(CFG_TOKEN,tok);
    // 若云端为空，把本机现有内容推上去（首次上传）
    const empty=!cloud||Object.keys(cloud).length===0;
    if(empty){
      cloudCache={};
      cloudCache[NOTE_KEY]=localStorage.getItem(NOTE_KEY)||'';
      cloudCache[HL_KEY]=localStorage.getItem(HL_KEY)||'';
      cloudCache[VC_KEY]=localStorage.getItem(VC_KEY)||'';
      await cloudPush(cloudCache);
      st.innerHTML='<span class="cloud-dot on"></span>已连接，本机内容已上传到云端';
    }else{
      st.innerHTML='<span class="cloud-dot on"></span>已连接，正在载入云端内容…';
    }
    updateCloudBtn();
    await reloadFromStore();                 // 重新用云端数据渲染
    st.innerHTML='<span class="cloud-dot on"></span>同步成功！其它设备填同一组即可看到相同内容';
    setTimeout(()=>syncModal.classList.remove('open'),1200);
  }catch(e){
    cloudOn=false;
    st.innerHTML='⚠ 连接失败：请检查 Gist ID 和 Token 是否正确（Token 需勾选 gist 权限）';
  }
};
function updateCloudBtn(){
  const b=document.getElementById('sync-btn');
  b.innerHTML=(cloudOn?'<span class="cloud-dot on"></span>':'<span class="cloud-dot"></span>')+'☁️ 同步';
}
// 清空当前内存并按 store 重新载入（切换云端后刷新界面）
async function reloadFromStore(){
  document.querySelectorAll('mark[data-hid]').forEach(mk=>{const p=mk.parentNode;while(mk.firstChild)p.insertBefore(mk.firstChild,mk);p.removeChild(mk);p.normalize()});
  document.querySelectorAll('span.vocab-mark').forEach(s=>s.replaceWith(document.createTextNode(s.textContent)));
  notes={};highlights=[];vocab=[];
  await load();
}


// ---- 字体大小调节 ----
(function(){
  const FS_KEY='__fs_level';
  const LEVELS=[14,15.5,16.5,18.5,21];           // 5 档字号(px)
  const NAMES=['小','较小','标准','较大','大'];
  let idx=parseInt(localStorage.getItem(FS_KEY));
  if(isNaN(idx)||idx<0||idx>4)idx=2;
  function apply(){
    document.documentElement.style.setProperty('--fs',LEVELS[idx]+'px');
    const c=document.getElementById('fs-cur');if(c)c.textContent=NAMES[idx];
    localStorage.setItem(FS_KEY,idx);
    if(typeof autoGrow==='function')autoGrow(document.getElementById('global-note'));
  }
  const minus=document.getElementById('fs-minus'),plus=document.getElementById('fs-plus');
  if(minus)minus.onclick=()=>{if(idx>0){idx--;apply()}};
  if(plus)plus.onclick=()=>{if(idx<4){idx++;apply()}};
  apply();
})();


// ---- 阅读书签（钉 / 跳，分开两个按钮） ----
(function(){
  const BM_KEY='__bookmark_y';
  const pinBtn=document.getElementById('bm-pin');
  const goBtn=document.getElementById('bm-go');
  function flashAt(y){
    const mid=y+window.innerHeight*0.35;
    const paras=document.querySelectorAll('.para,.quote,.sec-head');
    let best=null,bd=1e9;
    paras.forEach(p=>{const r=p.getBoundingClientRect();const top=r.top+window.scrollY;const d=Math.abs(top-mid);if(d<bd){bd=d;best=p}});
    if(best){best.classList.add('bm-flash');setTimeout(()=>best.classList.remove('bm-flash'),1200);}
  }
  if(pinBtn)pinBtn.onclick=()=>{
    localStorage.setItem(BM_KEY,String(Math.round(window.scrollY)));
    setState('📌 已钉书签，之后点「🔖 回书签」就能跳回来');
  };
  if(goBtn)goBtn.onclick=()=>{
    const y=parseInt(localStorage.getItem(BM_KEY));
    if(isNaN(y)){setState('还没有书签，先点「📌 钉这里」钉一个');return}
    window.scrollTo({top:y,behavior:'smooth'});
    flashAt(y);
    setState('🔖 已跳回书签位置');
  };
})();


// ================= 朗读 Read-Aloud =================
(function(){
  if(!('speechSynthesis' in window)) return;
  var synth=window.speechSynthesis;
  var IS_SENT = document.querySelector('.sent')!==null;  // louise/chris vs reading

  // 收集朗读单元：{el, en, zh}
  var UNITS=[];
  function buildUnits(){
    UNITS=[];
    if(IS_SENT){
      document.querySelectorAll('.para .sent, .quote .sent').forEach(function(s){
        var se=s.querySelector('.se'), sz=s.querySelector('.sz');
        UNITS.push({el:s, en:se?se.textContent.trim():'', zh:sz?sz.textContent.trim():''});
      });
    }else{
      // reading：把每个 p.en 的中文按句号/问号/叹号切句，包成 span.tts-sent
      document.querySelectorAll('.para p.en, .quote p.en').forEach(function(p){
        if(p.dataset.ttsReady) return;
        // 保留说话人 chip
        var chip=p.querySelector('.spk');
        var chipHtml=chip?chip.outerHTML:'';
        var raw=p.textContent;
        if(chip) raw=raw.replace(chip.textContent,'');
        raw=raw.trim();
        var parts=raw.match(/[^。！？]*[。！？]?/g).filter(function(x){return x.trim().length});
        p.innerHTML=chipHtml+parts.map(function(t){return '<span class="tts-sent">'+t+'</span>';}).join('');
        p.dataset.ttsReady='1';
      });
      document.querySelectorAll('.tts-sent').forEach(function(s){
        UNITS.push({el:s, en:'', zh:s.textContent.trim()});
      });
    }
  }

  var bar=document.getElementById('tts-bar');
  var playBtn=document.getElementById('tts-play');
  var rateEl=document.getElementById('tts-rate');
  var lang='en', scope='para', rate=1.0, idx=-1, playing=false, stopFlag=false;
  if(!IS_SENT){ lang='zh'; // 全中文页面默认读中文，并隐藏 EN 选项
    var le=document.querySelector('#tts-lang button[data-lang="en"]'); if(le)le.style.display='none';
    var lz=document.querySelector('#tts-lang button[data-lang="zh"]'); if(lz)lz.classList.add('on');
    var len=document.querySelector('#tts-lang button[data-lang="en"]'); 
    document.querySelector('#tts-lang button[data-lang="en"]').classList.remove('on');
  }

  function pickVoice(l){
    var vs=synth.getVoices();
    if(l==='zh'){
      return vs.find(function(v){return /zh|Chinese|普通话|Yue/i.test(v.lang+v.name)}) || null;
    }
    return vs.find(function(v){return /en[-_]GB/i.test(v.lang)}) || vs.find(function(v){return /^en/i.test(v.lang)}) || null;
  }

  function clearHi(){document.querySelectorAll('.tts-reading').forEach(function(e){e.classList.remove('tts-reading')})}
  function highlight(i){
    clearHi();
    if(i<0||i>=UNITS.length) return;
    var el=UNITS[i].el; el.classList.add('tts-reading');
    var r=el.getBoundingClientRect();
    if(r.top<80||r.bottom>window.innerHeight-140){ window.scrollTo({top:window.scrollY+r.top-window.innerHeight*0.4, behavior:'smooth'}); }
  }

  function textOf(i){ var u=UNITS[i]; if(!u)return ''; return (lang==='zh'? (u.zh||u.en) : (u.en||u.zh)); }

  function speakFrom(i){
    stopFlag=false;
    if(i>=UNITS.length){ stop(); return; }
    idx=i; highlight(i);
    var txt=textOf(i);
    if(!txt){ next(); return; }
    var u=new SpeechSynthesisUtterance(txt);
    u.rate=rate; u.lang=(lang==='zh'?'zh-CN':'en-GB');
    var v=pickVoice(lang); if(v)u.voice=v;
    u.onend=function(){
      if(stopFlag) return;
      if(scope==='para'){ if(idx+1<UNITS.length){ speakFrom(idx+1);} else stop(); }
      else { stop(); } // 单句/从这句起读到结尾同 para；此处 scope=='from' 也连读
    };
    u.onerror=function(){ if(!stopFlag){ if(idx+1<UNITS.length)speakFrom(idx+1); else stop(); } };
    synth.cancel(); synth.speak(u);
    playing=true; playBtn.textContent='⏸';
  }

  function play(){
    buildUnits();
    if(!UNITS.length) return;
    bar.classList.add('on');
    if(synth.paused){ synth.resume(); playing=true; playBtn.textContent='⏸'; return; }
    var start = idx>=0? idx : 0;
    speakFrom(start);
  }
  function pause(){ if(synth.speaking&&!synth.paused){ synth.pause(); playing=false; playBtn.textContent='▶'; } }
  function stop(){ stopFlag=true; synth.cancel(); playing=false; playBtn.textContent='▶'; clearHi(); }
  function next(){ stopFlag=true; synth.cancel(); if(idx+1<UNITS.length) speakFrom(idx+1); }
  function prev(){ stopFlag=true; synth.cancel(); if(idx-1>=0) speakFrom(idx-1); else speakFrom(0); }

  playBtn.onclick=function(){ if(playing){ pause(); } else { play(); } };
  document.getElementById('tts-next').onclick=next;
  document.getElementById('tts-prev').onclick=prev;
  document.getElementById('tts-x').onclick=function(){ stop(); bar.classList.remove('on'); };
  document.getElementById('tts-slow').onclick=function(){ rate=Math.max(0.5, Math.round((rate-0.1)*10)/10); rateEl.textContent=rate.toFixed(1)+'×'; if(playing&&idx>=0)speakFrom(idx); };
  document.getElementById('tts-fast').onclick=function(){ rate=Math.min(2.0, Math.round((rate+0.1)*10)/10); rateEl.textContent=rate.toFixed(1)+'×'; if(playing&&idx>=0)speakFrom(idx); };
  document.querySelectorAll('#tts-lang button').forEach(function(b){ b.onclick=function(){
    document.querySelectorAll('#tts-lang button').forEach(function(x){x.classList.remove('on')}); b.classList.add('on');
    lang=b.dataset.lang; if(playing){ speakFrom(idx<0?0:idx); }
  };});
  document.querySelectorAll('#tts-scope button').forEach(function(b){ b.onclick=function(){
    document.querySelectorAll('#tts-scope button').forEach(function(x){x.classList.remove('on')}); b.classList.add('on');
    scope=b.dataset.scope;
  };});

  // 点句子 → 从这句开始读（capture 阶段，先于高亮词的 stopPropagation）
  document.addEventListener('click',function(e){
    if(scope!=='from') return;              // 只在"从这句起"模式拦截
    if(!bar.classList.contains('on')) return; // 朗读条没开时不拦截
    var s=e.target.closest('.tts-sent, .sent');
    if(!s) return;
    e.stopPropagation(); e.preventDefault();
    buildUnits();
    var i=UNITS.findIndex(function(u){return u.el===s;});
    if(i>=0){ speakFrom(i); }
  }, true);

  // 工具栏 🔊 按钮
  var trig=document.getElementById('tts-trigger');
  if(trig)trig.onclick=function(){ bar.classList.toggle('on'); if(bar.classList.contains('on')){ buildUnits(); } else { stop(); } };

  // voices 异步加载
  if(synth.getVoices().length===0){ synth.onvoiceschanged=function(){}; }
  // 离开页面停止
  window.addEventListener('beforeunload',function(){ synth.cancel(); });
})();


// —— 更多菜单 ——
(function(){
  var mb=document.getElementById('more-btn'), mm=document.getElementById('more-menu');
  if(!mb) return;
  mb.onclick=function(e){ e.stopPropagation(); mm.classList.toggle('on'); };
  document.addEventListener('click',function(e){ if(!e.target.closest('.more-wrap')) mm.classList.remove('on'); });
  // 点菜单里的按钮后收起
  mm.querySelectorAll('button,a').forEach(function(b){ b.addEventListener('click',function(){ setTimeout(function(){mm.classList.remove('on')},50); }); });
})();

load();
})();
/* 对照阅读 / 生词库 云端同步:用课页同一组 Gist ID + Token,只读写 gist 里的 reader.json(不碰 data.json)。
   上传:生词本 + 每篇文章的 m(整段重点)/ n(笔记)/ h(划线),按文章名;绝不上传原文 p 和译文 z。 */
(function(){
var CFG_G='__cfg_gist_id',CFG_T='__cfg_gist_token',VK='__reader-vocab',LS='__reader_docs',
    VDEL='__reader_vdel',CN='__reader_cloudnotes',FILE='reader.json',API='https://api.github.com/gists/';
var state='off',subs=[],timer=null,running=null,again=false,lastPull=0,onChange=null,lastErr='';

function J(k,d){try{var v=JSON.parse(localStorage.getItem(k));return v==null?d:v}catch(e){return d}}
function W(k,v){try{localStorage.setItem(k,JSON.stringify(v));return true}catch(e){return false}}
function cfg(){try{return {id:localStorage.getItem(CFG_G)||'',tok:localStorage.getItem(CFG_T)||''}}catch(e){return {id:'',tok:''}}}
function enabled(){var c=cfg();return !!(c.id&&c.tok)}
function lc(w){return String(w||'').toLowerCase()}
function tu(w){return +(w&&(w.u||w.ts))||0}
function set(s){state=s;subs.forEach(function(f){try{f(s)}catch(e){}})}
function hdr(tok){return {'Authorization':'token '+tok,'Accept':'application/vnd.github+json'}}

function pull(c){
  return fetch(API+encodeURIComponent(c.id),{headers:hdr(c.tok),cache:'no-store'}).then(function(r){
    if(!r.ok)throw new Error(r.status===401?'Token 不对或已过期':r.status===404?'找不到这个 Gist(ID 不对,或 Token 没有 gist 权限)':'GitHub 返回 '+r.status);
    return r.json();
  }).then(function(j){
    var f=j.files&&j.files[FILE];
    if(!f)return {};
    if(f.truncated&&f.raw_url)return fetch(f.raw_url,{cache:'no-store'}).then(function(r){return r.json()});
    try{return JSON.parse(f.content||'{}')||{}}catch(e){return {}}
  });
}
function patch(c,obj){
  var files={};files[FILE]={content:JSON.stringify(obj)};
  return fetch(API+encodeURIComponent(c.id),{method:'PATCH',headers:hdr(c.tok),body:JSON.stringify({files:files})})
    .then(function(r){if(!r.ok)throw new Error('上传失败 '+r.status)});
}
function hasAnno(x){
  function ne(o){return o&&Object.keys(o).some(function(k){var v=o[k];return Array.isArray(v)?v.length:!!(v&&String(v).trim())})}
  return ne(x.m)||ne(x.n)||ne(x.h);
}
function pack(x){return {m:x.m||{},n:x.n||{},h:x.h||{},u:+(x.u||x.t)||0,c:(x.p||[]).length}}
function sortObj(o){var r={};Object.keys(o||{}).sort().forEach(function(k){r[k]=o[k]});return r}
function canonV(a){return JSON.stringify((a||[]).slice().sort(function(x,y){return lc(x.word)<lc(y.word)?-1:lc(x.word)>lc(y.word)?1:0}))}

/* 合并云端到本机;返回 {vocab:bool, docs:[...本机被更新的文章名], out:要上传的对象, stale:云端是否需要更新} */
function merge(cl){
  cl=cl||{};
  var res={vocab:false,docs:[],stale:false};
  // 删除记录(墓碑)
  var ld=J(VDEL,{}),cd=cl.del&&typeof cl.del==='object'?cl.del:{},del={};
  Object.keys(ld).concat(Object.keys(cd)).forEach(function(k){del[k]=Math.max(+ld[k]||0,+cd[k]||0)});
  // 生词
  var L=J(VK,[]);if(!Array.isArray(L))L=[];
  var C=Array.isArray(cl.vocab)?cl.vocab:[],map={};
  L.forEach(function(w){if(w&&w.word){var k=lc(w.word);if(!map[k]||tu(w)>tu(map[k]))map[k]=w}});
  C.forEach(function(w){if(w&&w.word){var k=lc(w.word);if(!map[k]||tu(w)>tu(map[k]))map[k]=w}});
  var V=Object.keys(map).map(function(k){return map[k]}).filter(function(w){var t=del[lc(w.word)];return !(t&&t>=tu(w))});
  V.sort(function(a,b){return (+b.ts||0)-(+a.ts||0)});
  if(canonV(V)!==canonV(L)){W(VK,V);res.vocab=true}
  // 墓碑只留 120 天
  var cut=Date.now()-120*864e5;Object.keys(del).forEach(function(k){if(del[k]<cut)delete del[k]});
  if(JSON.stringify(sortObj(del))!==JSON.stringify(sortObj(ld)))W(VDEL,del);
  // 文章批注
  var D=J(LS,{}),cn=J(CN,{}),cdocs=cl.docs&&typeof cl.docs==='object'?cl.docs:{},dch=false,cnch=false;
  Object.keys(cdocs).forEach(function(k){
    var c=cdocs[k];if(!c||typeof c!=='object')return;
    var x=D[k];
    if(x){
      if((+c.u||0)>(+x.u||0)&&(c.c==null||c.c===(x.p||[]).length)){
        x.m=c.m||{};x.n=c.n||{};x.h=c.h||{};x.u=+c.u;dch=true;res.docs.push(k);
        if(cn[k]){delete cn[k];cnch=true}
      }
    }else if(!cn[k]||(+c.u||0)>(+cn[k].u||0)){cn[k]=c;cnch=true}
  });
  if(dch)W(LS,D);
  if(cnch)W(CN,cn);
  var docs={};
  Object.keys(cn).forEach(function(k){docs[k]=cn[k]});
  Object.keys(D).forEach(function(k){var x=D[k];if(x&&(x.u||hasAnno(x)))docs[k]=pack(x)});
  var out={v:1,vocab:V,del:sortObj(del),docs:sortObj(docs),t:Date.now()};
  res.stale=canonV(V)!==canonV(cl.vocab)||
    JSON.stringify(out.del)!==JSON.stringify(sortObj(cd))||
    JSON.stringify(out.docs)!==JSON.stringify(sortObj(cdocs));
  res.out=out;
  return res;
}

function sync(){
  if(!enabled()){set('off');return Promise.resolve()}
  if(running){again=true;return running}
  var c=cfg();set('busy');
  running=pull(c).then(function(cl){
    lastPull=Date.now();
    var r=merge(cl);
    var p=r.stale?patch(c,r.out):Promise.resolve();
    return p.then(function(){
      lastErr='';set('ok');
      if((r.vocab||r.docs.length)&&onChange)try{onChange({vocab:r.vocab,docs:r.docs})}catch(e){}
    });
  }).catch(function(e){
    lastErr=(e&&e.message)||String(e);
    set(navigator.onLine===false?'offline':'fail');
  }).then(function(){
    running=null;
    if(again){again=false;return sync()}
  });
  return running;
}
function touch(){
  if(!enabled())return;
  set('busy');clearTimeout(timer);timer=setTimeout(sync,1500);
}
function delWord(w){var d=J(VDEL,{});d[lc(w)]=Date.now();W(VDEL,d);touch()}
function restore(name,count){
  var cn=J(CN,{}),c=cn[name];
  if(!c||(c.c!=null&&c.c!==count))return null;
  delete cn[name];W(CN,cn);
  return {m:c.m||{},n:c.n||{},h:c.h||{},u:+c.u||Date.now()};
}
function stash(name,x){
  if(!enabled()||!x||!hasAnno(x))return;
  var cn=J(CN,{});cn[name]=pack(x);W(CN,cn);
}

/* ---------- 状态药丸 + 设置弹窗(两页共用) ---------- */
var LABEL={off:'仅本机',offline:'仅本机',busy:'同步中',ok:'已同步',fail:'同步失败'};
function pill(el){
  if(!el)return;
  function up(s){
    el.textContent=LABEL[s]||'仅本机';
    el.className='rs-pill rs-'+s;
    el.title=s==='fail'?'同步失败:'+lastErr+'(数据已存本机,点这里检查设置)':s==='offline'?'离线,数据已存本机':s==='off'?'未连接云端,点这里设置':'点这里打开云端同步设置';
  }
  subs.push(up);up(state);
  el.addEventListener('click',openSettings);
}
var css='.rs-pill{border:1px solid var(--line);background:var(--card);color:#7d8f8b;border-radius:999px;padding:3px 10px 3px 20px;font-size:12px;cursor:pointer;position:relative;white-space:nowrap;line-height:1.5;font-family:inherit}'+
'.rs-pill:before{content:"";position:absolute;left:8px;top:50%;width:7px;height:7px;margin-top:-3.5px;border-radius:50%;background:#B9C6C3}'+
'.rs-pill.rs-ok:before{background:#4E9A6E}.rs-pill.rs-busy:before{background:var(--gold);animation:rsp 1s infinite alternate}.rs-pill.rs-fail{color:#B4513B}.rs-pill.rs-fail:before{background:#C9573F}'+
'@keyframes rsp{to{opacity:.3}}'+
'.rs-mask{position:fixed;inset:0;background:rgba(22,51,59,.32);z-index:200;display:none;align-items:center;justify-content:center;padding:16px}.rs-mask.open{display:flex}'+
'.rs-box{background:var(--card);border:1px solid var(--line);border-radius:10px;box-shadow:0 12px 40px rgba(22,51,59,.18);width:440px;max-width:100%;max-height:calc(100vh - 32px);overflow:auto;padding:20px 22px;font-size:13.5px;line-height:1.7;color:var(--ink-deep)}'+
'.rs-box h3{font-size:16px;margin:0 0 8px}.rs-box p{margin:0 0 10px;color:var(--zh)}.rs-box ol{margin:0 0 12px 18px;color:var(--zh);font-size:13px}.rs-box a{color:var(--ink)}'+
'.rs-box label{display:block;font-size:12.5px;color:var(--zh);margin:10px 0 4px}.rs-box input{width:100%;box-sizing:border-box;border:1px solid var(--line);border-radius:8px;padding:7px 10px;font-size:13.5px;background:var(--paper);color:var(--ink-deep)}'+
'.rs-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}.rs-row button{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;padding:6px 14px;font-size:13px;cursor:pointer;font-family:inherit}'+
'.rs-row .pri{background:var(--ink);border-color:var(--ink);color:#fff}.rs-row .sp{margin-left:auto}.rs-msg{min-height:20px;margin-top:10px;font-size:12.5px;color:var(--zh)}.rs-msg.bad{color:#B4513B}';
var modal=null;
function build(){
  if(modal)return modal;
  var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
  modal=document.createElement('div');modal.className='rs-mask';modal.id='rsModal';modal.setAttribute('translate','no');
  modal.innerHTML='<div class="rs-box ui" role="dialog" aria-label="云端同步设置"><h3>云端同步</h3>'+
    '<p>生词和笔记会备份到你自己的 GitHub Gist(文章原文不会上传)。清了浏览器缓存或换电脑,填同一组 ID 和 Token 就能找回。</p>'+
    '<ol><li>在 <a href="https://gist.github.com" target="_blank" rel="noopener">gist.github.com</a> 新建一个 secret gist(随便放一个文件),建好后地址栏最后那串就是 Gist ID。</li>'+
    '<li>在 <a href="https://github.com/settings/tokens" target="_blank" rel="noopener">github.com/settings/tokens</a> 新建 token,只勾「gist」权限。</li>'+
    '<li>课页的「同步」用的是同一组,填过的话这里自动就能用。阅读数据存在同一个 gist 的 reader.json 文件里,不影响课页笔记。</li></ol>'+
    '<label for="rsGist">Gist ID</label><input id="rsGist" autocomplete="off" spellcheck="false">'+
    '<label for="rsTok">Token</label><input id="rsTok" type="password" autocomplete="off" spellcheck="false">'+
    '<div class="rs-msg" id="rsMsg"></div>'+
    '<div class="rs-row"><button class="pri" id="rsGo">连接并同步</button><button id="rsOff">断开</button><button class="sp" id="rsClose">关闭</button></div></div>';
  document.body.appendChild(modal);
  var g=modal.querySelector('#rsGist'),t=modal.querySelector('#rsTok'),m=modal.querySelector('#rsMsg');
  function msg(s,bad){m.textContent=s;m.className='rs-msg'+(bad?' bad':'')}
  modal.addEventListener('click',function(e){if(e.target===modal)close()});
  modal.querySelector('#rsClose').onclick=close;
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&modal.classList.contains('open'))close()});
  modal.querySelector('#rsOff').onclick=function(){
    if(!enabled()){msg('现在没有连接云端。');return}
    if(!confirm('断开后这台电脑只存本机。课页的云端同步也会一起断开(两边用同一组设置)。确定?'))return;
    try{localStorage.removeItem(CFG_G);localStorage.removeItem(CFG_T)}catch(e){}
    g.value='';t.value='';t.placeholder='';set('off');msg('已断开,数据只存在这台电脑。');
  };
  modal.querySelector('#rsGo').onclick=function(){
    var old=cfg(),id=g.value.trim(),tok=t.value.trim()||(id===old.id?old.tok:'');
    if(!id||!tok){msg('Gist ID 和 Token 都要填。',true);return}
    msg('正在连接…');
    pull({id:id,tok:tok}).then(function(){
      try{localStorage.setItem(CFG_G,id);localStorage.setItem(CFG_T,tok)}catch(e){}
      t.value='';t.placeholder='已保存(留空就不改)';
      return sync().then(function(){
        if(state==='ok'){msg('已连接,生词和笔记已同步。');setTimeout(close,1200)}
        else msg('连接上了,但同步失败:'+lastErr,true);
      });
    }).catch(function(e){msg('连接失败:'+((e&&e.message)||e)+'。请检查 Gist ID、Token(要勾 gist 权限)和网络。',true)});
  };
  return modal;
}
function openSettings(){
  build();var c=cfg();
  modal.querySelector('#rsGist').value=c.id;
  var t=modal.querySelector('#rsTok');t.value='';t.placeholder=c.tok?'已保存(留空就不改)':'';
  var m=modal.querySelector('#rsMsg');
  m.className='rs-msg'+(state==='fail'?' bad':'');
  m.textContent=state==='ok'?'当前:已连接云端。':state==='fail'?'上次同步失败:'+lastErr:state==='offline'?'当前离线,数据已存本机。':enabled()?'':'当前只存这台电脑。';
  modal.classList.add('open');
}
function close(){if(modal)modal.classList.remove('open')}

function init(o){
  onChange=o&&o.onChange||null;
  set(enabled()?'busy':'off');
  sync();
  addEventListener('focus',function(){if(enabled()&&Date.now()-lastPull>30000)sync()});
  addEventListener('online',function(){if(enabled())sync()});
}

window.ReaderSync={init:init,touch:touch,sync:sync,delWord:delWord,restore:restore,stash:stash,pill:pill,
  openSettings:openSettings,enabled:enabled,state:function(){return state}};
})();

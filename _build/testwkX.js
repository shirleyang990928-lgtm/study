// 用法: node _build/testwkX.js <课页路径> [更多课页...]   (需先 npm install jsdom)
// 检查:章节/导航/双框/对白段/句对/紫词/朗读/PAGE_CONFIG.key==page-meta.key/乱码/资源路径深度
const {JSDOM}=require('jsdom');const fs=require('fs');const path=require('path');
const ROOT=path.resolve(__dirname,'..');
const css=fs.readFileSync(path.join(ROOT,'app.css'),'utf8');const js=fs.readFileSync(path.join(ROOT,'app.js'),'utf8');
async function test(f){
  let html=fs.readFileSync(f,'utf8');
  const rel=path.relative(ROOT,path.resolve(f)).split(path.sep);
  const want='../'.repeat(rel.length-1);
  const cssTag='<link rel="stylesheet" href="'+want+'app.css">',jsTag='<script src="'+want+'app.js"></script>';
  if(!html.includes(cssTag)||!html.includes(jsTag)){console.log(f,'FAIL: 资源路径应为 '+want+'app.css / '+want+'app.js');return false;}
  if(!html.includes('href="'+want+'index.html"')){console.log(f,'FAIL: 回到目录链接应为 '+want+'index.html');return false;}
  html=html.replace(cssTag,function(){return '<style>'+css+'</style>'});
  html=html.replace(jsTag,function(){return '<script>'+js+'</script>'});
  html=html.replace('<body>',function(){return '<body><script>window.__spoken=[];window.speechSynthesis={getVoices:function(){return[{lang:"en-GB"},{lang:"zh-CN"}]},speak:function(u){window.__spoken.push(u.text)},cancel:function(){},paused:false};window.SpeechSynthesisUtterance=function(t){this.text=t}</script>'});
  const dom=new JSDOM(html,{runScripts:'dangerously',url:'http://localhost/',pretendToBeVisual:true});
  const w=dom.window;w.fetch=function(){return Promise.reject(new Error('x'))};w.scrollTo=function(){};
  await new Promise(function(r){setTimeout(r,900)});
  const d=w.document;
  const meta=JSON.parse(d.getElementById('page-meta').textContent);
  const n=function(s){return d.querySelectorAll(s).length};
  const p=d.getElementById('tts-play');if(p){p.click();await new Promise(function(r){setTimeout(r,50)});}
  const bad=(html.match(/'''/g)||[]).length+(html.match(/�/g)||[]).length;
  const ok=meta.key===w.PAGE_CONFIG.key&&w.__spoken.length>0&&bad===0&&n('.map-foot a')===2;
  console.log(path.basename(f),'| 章节:',n('section'),'| 导航:',n('.map a'),'| 双框:',n('.keypoints')+'/'+n('.explain'),'| 对白段:',n('.para.dialog'),'| 句对:',n('.sent'),'| 紫词:',n('.vocab-mark.preset'),'| 朗读:',w.__spoken.length>0?'OK':'FAIL','| 键:',meta.key===w.PAGE_CONFIG.key?'OK':'MISMATCH '+w.PAGE_CONFIG.key,'| 乱码:',bad,'| 侧栏底部:',n('.map-foot a'),ok?'':'  <-- FAIL');
  return ok;
}
(async()=>{let all=true;for(const f of process.argv.slice(2)){if(!(await test(f)))all=false;}process.exit(all?0:1);})();

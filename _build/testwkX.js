// 用法: node _build/testwkX.js courses/<unit>/wkNN-date.html   (需先 npm install jsdom)
const {JSDOM}=require('jsdom');const fs=require('fs');const path=require('path');
const ROOT=path.resolve(__dirname,'..');
const css=fs.readFileSync(path.join(ROOT,'app.css'),'utf8');const js=fs.readFileSync(path.join(ROOT,'app.js'),'utf8');
const f=process.argv[2];
(async()=>{
  let html=fs.readFileSync(f,'utf8');
  if(!html.includes('href="../../app.css"')||!html.includes('src="../../app.js"')){console.log('FAIL: 资源路径不是 ../../app.css / ../../app.js');process.exit(1);}
  html=html.replace('<link rel="stylesheet" href="../../app.css">',function(){return '<style>'+css+'</style>'});
  html=html.replace('<script src="../../app.js"></script>',function(){return '<script>'+js+'</script>'});
  html=html.replace('<body>',function(){return '<body><script>window.__spoken=[];window.speechSynthesis={getVoices:function(){return[{lang:"en-GB"},{lang:"zh-CN"}]},speak:function(u){window.__spoken.push(u.text)},cancel:function(){},paused:false};window.SpeechSynthesisUtterance=function(t){this.text=t}</script>'});
  const dom=new JSDOM(html,{runScripts:'dangerously',url:'http://localhost/',pretendToBeVisual:true});
  const w=dom.window;w.fetch=function(){return Promise.reject(new Error('x'))};w.scrollTo=function(){};
  await new Promise(function(r){setTimeout(r,900)});
  const d=w.document;
  const meta=JSON.parse(d.getElementById('page-meta').textContent);
  console.log('章节:',d.querySelectorAll('section').length,'| 导航:',d.querySelectorAll('.map a').length,'| 双框:',d.querySelectorAll('.keypoints').length,'/',d.querySelectorAll('.explain').length,'| 对白段:',d.querySelectorAll('.para.dialog').length,'| 句对:',d.querySelectorAll('.sent').length,'| 紫词:',d.querySelectorAll('.vocab-mark.preset').length);
  const p=d.getElementById('tts-play');if(p){p.click();await new Promise(function(r){setTimeout(r,50)});}
  console.log('朗读:',w.__spoken.length>0?'OK':'FAIL','| 键:',w.PAGE_CONFIG.key,'| meta.key:',meta.key,meta.key===w.PAGE_CONFIG.key?'OK':'MISMATCH','| 乱码:',(html.match(/'''/g)||[]).length);
  process.exit(0);
})();

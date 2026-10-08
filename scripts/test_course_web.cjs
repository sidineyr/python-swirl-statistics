/* DOM integration tests: route through every real lesson, preserving local answers. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..'), script=fs.readFileSync(path.join(root,'site/course.js'),'utf8');
const modules=JSON.parse(fs.readFileSync(path.join(root,'curriculum/modules.json'),'utf8'));
const KEY='python-swirl-online-v1';
function page(name,state,blocked=false){
 const dom=new JSDOM(fs.readFileSync(path.join(root,'site',name),'utf8'),{url:'https://sidineyr.github.io/python-swirl-statistics/'+name,runScripts:'outside-only'});
 if(state)dom.window.localStorage.setItem(KEY,state);
 if(blocked)Object.defineProperty(dom.window,'localStorage',{get(){throw Error('blocked')}});
 dom.window.eval(script);return dom;
}
function event(w,el,name){el.dispatchEvent(new w.Event(name,{bubbles:true}));}
let stored;
for(const m of modules){
 let dom=page(m.slug+'.html',stored),w=dom.window,d=w.document;
 assert.equal(d.querySelectorAll('.question').length,2);
 assert.equal(d.querySelectorAll('iframe').length,0,'third party must not load automatically');
 d.querySelector('.load-video').click();assert.equal(d.querySelector('iframe').title,d.querySelector('.load-video').dataset.title);
 assert.equal(d.querySelector('#video a[href="#pratica"]').textContent,'Praticar esta aula');
 d.getElementById('complete-lesson').click();assert.match(d.getElementById('completion-feedback').textContent,/Execute/);
 for(const [i,q] of m.questions.entries()){
  let box=d.querySelector(`[data-question="${i}"]`),input=box.querySelector('input'),button=box.querySelector('button');
  for(const invalid of ['','print(4)','Infinity','0x10']){input.value=invalid;button.click();assert.match(box.querySelector('[role=status]').textContent,/Formato/);}
  input.value=String(q.expected+100);button.click();assert.match(box.querySelector('[role=status]').textContent,/Cálculo/);
  input.value=String(q.expected).replace('.',',');event(w,input,'input');button.click();assert.match(box.querySelector('[role=status]').textContent,/Resultado conferido/);
 }
 for(const a of d.querySelectorAll('[data-note]')){a.value='Meu procedimento e interpretação com limites.';event(w,a,'input');}
 for(const c of d.querySelectorAll('input[type=checkbox]')){c.checked=true;event(w,c,'change');}
 d.getElementById('complete-lesson').click();assert.match(d.getElementById('completion-feedback').textContent,/Atividade concluída/);
 stored=w.localStorage.getItem(KEY);assert.equal(JSON.parse(stored).modules[m.slug].completed,true);dom.window.close();
 dom=page(m.slug+'.html',stored);assert.equal(dom.window.document.getElementById('reflection').value,'Meu procedimento e interpretação com limites.');dom.window.close();
}
let dom=page('index.html',stored);assert.match(dom.window.document.getElementById('course-progress').textContent,/10 de 10 aulas visitadas · 10 de 10 atividades concluídas/);dom.window.close();
dom=page(modules[0].slug+'.html',stored);dom.window.document.getElementById('redo-lesson').click();assert.equal(dom.window.document.getElementById('reflection').value,'Meu procedimento e interpretação com limites.');assert.equal(JSON.parse(dom.window.localStorage.getItem(KEY)).modules[modules[0].slug].completed,false);dom.window.close();
dom=page('index.html',null,true);assert.match(dom.window.document.getElementById('storage-status').textContent,/não será salva/);dom.window.close();
dom=page('index.html','not-json');assert.match(dom.window.document.getElementById('storage-status').textContent,/Não foi possível/);dom.window.close();
console.log('OK: all 10 routes, correct/wrong/malformed answers, completion gates, video opt-in, resume and blocked storage.');

(async () => {
 const dom=page('index.html',stored),w=dom.window,d=w.document;
 const input=d.getElementById('import-course');
 const incoming=JSON.parse(stored);incoming.modules[modules[0].slug].notes.reflection='Outra interpretação preservada.';
 Object.defineProperty(input,'files',{value:[{size:100,text:async()=>JSON.stringify(incoming)}],configurable:true});
 event(w,input,'change');await new Promise(r=>setTimeout(r,0));
 const after=JSON.parse(w.localStorage.getItem(KEY));
 assert.match(after.modules[modules[0].slug].notes.reflection,/Outra interpretação preservada/);
 assert.match(after.modules[modules[0].slug].notes.reflection,/Meu procedimento/);
 assert.equal(after.modules[modules[0].slug].completed,false);
 const before=w.localStorage.getItem(KEY);
 Object.defineProperty(input,'files',{value:[{size:10,text:async()=>'bad-json'}],configurable:true});
 event(w,input,'change');await new Promise(r=>setTimeout(r,0));assert.equal(w.localStorage.getItem(KEY),before);
 let exported=false;w.URL.createObjectURL=blob=>{assert.ok(blob instanceof w.Blob);exported=true;return 'blob:test'};w.URL.revokeObjectURL=()=>{};w.HTMLAnchorElement.prototype.click=function(){assert.equal(this.download,'python-swirl-respostas.json')};
 d.getElementById('export-course').click();assert.equal(exported,true);
 dom.window.close();console.log('OK: export, import conflict preservation and invalid import rollback.');
})().catch(e=>{console.error(e);process.exitCode=1});

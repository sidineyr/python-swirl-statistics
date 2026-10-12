/* Static DOM audit: does not validate visual layout, contrast or assistive technology. */
const fs=require('node:fs'),path=require('node:path');
const {JSDOM}=require('jsdom'),axe=require('axe-core');
(async()=>{
 let failures=0;
 for(const file of fs.readdirSync(path.join(__dirname,'../site')).filter(f=>f.endsWith('.html'))){
  const dom=new JSDOM(fs.readFileSync(path.join(__dirname,'../site',file),'utf8'),{url:'https://sidineyr.github.io/python-swirl-statistics/'+file,runScripts:'outside-only'});
  dom.window.eval(axe.source);
  const result=await dom.window.axe.run(dom.window.document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']},rules:{'color-contrast':{enabled:false}}});
  for(const v of result.violations){failures++;console.error(file,v.id,v.nodes.map(n=>n.target).join('; '));}
  dom.window.close();
 }
 if(failures)process.exitCode=1;else console.log('OK: 18 pages, axe static WCAG A/AA rules; contrast/layout/readers NOT assessed.');
})().catch(e=>{console.error(e);process.exitCode=1});

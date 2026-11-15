// Usage: node export_scene.js <page.html> <outdir> <view: door|desk|music|tv> <light: day|evening>
// Opens the room page headless, sets the view and lights, and saves the exact scene (scene.glb) plus camera/light info (shot.json).
const { chromium } = require('playwright'); const fs=require('fs'), path=require('path');
(async()=>{
  const [page,out,view='door',light='day']=process.argv.slice(2);
  const html='<!doctype html><html><head><meta charset="utf-8"></head><body>'+fs.readFileSync(page,'utf8')+'</body></html>';
  const tmp=path.join(out,'_wrapped.html'); fs.mkdirSync(out,{recursive:true}); fs.writeFileSync(tmp,html);
  const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const p=await b.newPage({viewport:{width:1600,height:1000}});
  await p.goto('file://'+path.resolve(tmp)); await p.waitForFunction(()=>window.__room,{timeout:30000});
  await p.evaluate(()=>{ document.querySelector('.sheet').style.display='none'; }); await p.waitForTimeout(500);
  await p.click(light==='day'?'#lightDay':'#lightEve',{force:true}).catch(()=>{});
  await p.evaluate(([l])=>{ document.getElementById(l==='day'?'lightDay':'lightEve').click(); },[light]);
  await p.evaluate(([v])=>window.__room.setView(v,true),[view]); await p.waitForTimeout(1500);
  await p.screenshot({path:path.join(out,'page_view.png')});
  const glb=await p.evaluate(()=>window.__room.exportGLB()); fs.writeFileSync(path.join(out,'scene.glb'),Buffer.from(glb,'base64'));
  fs.writeFileSync(path.join(out,'shot.json'),JSON.stringify(await p.evaluate(()=>window.__room.shot())));
  await b.close(); console.log('exported',view,light);
})();

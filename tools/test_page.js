const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
  const html='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;font:14px system-ui}[hidden]{display:none!important}</style></head><body>'+fs.readFileSync('office-room.html','utf8')+'</body></html>';
  fs.writeFileSync('wrapped.html',html);
  const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const p=await b.newPage({viewport:{width:1280,height:800}});
  const errs=[]; p.on('console',m=>{if(m.type()==='error')errs.push(m.text())}); p.on('pageerror',e=>errs.push('PAGEERR '+e.message));
  await p.goto('file://'+process.cwd()+'/wrapped.html'); await p.waitForFunction(()=>window.__room,{timeout:30000}).catch(e=>errs.push('no __room'));
  await p.waitForTimeout(2500);
  const snap=async n=>{ await p.waitForTimeout(1500); await p.screenshot({path:n+'.png'}); };
  await snap('door');
  for(const v of ['vPlan','vIso','vDesk','vMusic','vTv']){ await p.click('#'+v); await snap(v); }
  await p.click('#lightEve'); await p.click('#vDoor'); await snap('eve');
  await p.click('#lightDay'); await p.click('#vHplan'); await snap('house_plan'); await p.click('#vHiso'); await snap('house_iso');
  for(const r of ['living','kitchen','hall','primary']){ await p.selectOption('#roomSel',r); await snap('room_'+r); }
  await p.keyboard.down('w'); await p.waitForTimeout(600); await p.keyboard.up('w');
  // select + drag test: select the loveseat via list, then drag it in plan view
  await p.click('#lightDay'); await p.click('#vPlan'); await p.waitForTimeout(1500);
  const before=await p.evaluate(()=>{ const it=window.__room.items().find(i=>i.t==='loveseat'); window.__room.select(it.id); return {x:it.x,z:it.z}; });
  // find screen position of the loveseat
  const pos=await p.evaluate(()=>{ const c=document.querySelector('canvas').getBoundingClientRect(); return {l:c.left,t:c.top,w:c.width,h:c.height}; });
  const sx=pos.l+pos.w*0.735, sy=pos.t+pos.h*0.46;
  await p.mouse.move(sx,sy); await p.mouse.down(); await p.mouse.move(sx-80,sy+40,{steps:8}); await p.mouse.up(); await p.waitForTimeout(500);
  const after=await p.evaluate(()=>{ const it=window.__room.items().find(i=>i.t==='loveseat'); return {x:it.x,z:it.z}; });
  console.log('DRAG',JSON.stringify(before),JSON.stringify(after));
  await snap('dragged');
  const n0=await p.evaluate(()=>window.__room.items().length);
  await p.selectOption('#addSel','bench'); await p.click('#addBtn'); await p.click('#selRot');
  const n1=await p.evaluate(()=>window.__room.items().length); await p.click('#selDel');
  const n2=await p.evaluate(()=>window.__room.items().length); console.log('ADD/REMOVE',n0,n1,n2);
  await p.click('#desk72'); await p.click('#lookOak'); await p.click('#vDoor'); await snap('oak72');
  console.log(await p.evaluate(()=>document.getElementById('fit').innerText));
  await p.click('#desk78'); await p.click('#lookWalnut');
  await p.setViewportSize({width:400,height:800}); await p.waitForTimeout(800); await snap('phone');
  console.log('ERRORS',errs); await b.close();
})();

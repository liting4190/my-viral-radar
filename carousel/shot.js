const {chromium}=require('/opt/node22/lib/node_modules/playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1440}});
for(let i=1;i<=7;i++){await p.goto('file://'+process.cwd()+`/build/s${i}.html`);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);
const rects=await p.evaluate(()=>{const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(!n.textContent.trim())continue;const r=document.createRange();r.selectNodeContents(n);for(const q of r.getClientRects())out.push([q.left,q.top,q.right,q.bottom,n.textContent.trim().slice(0,12)])}return out});
require('fs').writeFileSync(`build/rects${i}.json`,JSON.stringify(rects));
await p.screenshot({path:`out/slide${i}.png`});}
await b.close()})()

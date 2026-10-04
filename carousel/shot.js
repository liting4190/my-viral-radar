const {chromium}=require('/opt/node22/lib/node_modules/playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1440}});
for(let i=1;i<=7;i++){await p.goto('file://'+process.cwd()+`/build/s${i}.html`);await p.waitForTimeout(300);await p.screenshot({path:`out/slide${i}.png`});}
await b.close()})()

# -*- coding: utf-8 -*-
import re, os, html
from PIL import Image, ImageOps
from copy import SLIDES
P="/tmp/claude-0/-home-claude-my-viral-radar/88fa76fe-e52b-5e73-a12f-e50faf6a33c6/scratchpad/ph/"
os.makedirs("build",exist_ok=True); os.makedirs("out",exist_ok=True)
CSS="""
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1440px;background:#0e0e10;font-family:'WenQuanYi Zen Hei',sans-serif;color:#fff;position:relative;overflow:hidden}
.ph{position:absolute;inset:0;background-size:cover}
.shade{position:absolute;inset:0}
.title{position:absolute;left:64px;right:64px}
.t1{font-size:66px;line-height:1.25;color:#fff;-webkit-text-stroke:1.4px #fff;text-shadow:0 3px 16px rgba(0,0,0,.65)}
.t2{font-size:66px;line-height:1.25;color:#f3cd78;-webkit-text-stroke:1.4px #f3cd78;text-shadow:0 3px 16px rgba(0,0,0,.6)}
.rule{width:120px;height:4px;background:#f3cd78;margin-top:34px}
.body{position:absolute;left:64px;font-size:38px;line-height:1.62;color:#f2f0ea;text-shadow:0 2px 10px rgba(0,0,0,.7)}
.body p{margin-bottom:26px}
.y{color:#ffe14d;-webkit-text-stroke:.8px #ffe14d}
/* cover: bright face, dark only at top and bottom */
.cover .shade{background:linear-gradient(180deg,rgba(0,0,0,.62) 0%,rgba(0,0,0,.35) 15%,rgba(0,0,0,0) 28%,rgba(0,0,0,0) 56%,rgba(0,0,0,.78) 70%,rgba(0,0,0,.9) 100%)}
.cover .title{top:56px}.cover .t1,.cover .t2{font-size:84px}
.cover .body{top:900px;right:64px;font-size:42px}
/* content: darker */
.inner .shade{background:linear-gradient(90deg,rgba(8,8,10,.86) 0%,rgba(8,8,10,.68) 55%,rgba(8,8,10,.38) 100%)}
.inner .title{top:150px}.inner .t1,.inner .t2{font-size:68px}
.inner .body{top:480px;width:900px;font-size:42px}
"""
for s in SLIDES:
    im=ImageOps.exif_transpose(Image.open(P+s['photo'])).convert('RGB'); im.thumbnail((1700,1700)); im.save(f"build/p{s['n']}.jpg",quality=88)
    body="".join("<p>"+re.sub(r"【黄】(.*?)【/黄】",r'<span class="y">\1</span>',html.escape(p,quote=False))+"</p>" for p in s['body'])
    cls="cover" if s['n']==1 else "inner"
    open(f"build/s{s['n']}.html","w").write(f"""<!doctype html><meta charset=utf-8><style>{CSS}</style><body class="{cls}">
<div class=ph style="background-image:url(p{s['n']}.jpg);background-position:{s['pos']}"></div><div class=shade></div>
<div class=title><div class=t1>{s['t1']}</div><div class=t2>{s['t2']}</div><div class=rule></div></div>
<div class=body>{body}</div></body>""")

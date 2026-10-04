# -*- coding: utf-8 -*-
import re, os, html
from PIL import Image, ImageOps
from copy import SLIDES, count
P="/tmp/claude-0/-home-claude-my-viral-radar/88fa76fe-e52b-5e73-a12f-e50faf6a33c6/scratchpad/ph/"
os.makedirs("build",exist_ok=True); os.makedirs("out",exist_ok=True)
CSS="""
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1440px;background:#15171d;font-family:'WenQuanYi Zen Hei',sans-serif;color:#fff;position:relative;overflow:hidden}
.ph{position:absolute;left:0;top:0;width:1080px;height:760px;background-size:cover}
.fade{position:absolute;left:0;top:0;width:1080px;height:760px;background:linear-gradient(180deg,rgba(21,23,29,.35) 0%,rgba(21,23,29,0) 30%,rgba(21,23,29,.55) 62%,#15171d 100%)}
.tint{position:absolute;inset:0;background:rgba(40,50,80,.10)}
.tag{position:absolute;left:64px;top:52px;font-size:26px;letter-spacing:4px;color:#fff;opacity:.85;text-shadow:0 2px 8px rgba(0,0,0,.6)}
.pg{position:absolute;right:64px;top:52px;font-size:26px;color:#fff;opacity:.85;text-shadow:0 2px 8px rgba(0,0,0,.6)}
.title{position:absolute;left:64px;right:64px;top:520px}
.t1{font-size:62px;line-height:1.25;color:#fff;-webkit-text-stroke:1.2px #fff;text-shadow:0 3px 14px rgba(0,0,0,.7)}
.t2{font-size:50px;line-height:1.3;margin-top:8px;color:#f0c35a;-webkit-text-stroke:1px #f0c35a;text-shadow:0 3px 14px rgba(0,0,0,.7)}
.cover .t1{font-size:78px}.cover .t2{font-size:68px}
.body{position:absolute;left:64px;right:64px;top:780px;font-size:40px;line-height:1.6;color:#eceae4}
.body p{margin-bottom:24px}
.cover .body{font-size:44px}.cover .body p{margin-bottom:30px}
.y{color:#ffe14d;-webkit-text-stroke:.8px #ffe14d}
.bar{position:absolute;left:64px;bottom:44px;width:120px;height:6px;background:#f0c35a;border-radius:3px}
"""
for s in SLIDES:
    im=ImageOps.exif_transpose(Image.open(P+s['photo'])).convert('RGB'); im.thumbnail((1600,1600)); im.save(f"build/p{s['n']}.jpg",quality=88)
    body="".join("<p>"+re.sub(r"【黄】(.*?)【/黄】",r'<span class="y">\1</span>',html.escape(p,quote=False).replace('&','&amp;'))+"</p>" for p in s['body'])
    cls="cover" if s['n']==1 else ""
    h=f"""<!doctype html><meta charset=utf-8><style>{CSS}</style><body class="{cls}">
<div class=ph style="background-image:url(p{s['n']}.jpg);background-position:{s['pos']}"></div><div class=tint></div><div class=fade></div>
<div class=tag>{'小红书运营 · 新马版' }</div><div class=pg>{s['n']}/{len(SLIDES)}</div>
<div class=title><div class=t1>{s['t1']}</div><div class=t2>{s['t2']}</div></div>
<div class=body>{body}</div><div class=bar></div></body>"""
    open(f"build/s{s['n']}.html","w").write(h)

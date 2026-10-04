# -*- coding: utf-8 -*-
import re, os, html
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import sys; sys.path.insert(0, os.environ.get("EP","ep2"))
from content import SLIDES
SP=os.environ.get("PHOTOS","photos")+"/"
HANDLE="@liting_21"; TOTAL=len(SLIDES); NPTS=sum(1 for s in SLIDES if s['kind']=="inner")
os.makedirs("build",exist_ok=True); OUT=os.environ.get("EP","ep2")+"/out/"; os.makedirs(OUT,exist_ok=True)
FONT="node_modules/@fontsource/"
import json
TARGET={"cover":690,"inner":510,"summary":590}
def prep(s):
    f=SP+s['photo']
    if not os.path.exists(f): f=SP+"new/"+s['photo']
    im=ImageOps.exif_transpose(Image.open(f)).convert('RGB')
    W,H=1080,1440; sc=max(W/im.width,H/im.height)*s['zoom']
    im=im.resize((round(im.width*sc),round(im.height*sc)),Image.LANCZOS)
    x0n,x1n,y0n,y1n=s['head']
    fy0,fy1=y0n*im.height,y1n*im.height; fx0,fx1=x0n*im.width,x1n*im.width
    cy=(fy0+fy1)/2; cx=(fx0+fx1)/2; tgt=TARGET[s['kind']]
    y=round(cy-tgt); dy=0
    if y<0: dy=min(-y,260); y=0
    y=min(y,im.height-H)
    x=min(max(round(cx-W/2),0),im.width-W)
    crop=im.crop((x,y,x+W,y+H)); im=crop
    if dy:
        c=Image.new('RGB',(W,H)); c.paste(crop,(0,dy))
        top=crop.crop((0,0,W,dy)).transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(6)); c.paste(top,(0,0)); im=c
    json.dump(dict(l=fx0-x,r=fx1-x,t=fy0-y+dy,b=fy1-y+dy),open(f"build/face{s['n']}.json","w"))
    r,g,b=im.split(); r=r.point(lambda v:min(255,v*1.03)); b=b.point(lambda v:v*0.94)
    im=Image.merge('RGB',(r,g,b)); im=ImageEnhance.Color(im).enhance(0.94)
    im.save(f"build/p{s['n']}.jpg",quality=90)
def Y(t): return re.sub(r"【黄】(.*?)【/黄】",r'<span class="y">\1</span>',html.escape(t,quote=False)).replace(chr(10),'<br>')
def title(t1,t2):
    t1=re.sub(r"「(.*?)」",r'<span class="g">「\1」</span>',t1)
    return f'<div class=t1>{t1}</div><div class=t2>{t2}</div>'
CSS="""
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1440px;background:#0b0908;font-family:'Noto Sans SC','WenQuanYi Zen Hei',sans-serif;color:#fff;position:relative;overflow:hidden}
.ph{position:absolute;inset:0;background-size:cover}
.shade{position:absolute;inset:0}
.top{position:absolute;left:85px;right:87px;top:62px;height:34px;display:flex;align-items:center;justify-content:space-between;font-size:26px;letter-spacing:5px}
.kick{color:#e6c47d;display:flex;align-items:center;gap:22px;text-shadow:0 2px 8px rgba(0,0,0,.5)}
.dash{display:flex;gap:8px}.dash i{display:block;width:34px;height:3px;background:rgba(255,255,255,.38)}.dash i.on{background:#e6c47d}
.pg{color:#fff;opacity:.92;text-shadow:0 2px 8px rgba(0,0,0,.5);font-weight:500}
.title{position:absolute;left:85px;right:60px;font-family:'Noto Serif SC',serif;font-weight:900;text-shadow:0 4px 22px rgba(0,0,0,.55)}
.t1{color:#fff}.t2{color:#e6c47d}.g{color:#e6c47d}
.y{color:#efd08a}
.foot{position:absolute;left:85px;bottom:50px;font-size:24px;letter-spacing:5px;color:rgba(255,255,255,.78);text-shadow:0 2px 8px rgba(0,0,0,.6)}
.arrow{position:absolute;right:85px;bottom:56px}
.body{position:absolute;left:85px;right:85px;text-shadow:0 2px 12px rgba(0,0,0,.65)}
.lab{display:flex;align-items:center;gap:16px;font-size:25px;letter-spacing:8px;color:#e6c47d;margin-bottom:10px;font-weight:500}
.lab:after{content:"";width:42px;height:1px;background:#e6c47d;opacity:.8}
.sec{margin-bottom:34px}.sec p,.sec .b{margin-bottom:6px;font-size:36px;line-height:1.5;color:#fff;font-weight:400}
.b{position:relative;padding-left:26px}.b:before{content:"";position:absolute;left:2px;top:.66em;width:9px;height:9px;background:#e6c47d;transform:rotate(45deg)}
.call{border-left:3px solid #e6c47d;padding-left:24px;font-size:38px;line-height:1.5;font-weight:500;margin-top:10px}
/* cover */
.cover .shade{background:linear-gradient(180deg,rgba(10,8,7,.62) 0%,rgba(10,8,7,.30) 20%,rgba(10,8,7,0) 34%,rgba(10,8,7,0) 52%,rgba(10,8,7,.80) 68%,rgba(10,8,7,.93) 100%)}
.cover .title{top:128px;font-size:116px;line-height:1.14}
.cover .rule{position:absolute;left:85px;top:440px;width:88px;height:3px;background:#e6c47d}
.cover .body{top:1000px}.cover .body{right:60px}.cover .body p{font-size:33px;line-height:1.55;margin-bottom:26px;color:#fff}
/* inner */
.inner .shade{background:linear-gradient(180deg,rgba(10,8,7,.78) 0%,rgba(10,8,7,.55) 14%,rgba(10,8,7,.14) 30%,rgba(10,8,7,0) 38%,rgba(10,8,7,.30) 46%,rgba(10,8,7,.86) 60%,rgba(10,8,7,.94) 100%)}
.inner .title{top:130px;font-size:70px;line-height:1.22}
.inner .body{top:690px}
/* summary */
.summary .shade{background:linear-gradient(180deg,rgba(10,8,7,.72) 0%,rgba(10,8,7,.45) 14%,rgba(10,8,7,.10) 30%,rgba(10,8,7,0) 38%,rgba(10,8,7,.35) 50%,rgba(10,8,7,.88) 62%,rgba(10,8,7,.94) 100%)}
.summary .title{top:130px;font-size:84px;line-height:1.2}
.summary .rule{position:absolute;left:85px;top:372px;width:88px;height:3px;background:#e6c47d}
.summary .body{top:790px}
.li{display:flex;align-items:baseline;gap:22px;font-size:35px;line-height:1.5;margin-bottom:10px}.li b{font-family:'Noto Serif SC',serif;font-weight:700;color:#e6c47d;font-size:36px}
.summary .para{font-size:36px;line-height:1.5;font-weight:500;margin-top:14px}
.btn{display:inline-block;margin-top:26px;border:2px solid #e6c47d;color:#fff;font-size:30px;font-weight:500;letter-spacing:3px;padding:16px 40px;background:rgba(10,8,7,.35)}
"""
LINKS="".join(f'<link rel=stylesheet href="../node_modules/@fontsource/{f}.css">' for f in ("noto-serif-sc/700","noto-serif-sc/900","noto-sans-sc/400","noto-sans-sc/500"))
ARROW='<svg class=arrow width="72" height="20" viewBox="0 0 72 20"><path d="M0 10H70M62 2l8 8-8 8" fill="none" stroke="#fff" stroke-width="1.6"/></svg>'
for s in SLIDES:
    prep(s); k=s['kind']; n=s['n']
    top=f'<div class=top><div class=kick>'+(f'要点 {n-1:02d}<span class=dash>'+"".join(f'<i class="{"on" if i==n-2 else ""}"></i>' for i in range(NPTS))+'</span>' if k=="inner" else '')+f'</div></div>'
    out=[]
    for b in s['blocks']:
        t=b[0]
        if t=="para": out.append(f'<p class=para>{Y(b[1])}</p>')
        elif t=="call": out.append(f'<div class=call>{Y(b[1])}</div>')
        elif t=="sec": out.append(f'<div class=sec><div class=lab>{b[1]}</div>'+"".join(f'<div class="{ "b" if ty=="b" else "pp"}">{Y(tx)}</div>' if ty=="b" else f'<p>{Y(tx)}</p>' for ty,tx in b[2])+'</div>')
        elif t=="list": out.append("".join(f'<div class=li><b>{a}</b><span>{html.escape(x)}</span></div>' for a,x in b[1]))
        elif t=="btn": out.append(f'<div class=btn>{b[1]}</div>')
    rule='<div class=rule></div>' if k in("cover","summary") else ''
    arrow=ARROW if n<TOTAL else ''
    open(f"build/s{n}.html","w").write(f"""<!doctype html><meta charset=utf-8>{LINKS}<style>{CSS}</style><body class="{k}">
<div class=ph style="background-image:url(p{n}.jpg)"></div><div class=shade></div>{top}
<div class=title>{title(s['t1'],s['t2'])}</div>{rule}<div class=body>{''.join(out)}</div>
{arrow}</body>""")

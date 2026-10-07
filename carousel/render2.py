# -*- coding: utf-8 -*-
# 第2版排版：照片里的人放一侧，标题在上，正文放在人旁边的空位，金句放底部笔刷条（参考用户给的「怎么开始的」那张）
import re, os, html, json, sys, random
from PIL import Image, ImageOps, ImageEnhance
EP=os.environ.get("EP","ep2"); sys.path.insert(0,EP)
from content import SLIDES
SP=os.environ.get("PHOTOS","photos")+"/"
OUT=EP+"/out/"; os.makedirs("build",exist_ok=True); os.makedirs(OUT,exist_ok=True)
W,H=1080,1440

def prep(s):
    im=ImageOps.exif_transpose(Image.open(SP+s['photo'])).convert('RGB')
    sc=max(W/im.width,H/im.height)*s['zoom']
    im=im.resize((round(im.width*sc),round(im.height*sc)),Image.LANCZOS)
    x0,x1,y0,y1=s['head']; fx0,fx1,fy0,fy1=x0*im.width,x1*im.width,y0*im.height,y1*im.height
    x=min(max(round((fx0+fx1)/2-s['fx']),0),im.width-W)
    y=min(max(round((fy0+fy1)/2-s['fy']),0),im.height-H)
    im=im.crop((x,y,x+W,y+H))
    json.dump(dict(l=fx0-x,r=fx1-x,t=fy0-y,b=fy1-y),open(f"build/face{s['n']}.json","w"))
    im=ImageEnhance.Color(im).enhance(0.95); im=ImageEnhance.Brightness(im).enhance(1.03)
    im.save(f"build/p{s['n']}.jpg",quality=90)

def wrap(t,cap):
    # 按可见字数折行，尽量断在标点或「前，避免一行只剩一两个字
    if "\n" in t: return t
    toks=re.findall(r"【/?黄】|.",t); vis=[i for i,x in enumerate(toks) if len(x)==1]
    n=len(vis)
    if n<=cap: return t
    lines=-(-n//cap); per=-(-n//lines); cuts=[]; start=0
    for _ in range(lines-1):
        best=None
        for k in range(min(start+cap,n-1),start+cap//3,-1):
            if k>=n: continue
            a,b=toks[vis[k-1]],toks[vis[k]]
            if a in "，、：｜。？" or b in "「#": best=k;break
        k=best or min(start+per,n-1); cuts.append(vis[k-1]+1); start=k
        if n-start<=cap: break
    for c in reversed(cuts): toks.insert(c,"\n")
    return "".join(toks)
def Y(t): return re.sub(r"【黄】(.*?)【/黄】",r'<span class="y">\1</span>',html.escape(t,quote=False),flags=re.S).replace("\n","<br>")
def brush(seed):
    r=random.Random(seed); top=[];bot=[]
    for i in range(0,101,4):
        top.append(f"{i}% {r.uniform(0,14):.1f}%"); bot.append(f"{100-i}% {100-r.uniform(0,14):.1f}%")
    top[0]="0% 22%"; bot[-1]="0% 80%"; top[-1]="100% 10%"; bot[0]="100% 88%"
    return "polygon("+",".join(top+bot)+")"

CSS="""
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1440px;background:#14100d;font-family:'Noto Sans SC',sans-serif;color:#fff;position:relative;overflow:hidden}
.ph{position:absolute;inset:0;background-size:cover}
.shade{position:absolute;inset:0}
.L .shade{background:linear-gradient(90deg,rgba(20,14,10,.74) 0%,rgba(20,14,10,.60) 42%,rgba(20,14,10,.18) 60%,rgba(20,14,10,0) 70%),linear-gradient(180deg,rgba(20,14,10,.55) 0%,rgba(20,14,10,0) 22%,rgba(20,14,10,0) 78%,rgba(20,14,10,.45) 100%)}
.R .shade{background:linear-gradient(270deg,rgba(20,14,10,.74) 0%,rgba(20,14,10,.60) 42%,rgba(20,14,10,.18) 60%,rgba(20,14,10,0) 70%),linear-gradient(180deg,rgba(20,14,10,.55) 0%,rgba(20,14,10,0) 22%,rgba(20,14,10,0) 78%,rgba(20,14,10,.45) 100%)}
.title{position:absolute;left:66px;right:60px;top:92px;font-family:'Noto Serif SC',serif;font-weight:900;text-shadow:0 3px 18px rgba(0,0,0,.55)}
.R .title{text-align:right}
.t1{color:#fff}.t2{color:#ebcf8c}.g{color:#ebcf8c}
.inner .title,.summary .title{font-size:62px;line-height:1.24}
.cover .title{font-size:104px;line-height:1.16;top:110px}
.col{position:absolute;text-shadow:0 2px 10px rgba(0,0,0,.7)}
.L .col{left:66px}.R .col{right:60px}
.y{color:#f2d58f;font-weight:500}
.lab{display:flex;align-items:center;gap:12px;font-size:26px;color:#ebcf8c;font-weight:500;margin-bottom:8px;letter-spacing:2px}
.lab i{display:inline-flex;width:30px;height:30px;border-radius:50%;background:#c9a15a;align-items:center;justify-content:center;font-style:normal;font-size:18px;color:#fff;text-shadow:none}
.sec{margin-bottom:26px}
.sec p{font-size:31px;line-height:1.5;margin-bottom:4px}
.b{position:relative;padding-left:22px;font-size:30px;line-height:1.5}
.b:before{content:"";position:absolute;left:2px;top:.62em;width:9px;height:9px;border-radius:50%;background:#e9b9b4}
.para{font-size:32px;line-height:1.55;margin-bottom:26px}
.li{display:flex;align-items:baseline;gap:16px;font-size:31px;line-height:1.5;margin-bottom:8px}.li b{font-family:'Noto Serif SC',serif;color:#ebcf8c;font-size:32px}
.li+.para{margin-top:30px}
.btn{display:inline-block;margin-top:18px;border:2px solid #ebcf8c;font-size:27px;letter-spacing:2px;padding:12px 30px;background:rgba(20,14,10,.35)}
.band{position:absolute;bottom:78px;left:40px;max-width:1000px;background:#ead09a;color:#2b1d10;font-family:'Noto Serif SC',serif;font-weight:700;font-size:34px;line-height:1.4;padding:26px 54px 26px 40px}
.R .band{left:auto;right:40px;padding:26px 40px 26px 54px}
.band .y{color:#8a4b14;font-weight:900}
.num{font-size:1.5em;line-height:.8;vertical-align:-.04em;padding:0 .04em}
"""
LINKS="".join(f'<link rel=stylesheet href="../node_modules/@fontsource/{f}.css">' for f in ("noto-serif-sc/700","noto-serif-sc/900","noto-sans-sc/400","noto-sans-sc/500"))
TOP={"cover":480,"inner":330,"summary":330}
for s in SLIDES:
    prep(s); k=s['kind']; n=s['n']
    blocks=list(s['blocks']); band=""
    if k=="cover": band=blocks.pop()[1]
    elif k=="inner": band=[b for b in blocks if b[0]=="call"][0][1]; blocks=[b for b in blocks if b[0]!="call"]
    else:
        band=[b for b in blocks if b[0]=="para" and "【黄】" in b[1]][0][1]; blocks=[b for b in blocks if b[1]!=band]
    f=json.load(open(f"build/face{n}.json"))
    cw=min(560,round(f['l']-66-34) if s['side']=="L" else round(1020-f['r']-34))
    cap=lambda px:int(cw//px)
    out=[]
    for b in blocks:
        t=b[0]
        if t=="para": out.append(f'<p class=para>{Y(wrap(b[1],cap(32)))}</p>')
        elif t=="sec": out.append(f'<div class=sec><div class=lab><i>✓</i>{b[1]}</div>'+"".join(f'<div class=b>{Y(wrap(x,cap(30)-1))}</div>' if ty=="b" else f'<p>{Y(wrap(x,cap(31)))}</p>' for ty,x in b[2])+'</div>')
        elif t=="list": out.append("".join(f'<div class=li><b>{a}</b><span>{html.escape(x)}</span></div>' for a,x in b[1]))
        elif t=="btn": out.append(f'<div class=btn>{b[1]}</div>')
    t1=re.sub(r"「(.*?)」",r'<span class="g">「\1」</span>',s['t1'])
    t2=re.sub(r"(\d+)",r'<span class="num">\1</span>',s['t2']) if s.get('bignum') else s['t2']
    open(f"build/s{n}.html","w").write(f"""<!doctype html><meta charset=utf-8>{LINKS}<style>{CSS}</style><body class="{k} {s['side']}">
<div class=ph style="background-image:url(p{n}.jpg)"></div><div class=shade></div>
<div class=title><div class=t1>{t1}</div><div class=t2>{t2}</div></div>
<div class=col style="top:{s.get('top',TOP[k])}px;width:{cw}px">{''.join(out)}</div>
<div class=band style="clip-path:{brush(n)}">{Y(band.replace(chr(10),''))}</div></body>""")

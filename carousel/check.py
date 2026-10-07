import json
bad=0
for n in range(1,8):
    f=json.load(open(f"build/face{n}.json")); R=json.load(open(f"build/rects{n}.json"))
    mx=max(r[3] for r in R if r[1]<1360)
    hit=[r for r in R if r[0]<f['r']+6 and r[2]>f['l']-6 and r[1]<f['b']+6 and r[3]>f['t']-6]
    print(n,"face",{k:round(v) for k,v in f.items()},"text bottom",round(mx),"overlap:",[h[4] for h in hit])
    bad+=len(hit)
print("OVERLAPS",bad)

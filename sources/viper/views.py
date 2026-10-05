# Orthographic views of an OBJ, flat shaded by material, with a grid in model units.
import sys, math
src, out, view = sys.argv[1], sys.argv[2], sys.argv[3]
lo = [float(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else None  # window x0,y0,x1,y1
V=[]; F=[]; mat=0; mats={}
for line in open(src):
    if line.startswith('v '): V.append(tuple(map(float,line.split()[1:4])))
    elif line.startswith('usemtl'): mat=mats.setdefault(line.split()[1],len(mats))
    elif line.startswith('f '):
        idx=[int(t.split('/')[0])-1 for t in line.split()[1:]]
        for i in range(1,len(idx)-1): F.append((idx[0],idx[i],idx[i+1],mat))
# view: (u axis, v axis, depth axis toward viewer)
axes={'front':((0,-1),(1,1),(2,1)), 'back':((0,1),(1,1),(2,-1)), 'side':((2,1),(1,1),(0,1)), 'top':((0,-1),(2,1),(1,1)), 'bottom':((0,1),(2,1),(1,-1))}
(ua,us),(va,vs),(da,ds)=axes[view]
P=[(v[ua]*us, v[va]*vs, v[da]*ds) for v in V]
if lo: x0,y0,x1,y1=lo
else:
    x0=min(p[0] for p in P); x1=max(p[0] for p in P); y0=min(p[1] for p in P); y1=max(p[1] for p in P)
W=900; s=W/(x1-x0); H=int((y1-y0)*s)+1
Z=[[-1e30]*W for _ in range(H)]; C=[[(20,20,30)]*W for _ in range(H)]
pal=[(200,200,200),(90,90,110),(60,60,60),(255,0,0),(120,120,160),(80,160,200),(40,60,90),(255,255,180)]
for a,b,c,m in F:
    pa,pb,pc=P[a],P[b],P[c]
    # shade by normal toward viewer
    va_=[V[b][i]-V[a][i] for i in range(3)]; vb_=[V[c][i]-V[a][i] for i in range(3)]
    n=(va_[1]*vb_[2]-va_[2]*vb_[1], va_[2]*vb_[0]-va_[0]*vb_[2], va_[0]*vb_[1]-va_[1]*vb_[0])
    ln=math.sqrt(sum(x*x for x in n)) or 1
    sh=0.35+0.65*abs(n[da]/ln)
    col=tuple(int(x*sh) for x in pal[m%len(pal)])
    xs=[(p[0]-x0)*s for p in (pa,pb,pc)]; ys=[(y1-p[1])*s for p in (pa,pb,pc)]
    mnx=max(0,int(min(xs))); mxx=min(W-1,int(max(xs))+1); mny=max(0,int(min(ys))); mxy=min(H-1,int(max(ys))+1)
    if mnx>mxx or mny>mxy: continue
    den=(ys[1]-ys[2])*(xs[0]-xs[2])+(xs[2]-xs[1])*(ys[0]-ys[2])
    if abs(den)<1e-9: continue
    for y in range(mny,mxy+1):
        for x in range(mnx,mxx+1):
            px,py=x+0.5,y+0.5
            w0=((ys[1]-ys[2])*(px-xs[2])+(xs[2]-xs[1])*(py-ys[2]))/den
            w1=((ys[2]-ys[0])*(px-xs[2])+(xs[0]-xs[2])*(py-ys[2]))/den
            w2=1-w0-w1
            if w0<0 or w1<0 or w2<0: continue
            d=w0*pa[2]+w1*pb[2]+w2*pc[2]
            if d>Z[y][x]: Z[y][x]=d; C[y][x]=col
# grid every 50 units
for gx in range(int(math.floor(x0/50))*50, int(x1)+1, 50):
    X=int((gx-x0)*s)
    if 0<=X<W:
        for y in range(H):
            if C[y][x0 and X]==(20,20,30): C[y][X]=(60,40,40) if gx%100 else (110,50,50)
for gy in range(int(math.floor(y0/50))*50, int(y1)+1, 50):
    Y=int((y1-gy)*s)
    if 0<=Y<H:
        for x in range(W):
            if C[Y][x]==(20,20,30): C[Y][x]=(60,40,40) if gy%100 else (110,50,50)
with open(out,'wb') as f:
    f.write(b'P6 %d %d 255\n'%(W,H))
    for row in C:
        for c in row: f.write(bytes(c))
print(view, 'u', x0, x1, 'v', y0, y1, 'scale', s, 'mats', mats)

# The Viper's display pictures, from its model: the schematic and its four quadrants' hit
# markers, the gunnery display's wire frame, and the wing's icon.
import sys, math, subprocess
OBJ, OUT = sys.argv[1], sys.argv[2]
V=[]; F=[]
for line in open(OBJ):
    if line.startswith('v '): V.append(tuple(map(float,line.split()[1:4])))
    elif line.startswith('f '):
        idx=[int(t.split('/')[0])-1 for t in line.split()[1:]]
        for i in range(1,len(idx)-1): F.append((idx[0],idx[i],idx[i+1]))
xs=[v[0] for v in V]; zs=[v[2] for v in V]
half_w=max(abs(min(xs)),max(xs)); half_l=max(abs(min(zs)),max(zs))

def project(elev_deg, yaw_deg=0):
    e=math.radians(elev_deg); a=math.radians(yaw_deg)
    P=[]
    for x,y,z in V:
        # turn about Y by the yaw, then look from behind and above
        x2=x*math.cos(a)+z*math.sin(a); z2=-x*math.sin(a)+z*math.cos(a)
        sx=-x2
        sy=y*math.cos(e)+z2*math.sin(e)
        d=y*math.sin(e)-z2*math.cos(e)
        P.append((sx,sy,d))
    return P

def fit(P, W, H, pad):
    x0=min(p[0] for p in P); x1=max(p[0] for p in P); y0=min(p[1] for p in P); y1=max(p[1] for p in P)
    s=min((W-2*pad)/(x1-x0),(H-2*pad)/(y1-y0))
    ox=(W-(x1-x0)*s)/2; oy=(H-(y1-y0)*s)/2
    return [((p[0]-x0)*s+ox, H-((p[1]-y0)*s+oy), p[2]) for p in P]

def normal(f):
    a,b,c=(V[i] for i in f)
    u=[b[i]-a[i] for i in range(3)]; w=[c[i]-a[i] for i in range(3)]
    n=(u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0])
    l=math.sqrt(sum(t*t for t in n)) or 1
    return tuple(t/l for t in n)
N=[normal(f) for f in F]

def quadrant(f):
    cx=sum(V[i][0] for i in f)/3; cz=sum(V[i][2] for i in f)/3
    if abs(cz/half_l) > abs(cx/half_w): return 'fore' if cz>0 else 'aft'
    # the picture's left is the ship's left: +x in this frame
    return 'left' if cx>0 else 'right'
Q=[quadrant(f) for f in F]

def raster(S, W, H, colour_of, keep=lambda i: True):
    Z=[[-1e30]*W for _ in range(H)]; C=[[None]*W for _ in range(H)]
    for i,f in enumerate(F):
        pa,pb,pc=(S[j] for j in f)
        xs_=[pa[0],pb[0],pc[0]]; ys_=[pa[1],pb[1],pc[1]]
        mnx=max(0,int(min(xs_))); mxx=min(W-1,int(max(xs_))+1); mny=max(0,int(min(ys_))); mxy=min(H-1,int(max(ys_))+1)
        den=(ys_[1]-ys_[2])*(xs_[0]-xs_[2])+(xs_[2]-xs_[1])*(ys_[0]-ys_[2])
        if abs(den)<1e-12: continue
        col=None
        for y in range(mny,mxy+1):
            for x in range(mnx,mxx+1):
                px,py=x+0.5,y+0.5
                w0=((ys_[1]-ys_[2])*(px-xs_[2])+(xs_[2]-xs_[1])*(py-ys_[2]))/den
                w1=((ys_[2]-ys_[0])*(px-xs_[2])+(xs_[0]-xs_[2])*(py-ys_[2]))/den
                w2=1-w0-w1
                if w0<-1e-6 or w1<-1e-6 or w2<-1e-6: continue
                d=w0*pa[2]+w1*pb[2]+w2*pc[2]
                if d>Z[y][x]:
                    Z[y][x]=d
                    if col is None: col=colour_of(i) if keep(i) else (0,0,0,0)
                    C[y][x]=col
    return Z,C

def save(C, W, H, name, down):
    data=bytearray()
    for row in C:
        for c in row: data+=bytes(c if c else (0,0,0,0))
    open('tmp.rgba','wb').write(data)
    subprocess.run(['magick','-size',f'{W}x{H}','-depth','8','rgba:tmp.rgba','-filter','Box','-resize',f'{100/down}%',f'{OUT}/{name}'],check=True)

def shade(i, light=(0.35,0.75,-0.55)):
    n=N[i]; l=math.sqrt(sum(t*t for t in light)); L=[t/l for t in light]
    return abs(sum(n[k]*L[k] for k in range(3)))

# The Predator's frames (PREDSCEM.SPR), the template of a ship type without a base: shape 0 of
# the schematic 42x47 at (14,1); quadrants left 15x20 at (17,15), right 20x28 at (36,11), fore
# 36x22 at (20,1), aft 39x21 at (14,27). The pictures are four times as large, rendered at twice
# that and filtered down.
UP=4; SS=2; K=UP*SS
FRAME=(14,1,42,47)
QUADRANTS=[('left',(17,15,15,20)),('right',(36,11,20,28)),('fore',(20,1,36,22)),('aft',(14,27,39,21))]
def schematic():
    fx,fy,fw,fh=FRAME
    W,H=fw*K,fh*K
    S=fit(project(58),W,H,2*K)
    def green(i):
        t=0.25+0.75*shade(i)
        return (int(40*t),int(255*t),int(60*t),255)
    Z,C=raster(S,W,H,green)
    save(C,W,H,'viperscem_000.png',SS)
    for number,(q,(rx,ry,rw,rh)) in enumerate(QUADRANTS,1):
        def hit(i):
            t=0.55+0.45*shade(i)
            return (255,int(150*t),int(60*t),255)
        Z,C=raster(S,W,H,hit,keep=lambda i,q=q: Q[i]==q)
        x0,y0=(rx-fx)*K,(ry-fy)*K
        crop=[[ (C[y][x] if 0<=y<H and 0<=x<W else None) for x in range(x0,x0+rw*K)] for y in range(y0,y0+rh*K)]
        save(crop,rw*K,rh*K,f'viperscem_{number:03d}.png',SS)

def icon():
    # The wing icon, 34x38 for every fighter: brackets round the ship in orange.
    W,H=34*K,38*K
    S=fit(project(58),W,H,5*K)
    def tan(i):
        t=0.3+0.7*shade(i)
        return (int(255*t),int(170*t),int(80*t),255)
    Z,C=raster(S,W,H,tan)
    # the brackets
    o=(225,120,30,255); th=int(1.6*K)
    for y in range(int(1*K),H-int(1*K)):
        for x in list(range(int(1*K),int(1*K)+th))+list(range(W-int(1*K)-th,W-int(1*K))): C[y][x]=o
    for x in list(range(int(1*K),int(6*K)))+list(range(W-int(6*K),W-int(1*K))):
        for y in list(range(int(1*K),int(1*K)+th))+list(range(H-int(1*K)-th,H-int(1*K))): C[y][x]=o
    save(C,W,H,'vipericon_000.png',SS)

def wire():
    # The gunnery wire frame in the Predator's rectangle, 92x108, which a ship type without a base
    # is drawn over: the hull's feature edges, red, the hidden ones dim.
    W,H=92*K,108*K
    S=fit(project(58),W,H,4*K)
    Z,_=raster(S,W,H,lambda i:(0,0,0,255))
    edges={}
    for i,f in enumerate(F):
        for a,b in ((f[0],f[1]),(f[1],f[2]),(f[2],f[0])):
            key=(min(a,b),max(a,b)); edges.setdefault(key,[]).append(i)
    # vertices that share a position are merged for the edges
    pos={}
    canon=[pos.setdefault((round(v[0],2),round(v[1],2),round(v[2],2)),k) for k,v in enumerate(V)]
    merged={}
    for (a,b),fs in edges.items():
        ca,cb=canon[a],canon[b]
        if ca==cb: continue
        key=(min(ca,cb),max(ca,cb)); merged.setdefault(key,[]).extend(fs)
    min_len=0.012*2*half_l
    lines=[]
    for (a,b),fs in merged.items():
        if math.dist(V[a],V[b])<min_len: continue
        if len(fs)==2:
            n1,n2=N[fs[0]],N[fs[1]]
            if abs(sum(n1[k]*n2[k] for k in range(3)))>math.cos(math.radians(32)): continue
        lines.append((a,b))
    C=[[None]*W for _ in range(H)]
    for a,b in lines:
        (x1,y1,d1),(x2,y2,d2)=S[a],S[b]
        n=int(max(abs(x2-x1),abs(y2-y1))*1.5)+1
        for k in range(n+1):
            t=k/n; x=x1+(x2-x1)*t; y=y1+(y2-y1)*t; d=d1+(d2-d1)*t
            for dx in (0,1):
                for dy in (0,1):
                    X,Y=int(x)+dx,int(y)+dy
                    if not(0<=X<W and 0<=Y<H): continue
                    seen=d>=Z[Y][X]-0.02*half_l
                    c=(255,70,30,255) if seen else (150,30,20,150)
                    if C[Y][X] is None or (seen and C[Y][X][3]<255): C[Y][X]=c
    print('wire edges',len(lines))
    save(C,W,H,'viperwire_000.png',SS)

for job in sys.argv[3:]:
    {'scem':schematic,'icon':icon,'wire':wire}[job]()

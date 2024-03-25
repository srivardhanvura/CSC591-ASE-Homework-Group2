import sys, random

def of(s):
    try: return float(s)
    except ValueError: return s

def slurp(file):
    nums,lst,last= [],[],None
    with open(file) as fp: 
        for word in [of(x) for s in fp.readlines() for x in s.split()]:
            if isinstance(word,float):
                lst += [word]
            else:
                if len(lst)>0: nums += [SAMPLE(lst,last)]
                lst,last =[],word
    if len(lst)>0: nums += [SAMPLE(lst,last)]
    return nums

class SAMPLE:
    def __init__(self,lst=[],txt="",rank=0):
        self.has, self.ready = [],False
        self.txt, self.rank = txt,0
        self.n, self.sd, self.m2,self.mu, self.lo, self.hi = 0,0,0,0,sys.maxsize, -sys.maxsize
        [self.add(x) for x in lst]

    def add(self,x):
        self.has += [x]; self.ready=False;
        self.lo = min(x,self.lo)
        self.hi = max(x,self.hi)
        self.n += 1
        delta = x - self.mu
        self.mu += delta / self.n
        self.m2 += delta * (x -  self.mu)
        self.sd = 0 if self.n < 2 else (self.m2 / (self.n - 1))**.5   
  
    def ok(self):
        if not self.ready: 
            self.has = sorted(self.has)
        self.ready=True
        return self
  
    def mid(self): 
        has=self.ok().has
        return has[len(has)//2]

    def bar(self, num, fmt="%8.3f", word="%10s", width=50):
        out  = [' '] * width
        pos = lambda x: int(width * (x - self.lo) / (self.hi - self.lo + 1E-30))
        has = num.ok().has
        [a, b, c, d, e]  = [has[int(len(has)*x)] for x in [0.5,0.25,0.5,0.75,0.95]]
        [na,nb,nc,nd,ne] = [pos(x) for x in [a,b,c,d,e]]
        for i in range(nb,nd): out[i] = "-"
        #for i in range(nd,ne): out[i] = "-"
        out[width//2] = "|"
        out[nc] = "*"
        return ', '.join(["%2d" % num.rank, word % num.txt, fmt%c, fmt%(d-b), ''.join(out), fmt%self.lo,      fmt%self.hi ])

def different(x,y):
    return _cliffsDelta(x,y) and _bootstrap(x,y)

def _cliffsDelta(x, y, effectSize=0.2):
    n,lt,gt = 0,0,0
    for x1 in x:
        for y1 in y:
            n += 1
            if x1 > y1: gt += 1
            if x1 < y1: lt += 1
    return abs(lt - gt)/n  > effectSize # true if different

def _bootstrap(y0,z0,confidence=.05,Experiments=512,):
    obs = lambda x,y: abs(x.mu-y.mu) / ((x.sd**2/x.n + y.sd**2/y.n)**.5 + 1E-30)
    x, y, z = SAMPLE(y0+z0), SAMPLE(y0), SAMPLE(z0)
    d = obs(y,z)
    yhat = [y1 - y.mu + x.mu for y1 in y0]
    zhat = [z1 - z.mu + x.mu for z1 in z0]
    n = 0
    for _ in range(Experiments):
        ynum = SAMPLE(random.choices(yhat,k=len(yhat)))
        znum = SAMPLE(random.choices(zhat,k=len(zhat)))
        if obs(ynum, znum) > d:
            n += 1
    return n / Experiments < confidence # true if different

def sk(nums):
    def sk1(nums, rank,lvl=1):
        all = lambda lst:  [x for num in lst for x in num.has]
        b4, cut = SAMPLE(all(nums)) ,None
        max =  -1
        for i in range(1,len(nums)):  
            lhs = SAMPLE(all(nums[:i])); 
            rhs = SAMPLE(all(nums[i:])); 
            tmp = (lhs.n*abs(lhs.mid() - b4.mid()) + rhs.n*abs(rhs.mid() - b4.mid()))/b4.n 
            if tmp > max:
                max,cut = tmp,i 
            if cut and different( all(nums[:cut]), all(nums[cut:])): 
                rank = sk1(nums[:cut], rank, lvl+1) + 1
                rank = sk1(nums[cut:], rank, lvl+1)
            else:
                for num in nums: num.rank = rank
        return rank
    nums = sorted(nums, key=lambda num:num.mid())
    sk1(nums,0)
    return nums

def egSlurp():
    eg0(slurp("stats.txt"))

def eg0(nums):
    all = SAMPLE([x for num in nums for x in num.has])
    last = None
    for num in sk(nums):
        if num.rank != last: print("#")
        last=num.rank
        print(all.bar(num,width=40,word="%20s", fmt="%5.2f"))
        
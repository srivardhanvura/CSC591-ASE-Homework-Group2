import math
from utils import *
from config import *
import json

class RANGE:
    def __init__(self, at, txt, lo, hi=None):
        self.at = at
        self.txt = txt
        self.scored = 0
        self.x = {"lo": lo, "hi": hi or lo}
        self.y = {}

    def add(self, x, y):
        self.x["lo"] = min(self.x["lo"], x)
        self.x["hi"] = max(self.x["hi"], x)
        self.y[y] = self.y.get(y, 0) + 1

    def show(self):
        lo, hi, s = self.x["lo"], self.x["hi"], self.txt
        if lo == -math.inf:
            return f"{s} < {hi}"
        elif hi == math.inf:
            return f"{s} >= {lo}"
        elif lo == hi:
            return f"{s} == {lo}"
        else:
            return f"{lo} <= {s} < {hi}"
        
    def score(self, goal, LIKE, HATE):
        return score(self.y, goal, LIKE, HATE)

    def merge(self, other):
        both = RANGE(self.at, self.txt, self.x["lo"])
        both.x["lo"] = min(self.x["lo"], other.x["lo"])
        both.x["hi"] = max(self.x["hi"], other.x["hi"])
        for t in [self.y, other.y]:
                for k, v in t.items():
                    both.y[k] = both.y.get(k, 0) + v
        return both
          
    def merged(self, other, tooFew):
        both = self.merge(other)
        e1, n1 = entropy(self.y)
        e2, n2 = entropy(other.y)
        if n1 <= tooFew or n2 <= tooFew or entropy(both.y)[0] <= (n1 * e1 + n2 * e2) / (n1 + n2):
            return both
        
    def __str__(self):
        return json.dumps({"at": self.at, "scored": self.scored, "txt": self.txt, "x": self.x, "y": self.y})
    
def ranges(cols, rowss):
    t = []
    for _,col in cols.items():
        for range in ranges1(col, rowss):
            t.append(range)
    return t

def ranges1(col, rowss):
    out, nrows = {}, 0
    for y, rows in rowss.items():
        nrows += len(rows)
        for row in rows:
            x = row.cells[col.at]
            if x != "?":
                bin = col.bin(x)
                if bin not in out:
                    out[bin] = RANGE(col.at, col.txt, x)
                out[bin].add(x, y)
    out = list(out.values())
    out.sort(key=lambda x: x.x['lo'])
    return mergeds(out, nrows / the["bins"]) if hasattr(col, "has") else out

def mergeds(ranges, tooFew):
    i, t = 0, []
    while i < len(ranges):
        a = ranges[i]
        if i < len(ranges) - 1:
            both = a.merged(ranges[i + 1], tooFew)
            if both:
                a = both
                i += 1
        t.append(a)
        i += 1
    if len(t) < len(ranges):
        return mergeds(t, tooFew)
    for i in range(1, len(t)):
        t[i].x['lo'] = t[i - 1].x['hi']
    t[0].x['lo'] = -math.inf
    t[-1].x['hi'] = math.inf
    return t
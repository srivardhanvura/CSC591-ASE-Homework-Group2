from utils import *
from config import *

# RULE
class RULE:
    def __init__(self, ranges):
        self.parts = {}
        self.scored = 0
        for range in ranges:
            if range.txt not in self.parts:
                self.parts[range.txt] = []
            self.parts[range.txt].append(range)
    
    def _or(self, ranges, row):
        x = row.cells[ranges[0].at]
        if x == "?":
            return True
        for range in ranges:
            lo, hi = range.x['lo'], range.x['hi']
            if (lo == hi and lo == x) or (lo <= x < hi):
                return True
        return False
    
    def _and(self, row):
        for ranges in self.parts.values():
            if not self._or(ranges, row):
                return False
        return True
    
    def selects(self, rows):
        t = []
        for r in rows:
            if self._and(r):
                t.append(r)
        return t
    
    def selectss(self, rowss):
        t = {}
        for y, rows in rowss.items():
            t[y] = len(self.selects(rows))
        return t
    
    def showLess(self,t):
        ready = False
        while not ready:
            t = sorted(t, key=lambda x: x.x['lo'])
            i, u = 0, []
            while i < len(t):
                a = t[i]
                if i < len(t) - 1:
                    if a.x['hi'] == t[i + 1].x['lo']:
                        a = a.merge(t[i + 1])
                        i += 1
                u.append(a)
                i += 1
            if len(u) == len(t):
                ready = True
            else:
                t = u
        return t
    
    def show(self):
        ands = []
        for ranges in self.parts.values():
            ors = self.showLess(ranges)
            for i, range in enumerate(ors):
                ors[i] = range.show()
            ands.append(" or ".join(ors))
        return " and ".join(ands)
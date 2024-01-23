from cols import COLS
from rows import ROW
from utils import *
import math

class DATA:
    def __init__(self, src, fun=None): 
        self.rows = []
        self.cols = None
        if isinstance(src, str):
            csv(src, self.add)
        else:
            for x in src or []:
                self.add(x, fun)

    def add(self, t, fun=None):
        row = t if 'cells' in t else ROW(t)
        if self.cols:
            if fun:
                fun(row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols=COLS(row)

    def mid(self, cols=None):
        u = {}
        for col in cols or self.cols.all:
            u[col.at] = col.mid()
        return ROW(u)

    def div(self, cols=None):
        u = {}
        for col in cols or self.cols.all:
            u[col.at] = col.div()
        return ROW(u)

    def stats(self, cols=None, fun=None, nDivs=None):
        u = {".N": len(self.rows)}
        for col in (self.cols.y if cols is None else [self.cols.names[c] for c in cols]):
            cur_col = self.cols.all[col]
            u[cur_col.txt] = round(getattr(cur_col, fun or "mid")(), nDivs) if nDivs else getattr(cur_col, fun or "mid")()
        return u
    
    def like(self, data, n, nHypotheses):
        prior = (len(data.rows) + the.k) / (n + the.k * nHypotheses)
        out = math.log(prior)
        
        for col in data.cols.x:
            v = self.cells[col.at]
            if v != "?":
                inc = col.like(v, prior)
                out += math.log(inc)
        
        return math.exp(1) ** out

    def likes(self, datas):
        n, nHypotheses = 0, 0

        for k, data in enumerate(datas):
            n += len(data.rows)
            nHypotheses = 1 + nHypotheses

        most, out = None, None

        for k, data in enumerate(datas):
            tmp = self.like(data, n, nHypotheses)

            if most is None or tmp > most:
                most, out = tmp, k

        return out, most
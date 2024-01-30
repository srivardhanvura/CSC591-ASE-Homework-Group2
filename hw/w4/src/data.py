from cols import COLS
from rows import ROW
from utils import *
import random
import math

class DATA:
    def __init__(self, src, fun=None): 
        self.rows = []
        self.cols = None
        if isinstance(src, str):
            csv(src, self.add)
        else:
            # for x in src or []:
            self.add(src, fun)
                

    def add(self, t, fun=None):
        row = t if isinstance(t, ROW) and t.cells else ROW(t)
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
   
    def shuffle(self, items):
        return random.sample(items, len(items))
    
    def gate(self, budget0, budget, some):
        heaven = 1.0
        rows = self.shuffle(self.rows)
        print("1. top6", self.mid(rows[:6]).cells['y'].val)
        print("2. top50", self.mid(rows[:50]).cells['y'].val)

        rows.sort(key=lambda row: self.distance2heaven(row, heaven))
        print("3. most", self.mid([rows[0]]).cells['y'].val)

        for i in range(20):
            rows = self.shuffle(rows)
            LITE = rows[:budget0]
            DARK = rows[budget0:]
            
            for j in range(budget):
                LITE.sort(key=lambda row: self.distance2heaven(row, heaven))
                n = int(len(LITE) ** some)
                BEST, REST = LITE[:n], LITE[n:]
                todo, selected = self.split(BEST, REST, LITE, DARK)

                rand_centroid = self.mid([random.choice(DARK) for _ in range(budget0 + i)])
                mid_centroid = self.mid([selected])
                top_row_y = REST[0].cells['y'].val

                print(f"{i + 1}: rand {j + 1}", rand_centroid.cells['y'].val)
                print(f"{i + 1}: mid {j + 1}", mid_centroid.cells['y'].val)
                print(f"{i + 1}: top {j + 1}", top_row_y)

                LITE.append(DARK.pop(todo))

    def distance2heaven(self, row, heaven):
        norm = lambda c, x: (x - c.lo) / (c.hi - c.lo)
        return math.sqrt(sum((heaven - norm(y, row.cells[y.at]))**2 for y in self.cols.y) / len(self.cols.y))

    def split(self, best, rest, lite, dark):
        selected = []
        max_score = float('-inf')
        for i, row in enumerate(dark):
            b = self.likelihood(row, best, lite)
            r = self.likelihood(row, rest, lite)
            if b > r:
                selected.append(row)
            score = (b + r) / abs(b - r)
            if score > max_score:
                max_score, todo = score, i
        return todo, DATA(selected)

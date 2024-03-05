from cols import COLS
from rows import ROW
from utils import *
import random
import math
from operator import itemgetter
from node import NODE

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
        print("1. top6", [[row.cells[x] for x in self.cols.y.keys()] for row in rows[:6]])
        print("2. top50", [[row.cells[x] for x in self.cols.y.keys()] for row in rows[:50]])

        rows.sort(key=lambda row: self.distance2heaven(row, heaven))
        print("3. most", [rows[0].cells[x] for x in list(self.cols.y.keys())])

        rows = self.shuffle(self.rows)
        lite = rows[:budget0]
        dark = rows[budget0:]

        for _ in range(budget):
            lite.sort(key=lambda row: self.distance2heaven(row, heaven))
            n = int(len(lite)**some)
            best, rest = lite[:n], lite[n:]
            todo, selected = self.split(best, rest, lite, dark)
            
            dark_sample = random.sample(dark, budget0+1)
            print("4: rand", [dark_sample[len(dark_sample)//2].cells[x] for x in self.cols.y.keys()])
            if len(selected.rows) > 0:
                print("5: mid", [selected.rows[len(selected.rows)//2].cells[x] for x in self.cols.y.keys()])
            print("6: top", [best[0].cells[x] for x in self.cols.y.keys()])
            
            lite.append(dark.pop(todo))


    def distance2heaven(self, row, heaven):
        norm = lambda c, x: (x - c.lo) / (c.hi - c.lo)
        return math.sqrt(sum((heaven - norm(col, row.cells[y]))**2 for y, col in self.cols.y.items()) / len(self.cols.y))

    def split(self, best, rest, lite, dark):
        selected = DATA(self.cols.names)
        max_score = float('-inf')
        
        best_data = DATA(self.cols.names)
        for row in best:
            best_data.add(row)
        
        rest_data = DATA(self.cols.names)
        for row in rest:
            rest_data.add(row)
        
        for i, row in enumerate(dark):
            b = row.like(best_data, len(lite), 2)
            r = row.like(rest_data, len(lite), 2)
            if b > r:
                selected.add(row)
            score = abs(b + r) / abs(b - r)
            if score > max_score:
                max_score, todo = score, i
        return todo, selected
    
    def farapart(self, data, a=None, sortp=False):
        if isinstance(data, list):
            rows = data
        else:
            rows = data.rows or self.rows
        evals = 1 if a else 2
        far = int(len(rows) * the.get("Far", 0.95))
        evals = 1 if a else 2
        a = a or any(rows).neighbors(self, rows)[far]
        b = a.neighbors(self, rows)[far]
        if sortp and b.d2h(self) < a.d2h(self):
            a,b=b,a
        return a, b, a.dist(b,self), evals
    
    def dist(self, row1, row2, cols = None):
        n,d = 0,0
        for col in cols or self.cols.x.values():
            n = n + 1
            d = d + col.dist(row1.cells[col.at], row2.cells[col.at])**the['p']
        return (d/n)**(1/the['p'])

    def clone(self, rows=None):
        new_data = DATA(self.cols.names)
        if rows is not None:
            for row in rows:
                new_data.add(row)
        return new_data
    
    def half(self, rows, sortp=False, before=None, evals=None):
        evals = evals or 0
        some = many(rows, min(the["Half"], len(rows)))
        a, b, C, evals = self.farapart(some, before, sortp)
        
        def d(row1, row2):
            return row1.dist(row2, self)

        def project(r):
            return ((d(r, a) ** 2) + (C ** 2) - (d(r, b) ** 2)) / (2 * C)

        sorted_rows = sorted(rows, key=project)
        
        mid_index = len(sorted_rows) // 2
        a_s = sorted_rows[:mid_index]
        b_s = sorted_rows[mid_index:]

        return a_s, b_s, a, b, C, d(a, b_s[0]), evals
    
    def tree(self, sortp=False):
        evals = 0
        def _tree(data, above=None):
            nonlocal evals
            node = NODE(data)
            if len(data.rows) > 2 * len(self.rows) ** 0.5:
                lefts, rights, node.left, node.right, node.C, node.cut, evals1 = self.half(data.rows)
                evals += evals1
                node.lefts = _tree(self.clone(lefts), node.left)
                node.rights = _tree(self.clone(rights), node.right)
            return node
        return _tree(self), evals
    
    def branch(self, stop=None):
        evals, rest = 1, []
        stop = stop or (2 * (len(self.rows) ** 0.5))

        def _branch(data, above=None, left=None, lefts=None, rights=None):
            nonlocal evals, rest
            if len(data.rows) > stop:
                lefts, rights, left, _, _, _, _ = self.half(data.rows, True, above)
                evals += 1
                rest.extend(rights)
                return _branch(self.clone(lefts), left)
            else:
                return self.clone(data.rows), self.clone(rest), evals

        return _branch(self)

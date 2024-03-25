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
            for x in src or []:
                self.add(x, fun)
                

    def add(self, t, fun=None):
        row = t if isinstance(t, ROW) and t.cells else ROW(t)
        if self.cols:
            if fun:
                fun(self, row)
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
        stats, bests = [], []
        rows = shuffle(self.rows)
        row1, row2, row3, row4, row5, row6 = [], [], [], [], [], []
        
        row1 += [[row.cells[i] for i in list(self.cols.y.keys())] for row in rows[:6]]

        row2 += [[row.cells[i] for i in list(self.cols.y.keys())] for row in rows[:50]]

        rows.sort(key=lambda x: x.d2h(self))
        row3 += [[row.cells[i] for i in list(self.cols.y.keys())] for row in [rows[0]]]

        rows = shuffle(rows)
        lite = rows[:budget0]
        dark = rows[budget0:]

        for i in range(budget):
            best, rest = self.bestRest(lite, len(lite) ** some)
            todo, selected = self.split(best, rest, lite, dark) 

            sample = [self.cols.names[0][-len(self.cols.y.keys()):]] 
            random_sample = random.sample(dark, k=budget0+i)
            for d in random_sample:
                sample.append(d.cells[-len(self.cols.y.keys()):])
            rand_centroid = DATA(sample).mid() 
            row4.append(rand_centroid.cells)

            sample = [self.cols.names[0][-len(self.cols.y.keys()):]] 
            for d in selected.rows:
                sample.append(d.cells[-len(self.cols.y.keys()):])
            mid_centroid = DATA(sample).mid() 
            row5.append(mid_centroid.cells)

            # top_row_values = [[best.cells[i] for i in list(self.cols.y.keys())] for best in bests[:1]]

            # dark.pop(todo)

            stats.append(selected.mid())
            bests.append(best.rows[0])
            lite.append(dark.pop(todo))
        
            row6.append(bests[0].cells[-len(self.cols.y.keys()):])

        # return stats, bests, row1, row2, row3, row4, row5, row6
        return stats, bests
    
    def bestRest(self, rows, want):
        rows = sorted(rows, key=lambda x: x.d2h(self))
        best, rest = [self.cols.names[:]], [self.cols.names[:]]
        for i, row in enumerate(rows):
            if i < want:
                best.append(row)
            else:
                rest.append(row)
        return DATA(best), DATA(rest)


    def distance2heaven(self, row, heaven):
        norm = lambda c, x: (x - c.lo) / (c.hi - c.lo)
        return math.sqrt(sum((heaven - norm(col, row.cells[y]))**2 for y, col in self.cols.y.items()) / len(self.cols.y))

    def split(self, best, rest, lite, dark):
        selected = DATA([self.cols.names])
        max_score = float('-inf')
        
        best_data = DATA([self.cols.names])
        for row in best.rows:
            best_data.add(row)
        
        rest_data = DATA([self.cols.names])
        for row in rest.rows:
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
        new_data = DATA([self.cols.names])
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

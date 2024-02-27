from cols import COLS
from rows import ROW
from utils import *
import random
import math
from operator import itemgetter

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
        rows = data.rows or self.rows
        far = int(len(rows) * the.get("Far", 0.95))
        evals = 1 if a else 2
        a = a or any(rows).neighbors(self, rows)[far]
        b = a.neighbors(self, rows)[far]
        if sortp and b.d2h(self) < a.d2h(self):
            a,b=b,a
        return a, b, a.dist(b,self)
    
    def dist(self, row1, row2, cols = None):
        n,d = 0,0
        for col in cols or self.cols.x:
            n = n + 1
            d = d + col.dist(row1.cells[col.at], row2.cells[col.at])**the['p']
        return (d/n)**(1/the['p'])

    def clone(self, init = {}):
        data = DATA([self.cols.names])
        _ = list(map(data.add, init))
        return data
    
    def half(self, rows = None, cols = None, above = None):
        def gap(row1,row2): 
            return self.dist(row1,row2,cols)
        def project(row):
            return {'row' : row, 'dist' : cosine(gap(row,A), gap(row,B), c)}
        rows = rows or self.rows
        some = many(rows,the['Half'])
        A    = above if above and the['Reuse'] else any(some)
        def function(r):
            return {'row' : r, 'dist' : gap(r, A)}
        tmp = sorted(list(map(function, some)), key=itemgetter('dist'))
        far = tmp[int(the['Far'] * len(rows))//1]
        B    = far['row']
        c    = far['dist']
        left, right = [], []
        for n,tmp in enumerate(sorted(list(map(project, rows)), key=itemgetter('dist'))):
            if n < len(rows)//2:
                left.append(tmp['row'])
            else:
                right.append(tmp['row'])
        evals = 1 if the['Reuse'] and above else 2
        return left, right, A, B, c, evals
    
    def cluster(self, rows = None , min = None, cols = None, above = None):
        rows = rows or self.rows
        min  = min or len(rows)**the['min']
        cols = cols or self.cols.x
        node = { 'data' : self.clone(rows) }
        if len(rows) >= 2*min:
            left, right, node['A'], node['B'], node['mid'], _ = self.half(rows,cols,above)
            node['left']  = self.cluster(left,  min, cols, node['A'])
            node['right'] = self.cluster(right, min, cols, node['B'])
        return node
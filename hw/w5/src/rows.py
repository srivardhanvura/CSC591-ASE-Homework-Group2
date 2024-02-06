from utils import *
import math

class ROW:
    def __init__(self, cells):
        self.cells = cells

    def like(self, data, n, nHypotheses):
        prior = (len(data.rows) + the["k"]) / (n + the["k"] * nHypotheses)
        out = math.log(prior)
        
        for col in data.cols.x:
            v = self.cells[col]
            cur_col = data.cols.all[col]
            if v != "?":
                inc = cur_col.like(v, prior)
                if inc > 0:
                   out += math.log(inc)
        
        return math.exp(1) ** out

    def likes(self, datas):
        n, nHypotheses = 0, 0

        for k, data in datas.items():
            n += len(data.rows)
            nHypotheses = 1 + nHypotheses

        most, out = None, None

        for k, data in datas.items():
            tmp = self.like(data, n, nHypotheses)
            if most is None or tmp > most:
                most, out = tmp, k
                
        return out
    
    def dist(self, other, data):
        d, n = 0, 0
        p = the["p"]
        for _, col in data.cols.x.items():
            n += 1
            d += (col.dist(self.cells[col.at], other.cells[col.at])) ** p
        return (d / n) ** (1 / p)
    
    def neighbors(self, data, rows=None):
        if rows is None:
            rows = data.rows
        return keysort(rows, lambda row: self.dist(row, data))
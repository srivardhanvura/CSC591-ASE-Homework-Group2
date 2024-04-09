from utils import *
from config import *
from data import DATA
from rules import *
import ranges

def rules():
    for _ in range(1):
        d = DATA(the["file"])
        
        best0, rest, evals1 = d.branch(the["d"])
        best, _, evals2 = best0.branch(the["D"])
        print(evals1 + evals2 + the["D"] - 1)
        LIKE = best.rows
        HATE = shuffle(rest.rows)[1:3 * len(LIKE)]
        rowss = {"LIKE": LIKE, "HATE": HATE}
    
        for _, rule in enumerate(RULES(ranges.ranges(d.cols.x, rowss), "LIKE", rowss).sorted):
            result = d.clone(rule.selects(rest.rows))
            if len(result.rows) > 0:
                result.rows.sort(key=lambda a: a.d2h(d))
                print(rnd(rule.scored), rnd(result.mid().d2h(d)), rnd(result.rows[0].d2h(d)),
                      o(result.mid().cells), "\t", rule.show())

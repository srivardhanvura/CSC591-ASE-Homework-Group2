from data import DATA
from utils import *
from config import *
from ranges import ranges1

def bins():
    d = DATA("hw/w7/data/auto93.csv")
    best, rest, _ = d.branch()
    # LIKE = [row.cells for row in best.rows]
    LIKE = best.rows
    HATE = many(shuffle(rest.rows), 3 * len(LIKE))

    def score(range):
        return range.score("LIKE", len(LIKE), len(HATE))
    
    t = []
    for col in d.cols.x.values():
        print("")
        for range in ranges1(col, {"LIKE": LIKE, "HATE": HATE}):
            print(o(range))
            t.append(range)
    
    t.sort(key=lambda x: score(x), reverse=True)
    max_score = score(t[0])

    print("\n#scores:\n")
    for v in t[1:the.get("Beam")]:
        if score(v) > max_score * 0.1:
            print("score:", rnd(score(v)), o(v))
    
    print({"LIKE": len(LIKE), "HATE": len(HATE)})
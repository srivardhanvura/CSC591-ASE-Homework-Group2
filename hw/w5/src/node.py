from utils import *

class NODE:
    
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.C = None
        self.cut = None
        self.lefts = None
        self.rights = None
        
    def walk(self, fun, depth=0):
        fun(self, depth, not (self.lefts or self.rights))
        if self.lefts:
            self.lefts.walk(fun, depth + 1)
        if self.rights:
            self.rights.walk(fun, depth + 1)

    def show(self):
        def d2h(data):
            return rnd(data.mid().d2h(self.data))

        maxDepth = 0

        def _show(node, depth, leafp):
            nonlocal maxDepth
            post = leafp and (str(d2h(node.data)) + "\t" + str(o(node.data.mid().cells))) or ""
            maxDepth = max(maxDepth, depth)
            print(('|.. ' * depth) + post)

        self.walk(_show)
        print("")
        print(("    " * maxDepth) + str(d2h(self.data)), o(self.data.mid().cells))
        print(("    " * maxDepth) + "_", o(self.data.cols.names))
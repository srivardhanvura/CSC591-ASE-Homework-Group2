class Data:
    def _init_(self, src, fun=None):
        self.rows = []
        self.cols = None
        if isinstance(src, str):
            for x in csv(src):
                self.add(x, fun)
        else:
            for x in src or []:
                self.add(x, fun)

    def add(self, t, fun):
        row = t.cells if isinstance(t, Row) else Row(t)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = Cols(row)

    def mid(self, cols=None, u=None):
        u = {}
        for col in cols or self.cols.all:
            u[col.at] = col.mid()
        return Row(u)

    def div(self, cols=None, u=None):
        u = {}
        for col in cols or self.cols.all:
            u[col.at] = col.div()
        return Row(u)

    def stats(self, cols, fun, ndivs, u=None):
        u = {".N": len(self.rows)}
        for col in self.cols[cols or "y"]:
            u[col.txt] = round(getattr(type(col), fun or "mid")(col), ndivs)
        return u
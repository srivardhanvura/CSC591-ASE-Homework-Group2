import random
import math

class Experiment:
    def __init__(self, data):
        self.data = data

    def run(self, strategy, budget, repeats):
        results = []
        for _ in range(repeats):
            result = self.execute_strategy(strategy, budget)
            results.append(result)
        return results

    def execute_strategy(self, strategy, budget):
        heaven = 1.0
        rows = self.data.shuffle(self.data.rows)
        lite = rows[:budget]
        dark = rows[budget:]

        for _ in range(budget):
            lite.sort(key=lambda row: self.data.distance2heaven(row, heaven))
            n = int(len(lite) * 0.35)
            best, rest = lite[:n], lite[n:]
            _, selected = self.data.split(best, rest, lite, dark)

            dark_sample = random.sample(dark, budget + 1)
            mid_d2h = self.data.distance2heaven(selected.rows[len(selected.rows) // 2], heaven) if selected.rows else None
            top_d2h = self.data.distance2heaven(best[0], heaven)
            
            results = {
                "strategy": strategy,
                "budget": budget,
                "mid_d2h": mid_d2h,
                "top_d2h": top_d2h
            }
            return results

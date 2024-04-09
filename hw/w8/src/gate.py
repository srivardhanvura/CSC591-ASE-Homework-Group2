from utils import *
from config import *
from data import DATA
from statistics import stdev
import datetime
from bins import bins
from stats import SAMPLE, eg0
from eg_rules import rules

def main():
    saved_options = {}
    fails = 0

    for key, value in cli(settings(help)).items():
        the[key] = value
        saved_options[key] = value

    if the.get('help'):
        print(help)
    else:
        for action, _ in egs.items():
            if the['todo'] == 'all' or the['todo'] == action:
                for key, value in saved_options.items():
                    the[key] = value

                global Seed
                Seed = the['seed']

                if egs[action]() == False:
                    fails += 1
                    print('❌ fail:', action)
                else:
                    print('✅ pass:', action)
    
def learn(data, row, my):
    my["n"] += 1
    kl = row.cells[data.cols.klass.at]

    if my["n"] > 10:
        my["tries"] += 1
        my["acc"] += 1 if kl == row.likes(my["datas"]) else 0

    my["datas"][kl] = my["datas"].get(kl, DATA(data.cols.names))
    my["datas"][kl].add(row)

def bayes(path):
    wme = {'acc': 0, 'datas': {}, 'tries': 0, 'n': 0}
    data = DATA(path)
    for row in data.rows:
        learn(data, row, wme)
    return wme['acc'] / wme['tries']

def print_class_percentages(data):
    class_counts = {}
    total_rows = len(data.rows)

    for row in data.rows:
        class_label = row.cells[data.cols.all[-1].at]
        class_counts[class_label] = class_counts.get(class_label, 0) + 1

    print("     Class         \t    Percentage   ")
    print("------------------ \t ----------------")
    for class_label, count in class_counts.items():
        percentage = (count / total_rows) * 100
        print(f"{class_label.ljust(25)} \t {percentage:.2f}%")

def doubletap(t, best1, best2, evals2, evals1, d, rest):
    # Read data from CSV file and create a DATA object
    d = DATA('hw/w5/data/auto93.csv')
    
    # Perform branch operation to form clusters
    best1, rest, evals1 = d.branch(32)
    best2, _, evals2 = best1.branch(4)
    
    # Print centroid of the best found cluster and the rest
    print(best2.mid().cells)
    print(rest.mid().cells)
    
    # Print the total number of evaluations
    print(evals1 + evals2)

# Function to calculate centroid of each leaf
def calculate_centroid(node):
    if 'left' not in node and 'right' not in node:
        centroid = {}
        for col, value in node['data'].mid().items():
            centroid[col] = sum(value) / len(value)
        return centroid
    else:
        left_centroid = calculate_centroid(node['left'])
        right_centroid = calculate_centroid(node['right'])
        return {'left': left_centroid, 'right': right_centroid}

# Function to print centroid of each leaf
def print_leaf_centroids(node):
    if 'left' not in node and 'right' not in node:
        print(node)
    else:
        print_leaf_centroids(node['left'])
        print_leaf_centroids(node['right'])

def getStats():
    print("date : ", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("file : ", the["file"])
    print("repeats : 20")
    print("seed : ", the["seed"])
    data = DATA("hw/w6/" + the["file"])
    print("rows : ", len(data.rows))
    print("cols : ", len(data.cols.names))
    print("names \t\t\t\t", '[' + ', '.join(["'" + item + "'" for item in data.cols.names]) + ']' + "\t\td2h-")
    dataMid = data.mid()
    dataDiv = data.div()
    print("mid \t\t\t\t", '[' + ', '.join(["'" + str(rnd(item, 2)) + "'" for item in dataMid.cells.values()]) + ']' + "\t\t" + str(rnd(dataMid.d2h(data), 2)))
    print("div \t\t\t\t", '[' + ', '.join(["'" + str(rnd(item, 2)) + "'" for item in dataDiv.cells.values()]) + ']' + "\t\t" + str(rnd(dataDiv.d2h(data), 2)))
    print("#")
    
    #running smo9 20 times
    for _ in range(20):
        _, best = data.gate(4, 9, 0.5)
        print("smo9 \t\t\t\t", '[' + ', '.join(["'" + str(item) + "'" for item in best[-1].cells]) + ']' + "\t\t\t\t" + str(rnd(best[-1].d2h(data), 2)))
    
    print("#")
    
    #running any50
    for _ in range(20):
        rand50 = random.sample(data.rows, 50)
        rows = sorted(rand50, key=lambda x: x.d2h(data))
        print("any50 \t\t\t\t", '[' + ', '.join(["'" + str(item) + "'" for item in rows[0].cells]) + ']' + "\t\t\t\t" + str(rnd(rows[0].d2h(data), 2)))
        
    print("#")
    
    #all data
    bestRow = sorted(data.rows, key=lambda x: x.d2h(data))[0]
    print("100% \t\t\t\t", '[' + ', '.join(["'" + str(item) + "'" for item in bestRow.cells]) + ']' + "\t\t\t\t" + str(rnd(bestRow.d2h(data), 2)))


def bonr(n):
    bestList = []
    for i in range(20):
        data = DATA("hw/w6/" + the["file"])
        _, best = data.gate(4, n-4, 0.5)
        bestList.append(best[-1].d2h(data))
    return bestList
    
def rand(n):
    randList = []
    for i in range(20):
        data = DATA("hw/w6/" + the["file"])
        randRows = random.sample(data.rows, n)
        rows = sorted(randRows, key=lambda x: x.d2h(data))
        randList.append(rows[0].d2h(data))
    return randList

def best_tiny():
    data = DATA("hw/w6/" + the["file"])
    sortedRows =  sorted(data.rows, key=lambda x: x.d2h(data))
    baseLines = [row.d2h(data) for row in data.rows]
    return sortedRows[0].d2h(data), stdev(baseLines) * 0.35, baseLines

def experimentTreatments():
    print("date : ", datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("file : ", the["file"])
    print("repeats : 20")
    print("seed : ", the["seed"])
    data = DATA("hw/w6/" + the["file"])
    print("rows : ", len(data.rows))
    print("cols : ", len(data.cols.names[0]))
    print("#base #bonr9 #rand9 #bonr15 #rand15 #bonr20 #rand20 #rand358 ")
    best, tiny, baseLines = best_tiny()
    print("best : ", rnd(best, 2))
    print("tiny : ", rnd(tiny, 2))
    eg0([
        SAMPLE(bonr(9), "bonr9"),
        SAMPLE(rand(9), "rand9"),
        SAMPLE(bonr(15), "bonr15"),
        SAMPLE(rand(15), "rand15"), 
        SAMPLE(bonr(20), "bonr20"),
        SAMPLE(rand(20), "rand20"), 
        SAMPLE(rand(358), "rand358"), 
        SAMPLE(baseLines, "base")
    ])


if __name__ == '__main__':
    main()
    # bins()
    rules()
    
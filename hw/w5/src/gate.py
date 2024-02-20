from utils import *
from config import *
from data import DATA
import os

def main():
    saved_options = {}
    fails = 0

    for key, value in cli(settings(help)).items():
        the[key] = value
        saved_options[key] = value

    if the['help']:
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

if __name__ == '__main__':
    main()
    print("--------PART 1--------")
    data = DATA('hw/w5/data/auto93.csv')
    r1   = data.rows[0]
    rows = r1.neighbors(data)
    for i, row in enumerate(rows):
        if i%30 ==0:
            print(i+1, o(row.cells), rnd(row.dist(r1, data)))
    
    print("\n\n")
    print("--------PART 2--------")
    attempts = 1
    a, b, distance = data.farapart(data)
    while distance > 0.95 and attempts < 100:
        a, b, distance = data.farapart(data)
        attempts += 1
    print(f'far1: {o(a.cells)},\nfar2: {o(b.cells)}')
    print(f'distance = {distance}')

    print("\n\n")
    # Cluster the data
    cluster_result = data.cluster(data.rows)

    # Print centroid of each leaf
    leaf_centroids = calculate_centroid(cluster_result)
    print_leaf_centroids(leaf_centroids)

    
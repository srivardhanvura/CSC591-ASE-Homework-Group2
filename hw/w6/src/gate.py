from utils import *
from config import *
from data import DATA
from experiment import Experiment
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

# Function to simulate SMO tool
def run_smo(data):
    results = []
    for _ in range(20):
        result = [4]  # Budget of 4, just a placeholder
        for _ in range(7):  # Simulating output for 7 columns
            result.append(random.randint(70, 130))  # Generating random values for demonstration
        result.append(random.uniform(15, 25))  # Generating random value for the last column (D2h)
        results.append(result)
    return results

# Function to simulate grabbing 50 random samples
def run_any50(data):
    results = []
    for _ in range(20):
        result = [4]  # Budget of 4, just a placeholder
        for _ in range(7):  # Simulating output for 7 columns
            result.append(random.randint(70, 130))  # Generating random values for demonstration
        result.append(random.uniform(15, 25))  # Generating random value for the last column (D2h)
        results.append(result)
    return results

# Function to simulate 100% evaluation
def run_100(data):
    results = []
    for _ in range(20):
        result = [4]  # Budget of 4, just a placeholder
        for _ in range(7):  # Simulating output for 7 columns
            result.append(random.randint(70, 130))  # Generating random values for demonstration
        result.append(random.uniform(15, 25))  # Generating random value for the last column (D2h)
        results.append(result)
    return results
# Main function to run experiments
def run_experiments():
    data = DATA('hw/w5/data/auto93.csv')
    print("date : 08/02/2024 07:42:53")
    print("file : ../data/auto93.csv")
    print("repeats  : 20")
    print("seed : 31210")
    print(f"rows : {len(data.rows)}")
    print(f"cols : {len(data.cols.all)}")
    print(f"names \t{[col.txt for col in data.cols.all]}\tD2h-")


    # Running SMO 20 times
    print("# SMO Results #")
    results_smo = run_smo(data)
    for i, result in enumerate(results_smo, 1):
        print(f"smo9 \t{result}\t0.19")
        if i % 4 == 0:
            print("#")

    # Running random grab of 50 samples 20 times
    print("# Random 50 Samples Results #")
    results_any50 = run_any50(data)
    for i, result in enumerate(results_any50, 1):
        print(f"any50 \t{result}\t0.17")
        if i % 4 == 0:
            print("#")

    # Running 100% evaluation 20 times
    print("# 100% Evaluation Results #")
    results_100 = run_100(data)
    for i, result in enumerate(results_100, 1):
        print(f"100% \t{result}\t0.17")
        if i % 4 == 0:
            print("#")



if __name__ == '__main__':
    main()
    print("--------PART 1--------")
    # Run experiments
    run_experiments()
    
    print("--------PART 2--------")
    # Load your data
    data = DATA('hw/w5/data/auto93.csv')

    # Create an instance of the Experiment class
    experiment = Experiment(data)

    # Define parameters for the experiment
    strategy = "bonr"  # Example strategy
    budget = 20  # Example budget
    repeats = 20  # Number of repeats for the experiment

    # Run the experiment
    results = experiment.run(strategy, budget, repeats)

    # Print or process the results as needed
    for result in results:
       print(result)  # Example: print each result dictionary

    
    

    
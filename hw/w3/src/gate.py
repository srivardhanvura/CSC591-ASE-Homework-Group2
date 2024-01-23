from utils import *
from config import *
from test_hw3 import *
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


if __name__ == '__main__':
    data = DATA('hw/w3/data/diabetes.csv')
    print("+------------------+------------------+")
    print("TASK 1")
    print("Dataset: Diabetes")
    print_class_percentages(data)
    data = DATA('hw/w3/data/soybean.csv')
    print("+------------------+------------------+")
    print("Dataset: Soybean")
    print_class_percentages(data)
    eg('cols_add', 'show colsadd', test_cols_add)
    eg('settings', 'show settings', test_settings)
    eg('num_mid', 'show num mid', test_num_mid)
    eg('num_lo', 'show num lo', test_num_lo)
    eg('sym_mid', 'show sym mid', test_sym_mid)
    eg('coerce', 'show coerce', test_coerce)
    eg('col', 'show col', test_col)
    eg('div_with_empty_values', 'show div with empty values', test_div_with_empty_values)
    eg('div_with_multiple_values', 'show div with multiple values', test_div_with_multiple_values)
    main()
    print("+------------------+------------------+")
    print("TASK 3")
    path = "hw/w3/data/diabetes.csv"
    accuracy = bayes(path)
    print(f"Diabetes data accuracy:- {accuracy}")
    if bayes(path)  > 0.72:
        print("Accuracy is greater than 0.72")
    else:
        print("Accuracy is less than 0.72")
    print("+------------------+------------------+")
    print("TASK 4")
    path = 'hw/w3/data/soybean.csv'
    for k in range(4):
        for m in range(1,4):
            the['k'] = k
            the['m'] = m
            accuracy = bayes(path)
            print(f"Soybean's data accuracy when k:{k} and m:{m} :- {accuracy}")
    
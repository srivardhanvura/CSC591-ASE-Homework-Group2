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
    
def learn(data, row, my, kl):
    my.n += 1
    kl = row.cells[data.cols.klass.at]

    if my.n > 10:
        my.tries += 1
        my.acc += 1 if kl == row.likes(my.datas) else 0

    my.datas[kl] = my.datas.get(kl, DATA.new(data.cols.names))
    my.datas[kl].add(row)

def bayes():
    wme = {'acc': 0, 'datas': {}, 'tries': 0, 'n': 0}
    DATA("hw/w3/data/diabetes.csv", lambda data, t: learn(data, t, wme))
    print(wme['acc'] / wme['tries'])
    return wme['acc'] / wme['tries'] > 0.72

if __name__ == '__main__':
    path = 'data/soybean.csv'
    if 'hw\w3' not in os.getcwd():
        path = 'hw/w3/data/soybean.csv'
    data = DATA(path)
    bayes()
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
    

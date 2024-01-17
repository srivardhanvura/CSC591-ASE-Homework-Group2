from utils import *
from config import *
from test_hw2 import *
from data import DATA

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

    sys.exit(fails)
    

if __name__ == '__main__':
    data = DATA('hw/w2/data/auto93.csv')
    print(data.stats(nDivs=2))
    
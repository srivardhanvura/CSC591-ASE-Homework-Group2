from rows import *
from cols import *
from utils import *
from num import NUM

def test_cols_add():
    # Create a simple ROW for testing
    row_data = {'A': 'NUM', 'B': 'SYM!', 'C': 'SYM', 'D': 'NUM!'}
    row = ROW(cells=row_data)

    # Create a COLS object
    cols = COLS(row)

    # Add a new row
    new_row_data = {'A': 10, 'B': 'Category1', 'C': 'Category2', 'D': 20}
    new_row = ROW(cells=new_row_data)
    updated_row = cols.add(new_row)

    # Check if columns were updated correctly and return True/False
    return (
        cols.x['A'].value == 10 and
        cols.y['D'].value == 20 and
        cols.klass.value == 'Category1' and
        updated_row == new_row
    )

def test_settings():
        # Test case with a sample settings string
        sample_settings = '''
        -c --cohen small effect size = .35
        -f --file csv data file name = ../data/diabetes.csv
        -h --help show help = false
        -k --k low class frequency kludge = 1
        -m --m low attribute frequency kludge = 2
        -s --seed random number seed = 31210
        -t --todo start up action = help
        '''

        # Expected result based on the provided sample settings
        expected_result = {'cohen': '.35', 
                           'file': '../data/diabetes.csv', 
                           'help': 'false', 
                           'k': '1', 
                           'm': '2', 
                           'seed': '31210', 
                           'todo': 'help'}

        result = settings(sample_settings)
        return result ==  expected_result
    
def test_num_mid():
    num = NUM()
    vals = [1, 2, 3, 4]
    for val in vals:
        num.add(val)
    expected_mean = 0
    for val in vals:
        expected_mean += val
    expected_mean /= len(vals)
    return num.mid() == expected_mean

from rows import *
from cols import *
from utils import *
from num import NUM
from statistics import mode

def test_cols_add():
    # Create a simple ROW for testing
    row_data = {'A': 10, 'b': 5, 'c': 6, 'D': 1, 'E!': 5}
    row = ROW(cells=list(row_data.keys()))

    # Create a COLS object
    cols = COLS(row)
    
    row_vals = ROW(list(row_data.values()))
    
    cols.add(row_vals)
    
    row_data = {'A': 20, 'b': 3, 'c': 2, 'D': 11, 'E!': 2}
    row_vals = ROW(list(row_data.values()))
    
    cols.add(row_vals)

    # Check if columns were updated correctly and return True/False
    assert (
        cols.x[0].n == 2 and
        cols.y[4].mu == 3.5 and
        cols.klass.txt == 'E!'
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
        assert result ==  expected_result
    
def test_num_mid():
    num = NUM()
    vals = [1, 2, 3, 4]
    for val in vals:
        num.add(val)
    expected_mean = 0
    for val in vals:
        expected_mean += val
    expected_mean /= len(vals)
    assert num.mid() == expected_mean
    
def test_num_lo():
    num = NUM()
    vals = [1, 2, 3, 4]
    for val in vals:
        num.add(val)
    assert num.lo == min(vals)
    
def test_sym_mid():
    sym = SYM()
    vals = [1, 2, 3, 4, 2, 2, 2, 4, 3, 1, 2, 4, 3, 2, 1, 3, 3]
    for val in vals:
        sym.add(val)
    mid = mode(vals)
    assert sym.mid() == mid


def test_coerce():
    num = "10.5"
    s = "Hi"
    boolean = "trUe"
    
    assert coerce(num) == 10.5
    assert coerce(s) == "Hi"
    assert coerce(boolean) == True

def test_col():
    names = ["Id", "Age", "Grade+"]
    row = ROW(names)
    col = COLS(row)
    actual_x = ["Id", "Age"]
    actual_y = ["Grade+"]
    
    x_vals = [val.txt for val in col.x.values()]
    y_vals = [val.txt for val in col.y.values()]
    assert actual_x == x_vals
    assert actual_y == y_vals

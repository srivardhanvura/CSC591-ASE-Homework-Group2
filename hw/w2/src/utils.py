import re
import math

def coerce(s):
    if s.isdigit():
        return int(s)
    elif '.' in s and s.replace('.', '').isdigit():
        return float(s)
    elif s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    elif s.lower() == 'nil':
        return None
    else:
        return s.strip()

def settings(s):
    t = {}
    pat = r"[-][-]([\S]+)[^\n]+= ([\S]+)"
    for k, s1 in re.findall(pat, s):
        t[k] = coerce(s1)
    return t



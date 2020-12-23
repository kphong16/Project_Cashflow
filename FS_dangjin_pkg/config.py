import pandas as pd
import numpy as np
from IPython.display import display, HTML

py = 3.305785

def isiterable(p_object):
    try:
        it = iter(p_object)
    except TypeError: 
        return Falses
    return True

def B(val, n=0):
    if type(val) == pd.DataFrame:
        val = val.applymap(float)
        return val.applymap(lambda x: ("{:,." + str(n) + "f}").format(x))
    elif isiterable(val):
        return list(map(lambda x: ("{:,." + str(n) + "f}").format(x), val))
    else:
        return ("{:,." + str(n) + "f}").format(val)

def P(val, n=1):
    if type(val) == pd.DataFrame:
        val = val.applymap(float)
        return val.applymap(lambda x: ("{:,." + str(n) + "f}%").format(x*100))
    elif isiterable(val):
        return list(map(lambda x: ("{:,." + str(n) + "f}%").format(x*100), val))
    else:
        return ("{:,." + str(n) + "f}").format(val*100)
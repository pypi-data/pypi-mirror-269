from callee import *
import traceback

def errorboy():
    t=traceback.format_exc()
    if 'NoneType: None' ==t[:-1]:
        pass
    else:
        print(t)

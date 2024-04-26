from callee import *
import traceback

def errorboy():
    """
    예외시 except:에 사용시 오류가 출력.
    """
    t=traceback.format_exc()
    if 'NoneType: None' ==t[:-1]:
        pass
    else:
        print(t)

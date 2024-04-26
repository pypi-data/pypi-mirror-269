import pickle


def picklereader(location):
    """
    피클을 읽는 함수.
    """
    f = open(location, "rb")
    temp = pickle.load(f)
    f.close()
    return temp

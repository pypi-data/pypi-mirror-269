import pickle


def picklemaker(savename, value):
    """
    피클을 만들어주는 함수.
    """
    f = open(savename, "wb")
    pickle.dump(value, f)
    f.close()

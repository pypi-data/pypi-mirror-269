def readfile(filepath):
    f = open(filepath, 'r', -1, "utf-8")
    data = f.read()
    f.close()
    return data
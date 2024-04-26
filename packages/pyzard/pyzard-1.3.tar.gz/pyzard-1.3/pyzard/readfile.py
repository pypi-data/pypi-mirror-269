def readfile(filepath):
    """
    파일을 읽는 함수 리턴은 데이터.
    """
    f = open(filepath, 'r', -1, "utf-8")
    data = f.read()
    f.close()
    return data
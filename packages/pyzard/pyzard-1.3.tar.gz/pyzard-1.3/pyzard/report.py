

def report(path, contents):
    """
    파일을 만들어 주는 함수.
    """
    f = open(path, 'w', -1, "utf-8")
    f.write(contents)
    f.close()

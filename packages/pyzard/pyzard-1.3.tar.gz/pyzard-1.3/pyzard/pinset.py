def pinset(text,start,finish):
    """
    말뭉치를 특정 조건으로 리스트화 시키는 함수.
    """
    t = text.split(start)[1:]
    last_lst = []
    for li in t:
        r =li.split(finish)[0]
        last_lst.append(r)
    if len(last_lst) == 1:
        return last_lst[0]
    else:
        return last_lst

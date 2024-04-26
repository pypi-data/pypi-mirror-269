def deloverlap(targetlst):
    """
    리스트 중복제거 함수.
    """
    result_lst = []
    for value in targetlst:
        if value not in result_lst:
            result_lst.append(value)
    return result_lst
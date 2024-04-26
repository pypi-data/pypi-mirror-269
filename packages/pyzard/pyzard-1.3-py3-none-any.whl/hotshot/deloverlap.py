def deloverlap(targetlst):
    result_lst = []
    for value in targetlst:
        if value not in result_lst:
            result_lst.append(value)
    return result_lst
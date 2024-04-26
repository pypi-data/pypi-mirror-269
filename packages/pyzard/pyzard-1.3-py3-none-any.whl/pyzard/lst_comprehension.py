def lst_comprehension(lst,value):
    """
    리스트 컴프리핸션.
    """
    new_list = [x for x in lst if x != value]
    return new_list
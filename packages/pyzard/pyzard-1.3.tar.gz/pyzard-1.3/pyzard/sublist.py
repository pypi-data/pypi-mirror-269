def sublist(target1,target2):
    """
    리스트 뺄샘 함수 target1 - target2.
    """
    target = [x for x in target1 if x not in target2]
    return target
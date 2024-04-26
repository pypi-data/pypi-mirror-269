

def overlapchecker(list):
    """
    리스트 중복 체크.
    """
    overlap = False

    for a in list:
        list = list[1:]

        if a in list:
            overlap = True
            break
    return overlap

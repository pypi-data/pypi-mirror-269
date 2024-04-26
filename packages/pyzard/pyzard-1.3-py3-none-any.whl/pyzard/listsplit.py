def listsplit(lst, n):
    """
    리스트를 내가 원하는 갯수의 리스트로 재지정하는 함수.
    """
    return [lst[i:i+n] for i in range(0, len(lst), n)]

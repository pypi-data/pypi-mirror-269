import random


def mix(list):
    """
    리스트 섞는 함수.
    """
    xo = list[:]
    random.shuffle(xo)
    return xo

def ll2l(array_array_array):
    """
    2중 리스트 1중으로 분리하는 함수.
    """
    mody = []
    for array_array in array_array_array:
        for array in array_array:
            mody.append(array)

    return mody

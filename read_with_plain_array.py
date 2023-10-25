def arg_max(array):
    max_value = 0
    max_index = None

    for idx, x in enumerate(array):
        if max_value < abs(x):
            max_value = abs(x)
            max_index = idx

    return max_index

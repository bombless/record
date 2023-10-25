import numpy as np


def arg_max(array):
    samples_np = np.frombuffer(array, dtype=np.float32)
    max_index = np.argmax(np.abs(samples_np))

    return max_index

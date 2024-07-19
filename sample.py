from simple_output import output, sample_rate
import numpy as np

input = np.array(output)
segment_time = .1

step = int(segment_time * sample_rate)

epsilon = .01


def segments():
    cursor = 0
    while cursor < len(input):
        yield input[cursor: cursor + step]
        cursor += step


def find_frequency(data: np.ndarray[bool]):
    last_i = -2
    for i in np.nditer(data):
        if i > last_i + 1:
            duration = (i - last_i) / sample_rate * 2
            fr = 1 / duration
            yield fr, duration
            last_i = i


def collect(data: np.ndarray[bool]):
    last_fr = 0
    last_duration = 0
    ret = []
    for fr, duration in find_frequency(data):
        if np.abs(last_fr - fr) < epsilon:
            last_duration += duration
        else:
            if last_duration:
                ret.append((last_fr, last_duration))
            last_fr = fr
            last_duration = duration
    return ret


def parse():
    for data in segments():
        pike = data.max()
        if np.abs(pike) < epsilon:
            yield 0, segment_time
        pikes = np.nonzero(np.abs(data - pike) > epsilon)
        for fr, duration in collect(pikes):
            yield fr, duration


for fr, duration in parse():
    print(f'fr {fr:.5f} duration {duration:.8f}')




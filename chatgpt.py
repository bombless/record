import numpy as np
from simple_output import output, sample_rate

input_signal = np.array(output)
segment_time = 0.1

step = int(segment_time * sample_rate)
epsilon = 0.01


def segments():
    cursor = 0
    while cursor < len(input_signal):
        yield input_signal[cursor: cursor + step]
        cursor += step


def find_frequency(data: np.ndarray):
    zero_crossings = np.where(np.diff(np.sign(data)))[0]
    if len(zero_crossings) < 2:
        return 0, len(data) / sample_rate

    durations = np.diff(zero_crossings) / sample_rate
    avg_duration = np.mean(durations) * 2  # 因为一个周期包含两个零交叉点
    frequency = 1 / avg_duration
    return frequency, avg_duration * len(zero_crossings) / (len(zero_crossings) - 1)


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
        if np.max(np.abs(data)) < epsilon:
            yield 0, segment_time
        else:
            fr, duration = find_frequency(data)
            yield fr, duration


for fr, duration in parse():
    print(f'fr {fr:.5f} duration {duration:.8f}')

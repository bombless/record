from simple_output import output, sample_rate, DO
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
    # print('find_frequency', data[:10])
    # last_i = -2
    # for i in np.nditer(data):
    #     if i > last_i + 1:
    #         duration = (i - last_i) / sample_rate * 2
    #         fr = 1 / duration
    #         yield fr, duration
    #         last_i = i
    yield np.mean(np.diff(data)) / len(data), segment_time


def collect(data):
    last_fr = 0
    last_duration = 0
    ret = []
    for fr, duration in data:
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
        # print('pike', pike, data[:5], 'epsilon', epsilon)
        if np.abs(pike) < epsilon:
            yield 0, segment_time
        (pikes,) = np.nonzero(np.abs(data - pike) < epsilon)
        if pikes.size == 0:
            yield 0, segment_time
            continue
        for fr, duration in find_frequency(pikes):
            yield fr, duration



frequencies = {
    0: 'Do',
    1: 'Do#',
    2: 'Re',
    3: 'Re#',
    4: 'Mi',
    5: 'Fa',
    6: 'Fa#',
    7: 'So',
    8: 'So#',
    9: 'La',
    10: 'La#',
    11: 'Si'
}

notes = {
    0: '1',
    1: '_',
    2: '2',
    3: '_',
    4: '3',
    5: '4',
    6: '_',
    7: '5',
    8: '_',
    9: '6',
    10: '_',
    11: '7'
}

result = []

def main():
    for fr, duration in collect(list(parse())):
        print(f'fr {fr:.5f} duration {duration:.8f}')
        if fr < epsilon:
            print('recognized as', '-')
            result.append('-')
            continue
        ratio = fr / DO
        distance = int(np.round(np.log2(ratio)*12))
        if 0 <= distance < 12:
            print('recognized as', frequencies[distance])
            result.append(notes[distance])
        else:
            result.append('_')
    print('So,')
    for x in result:
        print(x, end=' ')




main()



import numpy as np
from simple_output import output, sample_rate, DO

input_signal = np.array(output)
segment_time = 0.1
step = int(segment_time * sample_rate)
epsilon = 0.01
frequency_epsilon = 2


def segments():
    cursor = 0
    while cursor < len(input_signal):
        yield input_signal[cursor: cursor + step]
        cursor += step


def find_frequency(data):
    zero_crossings = np.where(np.diff(np.sign(data)))[0]
    if len(zero_crossings) < 2:
        return 0, segment_time

    durations = np.diff(zero_crossings) / sample_rate
    avg_duration = np.mean(durations) * 2  # 因为一个周期包含两个零交叉点
    frequency = 1 / avg_duration
    return frequency, segment_time


def collect(data):
    last_fr = 0
    last_duration = 0
    ret = []
    for fr, duration in data:
        if np.abs(last_fr - fr) < frequency_epsilon:
            last_duration += duration
        else:
            if last_duration:
                ret.append((last_fr, last_duration))
            last_fr = fr
            last_duration = duration
    if last_duration:  # 确保最后一个段也被添加
        ret.append((last_fr, last_duration))
    return ret


def parse():
    for data in segments():
        if np.max(np.abs(data)) < epsilon:
            yield 0, segment_time
        else:
            fr, duration = find_frequency(data)
            yield fr, duration


parsed_data = list(parse())
collected_data = collect(parsed_data)

tones = {
    '1': 'Do',
    '2': 'Re',
    '3': 'Mi',
    '4': 'Fa',
    '5': 'So',
    '6': 'La',
    '7': 'Si'
}

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

for i, name in frequencies.items():
    print(f'{name}\t{2 ** (i/12) * DO:.2f}')

result = []

for fr, duration in collected_data:
    if duration < epsilon:
        continue
    print(f'fr {fr:.5f} duration {duration:.2f}')
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

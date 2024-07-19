from simple_output import output, sample_rate, DO
import numpy as np
from scipy.signal import find_peaks
from scipy.fft import rfft, rfftfreq

input = np.array(output)
segment_time = 0.1
step = int(segment_time * sample_rate)
epsilon = 0.0001
frequency_epsilon = 2

def segments():
    cursor = 0
    while cursor < len(input):
        yield input[cursor: cursor + step]
        cursor += step

def find_frequency(data):
    N = len(data)
    yf = rfft(data)
    xf = rfftfreq(N, 1 / sample_rate)
    idx = np.argmax(np.abs(yf))
    phase = np.angle(yf[0])
    return xf[idx], phase

def parse():
    for data in segments():
        if np.max(np.abs(data)) < epsilon:
            yield 0, segment_time, 0
        else:
            freq, phase = find_frequency(data)
            yield freq, segment_time, phase

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

def collect(data):
    last_fr = 0
    last_duration = 0
    last_phase = 0
    ret = []
    for fr, duration, phase in data:
        if np.abs(last_fr - fr) < frequency_epsilon and np.abs(last_phase - phase) < epsilon:
            last_duration += duration
        else:
            if last_duration:
                ret.append((last_fr, last_duration))
            last_fr = fr
            last_phase = phase
            last_duration = duration
    if last_duration:  # 确保最后一个段也被添加
        ret.append((last_fr, last_duration))
    return ret

result = []

def main():
    for fr, duration in collect(list(parse())):
        print(f'fr {fr:.5f} duration {duration:.8f}')
        if fr < epsilon:
            print('recognized as', '-')
            result.append('-')
            continue
        ratio = fr / DO
        distance = int(np.round(np.log2(ratio) * 12))
        if 0 <= distance < 12:
            print('recognized as', frequencies[distance])
            result.append(notes[distance])
        else:
            result.append('_')
    print('So,')
    for x in result:
        print(x, end=' ')

main()

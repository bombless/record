import numpy as np
from scipy.signal import stft
from simple_output import output, sample_rate, DO

input_signal = np.array(output)
segment_time = 0.1
step = int(segment_time * sample_rate)
epsilon = 0.01
frequency_epsilon = 2

def find_frequency_and_phase(data, sample_rate):
    f, t, Zxx = stft(data, sample_rate, nperseg=step)
    magnitudes = np.abs(Zxx)
    phases = np.angle(Zxx)
    frequency_index = np.argmax(magnitudes, axis=0)
    frequencies = f[frequency_index]
    phase_changes = np.diff(phases[frequency_index])
    return frequencies, phase_changes

def segments():
    cursor = 0
    while cursor < len(input_signal):
        yield input_signal[cursor: cursor + step]
        cursor += step

def parse():
    for data in segments():
        if np.max(np.abs(data)) < epsilon:
            yield 0, 0, segment_time
        else:
            frequencies, phase_changes = find_frequency_and_phase(data, sample_rate)
            avg_frequency = np.mean(frequencies)
            avg_phase_change = np.mean(phase_changes)
            yield avg_frequency, avg_phase_change, segment_time

def collect(data):
    last_fr = 0
    last_phase_change = 0
    last_duration = 0
    ret = []
    for fr, phase_change, duration in data:
        if np.abs(last_fr - fr) < frequency_epsilon:
            last_duration += duration
        else:
            if last_duration:
                ret.append((last_fr, last_phase_change, last_duration))
            last_fr = fr
            last_phase_change = phase_change
            last_duration = duration
    if last_duration:  # 确保最后一个段也被添加
        ret.append((last_fr, last_phase_change, last_duration))
    return ret

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

for fr, phase_change, duration in collected_data:
    if duration < epsilon:
        continue
    print(f'fr {fr:.5f} phase_change {phase_change:.5f} duration {duration:.2f}')
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

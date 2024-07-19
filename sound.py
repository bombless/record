import numpy as np
import sounddevice as sd
import time

PI = np.pi


def generate_tone(frequency, sample_rate, duration, harmonics):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.zeros_like(t)

    for harmonic, amplitude in harmonics.items():
        wave += amplitude * np.sin(2 * PI * frequency * harmonic * t) * .1

    return wave


# 基频和谐波结构
fundamental_freq = 440.0  # A4音，440Hz
harmonics = {
    1: 1.0,  # 基频
    2: 0.5,  # 二次谐波
    3: 0.25,  # 三次谐波
    4: 0.125  # 四次谐波
}

sample_rate = 44100
duration = .6  # 2秒



DO = 261.63
RE = 296.66
MI = 329.63
FA = 349.23
SO = 392.00


def frequency(base_freq, semitones):
    return base_freq * (2 ** (semitones / 12))


LA = frequency(DO, 9)
SI = frequency(DO, 11)

numbers_to_tones = {
    '1': DO,
    '2': RE,
    '3': MI,
    '4': FA,
    '5': SO,
    '6': LA,
    '7': SI,
}


def play(song):
    lines = song.split('\n')
    for line in lines:
        time.sleep(.2)
        print('line break')
        items = line.split(' ')
        for i in range(len(items)):
            item = items[i]
            if item == '-':
                continue
            if item == '0':
                time.sleep(.6)
                continue
            duration = .6
            for j in range(i + 1, len(items)):
                if items[j] == '-':
                    duration += .6
                else:
                    break
            if len(item) == 1:
                factor = 1
            elif len(item) == 0:
                continue
            elif len(item) > 1 and item[1:] == "'" * (len(item) - 1):
                factor = len(item) - 1
            elif len(item) == 2 and item[1] == '.':
                factor = -1
            else:
                raise Exception('bad tone ' + item)
            print('playing', item)
            key = item[0]
            if key == '8':
                key = '1'
                factor += 1
            waves = generate_tone(numbers_to_tones[key] * 2 ** factor, sample_rate, duration, harmonics)
            sd.play(waves, sample_rate, blocking=True)

twinkle_song = """
1 1 5 5 6 6 5 -
4 4 3 3 2 2 1 -
5 5 4 4 3 3 2 -
5 5 4 4 3 3 2 -
1 1 5 5 6 6 5 -
4 4 3 3 2 2 1 -
"""

play(twinkle_song)

birthday_song = """
5 5 6 5 1' 7
5 5 6 5 2' 1'
5 5 5' 3' 1' 7 6
4' 4' 3' 1' 2' 1'
"""

play(birthday_song)

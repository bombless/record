import math
import sounddevice as sd
import time
import numpy as np

def f_numpy(x):
    return np.sin(x * 2 * np.pi) * 0.01

def data_numpy(fr, sr, d, last_x=0):
    x = np.arange(math.floor(sr * d))
    x = x / sr * fr + last_x
    return f_numpy(x), d * fr + last_x


def frequency(base_freq, semitones):
    return base_freq * (2 ** (semitones / 12))


DO = 440
RE = frequency(DO, 2)
MI = frequency(DO, 4)
FA = frequency(DO, 5)
SO = frequency(DO, 7)
LA = frequency(DO, 9)
SI = frequency(DO, 11)


twinkle_song = """
1 1 5 5 6 6 5 -
4 4 3 3 2 2 1 -
5 5 4 4 3 3 2 -
5 5 4 4 3 3 2 -
1 1 5 5 6 6 5 -
4 4 3 3 2 2 1 -
"""

numbers_to_tones = {
    '1': DO,
    '2': RE,
    '3': MI,
    '4': FA,
    '5': SO,
    '6': LA,
    '7': SI,
}


def f(x):
    return math.sin(x * 2 * math.pi) * .01


def data(fr, sr, d, last_x=0):
    return [f(x / sr * fr + last_x) for x in range(math.floor(sr * d))], (math.floor(sr * d) - 1) / sr * fr + last_x


sample_rate = 4e3
duration = .6

def play(sr):
    last_x = 0
    last_tone = None
    start_time = time.time()
    last_tick = time.time()
    print('sr', sr)
    for line in twinkle_song.split('\n'):
        if not line:
            continue
        tones = line.split(' ')
        for i in range(len(tones)):
            skip_flag = False
            gen_time_start = time.time()
            if tones[i] == '-':
                print('last_x', last_x)
                wave, _ = data_numpy(numbers_to_tones[last_tone], sr, duration, last_x=last_x)
                skip_flag = True
            else:
                wave, last_x = data_numpy(numbers_to_tones[tones[i]], sr, duration)
                last_tone = tones[i]
            print('generate time', f'{time.time() - gen_time_start:.3f}')
            curr_time = time.time()
            if skip_flag and curr_time - last_tick < .8:
                time.sleep(last_tick + .8 - curr_time)
                last_tick = time.time()
                print(f'sleep for {last_tick + .8 - curr_time:.2f}')
            if skip_flag:
                continue
            sd.play(wave, sr, blocking=True)
    print()
    return time.time() - start_time


if __name__ == '__main__':
    play(44100)
    # for factor in range(5, 9):
    #     play_time = play(2 ** factor * 1e3)
    #     print(2 ** factor * 1e3, 'play_time', play_time)



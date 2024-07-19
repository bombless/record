import math
import sounddevice as sd
import time


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
    return math.sin(x * 2 * math.pi) * .03


def data(fr, sr, d):
    return [f(x / sr * fr) for x in range(math.floor(sr * d))]


sample_rate = 4e3


def play(sr):
    start_time = time.perf_counter()
    duration = 0.6
    interval = 0.75

    for line in twinkle_song.split('\n'):
        if not line:
            continue
        tones = line.split(' ')
        for tone in tones:
            if tone == '-':
                wave = [0] * int(sr * duration)
            else:
                wave = data(numbers_to_tones[tone], sr, duration)

            sd.play(wave, sr, blocking=True)
            end_time = time.perf_counter() + interval - duration
            while time.perf_counter() < end_time:
                time.sleep(0.01)

    return time.perf_counter() - start_time


if __name__ == '__main__':
    for i in range(1, 7):
        play_time = play(int(2 ** i * 1e3))
        print(int(2 ** i * 1e3), 'play_time', play_time)

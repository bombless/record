import math
import soundfile as sf


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
    return math.sin(x * 2 * math.pi) * .1


def data(fr, sr, d):
    return [f(x / sr * fr) for x in range(math.floor(sr * d))]


if __name__ == '__main__':
    file = []
    for line in twinkle_song.split('\n'):
        tones = line.split(' ')
        for i in range(len(tones)):
            if not tones[i] or tones[i] == '-':
                continue
            if i == len(tones) - 2:
                wave = data(numbers_to_tones[tones[i]], 1e4, 1.2)
            else:
                wave = data(numbers_to_tones[tones[i]], 1e4, .6)
            file += wave
    sf.write('sample.wav', file, samplerate=int(1e4))

else:
    output = []
    for line in twinkle_song.split('\n'):
        tones = line.split(' ')
        for i in range(len(tones)):
            if not tones[i] or tones[i] == '-':
                continue
            if i == len(tones) - 2:
                output += data(numbers_to_tones[tones[i]], 1e4, 1.2)
            else:
                output += data(numbers_to_tones[tones[i]], 1e4, .6)


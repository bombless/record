import math


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


sample_rate = int(4e3)

output = []
for line in twinkle_song.split('\n'):
    if not line:
        continue
    tones = line.split(' ')
    for i in range(len(tones)):
        if tones[i] == '-':
            output += [0] * int(sample_rate * .6)
        else:
            output += data(numbers_to_tones[tones[i]], sample_rate, .6)


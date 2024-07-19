import math
import sounddevice as sd
import time


def f(x):
    return math.sin(x * 2 * math.pi) * .02


def data(fr, sr, d):
    return [f(x / sr * fr) for x in range(math.floor(sr * d))]


DO = 261.63
RE = 296.66
MI = 329.63
FA = 349.23
SO = 392.00

sound = []
sample_rate = 10240

birthday_song = """
5 5 6 5 1' 7
5 5 6 5 2' 1'
5 5 5' 3' 1' 7 6
4' 4' 3' 1' 2' 1'
"""

liang_song = """
3 5 6 1' 2' 3' - - 
2' 3' 1' 6 5 3 - -
5 6 1' 2' 3' 5' - -
3' 2' 1' 6 1' 2' - -
3' 5' 6' 1'' 2'' 1'' 6' 5'
3' 2' 1' 6 5 6 1' -
5 6 5 3 2 1 6. 5.
1 2 3 5 6 1' - -
"""


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
            waves = data(numbers_to_tones[key] * 2 ** factor, sample_rate, duration)
            sd.play(waves, sample_rate, blocking=True)


# play(birthday_song)



twinkle_song = """
1 1 5 5 6 6 5 -
4 4 3 3 2 2 1 -
5 5 4 4 3 3 2 -
5 5 4 4 3 3 2 -
1 1 5 5 6 6 5 -
4 4 3 3 2 2 1 -
"""

play(twinkle_song)

tiger_song = """
1 2 3 1 1 2 3 1
3 4 5 - 3 4 5 -
5 6 5 4 3 1 5 6 5 4 3 1
1 5. 1 - 1 5. 1 -
"""

# play(tiger_song)

flower_song = """
3 3 5 6 5 3 5 -
3 2 1 2 3 5 3 2
1 1 2 3 2 1 2 -
5. 5. 6. 1 3 2 1 -
"""
# play(flower_song)

ussr_song = """
1  2  3  4  5  6 
7  1  2  3  4  5 
6  7  1  2  3  4  5
1  2  3  4  5  6 
7  8  7  6  5  4 
3  2  1  2  3  4  5
"""


us_song = """
1  2  3  4  5  6 
7  8  7  6  5  4 
3  2  1  2  3  4  5
1  2  3  4  5  6 
7  1  2  3  4  5 
6  7  1  2  3  4  5
"""

# play(us_song)

china_song = """
1  2  3  4  5  1  2  3  4  5 
6  7  1  2  3  4  5
1  6  5  4  3  2  1  7  6  5 
4  3  2  1  7  6  5
"""

# play(china_song)

my_song = """
1'' 7' 1'' 3'' 7' -
6' 5' 6' 1'' 5' -
4' 3' 3' 1'' 7' 5'
6' 7' 1'' 3'' 2'' -
1'' 7' 1'' 3'' 7' 5'
6' 7' 1'' 2'' 3'' 3''
4'' 3'' 2'' 1'' 7' 3'' 5' 7'
6' - - -


"""

play(my_song)

import math
import sounddevice as sd

PI = 3.1415926535897

def f(x):
    return math.sin(x * 2 * PI) * .1

def data(fr, sr, d):
    length = int(sr * d)
    step = 1 / sr
    ret = []
    for i in range(length):
        ret.append(f(i * step * fr))
    return ret

# 音符频率
DO = 261.63
RE = 293.66
MI = 329.63
FA = 349.23
SO = 392.00
LA = 440.00
TI = 493.88

# 处理带装饰音的音符
def note_with_grace(main_note, grace_note, sr, grace_duration, main_duration):
    grace_part = data(grace_note, sr, grace_duration)
    main_part = data(main_note, sr, main_duration)
    return grace_part + main_part

# 乐谱中的音符和节拍（以含装饰音的音符为例）
notes = [
    (DO * 1.5, 0.5), (TI, 0.5), (MI, 0.5), (TI, 0.5),
    (SO, 0.5), (FA, 0.5), (MI, 0.5), (SO, 0.5),
    note_with_grace(RE, LA, 10240, 0.1, 0.4)
]

sound = []
sample_rate = 10240

# 生成音频数据
for item in notes:
    if isinstance(item, tuple):
        note, duration = item
        sound += data(note, sample_rate, duration)
    else:
        sound += item

print('playing')
sd.play(sound, sample_rate, blocking=True)

import numpy as np
import sounddevice as sd

PI = np.pi

def generate_tone(frequency, sample_rate, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(2 * PI * frequency * t) * .03
    return wave

# 定义五声音阶的频率
NOTES = {
    '1': 261.63,  # Do
    '2': 293.66,  # Re
    '3': 329.63,  # Mi
    '5': 392.00,  # Sol
    '6': 440.00   # La
}

# 定义《春江花月夜》的部分旋律
melody = [
    ('5', 0.5), ('6', 0.5), ('1', 1.0),
    ('2', 0.5), ('3', 0.5), ('5', 1.0),
    ('6', 0.5), ('1', 0.5), ('2', 1.0),
    ('3', 0.5), ('5', 0.5), ('6', 1.0)
]

sample_rate = 44100
sound = []

# 生成音频数据
for note, duration in melody:
    frequency = NOTES[note]
    sound += list(generate_tone(frequency, sample_rate, duration))

# 转换为numpy数组
sound = np.array(sound)

# 播放音频
print('playing')
sd.play(sound, sample_rate, blocking=True)

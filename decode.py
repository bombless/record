import librosa
import numpy as np
import matplotlib.pyplot as plt
from mido import Message, MidiFile, MidiTrack

# 从音频文件中加载数据
from simple_output import output
y = np.array(output, dtype=np.float32)
sr = 1e4

# 使用librosa检测音高
pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

# 提取音高
def extract_pitches(pitches, magnitudes):
    pitch_values = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitch_values.append(pitch)
    return pitch_values

pitch_values = extract_pitches(pitches, magnitudes)

# 将音高转换为MIDI音符
def pitch_to_midi(pitch):
    return int(librosa.hz_to_midi(pitch))

midi_notes = [pitch_to_midi(p) for p in pitch_values]

# 创建MIDI文件
midi = MidiFile()
track = MidiTrack()
midi.tracks.append(track)

# 添加MIDI消息
for note in midi_notes:
    track.append(Message('note_on', note=note, velocity=64, time=0))
    track.append(Message('note_off', note=note, velocity=64, time=480))

# 保存MIDI文件
midi.save('output.mid')

# 可视化音高
plt.figure(figsize=(10, 6))
plt.plot(pitch_values, marker='o', linestyle='None')
plt.xlabel('Time (frames)')
plt.ylabel('Pitch (Hz)')
plt.title('Pitch Tracking')
plt.show()

import mido
import pygame
import pygame.midi

# 初始化pygame和pygame.midi
pygame.init()
pygame.midi.init()

# 打开MIDI文件
midi_file = mido.MidiFile('sample.wav.mid')

# 初始化MIDI输出
midi_out = pygame.midi.Output(0)

# 播放MIDI文件
for message in midi_file.play():
    if not message.is_meta:
        # 将MIDI消息发送到MIDI输出设备
        print(len(message.bytes()))
        midi_out.write_short(*message.bytes())

# 关闭MIDI输出
midi_out.close()

# 退出pygame和pygame.midi
pygame.midi.quit()
pygame.quit()
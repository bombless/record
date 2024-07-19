import numpy as np
import sounddevice as sd


def sine_wave(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sin(2 * np.pi * freq * t)


def white_noise(duration, sample_rate=44100):
    return np.random.uniform(-1, 1, int(sample_rate * duration))


def apply_envelope(audio, attack=0.01, decay=0.1, sustain=0.8, release=0.1):
    total_samples = len(audio)
    attack_samples = int(attack * total_samples)
    decay_samples = int(decay * total_samples)
    sustain_samples = int(sustain * total_samples)
    release_samples = total_samples - attack_samples - decay_samples - sustain_samples

    envelope = np.concatenate([
        np.linspace(0, 1, attack_samples),
        np.linspace(1, sustain, decay_samples),
        np.ones(sustain_samples) * sustain,
        np.linspace(sustain, 0, release_samples)
    ])

    return audio * envelope


def bass_drum(duration=0.1, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    frequency = np.linspace(150, 50, len(t))
    wave = np.sin(2 * np.pi * frequency * t)
    return apply_envelope(wave, attack=0.01, decay=0.01, sustain=0.1, release=0.08)


def snare_drum(duration=0.1, sample_rate=44100):
    noise = white_noise(duration, sample_rate)
    wave = sine_wave(180, duration, sample_rate)
    snare = noise * 0.7 + wave * 0.3
    return apply_envelope(snare, attack=0.01, decay=0.05, sustain=0.1, release=0.04)


def hi_hat(duration=0.1, sample_rate=44100, open=False):
    noise = white_noise(duration, sample_rate)
    filtered_noise = np.clip(noise * 10, -1, 1)  # Amplify and clip for more "crisp" sound
    if open:
        return apply_envelope(filtered_noise, attack=0.01, decay=0.1, sustain=0.3, release=0.1)
    else:
        return apply_envelope(filtered_noise, attack=0.01, decay=0.05, sustain=0.1, release=0.04)


def crash(duration=0.5, sample_rate=44100):
    noise = white_noise(duration, sample_rate)
    filtered_noise = np.clip(noise * 5, -1, 1)
    return apply_envelope(filtered_noise, attack=0.01, decay=0.1, sustain=0.3, release=0.3)


def create_drum_pattern(pattern, sample_rate=44100):
    drum_pattern = np.zeros(int(sample_rate * len(pattern) * 0.25))
    for i, beat in enumerate(pattern):
        if beat == 'B':
            drum_pattern[int(i * 0.25 * sample_rate):] += bass_drum(0.25, sample_rate)
        elif beat == 'S':
            drum_pattern[int(i * 0.25 * sample_rate):] += snare_drum(0.25, sample_rate)
        elif beat == 'H':
            drum_pattern[int(i * 0.25 * sample_rate):] += hi_hat(0.25, sample_rate)
        elif beat == 'O':
            drum_pattern[int(i * 0.25 * sample_rate):] += hi_hat(0.25, sample_rate, open=True)
        elif beat == 'C':
            drum_pattern[int(i * 0.25 * sample_rate):] += crash(0.25, sample_rate)
    return drum_pattern


birthday_song = """
5 5 6 5 1' 7 -
5 5 6 5 2' 1' -
5 5 5' 3' 1' 7 6 -
4' 4' 3' 1' 2' 1' -
"""

DO = 261.63
RE = 293.66
MI = 329.63
FA = 349.23
SO = 392.00
LA = 440.00
SI = 493.88

notes = {'1': DO, '2': RE, '3': MI, '4': FA, '5': SO, '6': LA, '7': SI}


def create_chord(root_freq, duration, sample_rate=44100):
    root = sine_wave(root_freq, duration, sample_rate)
    third = sine_wave(root_freq * 1.25, duration, sample_rate)  # Major third
    fifth = sine_wave(root_freq * 1.5, duration, sample_rate)   # Perfect fifth
    return (root + third + fifth) / 3

def square_wave(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sign(np.sin(2 * np.pi * freq * t))
def create_rhythm(duration, sample_rate=44100):
    beat = np.concatenate([
        square_wave(440, 0.05, sample_rate) * 0.1,
        np.zeros(int(0.15 * sample_rate))
    ])
    num_beats = int(duration / 0.2)
    rhythm = np.tile(beat, num_beats)
    return rhythm[:int(duration * sample_rate)]
def play_note(note, duration, sample_rate=44100):
    if note == '-':
        return np.zeros(int(duration * sample_rate))

    freq = notes[note[0]]
    if "'" in note:
        freq *= 2 ** (note.count("'"))
    elif "." in note:
        freq /= 2 ** (note.count("."))

    melody = sine_wave(freq, duration, sample_rate)
    melody = apply_envelope(melody)

    chord = create_chord(freq/2, duration, sample_rate)
    rhythm = create_rhythm(duration, sample_rate)

    # 添加鼓声
    drum_pattern = 'B H S H B H S H'
    drums = create_drum_pattern(drum_pattern, sample_rate)
    drums = drums[:len(melody)]  # 确保鼓声长度与旋律相同

    return (melody * 0.4 + chord * 0.3 + rhythm * 0.1 + drums * 0.2) * 0.3


def play_song(song):
    audio = np.array([])
    for line in song.strip().split('\n'):
        for note in line.split():
            audio = np.concatenate([audio, play_note(note, 1)])
            audio = np.concatenate([audio, np.zeros(int(0.05 * 44100))])  # Short pause between notes

    sd.play(audio, 44100)
    sd.wait()

# birthday_song 和 play_song 函数保持不变...

play_song(birthday_song)
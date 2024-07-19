import numpy as np
import sounddevice as sd

# 保留之前所有的函数定义...

DO = 261.63
RE = 293.66
MI = 329.63
FA = 349.23
SO = 392.00
LA = 440.00
SI = 493.88

notes = {'1': DO, '2': RE, '3': MI, '4': FA, '5': SO, '6': LA, '7': SI}


def frequency(note):
    if note == '-':
        return None
    base = notes[note[0]]
    if "'" in note:
        return base * (2 ** note.count("'"))
    elif "." in note:
        return base / (2 ** note.count("."))
    return base


def sine_wave(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sin(2 * np.pi * freq * t)

def square_wave(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sign(np.sin(2 * np.pi * freq * t))


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

def white_noise(duration, sample_rate=44100):
    return np.random.uniform(-1, 1, int(sample_rate * duration))
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

def apply_envelope(audio, attack=0.01, decay=0.1, sustain=0.8, release=0.1):
    total_samples = len(audio)
    attack_samples = int(attack * total_samples)
    decay_samples = int(decay * total_samples)
    sustain_samples = int(sustain * total_samples)
    release_samples = total_samples - attack_samples - decay_samples - sustain_samples

    envelope = np.concatenate([
        np.linspace(0, 1, attack_samples),
        np.linspace(1, 0.7, decay_samples),
        np.ones(sustain_samples) * 0.7,
        np.linspace(0.7, 0, release_samples)
    ])

    return audio * envelope


def create_chord(root_freq, duration, sample_rate=44100):
    root = sine_wave(root_freq, duration, sample_rate)
    third = sine_wave(root_freq * 1.25, duration, sample_rate)  # Major third
    fifth = sine_wave(root_freq * 1.5, duration, sample_rate)  # Perfect fifth
    return (root + third + fifth) / 3

def create_rhythm(duration, sample_rate=44100):
    beat = np.concatenate([
        square_wave(440, 0.05, sample_rate) * 0.1,
        np.zeros(int(0.15 * sample_rate))
    ])
    num_beats = int(duration / 0.2)
    return np.tile(beat, num_beats)[:int(duration * sample_rate)]

def play_note(note, duration, sample_rate=44100):
    if note == '-':
        return np.zeros(int(duration * sample_rate))

    freq = frequency(note)
    if freq is None:
        return np.zeros(int(duration * sample_rate))

    melody = sine_wave(freq, duration, sample_rate)
    melody = apply_envelope(melody)

    chord = create_chord(freq / 2, duration, sample_rate)
    rhythm = create_rhythm(duration, sample_rate)

    # Ensure all components have the same length
    min_length = min(len(melody), len(chord), len(rhythm))
    melody = melody[:min_length]
    chord = chord[:min_length]
    rhythm = rhythm[:min_length]

    drum_pattern = 'B H S H B H S H'
    drums = create_drum_pattern(drum_pattern, sample_rate)[:min_length]

    return (melody * 0.4 + chord * 0.3 + rhythm * 0.1 + drums * 0.2) * 0.3


twinkle_star = [
    ('1', 0.5), ('1', 0.5), ('5', 0.5), ('5', 0.5), ('6', 0.5), ('6', 0.5), ('5', 1.0),
    ('4', 0.5), ('4', 0.5), ('3', 0.5), ('3', 0.5), ('2', 0.5), ('2', 0.5), ('1', 1.0),
    ('5', 0.5), ('5', 0.5), ('4', 0.5), ('4', 0.5), ('3', 0.5), ('3', 0.5), ('2', 1.0),
    ('5', 0.5), ('5', 0.5), ('4', 0.5), ('4', 0.5), ('3', 0.5), ('3', 0.5), ('2', 1.0),
    ('1', 0.5), ('1', 0.5), ('5', 0.5), ('5', 0.5), ('6', 0.5), ('6', 0.5), ('5', 1.0),
    ('4', 0.5), ('4', 0.5), ('3', 0.5), ('3', 0.5), ('2', 0.5), ('2', 0.5), ('1', 1.0),
]


def play_song(song):
    audio = np.array([])
    for note, duration in song:
        note_audio = play_note(note, duration)
        audio = np.concatenate([audio, note_audio])
        audio = np.concatenate([audio, np.zeros(int(0.01 * 44100))])  # Very short pause between notes

    sd.play(audio, 44100)
    sd.wait()


play_song(twinkle_star)
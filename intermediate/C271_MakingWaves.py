# Author: Reddit user "bearific"
# Downloaded as a proof of concept
# Modified to work on Python 2

import winsound
import struct
import math
import wave

volume = 32767
note_duration = 1.5
sample_rate = 8000
result = wave.open('data/wave.wav', 'w')
result.setparams((2, 2, sample_rate, 0, 'NONE', 'no compression'))

freqs = {'A': 440.0, 'B': 493.88, 'C': 523.25, 'D': 587.33, 'E': 659.25, 'F': 698.46, 'G': 783.99, '_': 0}

notes = 'C__DE__CEECCEE__D__EFFEDFFFF____E__FG__EGGEEGG__F'
values = []
freq = 0
for i in range(0, int(note_duration * len(notes) * sample_rate)):
    if i % (int(note_duration * len(notes) * sample_rate) // len(notes)) == 0:
        freq = freqs[notes[i // (int(note_duration * len(notes) * sample_rate) // len(notes))]]
    value = int(volume * math.cos(freq * math.pi * i / sample_rate))
    packed_value = struct.pack('<h', value)
    values.append(packed_value)
    values.append(packed_value)

result.writeframes(b''.join(values))
result.close()

winsound.PlaySound('data/wave.wav', winsound.SND_FILENAME)

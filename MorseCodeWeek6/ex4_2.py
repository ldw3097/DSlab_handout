import math
import struct

import pyaudio

FREQ_START = 512
FREQ_STEP = 128
HEX_LIST = ['0', '1', '2', '3', '4',
            '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E',
            'F']
HEX = set(HEX_LIST)

rules = {}
print('Frequency Rules:')
rules['START'] = FREQ_START
for i in range(len(HEX_LIST)):
    h = HEX_LIST[i]
    rules[h] = FREQ_START + FREQ_STEP + FREQ_STEP*(i+1)
rules['END'] = FREQ_START + FREQ_STEP + FREQ_STEP*(len(HEX_LIST)) + FREQ_STEP*2

for k, v in rules.items():
    print(f'{k}: {v}')



SHORTMAX = 2 ** (16 - 1) - 1
channels = 1
unit = 0.1
samplerate = 48000

text = '엄'
string_hex = text.encode('utf-8').hex().upper()

audio = []
for i in range(int(unit * samplerate * 2)):
    audio.append(SHORTMAX * math.sin(2 * math.pi * rules['START'] * i / samplerate))
for s in string_hex:
    for i in range(int(unit * samplerate * 1)):
        audio.append(SHORTMAX * math.sin(2 * math.pi * rules[s] * i / samplerate))
for i in range(int(unit * samplerate * 2)):
    audio.append(SHORTMAX * math.sin(2 * math.pi * rules['END'] * i / samplerate))

import wave

with wave.open("activity4.wav", 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(48000)
    for a in audio:
        w.writeframes(struct.pack('<h', int(a)))


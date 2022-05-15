import wave
import struct

import scipy.fftpack
import numpy as np

unit = 0.1
samplerate = 48000
padding = 5

filename = 'activity4.wav'

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

print('Raw hex:')
text = ''
with wave.open(filename, 'rb') as w:
    framerate = w.getframerate()
    frames = w.getnframes()
    audio = []
    for i in range(frames):
        frame = w.readframes(1)
        d = struct.unpack('<h', frame)[0]
        audio.append(d)
        if len(audio) >= unit * framerate:
            freq = scipy.fftpack.fftfreq(len(audio))
            fourier = scipy.fftpack.fft(audio)
            top = freq[np.argmax(abs(fourier))] * samplerate

            data = ''
            for k, v in rules.items():
                if v - padding <= top and top <= v + padding:
                    data = k

            if data == 'END':
                print()
                print(data, end='')
            if data != 'START' and data != 'END':
                text = f'{text}{data}'
                print(data, end='')
            if data == 'START':
                print(data)

            audio.clear()
    print()

print(f'Decoded: {bytes.fromhex(text).decode("utf-8")}')

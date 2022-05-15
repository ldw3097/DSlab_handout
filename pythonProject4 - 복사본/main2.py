import math
import struct
import wave

import numpy as np
import scipy.fftpack
import matplotlib.pyplot as plt

DATA_LEN = 12
RSC_LEN = 4
SHORTMAX = 2**(16-1)-1
UNIT = 0.1
SAMPLERATE = 48000
padding = 5

FREQ_START = 512
FREQ_STEP = 128
HEX_LIST = ['0', '1', '2', '3', '4',
            '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E',
            'F']
HEX = set(HEX_LIST)

rules = {}
rules['START'] = FREQ_START
for i in range(len(HEX_LIST)):
    h = HEX_LIST[i]
    rules[h] = FREQ_START + FREQ_STEP + FREQ_STEP*(i+1)
rules['END'] = FREQ_START + FREQ_STEP + FREQ_STEP*(len(HEX_LIST)) + FREQ_STEP*2




print('Raw hex:')
text = ''
isfirst = False
isstarted = False
with wave.open('201802123-p3.wav', 'rb') as w:
    framerate = w.getframerate()
    frames = w.getnframes()
    audio = []
    for i in range(frames):
        frame = w.readframes(1)
        d = struct.unpack('<h', frame)[0]
        audio.append(d)

        if len(audio) >= UNIT * framerate:
            if (isfirst):
                plt.plot(audio)
                plt.show()
            freq = scipy.fftpack.fftfreq(len(audio))
            fourier = scipy.fftpack.fft(audio)
            top = freq[np.argmax(abs(fourier))] * SAMPLERATE
            if(isfirst):
                print(top)

            data = ''
            for k, v in rules.items():
                if v - padding <= top and top <= v + padding:
                    data = k

            if data == 'END':
                print()
                print(data, end='')
                break
            if data != 'START' and data != 'END' and isstarted:
                text = f'{text}{data}'
                print(data, end='')
                isfirst = False
            if data == 'START':
                isstarted = True
                isfirst = True
                print(data)


            audio.clear()
    print()







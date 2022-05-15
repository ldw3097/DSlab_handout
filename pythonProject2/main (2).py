import sys
import math
import wave
import struct
import statistics
INTMAX = 2 ** (32 - 1) - 1
'''

t = 1.0
fs = 48000
f = 261.626  # C4
audio = []
for i in range(int(t * fs)):
    audio.append(int(INTMAX * math.sin(2 * math.pi * f * (i / fs))))
filename = 't.wav'
with wave.open(filename, 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(4)
    w.setframerate(48000)
    for a in audio:
        w.writeframes(struct.pack('<l', a))
        
'''

english = {'A': '.-', 'B': '-...', 'C': '-.-.',
           'D': '-..', 'E': '.', 'F': '..-.',
           'G': '--.', 'H': '....', 'I': '..',
           'J': '.---', 'K': '-.-', 'L': '.-..',
           'M': '--', 'N': '-.', 'O': '---',
           'P': '.--.', 'Q': '--.-', 'R': '.-.',
           'S': '...', 'T': '-', 'U': '..-',
           'V': '...-', 'W': '.--', 'X': '-..-_',
           'Y': '-.--', 'Z': '--..'}

number = {'1': '.----', '2': '..---', '3': '...--',
          '4': '....-', '5': '.....', '6': '-....',
          '7': '--...', '8': '---..', '9': '----.',
          '0': '-----'}

englishR = {v: k for k,v in english.items()}
allR = {v: k for k, v in number.items()}
allR.update(englishR)
allR.update({'/': ' '})
allS = {v: k for k,v in allR.items()}


def text2morse(text):
    text = text.upper()
    morse = ''
    for t in text:
        for key, value in allS.items():
            if t == key:
                morse = morse + value + ' '
                break
    return morse


# print(text2morse('hel lo3'))


def morse2audio(morse):
    t = 0.1
    fs = 48000
    f = 523.251
    audio = []
    for m in morse:
        if m == '.':
            for i in range(int(t * fs * 1)):
                audio.append(int(INTMAX * math.sin(2 * math.pi * f * (i / fs))))
        elif m == '-':
            for i in range(int(t * fs * 3)):
                audio.append(int(INTMAX * math.sin(2 * math.pi * f * (i / fs))))
        elif m == ' ':
            for i in range(int(t * fs * 1)):
                audio.append(int(0))
        elif m == '/':
            for i in range(int(t * fs * 1)):
                audio.append(int(0))
        for i in range(int(t * fs * 1)):
            audio.append(int(0))
    return audio


def audio2file(audio, filename):
    with wave.open(filename, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(4)
        w.setframerate(48000)
        for a in audio:
            w.writeframes(struct.pack('<l', a))


audio2file(morse2audio(text2morse('YEAR 5482 ELECTION 4014 CHAPTER 5920 201802123')), 'hw2.wav')


def file2morse(filename):
    with wave.open(filename, 'rb') as w:
        audio = []
        framerate = w.getframerate()
        frames = w.getnframes()
        for i in range(frames):
            frame = w.readframes(1)
            audio.append(struct.unpack('<i', frame)[0])
        morse = ''
        unit = int(0.1 * framerate)
        for i in range(1, math.ceil(len(audio)/unit)+1):
            stdev = statistics.stdev(audio[(i-1)*unit:i*unit])
            if stdev > 10000:
                morse = morse + '.'
            else:
                morse = morse + ' '
        morse = morse.replace('... ', '-')
        morse = morse.replace('. ', '.')
        morse = morse.replace('  ', ' ')
        morse = morse.replace('   ', ' / ')

    return morse


def morse2text(morse):
    text = ''
    arr = morse.split()
    for a in arr:
        for key, value in allR.items():
            if a == key:
                text = text + value
                break
    return text





# print(text2morse('helloworld'))
# audio2file(morse2audio(text2morse('helloworld')), 'helloworld.wav' )

# print(morse2text(file2morse('201802123.wav')))

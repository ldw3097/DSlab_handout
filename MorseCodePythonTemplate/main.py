import os
import sys
import re
import math
import wave
import struct
import statistics
import time

import pyaudio

import morsecode

FLAGS = _ = None
DEBUG = False
CHANNELS = 1
SAMPLERATE = 48000
FREQUENCY = 523.251
UNIT = 0.1
SHORTMAX = 2**(16-1)-1
MORSE_THRESHOLD = SHORTMAX // 18
UNSEEN_THRESHOLD = 3.0


def text2morse(text):
    text = text.upper()
    morse = ''
    for t in text:
        for key, value in morsecode.code.items():
            if t == key:
                morse = morse + value + ' '
                break
    return morse



def morse2audio(morse):
    audio = []
    for m in morse:
        if m == '.':
            for i in range(round(UNIT * SAMPLERATE * 1)):
                audio.append(int(SHORTMAX * math.sin(2 * math.pi * FREQUENCY * i / SAMPLERATE)))
        elif m == '-':
            for i in range(round(UNIT * SAMPLERATE * 3)):
                audio.append(int(SHORTMAX * math.sin(2 * math.pi * FREQUENCY * i / SAMPLERATE)))
        elif m == ' ':
            for i in range(round(UNIT * SAMPLERATE * 1)):
                audio.append(int(0))
        elif m == '/':
            for i in range(round(UNIT * SAMPLERATE * 1)):
                audio.append(int(0))
        for i in range(round(UNIT * SAMPLERATE * 1)):
            audio.append(int(0))
    return audio


def play_audio(audio):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=SAMPLERATE,
                    frames_per_buffer=SAMPLERATE,
                    output=True)

    for a in audio:
        stream.write(struct.pack('<h', a))

    time.sleep(0.5/UNIT) # Wait for play

    stream.stop_stream()
    stream.close()
    p.terminate()


def send_data():
    while True:
        print('Type some text (only English)')
        text = input('User input: ').strip()
        if re.match(r'[A-Za-z0-9 ]+', text):
            break
    morse = text2morse(text)
    print(f'MorseCode: {morse}')
    audio = morse2audio(morse)
    print(f'AudioSize: {len(audio)}')
    play_audio(audio)


def record_audio():
    unit_size = math.ceil(SAMPLERATE*UNIT)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=SAMPLERATE,
                    frames_per_buffer=SAMPLERATE,
                    input=True)
    morse = ''
    while True:
        data = stream.read(unit_size)
        for i in range(0, len(data), 2):
            d = struct.unpack('<h', data[i:i+2])[0]
            if abs(d) > MORSE_THRESHOLD:
                print(i)
                stream.read(i)
                morse+= '.'
                endcounter = 0
                while endcounter < 30:
                    data = stream.read(unit_size)
                    broke = False
                    for j in range(4800-100, 4800+100, 2):
                        apnd = struct.unpack('<h', data[j:j+2])[0]
                        if abs(apnd) > MORSE_THRESHOLD:
                            morse+= '.'
                            endcounter = 0
                            broke = True
                            break
                    if not broke :
                        morse += ' '
                        endcounter += 1

        if len(morse) != 0:
            print(f'RawMorse: {morse}')
            stream.stop_stream()
            stream.close()
            p.terminate()
            break
    morse = morse.replace('... ', '-')
    morse = morse.replace('. ', '.')
    morse = morse.replace('  ', ' ')
    morse = morse.replace('   ', ' / ')

    return morse


def morse2text(morse):
    text = ''
    arr = morse.split()
    for a in arr:
        for key, value in morsecode.code.items():
            if a == value:
                text = text + key
                break
    return text


def receive_data():
    morse = record_audio()
    print(f'Morse: {morse}')
    text = morse2text(morse)
    print(f'Sound input: {text}')


def main():
    while True:
        print('Morse Code Data Communication 2022')
        print('[1] Send data over sound (play)')
        print('[2] Receive data over sound (record)')
        print('[q] Exit')
        select = input('Select menu: ').strip().upper()
        if select == '1':
            send_data()
        elif select == '2':
            receive_data()
        elif select == 'Q':
            print('Terminating...')
            break


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                         help='The present debug message')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()


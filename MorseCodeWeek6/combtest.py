import pyaudio
import math
import struct
import time

SHORTMAX = 2 ** (16 - 1) - 1
channels = 1
length = 5.0
samplerate = 48000
frequencies = [261.625, 523.251, 1046.502]  # C4, C5, C6
volumes = [0.3, 0.75, 0.5]
waves = []

for frequency, volume in zip(frequencies, volumes):
    audio = []
    for i in range(int(length * samplerate)):
        audio.append(volume * SHORTMAX * math.sin(2 * math.pi * frequency * i / samplerate))
    waves.append(audio)

track = [0] * int(length * samplerate)
for i in range(len(track)):
    for w, v in zip(waves, volumes):
        track[i] = track[i] + w[i]
    track[i] = track[i] / len(waves)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=channels,
                rate=samplerate,
                frames_per_buffer=samplerate,
                output=True)

for t in track:
    stream.write(struct.pack('<h', int(t)))

stream.stop_stream()
stream.close()
p.terminate()

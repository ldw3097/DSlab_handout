import math

import reedsolo

DATA_LEN = 12
RSC_LEN = 4
SHORTMAX = 2**(16-1)-1
UNIT = 0.1
SAMPLERATE = 48000

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

text = '🧡💛💚💙💜'
byte_hex = text.encode('utf-8')
string_hex = byte_hex.hex().upper()

audio = []
for i in range(int(UNIT*SAMPLERATE*2)):
    audio.append(SHORTMAX*math.sin(2*math.pi*rules['START']*i/SAMPLERATE))

client_rsc = reedsolo.RSCodec(RSC_LEN)
for k in range(0, len(byte_hex), DATA_LEN):
    data = byte_hex[k:k+DATA_LEN]
    encoded_data = client_rsc.encode(data).hex().upper()
    print(f'encoded_data: {encoded_data}')
    for s in encoded_data:
        for i in range(int(UNIT*SAMPLERATE*1)):
            audio.append(SHORTMAX*math.sin(2*math.pi*rules[s]*i/SAMPLERATE))

for i in range(int(UNIT*SAMPLERATE*2)):
    audio.append(SHORTMAX*math.sin(2*math.pi*rules['END']*i/SAMPLERATE))

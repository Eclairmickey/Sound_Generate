import pyaudio
import numpy as np
import array
import math
import matplotlib.pyplot as plt

CHUNK=4096
RATE=44100 #サンプリング周波数

def triangle(freq,sec,velocity,rate):
    def gen():
        n=int(rate*sec)
        for i in range(n):
           yield sum([math.sin(2.0 * math.pi * i /rate * freq * (2 * j - 1)) * (velocity / (2 * j - 1)) for j in range(10)])
    return array.array('f',gen()).tostring()

#半音上がるときの周波数割合
#2^(1/12)
r_semitone=math.pow(2,1.0/12)

#12+1音階の周波数
scale_hz=[261.625]
for _ in range(12):
    scale_hz.append(scale_hz[-1]*r_semitone)

p=pyaudio.PyAudio()
stream_out=p.open(
    format=pyaudio.paFloat32,
    channels=1,
    rate=RATE,
    frames_per_buffer=CHUNK,
    input=True,
    output=True
)

for i in [0,2,4,5,7,9,11,12]:
    stream_out.write(triangle(scale_hz[i],1,0.5,RATE))

stream_out.close()
p.terminate()
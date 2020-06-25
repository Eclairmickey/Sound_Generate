import pyaudio
import numpy as np
import math
import matplotlib.pyplot as plt

CHUNK=4096
RATE=44100 #サンプリング周波数
def plot(function):
    plt.plot(function)
    plt.show()

def tone(freq,length,gain):
    """
    定常波を作成
    freq:周波数[Hz]
    length:長さ[s]
    gain:振幅の大きさ
    """
    t=np.arange(int(length*RATE))/RATE
    return np.sin(t*float(freq)*np.pi*2)*gain

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
"""
全音階
0,1,2,3,4,5,6,7,8,9,10,11,12
C,C#,G,G#,E,F,F#,G,G#,A,A#H,C
"""
#C,D,A,F,G,A,H,C
for i in [0,2,4,5,7,9,11,12]:
    sound=tone(scale_hz[i],0.5,1.0).astype(np.float32).tostring()
    stream_out.write(sound)

stream_out.close()
p.terminate()



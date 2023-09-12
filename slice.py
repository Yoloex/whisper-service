import librosa
import glob
import os
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from librosa import display

for file in glob.glob('*.wav'):
    os.system(f'del {file}')

n_fft = 1024
wave, sr = librosa.load('test/test1.wav')
wave_16 = librosa.resample(wave, orig_sr=sr, target_sr=16000)

segments = librosa.effects.split(wave_16, top_db=13, frame_length=12800, hop_length=1200, ref=np.max)

for i, segment in enumerate(segments):
    sf.write(f'{i}.wav', wave_16[segment[0]:segment[1]], 16000)
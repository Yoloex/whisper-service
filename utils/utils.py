import librosa
import numpy as np
import soundfile as sf
import time
import io
from inference import generate_transcription

def transcribe(input: str):
    wave, sr = librosa.load(input)
    wave_16 = librosa.resample(wave, orig_sr=sr, target_sr=16000)
    segments = librosa.effects.split(wave_16, top_db=13, frame_length=12800, hop_length=1200, ref=np.max)
    duration = generate_transcription([wave_16[segment[0]:segment[1]] for segment in segments])

def save_audio(id: str, data: bytes):
    """
    Save input bytes data as an audio.
    """
    now = time.strftime('%Y%m%d%H%M%S')
    wave, sr = sf.read(io.BytesIO(data), dtype='float32')
    sf.write(f'{id}_{now}.wav', wave, samplerate=sr)
    
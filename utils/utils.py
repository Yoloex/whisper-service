import librosa
import numpy as np
import soundfile as sf
import time
import io
import os
import whisper
import torch

def transcribe(input: str, model):
    wave, sr = librosa.load(input)
    wave_16 = librosa.resample(wave, orig_sr=sr, target_sr=16000)
    segments = librosa.effects.split(wave_16, top_db=13, frame_length=12800, hop_length=1200, ref=np.max)
    duration, text = generate_transcription([wave_16[segment[0]:segment[1]] for segment in segments], model)
    
    return duration, text

def save_audio(groupid: str, id: str, data: bytes):
    """
    Save input bytes data as an audio.
    Input:
        id: Identifier of the sender
        data: Audio bytes data
    Returns:
        str: Saved file name
    """
    now = time.strftime('%Y%m%d%H%M%S')
    wave, sr = sf.read(io.BytesIO(data), dtype='float32')
    filename = f'temp/{groupid.zfill(2)}_{id}_{now}.wav'
    sf.write(filename, wave, samplerate=sr)
    
    return filename

batchsize = 8

def generate_transcription(inputs, model):
    """   Transcription generation function
        inputs: numpy array, a list of audio waveforms
        model: Whisper model
    """

    # Whisper only accpets 30s-long file 
    # For that, padding and cutting is done on wave segment.
    mel_spects = []
    for input in inputs:
        input = whisper.pad_or_trim(input)
        mel = whisper.log_mel_spectrogram(audio=input).to(model.device)
        mel_spects.append(mel)

    options = whisper.DecodingOptions(fp16=False)

    inputs = torch.stack(mel_spects)
    
    results = []
    start = time.time()

    for i in range(0, len(mel_spects), batchsize):

        inference = whisper.decode(model, inputs[i : i + batchsize], options=options)
        results.append("\n".join([infer.text for infer in inference]))
    
    end = time.time()

    return end - start, "\n".join([result for result in results])

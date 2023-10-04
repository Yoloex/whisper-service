import librosa
import numpy as np
import soundfile as sf
import time
import io
import whisper
import torch
import yaml

with open('cfg/server.yaml') as f:
    server_cfg = yaml.safe_load(f.read())
    config = server_cfg['preprocessing']

def transcribe(input: str, model):
    wave, sr = librosa.load('temp/' + input)
    wave_16 = librosa.resample(wave, orig_sr=sr, target_sr=config['resampling_rate'])
    segments = librosa.effects.split(wave_16, top_db=config['silence_top_db'], frame_length=config['frame_length'], hop_length=config['hop_length'], ref=np.max)
    
    success = True
    
    try:
        duration, text = generate_transcription([wave_16[segment[0]:segment[1]] for segment in segments], model)
    except:
        success = False
    
    if success:
        return duration, text
    else:
        return 0, ''

def save_audio(groupid: str, id: str, data: bytes):
    """
    Save input bytes data as an audio.
    Input:
        id: Identifier of the sender
        data: Audio bytes data
    Returns:
        str: Saved file name
    """
    timestamp = time.strftime('%Y%m%d%H%M%S')
    wave, sr = sf.read(io.BytesIO(data), dtype='float32')
    filename = f'{groupid.zfill(2)}_{id}_{timestamp}.wav'
    sf.write('temp/' + filename, wave, samplerate=sr)
    
    return filename

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

    options = whisper.DecodingOptions(fp16=config['float16_decode'])
    batchsize = config['batchsize']

    inputs = torch.stack(mel_spects)
    
    results = []
    start = time.time()

    for i in range(0, len(mel_spects), batchsize):

        inference = whisper.decode(model, inputs[i : i + batchsize], options=options)
        results.append("\n".join([infer.text for infer in inference]))
    
    end = time.time()

    return end - start, "\n".join([result for result in results])

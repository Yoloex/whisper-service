import whisper
import time
import torch
from whisper import load_audio

print("Loading model ...")

model = whisper.load_model("medium")
batchsize = 8

print("Model loaded.")

def generate_transcription(inputs):
    """   Transcription generation function
        inputs: numpy arry, a list of audio waveforms
    """
    print('number of segments', len(inputs))
    mel_spects = []
    for input in inputs:
        input = whisper.pad_or_trim(input)
        mel = whisper.log_mel_spectrogram(audio=input).to(model.device)
        mel_spects.append(mel)

    # mel_spects = mel_spects + [torch.zeros(size=mel_spects[0].shape).to(model.device)] * (len(mel_spects) % batchsize)

    options = whisper.DecodingOptions()

    inputs = torch.stack(mel_spects)
    
    results = []
    start = time.time()

    for i in range(0, len(mel_spects), batchsize):
        inference = whisper.decode(model, inputs[i : i + batchsize], options=options)
        results.append("\n".join([infer.text for infer in inference]))
    end = time.time()

    print("\n".join([result for result in results]))

    return end - start

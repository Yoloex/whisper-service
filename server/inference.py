import whisper
import time
import torch

print("Loading model ...")

model = whisper.load_model("base")

print("Model loaded.")

def generate_transcription(inputs):
    """   Transcription generation function
        nputs: numpy arry, a list of audio waveforms
    """
    mel_spects = []
    for input in inputs:
        input = whisper.pad_or_trim(input)
        mel = whisper.log_mel_spectrogram(audio=input).to(model.device)
        mel_spects.append(mel)

    options = whisper.DecodingOptions()

    inputs = torch.stack(mel_spects)
    
    start = time.time()
    results = whisper.decode(model, inputs, options=options)
    end = time.time()

    print('Calculation time: ', end - start)
    print("\n".join([result.text for result in results]))

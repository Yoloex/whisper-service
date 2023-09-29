import whisper
import time
import torch

print("Loading model ...")

model = whisper.load_model("base")
batchsize = 8

print("Model loaded.")

def generate_transcription(inputs):
    """   Transcription generation function
        inputs: numpy array, a list of audio waveforms
    """
    print('number of segments', len(inputs))
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

    print("\n".join([result for result in results]))

    return end - start

import whisper
import time
import torch

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

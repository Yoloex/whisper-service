import whisper
import time
import torch
import glob

print("Loading model ...")

model = whisper.load_model("base")

print("Model loaded.")

file_list = glob.glob('test/*.m4a')
files = []

for file in file_list:
    input = whisper.load_audio(file)
    files.append(input)

max_length = max([file.shape[0] for file in files])

mel_spects = []

for file in files:
    input = whisper.pad_or_trim(file, length=max_length)
    mel = whisper.log_mel_spectrogram(audio=input).to(model.device)
    mel_spects.append(mel)

options = whisper.DecodingOptions()

start = time.time()

inputs = torch.stack(mel_spects)
results = whisper.decode(model, inputs, options=options)
# results = whisper.transcribe(model=model, audio=inputs)
end = time.time()

print('Calculation time: ', end - start)
print("\n".join([result.text for result in results]))
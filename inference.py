import whisper
import time
import torch
import glob

print("Loading model ...")

model = whisper.load_model("base")

print("Model loaded.")

# file_list = glob.glob('')

input = whisper.load_audio("test/test1.m4a")
# input = whisper.pad_or_trim(input)
mel = whisper.log_mel_spectrogram(input).to(model.device)

mel = torch.unsqueeze(mel, dim=0)

options = whisper.DecodingOptions()

start = time.time()
results = whisper.decode(model, torch.concat([mel] * 16, dim=0), options=options)
# results = whisper.transcribe(model=model, audio=torch.concat([mel] * 16, dim=0))
end = time.time()

print('Calculation time: ', end - start)
print("\n".join([result.text for result in results]))
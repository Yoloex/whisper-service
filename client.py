import requests
import soundfile as sf
import io

url = 'http://localhost:5000/generate'

with open('test/Recording.wav', 'rb') as f_mp3:
    byte_data = f_mp3.read()
    # data, samplerate = sf.read(io.BytesIO(byte_data))
    # print(data)
    # print('sample rate', samplerate)
    result = requests.post(url, data=byte_data)
    
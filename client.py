import requests

url = 'http://localhost:5000/generate'

with open('test/sample.wav', 'rb') as f_mp3:
    byte_data = f_mp3.read()
    response = requests.post(url, data=byte_data)
    result = response.json()
    print(result['duration'])
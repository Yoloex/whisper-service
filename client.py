import os
import requests
from bitstring import BitArray

url = 'http://localhost:5000/generate'

with open(r'test/output.mp3', 'rb') as f_mp3:
    mp3 = f_mp3.read()
    binary = BitArray(bytes=mp3)
    result = requests.post(url, data={'inputs': binary})
    
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

url = 'http://172.20.3.1:5000/generate'

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

with open('test/sample.wav', 'rb') as f_mp3:
    byte_data = f_mp3.read()
    for i in range(12):
        session.post(url, data=byte_data)
        print(f'{i+1} request submitted')
        time.sleep(1)
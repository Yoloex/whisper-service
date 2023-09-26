import io
import numpy as np
import soundfile as sf
import librosa
from flask import Flask, request, jsonify
from inference import generate_transcription

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return jsonify({
        'status': 'loaded'
    })

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        data = request.get_data()
        wave, sr = sf.read(io.BytesIO(data), dtype='float32')

        wave_16 = librosa.resample(wave, orig_sr=sr, target_sr=16000)
        segments = librosa.effects.split(wave_16, top_db=13, frame_length=12800, hop_length=1200, ref=np.max)
        duration = generate_transcription([wave_16[segment[0]:segment[1]] for segment in segments])

        return jsonify({'status': 'accpeted', 'duration': f'{duration}'})

if __name__ == '__main__':
    app.run(port=5005, debug=True)
    print('Server 5 is listening on 5005 ...')
from flask import Flask, request, jsonify
from utils.utils import save_audio, transcribe
from threading import Thread, get_native_id
import queue
import whisper

app = Flask(__name__)
filelist = queue.Queue()

class TranscribeThread(Thread):

    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        print('Loading model ...')

        model = whisper.load_model("base")

        print('Model loaded')

        while True:
            print(f'{get_native_id()} is waiting ...')

            file = filelist.get()

            print(f'{get_native_id()} is processing {file}')
            duration, text = transcribe(file, model)
            
            print(f'{get_native_id()} finished processing {file} in {duration}s')

@app.route('/generate', methods=['POST'])
def generate():
    global filelist

    if request.method == 'POST':
        print('Accepted')
        
        data = request.get_data()
        saved_file = save_audio('JHS', data)

        filelist.put(saved_file)

    return jsonify({'status': 'accepted'})

if __name__ == '__main__':
    threads = []
    thread_num = 4
    for i in range(thread_num):
        newthread = TranscribeThread()
        newthread.start()
        threads.append(newthread)
    
    print('Server is listening on 5000 ...')
    app.run(port=5000, threaded=True)
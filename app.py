import queue
import whisper
import mysql.connector
from flask import Flask, request, jsonify
from utils.utils import save_audio, transcribe
from threading import Thread, get_native_id

app = Flask(__name__)
filelist = queue.Queue()
results = queue.Queue()

class TranscribeThread(Thread):

    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        print('Loading model ...')

        model = whisper.load_model("base")

        print('Model loaded')

        while True:
            file = filelist.get()

            print(f'{get_native_id()} is processing {file}')
            duration, text = transcribe(file, model)
            results.put([file, text])
            
            print(f'{get_native_id()} finished processing {file} in {duration}s')

class DatabaseThread(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        db = mysql.connector.connect(host='localhost', user='root', password='notouch1234!@#$')
        cursor = db.cursor()

        cursor.execute('USE test;')

        print([x for x in cursor])

        while True:
            result = results.get()
            sql = """INSERT INTO calldata (idx, groupid, id, dateid, timeid, content)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (None, result[0][:2], result[0][3:6], result[0][7:15], result[0][15:21], result[1]))
            db.commit()

            print(f'{result[0]} saved successfully')

@app.route('/generate', methods=['POST'])
def generate():

    if request.method == 'POST':
        print('Accepted')
        
        data = request.get_data()
        saved_file = save_audio('1', 'JHS', data)

        filelist.put(saved_file)

    return jsonify({'status': 'accepted'})

if __name__ == '__main__':
    dbthread = DatabaseThread()
    threads = []
    thread_num = 2
    
    for i in range(thread_num):
        newthread = TranscribeThread()
        newthread.start()
        threads.append(newthread)
    
    dbthread.start()

    print('Server is listening on 5000 ...')
    app.run(port=5000, threaded=True)
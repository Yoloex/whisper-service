import whisper
import mysql.connector
import logging
import yaml
import queue
import time
import glob
import os
from threading import Thread
from flask import Flask, request, jsonify
from utils.utils import save_audio, transcribe

with open('cfg/log.yaml') as f:
    log_cfg = yaml.safe_load(f.read())
    logging.config.dictConfig(log_cfg)

app = Flask(__name__)
filelist = queue.Queue()
results = queue.Queue()
logger = logging.getLogger('Server')

class TranscribeThread(Thread):

    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        try:
            model = whisper.load_model("base")
        except:
            logger.warning('Failed to load model.')

        while True:
            file = filelist.get()

            logger.debug(f'{file} is being processed ')
            duration, text = transcribe(file, model)
            results.put([file, text])
            
            logger.debug(f'{file} processing finished in {duration}s')
            
            time.sleep(0.1)

class DatabaseThread(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        db = mysql.connector.connect(host='localhost', user='root', password='notouch1234!@#$')
        cursor = db.cursor(buffered=True)

        cursor.execute('USE test;')

        while True:
            result = results.get()
            sql = """INSERT INTO calldata (idx, groupid, id, dateid, timeid, content)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (None, result[0][:2], result[0][3:6], result[0][7:15], result[0][15:21], result[1]))
            db.commit()
            os.remove(result[0])
            
            logger.debug(f'{result[0]} saved in database successfully')

            time.sleep(0.1)

@app.route('/generate', methods=['POST'])
def generate():

    if request.method == 'POST':
        data = request.get_data()
        saved_file = save_audio('1', 'JHS', data)

        logger.debug(f'Finished writing {saved_file}')

        filelist.put(saved_file)

    return jsonify({'status': 'accepted'})

if __name__ == '__main__':
    dbthread = DatabaseThread()
    threads = []
    thread_num = 2
    
    temps = glob.glob('temp/*.wav')

    for tmp in temps:
        filelist.put(tmp)

    for i in range(thread_num):
        newthread = TranscribeThread()
        newthread.start()
        threads.append(newthread)
    
    dbthread.start()

    logger.info('Server is listening on 5000 ...')
    app.run(port=5000, threaded=True)
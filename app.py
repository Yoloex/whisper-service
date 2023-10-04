import whisper
import mysql.connector
import logging.config
import yaml
import queue
import time
import glob
import os
import sys
from threading import Thread
from flask import Flask, request, jsonify
from getpass import getpass
from utils.utils import save_audio, transcribe

with open('cfg/log.yaml') as f:
    log_cfg = yaml.safe_load(f.read())
    logging.config.dictConfig(log_cfg)

with open('cfg/server.yaml') as f:
    server_cfg = yaml.safe_load(f.read())

app = Flask(__name__)
filelist = queue.Queue()
results = queue.Queue()
logger = logging.getLogger('Server')

class TranscribeThread(Thread):

    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        try:
            model = whisper.load_model(server_cfg['server']['model'])
        except:
            logger.warning('Failed to load model.')
            sys.exit()

        while True:
            file = filelist.get()

            logger.debug(f'{file} is being processed')
            duration, text = transcribe(file, model)
            results.put({
                'filename': file,
                'groupid': file[:2],
                'id': file[3:6],
                'dateid': file[7:15],
                'timeid': file[15:21],
                'content': text
            })
            
            logger.debug(f'{file} processing finished in {duration}s')
            
            time.sleep(0.1)

class DatabaseThread(Thread):
    def __init__(self, database):
        Thread.__init__(self)
        self.database = database
    def run(self):
        
        cursor = self.database.cursor(buffered=True)
        cursor.execute('USE test;')

        while True:
            result = results.get()
            sql = """INSERT INTO calldata (idx, groupid, id, dateid, timeid, content)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (None, result['groupid'], result['id'], result['dateid'], result['timeid'], result['content']))
            db.commit()
            os.remove('temp/' + result['filename'])
            
            logger.debug(f"{result['filename']} saved in database successfully")

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

    connected = True

    for i in range(3):
        if connected and i == 1:
            break
        else:
            try:
                password = getpass()
                db = mysql.connector.connect(host=server_cfg['database']['host'], user=server_cfg['database']['user'], password=password)
                connected = True
            except Exception as e:
                print('Connection failed with', e)
                connected = False

    if not connected:
        sys.exit()

    dbthread = DatabaseThread(db)
    threads = []
    thread_num = server_cfg['server']['thread_count']
    
    temps = glob.glob('temp/*.wav')

    for tmp in temps:
        filelist.put(tmp[5:])

    for i in range(thread_num):
        newthread = TranscribeThread()
        newthread.start()
        threads.append(newthread)
    
    dbthread.start()

    logger.info(f"Server is listening on {server_cfg['server']['port']} ...")
    app.run(port=server_cfg['server']['port'], threaded=server_cfg['server']['threaded'], host=server_cfg['server']['host'])
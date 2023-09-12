import flask
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    pass

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        data = request.form['inputs']
        print('inputs', data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    print('Listening on 5000 ...')
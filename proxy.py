import random
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return {
        "status": "Loaded"
    }

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == "POST":
        serverid = random.randint(1, 5)
        data = request.get_data()
        response = requests.post(f"http://localhost:500{serverid}/generate", data=data)
    return response

if __name__ == '__main__':
    app.run(port=6000, debug=True)
    print("Listening on 6000 ...")
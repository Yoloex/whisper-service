import random
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return {"status":"Loaded"}

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == "POST":
        serverid = random.randint(1, 5)

        print(f"Redirected to Server {serverid}")

        data = request.get_data()
        response = requests.post(f"http://localhost:500{serverid}/generate", data=data)
    return jsonify(response.json())

if __name__ == '__main__':
    print("Listening on 3000 ...")
    app.run(port=3000, debug=True, host='0.0.0.0')
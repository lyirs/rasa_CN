from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

RASA_SERVER_URL = "http://localhost:5005"  # 根据您的 Rasa 服务器配置进行修改

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    response = requests.post(f"{RASA_SERVER_URL}/webhooks/rest/webhook", json={"message": message})
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)

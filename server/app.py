import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import requests

app = Flask(__name__)
CORS(app)

# 简易前端服务
RASA_SERVER_URL = "http://localhost:5005"  # 根据您的 Rasa 服务器配置进行修改

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    response = requests.post(f"{RASA_SERVER_URL}/webhooks/rest/webhook", json={"message": message})
    return jsonify(response.json())


# 获取用户对应session
def get_sessions_by_user(user_id):
    connection = sqlite3.connect("user_sessions.db")
    cursor = connection.cursor()

    cursor.execute("SELECT session_id FROM user_sessions WHERE user_id=?", (user_id,))
    sessions = cursor.fetchall()

    if not sessions:
        connection.close()
        return []

    sessions = [row[0] for row in sessions]
    connection.close()
    return sessions


@app.route("/user_sessions/<user_id>", methods=["GET"])
def get_user_sessions(user_id):
    sessions = get_sessions_by_user(user_id)
    return jsonify({"sessions": sessions})


# 创建新对话
@app.route('/new_conversation/<user_id>/<session_id>', methods=['GET'])
def new_conversation(user_id, session_id):
    conn = sqlite3.connect('user_sessions.db')
    with conn:
        cur = conn.cursor()
        # 检查是否存在相同的 session_id
        cur.execute("SELECT session_id FROM user_sessions WHERE user_id=? AND session_id=?", (user_id, session_id))
        existing_session_id = cur.fetchone()

        # 如果不存在重复的 session_id，则插入新会话
        if not existing_session_id:
            cur.execute("INSERT INTO user_sessions (user_id, session_id) VALUES (?, ?)", (user_id, session_id))
            conn.commit()

    return "OK", 200



# 删除对话（tracker_store.db）
@app.route("/delete_conversation/<session_id>", methods=["DELETE"])
def delete_conversation(session_id):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("tracker_store.db")
        cursor = conn.cursor()

        # Delete the conversation from the database
        cursor.execute("DELETE FROM events WHERE sender_id = ?", (session_id,))
        conn.commit()

        # Close the database connection
        conn.close()
        return jsonify({"success": True}), 200
    except Exception as e:
        print(f"Error deleting conversation: {e}")
        return jsonify({"error": "Failed to delete conversation"}), 500

# 删除对话（user_sessions.db）
@app.route("/delete_session/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    try:
        conn = sqlite3.connect('user_sessions.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM user_sessions WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()

        return jsonify({"success": True}), 200
    except Exception as e:
        print(f"Error deleting conversation: {e}")
        return jsonify({"error": "Failed to delete session"}), 500

# 获取可用的模型列表
current_script_path = os.path.abspath(__file__)
root_dir = os.path.dirname(current_script_path)
MODELS_DIR = os.path.join(root_dir, "../models")
MODELS_DIR = os.path.abspath(MODELS_DIR)
def get_models_list():
    models = []
    for entry in os.listdir(MODELS_DIR):
        if os.path.isfile(os.path.join(MODELS_DIR, entry)):
            models.append(entry)
    return models
@app.route("/models", methods=["GET"])
def get_models():
    models = get_models_list()
    return jsonify({"models": models})

if __name__ == '__main__':
    app.run(port= 5001 ,debug=True)

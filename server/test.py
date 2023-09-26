from flask import Flask, render_template, request, jsonify
import requests
from visualize_story import visualize_story
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route('/visualize', methods=['GET'])
def visualize():
    story_html_content = visualize_story()
    if story_html_content is None:
        return jsonify({"error": "Error occurred while visualizing the story"}), 500

    return jsonify({"html_content": story_html_content})


@app.route('/db', methods=['GET'])
def get_db():
    conn = sqlite3.connect('tracker_store.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events")
    sessions = cursor.fetchall()

    conn.close()

    return jsonify({"sessions": sessions})

@app.route('/sessions', methods=['GET'])
def get_sessions():
    conn = sqlite3.connect('user_sessions.db')
    cursor = conn.cursor()

    cursor.execute("SELECT session_id FROM user_sessions WHERE user_id='user-1681053215919-47i5rwav7'")
    sessions = cursor.fetchall()

    conn.close()

    return jsonify({"sessions": sessions})


if __name__ == '__main__':
    app.run(port= 5002 ,debug=True)

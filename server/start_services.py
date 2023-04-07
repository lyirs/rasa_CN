import subprocess
import webbrowser
import os

os.chdir(os.path.dirname(os.path.abspath(__file__ + "/../")))
# Start Rasa action server
action_server = subprocess.Popen(["rasa", "run", "actions"])

# Start Rasa server
rasa_server = subprocess.Popen(["rasa", "run", "--enable-api", "--cors", "*"])

# Start your backend server (e.g., Flask)
# backend_server = subprocess.Popen(["python", "server/app.py"])

# Open the web page in a new browser tab
# webbrowser.open("http://localhost:5000")

# Wait for the servers to finish
action_server.wait()
rasa_server.wait()
# backend_server.wait()

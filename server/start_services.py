import subprocess
import webbrowser
import os
import signal
import time
import sqlite3
import requests
from sqlite3 import Error


class RasaServicesManager:
    def __init__(self):
        self.processes = []

    def start_service(self, command, name, check_url=None):
        try:
            process = subprocess.Popen(
                command, stdout=None, stderr=None)
            self.processes.append((name, process))
            print(f"Starting {name}...")

            if check_url:
                # 等待服务可用
                for _ in range(60):  # 最长等待 60 秒
                    try:
                        response = requests.get(check_url)
                        if response.status_code == 200:
                            print(f"{name} started successfully.")
                            break
                    except requests.exceptions.ConnectionError:
                        pass
                    time.sleep(1)
                else:
                    print(
                        f"Warning: {name} may not have started successfully within the expected time.")
            else:
                print(f"{name} started successfully.")
        except Exception as e:
            print(f"Failed to start {name}: {e}")

    def stop_all_services(self):
        for name, process in self.processes:
            try:
                os.kill(process.pid, signal.SIGTERM)
                print(f"{name} stopped successfully.")
            except Exception as e:
                print(f"Failed to stop {name}: {e}")

    def wait_for_services(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping all services...")
            self.stop_all_services()


def create_user_sessions_table():
    try:
        conn = sqlite3.connect("user_sessions.db")
        with conn:
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS user_sessions (
                            user_id TEXT NOT NULL,
                            session_id TEXT NOT NULL
                           );''')
        print("Database checked/created successfully.")
    except Error as e:
        print(f"Error creating database: {e}")


if __name__ == "__main__":
    manager = RasaServicesManager()

    os.chdir(os.path.dirname(os.path.abspath(__file__ + "/../")))

    # Check and create the user_sessions database if it doesn't exist
    create_user_sessions_table()

    # Start Rasa action server
    manager.start_service(["rasa", "run", "actions"], "Rasa Action Server")

    # Start Rasa server, wait until it's available
    manager.start_service(
        ["rasa", "run", "--enable-api", "--cors", "*"],
        "Rasa Server",
        check_url="http://localhost:5005/status"
    )

    # Start your backend server (e.g., Flask)
    manager.start_service(["python", "server/app.py"],
                          "Backend Server", check_url="http://localhost:5001")

    # Open the web page in a new browser tab
    webbrowser.open("http://localhost:5001")

    # Wait for the services to finish
    manager.wait_for_services()

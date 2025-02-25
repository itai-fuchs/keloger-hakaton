import os
import requests
import json
from pathlib import Path


class Writer:
    def __init__(self, url="http://127.0.0.1:5000"):
        self.backend_url = url
        self.file_name = None

    def is_connected(self,mac="abc"):
        response = requests.get(f"{self.backend_url}/connection/{mac}")
        return response.status_code == 200

    def write_to_file(self, data):
        Path("logs").mkdir(parents=True, exist_ok=True)
        with open(self.file_name, "w") as file:
            y = json.dumps(data)
            file.write(y)
            print(f"saved to JSON: {self.file_name}")

    def send_files(self):
        for filename in os.listdir("logs"):
            file_path = os.path.join("logs", filename)
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    content = file.read()
                    data = {"file_name": filename, "content": content}
                    try:
                        response = requests.post(f"{self.backend_url}/log", json=data, timeout=5)
                        if response.status_code == 200:
                            print(f"{filename} sent successfully")
                            os.remove(file_path)
                    except requests.RequestException as e:
                        print(f"error: {filename}: {e}")

    def send_to_server(self, data):
        try:
            response = requests.post(f"{self.backend_url}/log", json=data, timeout=5)
            print("sending",response.status_code)
            if 200 < response.status_code < 300:
                return True
            else:
                return False
        except requests.RequestException as e:
            print(f"sending error: {e}")
            return False


    def save_manager(self, data,file_name):
        self.file_name = f"logs/log_{file_name}.json"
        if self.is_connected():
            if os.path.exists("logs"):
                self.send_files()
                Path("logs").rmdir()
            print("connected, sending to server")
            self.send_to_server(data)
        else:
            print("unconnected, saving to file")
            self.write_to_file(data)

import socket
import json
from datetime import datetime
import requests


class Writer:
    def __init__(self, file_name="data.json", url="http://127.0.0.1:5000"):
        self.backend_url = url
        self.file_name = file_name

    def is_connected(self,mac="abc"):
        response = requests.get(f"{self.backend_url}/connection")
        print(response.status_code)
        return response.status_code == 200

    def write_to_file(self, data):
        with open(self.file_name, "w") as file:
            y = json.dumps(data)
            file.write(y)
            print(f"saved to JSON: {self.file_name}")

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


    def save_manager(self, data):
        if self.is_connected():
            print("connected, sending to server")
            self.send_to_server(data)
        else:
            print("unconnected, saving to file")
            self.write_to_file(data)


test = Writer()
is_connected = test.is_connected()
print("is_connected:",is_connected)
new_data={
        "Data": "Device  successfully",
        "Date": "2026-02-16 14:30:00",
        "MAC": "00:1A:2B:3C:4D:5E"
    }
test.write_to_file(new_data)
send_to_server = test.send_to_server(new_data)
print(send_to_server)
test.save_manager(new_data)

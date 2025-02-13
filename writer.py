import socket
import json
from datetime import datetime
import requests


class writer:
    def __init__(self, file_name="data.json", server_handler=None):
        self.file_name = file_name
        self.server_handler = server_handler

    def is_connected(self,url):
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except (requests.ConnectionError, requests.Timeout):
            return False

    def write_to_file(self, data):
        with open(self.file_name, "wb") as file:
            file.write(data)

    def send_to_server(self, url, data):
        try:
            response = requests.post(url, json=data, timeout=5)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.RequestException as e:
            print(f"sending error: {e}")
            return False

    def send_to_ser(self, data):
        if self.server_handler:
            self.server_handler.receive_data(data)
        else:
            print("error: no server")

    def process_list(self, data, url):
        if self.is_connected(url):
            print("connected, sending to server")
            self.send_to_server(url,data)
        else:
            print("unconnected, saving to file")
            self.write_to_file(data)


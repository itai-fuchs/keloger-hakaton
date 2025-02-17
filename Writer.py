import json
import requests


class Writer:
    def __init__(self, file_name="data", url="http://127.0.0.1:5000"):
        self.backend_url = url
        self.file_name = f"logs/log_{file_name}.json"

    def is_connected(self,mac="abc"):
        response = requests.get(f"{self.backend_url}/connection/{mac}")
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



#testing functions
new_data={
    "Data": "b'gAAAAABnswc_OW7K0TMWBI1Z9hPoKV9M1El2LXlj8gaOXwN89hCZm24uDqtJ7CAhb6jZYKcuaIw4Igfq39TXiDSU-a70XEXR5g=='",
    "Date": "2026-02-16 14:30:00",
    "MAC": "38-87-D5-0D-C6-36"
}
test = Writer()
is_connected = test.is_connected(new_data["MAC"])
print("is_connected:",is_connected)
test.write_to_file(new_data)
send_to_server = test.send_to_server(new_data)
print("send_to_server: ", send_to_server)
test.save_manager(new_data)

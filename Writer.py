import json
import requests
import os


class Writer:
    def __init__(self, url="http://127.0.0.1:5000"):
        self.backend_url = url
        self.file_name = None

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


    def is_connected(self,mac):
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
                print("Sent")
            else:
                print("did not send")
                self.write_to_file(data)
        except requests.RequestException as e:
            print(f"sending error: {e}")
            self.write_to_file(data)


    def save_manager(self, data,file_name):
        self.file_name = f"logs/log_{file_name}.json"
        print("sending to server")
        self.send_to_server(data)
        #print("unconnected, saving to file")
        #self.write_to_file(data)



#testing functions
# new_data={
#     "Data": "b'gAAAAABnswc_OW7K0TMWBI1Z9hPoKV9M1El2LXlj8gaOXwN89hCZm24uDqtJ7CAhb6jZYKcuaIw4Igfq39TXiDSU-a70XEXR5g=='",
#     "Date": "2026-02-16 14:30:00",
#     "MAC": "38-87-D5-0D-C6-36"
# }
# test = Writer()
# is_connected = test.is_connected(new_data["MAC"])
# print("is_connected:",is_connected)
# test.file_name = "logs/log_test1.json"
# test.write_to_file(new_data)
# send_to_server = test.send_to_server(new_data)
# print("send_to_server: ", send_to_server)
# test.save_manager(new_data,"log_test2.json")

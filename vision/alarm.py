from pygame import mixer

alarm_on = False
ALARM_FILE = "alarm.wav"

def init_alarm():
    mixer.init()

def start_alarm():
    global alarm_on
    if not alarm_on:
        mixer.music.load(ALARM_FILE)
        mixer.music.play(-1)
        alarm_on = True

def stop_alarm():
    global alarm_on
    if alarm_on:
        mixer.music.stop()
        alarm_on = False

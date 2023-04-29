# -- coding: utf-8 --
import RPi.GPIO as GPIO
import time
import os

# Definition der Verzeichnisse fÃ¼r die Voicemail und Beep-Ton Dateien sowie des Aufnahme Verzeichnisses
voicemail_file = "/home/ab/Audiobook/voicemail.wav"
beep_file = "/home/ab/Audiobook/beep.wav"
recordings_dir = "/home/ab/Audiobook/Recordings/"

# Setzen der Pin-Nummerierungsmethode auf BCM
GPIO.setmode(GPIO.BCM)

# Setzen des GPIO23 Pins auf Eingang mit aktiviertem Pull-up Widerstand
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def record_message():
    timestamp = time.strftime("%H:%M:%S")
    filename = recordings_dir + "message-" + timestamp + ".wav"
    cmd = "arecord -f cd -D hw:1 -c 1 "
    cmd += "-V mono -r 48000 -q -t wav -d 0 -q " + filename
    os.system(cmd)

def play_message():
    os.system("aplay -D hw:1,0 -c 1 -r 32000 " + voicemail_file)

def play_beep():
    os.system("aplay -D hw:1,0 -c 1 -r 32000 " + beep_file)

# Starten im Wartemodus mit Print-BestÃ¤tigung
print("Standby")

while True:
    if GPIO.input(23) == GPIO.HIGH:
        # GPIO23 ist auf HIGH, Programm bleibt im Wartemodus
        time.sleep(0.5)
    elif GPIO.input(23) == GPIO.LOW:
        # GPIO23 hat den Zustand von HIGH zu LOW gewechselt, 2 Sekunden warten und dann Voicemail abspielen und Beep-Ton abspielen
        time.sleep(2)
        play_message()
        play_beep()
        record_message()
        # Warten auf RÃ¼ckkehr von GPIO23 zu HIGH
        while GPIO.input(23) == GPIO.LOW:
            time.sleep(0.1)
        # Nach Beenden der Aufnahme, zurÃ¼ck in den Wartemodus und Print-BestÃ¤tigung
        print("Standby")

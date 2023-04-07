# coding=utf-8
import os
import time
import RPi.GPIO as GPIO

# Hier definieren wir die Dateipfade der Audio-Dateien
VOICEMAIL_FILE = "/home/ab/Audiobook/Aufnahme/voicemail.wav"
BEEP_FILE = "/home/ab/Audiobook/beep.wav"
RECORDING_FILE = "/home/ab/Audiobook/Recording/recording.wav"

# Hier definieren wir die GPIO-Pins, die wir verwenden möchten
GPIO_PIN = 22

# Hier initialisieren wir die GPIO-Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN)

# Funktion zum Abspielen der Audio-Dateien
def play_audio_file(file_path):
    os.system("aplay " + file_path)

# Schleife, die auf Benutzereingaben wartet
while True:
    # Überprüfung, ob das Telefonhörer abgenommen wurde
    if not GPIO.input(GPIO_PIN):
        # Wenn das Telefonhörer abgenommen wurde, wird eine kurze Pause eingelegt
        time.sleep(2.5)

        # Die Voicemail wird abgespielt
        print("Hörer abgenommen, bitte sprechen Sie nach dem Signalton")
        play_audio_file(VOICEMAIL_FILE)

        # Eine weitere Pause wird eingelegt
        time.sleep(1)

        # Der Signalton wird abgespielt
        play_audio_file(BEEP_FILE)

        # Die Audioaufnahme beginnt
        os.system("arecord -D hw:1 -f S16_LE -c 1 -d 10 -r 44100 " + RECORDING_FILE)
        print("Aufnahme beendet")

        # Die Schleife wird beendet
        break

# Hier räumen wir die GPIO-Pins auf, bevor das Programm endet
GPIO.cleanup()

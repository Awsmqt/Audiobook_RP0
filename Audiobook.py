# coding=utf-8
import os
import time
import RPi.GPIO as GPIO
import subprocess

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

# Funktion zum Starten der Aufnahme
def start_recording():
   subprocess.Popen(["arecord", "-D", "hw:1", "-f", "S16_LE", "-c", "2", "-r", "44100", "-d", "5", RECORDING_FILE])

# Funktion zum Beenden der Aufnahme
def stop_recording(process):
    # Beenden des Aufnahme-Prozesses
    process.terminate()
    # Warten, bis der Prozess beendet ist
    process.wait()
    print("Aufnahme beendet")

# Schleife, die auf Benutzereingaben wartet
while True:
    # Überprüfung, ob das Telefonhörer aufgelegt ist
    if GPIO.input(GPIO_PIN):
        # Wenn das Telefonhörer aufgelegt ist, wird die Voicemail abgespielt
        print("Hörer abgenommen, bitte sprechen Sie nach dem Signalton")
        play_audio_file(VOICEMAIL_FILE)
        play_audio_file(BEEP_FILE)

        # Die Audioaufnahme beginnt
        recording_process = start_recording()
        print("Aufnahme gestartet")

        # Schleife, die auf das Auflegen des Hörers wartet
        while True:
            # Überprüfung, ob der Hörer aufgelegt wurde
            if not GPIO.input(GPIO_PIN):
                # Aufnahme beenden
                stop_recording(recording_process)
                # Schleife beenden und auf neue Eingabe warten
                break

# Hier räumen wir die GPIO-Pins auf, bevor das Programm endet
GPIO.cleanup()

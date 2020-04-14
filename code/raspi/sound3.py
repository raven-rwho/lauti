from soundplayer import SoundPlayer
from dosound import DoSound
import RPi.GPIO as GPIO
import time
import os

# Button pins, adapt to your configuration
P_TON1 = 10
P_TON2 = 11
P_TON3 = 12
P_TON4 = 13
P_TON5 = 15
P_TON6 = 16
P_LOWBAT = 18
P_POWER = 19
P_POWSWITCH = 21
dev = 1  # USB Soundadapter
AUSLIMIT = 900  # Grenze fuer aut.Ausschalten 300 = 1min
schleife = 0  # Schleifenzaehler fuer aut. Ausschalten
maja = 0  # Maja Abwechslung...

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_TON1, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(P_TON2, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(P_TON3, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(P_TON4, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(P_TON5, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(P_TON6, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(P_LOWBAT, GPIO.IN, GPIO.PUD_UP)  # Battery leer == Low
    GPIO.setup(P_POWSWITCH, GPIO.IN, GPIO.PUD_UP)  # Einschalter abfragen Ein == Low
    GPIO.setwarnings(False)
    GPIO.setup(P_POWER, GPIO.OUT)
    GPIO.output(P_POWER, True)  # Netzteil eingeschaltet lassen
    DoSound.playTone(440, 0.3, dev)
    DoSound.playTone(550, 0.3, dev)
    DoSound.playTone(660, 0.3, dev)
    time.sleep(1)
    DoSound.playTone([440, 550, 660], 3, dev)
    time.sleep(2)

setup()
print "Bereit..."
p = SoundPlayer("/home/pi/mp3/Nanue.mp3", 1)
p.play(1)

while True:
    if GPIO.input(P_TON1) == GPIO.LOW:
        print "Ton1..."
        p.stop()
        DoSound.playTone(440, 0.3, dev)
    elif GPIO.input(P_TON2) == GPIO.LOW:
        print "Ton2..."
        p.stop()
        DoSound.playTone(550, 0.3, dev)
        p.play()
    elif GPIO.input(P_TON3) == GPIO.LOW:
        print "Ton3..."
        p.stop()
        DoSound.playTone(660, 0.3, dev)
        p = SoundPlayer("/home/pi/mp3/Das_kleine_Kaninchen.mp3", 1)
        p.play()
    elif GPIO.input(P_TON4) == GPIO.LOW:
        print "Ton4..."
        p.stop()
        DoSound.playTone(770, 0.3, dev)
        p = SoundPlayer("/home/pi/mp3/Der_kleine_Elefant.mp3", 1)
        p.play()
    elif GPIO.input(P_TON5) == GPIO.LOW:
        print "Ton5..."
        p.stop()
        DoSound.playTone(880, 0.3, dev)
        if maja == 0:
            maja = 1
            p = SoundPlayer("/home/pi/mp3/maja.mp3", 1)
        else:
            maja = 0
            p = SoundPlayer("/home/pi/mp3/Gemuetlichkeit_n.mp3", 1)
        p.play()
    elif GPIO.input(P_TON6) == GPIO.LOW:
        print "Ton6..."
        p.stop()
        DoSound.playTone(1000, 0.3, dev)
        p = SoundPlayer("/home/pi/mp3/Wie_kleine_Tiere.mp3", 1)
        p.play()
    elif GPIO.input(P_LOWBAT) == GPIO.LOW:
        time.sleep(0.1)  # Entprellen zur Sicherheit
        if GPIO.input(P_LOWBAT) == GPIO.LOW:
            print "Batterie leer, Ausschaltmeldung und runterfahren"
            GPIO.output(P_POWER, False)  # Netzteil abschalten
            p.stop()
            DoSound.playTone([440, 550, 660], 10, dev)
            p = SoundPlayer("/home/pi/mp3/BatterieLeer_n.mp3", 1)
            p.play()
            time.sleep(2)
            os.system("sudo poweroff")
    elif (GPIO.input(P_POWSWITCH) == GPIO.HIGH) or (schleife > AUSLIMIT):
        time.sleep(0.1)  # Entprellen zur Sicherheit
        if (GPIO.input(P_POWSWITCH) == GPIO.HIGH) or (schleife > AUSLIMIT):
            print "Ausschalten gewuenscht, runterfahren und ausschalten"
            GPIO.output(P_POWER, False)
            p.stop()
            DoSound.playTone([440, 550, 660], 0.2, dev)
            os.system("sudo poweroff")
    if p.isPlaying() == True:
        schleife = 0
    else:
        schleife = schleife + 1
    time.sleep(0.1)  # Do not waste processor time

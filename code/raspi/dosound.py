#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-Sound/dosound.py
import os

class DoSound:
    '''
    Soundplayer ueber SoX, Aufnahme ueber arecord.
    Dieser einfache Python-Wrapper ruft Shellkommandos auf.
    Fuer den Raspberry Pi muessen die Pakete sox und mp3
    installiert sein:
    '''

    def __init__(self, device = 0):
        '''
        Erzeugt einen Soundplayer fuer das angegebenen Device (ID).
        @param device: die Sound-Device-ID
        (e.g. 0: intern, 1: USB Soundadapter)
        '''
        self.device = device

    def play(self, audiofile, volume = 1):
        '''
        Spielt die angegebenen Datei mit der gewähten Lautstaerke (default: 1).
        Wirft eine Exception, wenn die Datei nicht existiert.
        @param audiofile: Sounddatei
        @param volume: Lautstaerke (default: 1)
        '''
        if not os.path.isfile(audiofile) :
            raise Exception("Audio resource " + audiofile + " not found")
        self.audiofile = audiofile
        self.volume = volume
        cmd = "AUDIODEV=hw:" + str(self.device) + \
            " play -v " + str(self.volume) + \
            " -q " + self.audiofile + " 2> /dev/null"
        os.system(cmd)

    @staticmethod
    def soundSample(self, duration = 5):
        from scipy.io import wavfile
        '''
        Sound-Sample von der angegebenen Dauer aufnehmen.
        Die Aufnahme erfolgt mit 8000 Samples/s als .wav-Datei.
        Mittels wavfile-read() wird das Samle in einer Liste gespeichert und zurueckgegeben.
        Da soundSample() eine statische Methode ist, kann diese durch Voranstellen des
        Klassennamens aufgerufen werden.
        @param duration: Aufnahmedauer in s
        '''
        snd = []
        tmpfile = "/tmp/sound.wav"
        cmd = "/usr/bin/arecord -D plug:default -f S16_LE -r 8000 -d " + \
            str(duration) + " " + tmpfile + " >/dev/null 2>&1"
        os.system(cmd)
        sampFreq, snd = wavfile.read(tmpfile)
        os.remove(tmpfile)
        return(snd)

    @staticmethod
    def playTone(frequencies, duration, device = 0):
        '''
        Spielt einen oder mehrere Sinustoene ab, deren Frequenz und Dauer angegeben
        wird. Als Frequenz kann entweder ein Wert oder eine Liste uebergeben werden.
        Da playTone() eine statische Methode ist, kann diese durch Voranstellen des
        Klassennamens aufgerufen werden.
        @param frequencies: Frequenz oder Liste von Frequenzen in Hz
        @param duration: Dauer in s
        @param device: Sound-Device-ID (0: intern, 1: USB Soundadapter)
        '''
        if not type(frequencies) == list:
            frequencies = [frequencies]
        s = " "
        for f in frequencies:
            s += "sin " + str(f) + " "
        cmd = "AUDIODEV=hw:" + str(device) + " play -q -n synth " + str(duration) + \
            s + " 2> /dev/null"
        os.system(cmd)

    @staticmethod
    def isPlaying():
        '''
        Prueft, ob noch ein Player-Prozess laeuft
        Da isPlaying() eine statische Methode ist, kann diese durch Voranstellen des
        Klassennamens aufgerufen werden.
        @return: True, falls noch ein Player laeuft; sonst False
        '''
        info = os.popen("ps ax | grep -c play").read()
        count = int(info)
        # print "count: %d" % count
        return count > 2

    @staticmethod
    def stopPlaying():
        '''
        Stoppt ale laufenden Soundplayer.
        Da stopPlaying() eine statische Methode ist, kann diese durch Voranstellen des
        Klassennamens aufgerufen werden.
        '''
        cmd = "sudo killall -HUP play"
        os.system(cmd)


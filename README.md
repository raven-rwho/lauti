# lauti
Instructions and code to build a Rasberry Pi powered speaker for children

english version [here](english.md)

Ein Akkuvetriebener Hörspielabspieler lässt sich auf viele Arten bauen. Mit einem solchen Gerät können Schlummerhörspiele oder anderes mobil / ohne Kabel genutzt werden und dank der eigenen Programmierung sind der Ausgestaltung wenig Grenzen gesetzt.
Der eingesetzte Pi kann per WLAN administriert, mit frischen Hörspielen oder modifizierten Programmen versorgt werden. Die eingesetzten 6 Taster können frei im Programm genutzt werden.
BlueTooth ist auch an Bord und schafft weitere Möglichkeiten.
In der hier beschriebenen Version sind 2-3 Stunden Abspielzeit erreichbar. Je nach Wahl der Komponenten natürlich ist vieles möglich. Der eingesetzte Energieversorgungsbaustein kann auch höhere Leistungen abgeben und damit komplexere Schaltungen versorgen (LEDs, Display, ...) aber je mehr die Schaltung erweitert wird desto mehr Energie muss der eingesetzte Akku natürlich bereit stellen.

Eine Zusammenfassung der benötigten Teile und einen Schaltplan findet ihr [hier](Akku_Lauti_Teile_und_Schaltung.pdf)

Das hier beschriebene Gerät nutzt:
- einen Raspberry Pi Zero W oder WH mit Raspian Linux mit einem Python Programm zur Steuerung
- eine USB „Soundkarte“ für den Pi
- eine USB Stromversorgte PC Aktivbox als Gehäuse, Audioverstärker und Lautsprecher
- einige Taster freier Wahl als HMI
- die Schaltung von Adafruit PowerBoost 1000C zur Energieversorgung aus USB und LiPo Akku mit Ladeschaltung für den Akku
- einen LiPo Akku ausreichender Kapazität, hier genutzt 3.6V 1800mAh mit kleiner Bauform
- einige Drähte, Lötzinn, Widerstände, Kondensatoren, Dioden und einen Feldeffekttransistor wie im Schaltplan
- einiges mechanische und elektrotechnische Geschick und Schwups ist es vollbracht
- große Vorsicht bei der Handhabung der Schaltungsteile (ESD!!!) um Zerstörung von Bauelementen zu Vermeiden beim Aufbau, besonders beim eingesetzten Feldeffekttransistor
- hilfreich zur Inbetriebnahme des Pi ist ein MiniHDMI ZU HDMI Adapter, teils enthalten in Starter Kits zum Raspberry Pi Zero

Zur Installation des Raspberry Pi W/H dienen die folgenden Schritte, sicher lassen sich auch andere Dinge denken. Alle Software ist Freeware und leicht im Internet zu finden.
- Mit Win32DiskImager das Image von Raspian buster full.img auf SD Karte schreiben
- Leere Datei ssh. in Root Verzeichnis der SD Karte anlegen (startet automatisch SSH Zugang auf Raspi bei Boot
- Datei wpa_supplicant.conf in Root Verzeichnis der SD Karte anlegen und darin SSID und Passwort eintragen für das WLAN das der Raspi beim Boot verbinden soll
- Anschluss Maus an MicroUSB Anschluss und HDMI mit Adapter MiniHDMI to HDMI an TV
- Booten mit 5V an MicroUSB Power
- Updaten und Einstellungen wie aufpoppen... (Defaultuser pi passwd raspberry)
- ```sudo apt-get update && sudo apt-get upgrade```
- ```sudo raspi-config``` Einstellungen anpassen (Desktop ausstellen)
- ```sudo reboot``` bzw. sudo halt
- Startdatei Pi einstellen mit „sudo nano /etc/rc.local“ und dort vor „exit 0“ eine Zeile einfügen mit „python /home/pi/test.py &“
- Installation SoX für Tonausgabe auf ext. Soundkarte mit ```sudo apt-get install sox``` und ```sudo apt-get install libsox-fmt-mp3```
- datei „soundplayer.py“ im gleichen Verzeichnis wie python programm anlegen / speichern [hier](http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-Sound/dosound.py)
- datei „dosound.py“ im gleichen Verzeichnis wie python programm anlegen / speichern [hier](http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-Sound/dosound.py)
- wenn alle Dateien angelegt sind inkl. MP3 Dateien in Ordner mp3 dann allet jut. Phyton Programm hat Probleme mit mp3 Dateien mit Leerzeichen wenn Name mit „ eingeklammert wird!
- Zusätzliches WLAN kann eingetragen werden un /etc/wpa_supplicant/wpa_supplicant.conf (neuen zusötzlichen Eintrag anlegen wie bereits vorhandener...

## Schaltung
Kurze Schaltungsbeschreibung
Die Schaltung rund um den PowerBoost 1000C dient zur Energieversorgung der Schaltung. Sie kann aus dem MikroUSB Anschluss oder wenn nicht vorhanden aus einem LiPo Akku arbeiten. Die Umschaltung erfolgt automatisch.
Das Eingangs IC des 1000C übernimmt diese Funktionen rund um das Akkumanagment und automatischen Quellenumschaltung.
Das zweite IC des 1000C generiert aus der Akkuspannung bzw. der Spannung vom USB eine stabile Ausgangsspannung von 5.3V zur Versorgung der Schaltung.
Das IC hat einen Enable Eingang der bei Lowpegel den Ausgang deaktiviert und den Stromverbrauch damit nahezu auf 0A bringt. Der BS170 FET dient zur sicheren Aktivierung der Schaltung. Der Einschalter lädt über den Koppelkondensator von 47uF den 1uF Kondensator am Gate des FET und aktiviert damit letzten Endes die Ausgangsspannung von 5.3V. Der 1uF Kondensator wird hauptsächlich durch die vorgeschalteten Dioden wieder entladen, sofern er ein keramischer Kondensator mit sehr kleinen Leckströmen ist. Der einmal geladene Kondensator bewirkt für ca. drei Minuten die Ausgabe der 5.3V zur Versorgung des Raspberry Pi Zero und parallel auch des Audioverstärkers.
In dieser Zeit startet der Raspberry Pi und startet das Steuerungsprogramm das über einen Ausgang das Gate des FET weiter mit Spannung versorgt.
Durch die Entkopplung über den 47uF Kondensator ist nach dem Einschalten der Spannungsausgabe der Einschalter nicht mehr relevant für die Spannungsausgabe. Sie höngt einzig nach dem Start vom Ausgang des Pi ab.
Über einen weiteren Kontakt des Einschalters wird dem Pi gemeldet, dass die Schaltung eingeschaltet bleiben soll. Das Schaltersignal arbeitet gegen GND und zur Funktion ist der Eingang mit aktivem PullUp Widerstand konfiguriert.
Wenn der Einschalter ausgeschaltet wird, erkennt der Pi dies und leitet den Shutdown ein. Beim Shutdown des Pi wird geht der Steuerungsausgang auf Low Pegel und hält damit das Gate des FET nicht mehr dauerhaft auf High Potential.
Nachdem der 1uF Kondensator am FET über die vorgeschalteten Dioden / Widerstände den Schwellwert des FET unterschreitet, wird die 5.3V Generierung deaktiviert und alles geht aus.
Aus dem zweiten IC des 1000C kommt ein Open Collector Low Signal (LOB), dass einen leeren Akku meldet und dass ebenfalls an einen Eingang des Pi geht. Erkennt das Steuerungsprogramm des Pi diesen Low Pegel wird ein Warnton generiert und der Pi runtergefahren. Was wiederum die Abschaltung einleitet. Der Eingang ist zur Funktion mit PullUp Widerstand zu konfigurieren.
Die Taster zur Steuerung der Wiedergabetitel sind ebenfalls nach GND verbunden und können über Eingänge am Pi gelesen werden. Die Eingänge sind dazu am Pi mit PullUp Widerständen konfiguriert.
Die auszugebende Hörspieleatei wird über die am Pi angeschlossene „Soundkarte“ ausgegeben, da der Pi Zero keine analogen Audioausgänge hat wurde dieser Weg gewählt. Der Ausgang der Soundkarte geht in den analogen Eingang der Aktivbox / des Audioverstärkers.
Die Audioausgabe erfolgt immer mit maximaler Lautstärke, die Lautstärke kann über das Potentiometer der Aktivbox weiter zwischen 0 und Maximum eingestellt werden.
Durch Wahl einer kleineren  und leistungsschwachen Aktivbox (3W) ist die Ausgangleistung begrenzt und zeitgleich die Stromaufnahme gering.
Die Schaltung ermöglicht durch diese weitgehende Steuerung durch den Pi zahlreiche Funktionalitäten.
Beim Zusammenbau ist zu beachten, dass die Ladeschaltung des 1000C recht warm werden kann. Sie ist mit ausreichend Abstand zu anderen Teilen zu montieren.
Ein wenig trickreich ist der JST Anschluss am 1000C. Es sind leider zahlreiche JST Stecker definiert und jeder scheint einen anderen zu nutzen. Insofern ist die Wahl eines LiPo Akkus der direkt an den 1000C gesteckt werden kann nicht leicht. Zudem wird in den Beschreibungen gewarnt, dass auch passende JST Stecker keine genormte Belegung der Pins mit + und - des Akkus aufweisen. Insofern ist vor dem Anschluss des Akkus zu prüfen das die Polarität von Akku und des 1000C übereinstimmen!!! Andernfalls kann der Akku und oder der 1000C beschädigt werden. Bei der Wahl des Akkus sollte aus sicherheitsgründen ein Akku mit eingebauter Sicherheitsschaltung gewählt werden, der bei Überstrom, Überspannung, Übertemperatur etc. den Akku trennt / schützt.

__Viel Freude mit der Schaltung!!__

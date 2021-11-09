# MessBox

MessBox für den Kreiselversuch des P1 Praktikums

## Table of contents
- [Beschreibung](#Beschreibung)
- [Installation](#Installation)
- [Vorbereitung](#Vorbereitung)
- [Messung](#Messung)
- [Anderer COM Port](#Anderer-COM-Port)
- [License](#License)


## Beschreibung

Dies ist die Anleitung zur MessBox, welche den Versuchsteil "4. Die Dämpfung des Kreisels" 
beim Versuch "Kreisel" erleichtern soll.
Konkret übernimmt die Messbox bei richtiger Benutzung die Messwertaufzeichnung des Versuches.

Drehzahlwerte werden als .csv Datei gespeicher und es wird ein Plot erstellt.
Der Output Ordner "out", in welchen die generierte .csv Datei gespeichert wird, wird automatisch erstellt.

## Installation

Benötigt werden:

- Das MessBox.py Program
- Installiertes Python 3
  
Optional sollte `matplotlib` installiert werden, um den Plot anzuzeigen

Empfohlen wird Windows als Betriebssystem.
Bei Linus müssen das Paket `pyserial` extra installiert werden und der default COM port geändert werden.


Idealerweise muss `pyserial` unter Windows nicht extra installiert werden, da dieses dem Programm im Ordner "packages" beiliegen.

## Vorbereitung

1. Verbinde die MessBox mit USB mit dem PC. 
   Die Treiber sollten automatisch installiert werden.
   (Grüne Lampe = Strom an)


2. Überprüfe auf welchem COM Port die MessBox liegt.
   Starte dazu in einem Terminal das `Port_finder.py` Programm.
   Ist der COM Port von "USB Serial" der Port "COM4", 
   musst du im folgenden keine Änderungen vornehmen.
   Ist der Port nicht "COM4" siehe unter [Anderer COM Port](#Anderer COM Port) was zu tun ist.


3. Verbindung testen.
   Starte dazu in einem Terminal das `Port_tester.py` Programm.
   Sobald im Terminal "Test active" zu sehen ist, drücke den Knopf auf der MessBox.
   Ist der Test erfolgreich, ist die Vorbereitung abgeschlossen.
   

## Messung

### Einfache Version:
1. Schließe den Photosensor an die MessBox an.
   

2. Starte in einem Terminal das `Messbox.py` Program.
   

3. Sobald im Terminal "Start" zu lesen ist, drücke den Knopf auf der MessBox.
   (Gelbe Lampe = Messung an)
   

4. Sollte kein Fehler aufgetreten sein, genieße deine 25-35 min Pause.
   

5. Nach der Messung findest du eine .csv Datei im Ordner out. 
    Solltest du `matplotlib` installiert haben, so sollte dir auch direkt ein Plot angezeigt werden.

### Fortgeschrittene Version:

Es ist zusätzlich möglich zur Kontrolle das T-Stück (siehe Bild)
anzuschließen und somit den selben Photosensor mit dem Frequenzzähler zu verbinden.

![TStück]
(T-Stück)
		

Auch können die Defaultparameter durch Ändern des Programmcodes 
oder durch Termianlargumente modifiziert werden.

Die Defaultparameter sind:

| parameter        | Erklärung           | Defaultwert  |
| ------------- |:-------------:| -----:|
| port            |      COM Port                | COM4 |
| name            |      Name der .csv Datei     | data |
| live_save       |      Bool, ob wärend der Messung die  <br/>Daten gespeichet werden sollen oder erst am Ende| True |
| interval        |      Zeitintervall für <br/> die Aufnahmen von Messpunken in s     | 30 |
| total            |      Gesamtlaufzeit der Programms in s <br/>  (2100s ~ 35min)     | 2100 |
| cutoff            |      Bool, ob bei zu lange nicht erhaltenen Daten <br/> die Messung beendet werden soll. <br/> Wenn der Kreisel vor 2100s (35min) zum Stillstand kommen sollte.     | True |
| max_cutoff            |      Wie viele "Nichterhalten Werte" in Folge <br/>bis cutoff gewartet werden soll.     | 20 |
| speed            |      Nach wie vielen Sekunden ein "Nichterhalten Wert" <br/>gezählt werden soll in s.     | 0.5 |
| plot            |      Bool, ob die Daten am ende geplottet werden sollen.     | True |
| micros            |      Bool, ob der Arduino in Millisekunden arbeiten soll. <br/> Wenn False dann werden Mikrosekunden genommen.    | True |
| baudrate            |      Baudrate. NICHT verändern     | 57600 |

		
Wenn die Werte durch Termianlargumente geändert werden sollen, 
benutze folgende Schreibweise beim Start des Programms:

```shell
python MessBox.py port=COM3 name=Messung interval=20 plot=False
```
oder
```shell
py -3 MessBox.py port=COM3 name=Messung interval=20 plot=False
```

## Anderer COM Port
Um bei den Programmen `Port_tester.py` und `MessBox.py` einen anderen Port anzugeben, 
ändere die Port Variable im Programm oder gebe den neuen Port als durch Termianlargument an.
	
Wenn die Werte durch Termianlargumente geändert werden sollen, 
benutze folgende Schreibweise beim Start des Programms:
Bei `Port_tester.py`:
```shell
python Port_tester.py COM3
```
Bei `MessBox.py`:
```shell
python MessBox.py port=COM3
```

## License
Code released under the [MIT License](https://github.com/twbs/bootstrap/blob/main/LICENSE). Docs released under [Creative Commons](https://creativecommons.org/licenses/by/3.0/).
***
PS: Erweiterungen und Verbesserungsvorschläge sind erwünscht.

[TStück]: ./Bilder/T-Stück.jpg

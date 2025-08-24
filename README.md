# Analoge Uhr mit Stundenschlag

Ein Projekt zur Erstellung einer analogen Uhr mit römischen Ziffern, deutscher Datumsanzeige und anpassbaren Farben.

## Überblick

Dieses Projekt umfasst zwei Versionen einer analogen Uhr:

*   **HTML-Version:** Eine webbasierte Version, die mit HTML, CSS und JavaScript erstellt wurde. Sie bietet eine benutzerfreundliche Oberfläche zum Ändern der Farben und Stummschalten des Stundenschlags.
*   **Python-Version:** Eine Desktop-Anwendung, die mit Tkinter erstellt wurde.  Sie bietet ähnliche Funktionen wie die HTML-Version, läuft jedoch als eigenständige Anwendung.

## Features

*   **Analoge Anzeige:** Zeigt die Uhrzeit mit römischen Ziffern.
*   **Deutsche Datumsanzeige:** Zeigt das Datum im deutschen Format.
*   **Anpassbare Farben:** Ermöglicht das Ändern des Hintergrunds, Zifferblatts, Zeiger und Datumsanzeige.
*   **Stundenschlag:** Spielt einen akustischen Stundenschlag, der über einen Schalter ein- oder ausgeschaltet werden kann.
*   **Farbpersistenz:** Die zuletzt verwendeten Farben werden im Browser (für die HTML-Version) bzw. in einer INI-Datei (für die Python-Version) gespeichert.
*   **Benutzerfreundliche Oberfläche:** Einfache Steuerung über Menüs und Dialogfenster.

## Benötigte Software

*   **HTML-Version:**
    *   Ein moderner Webbrowser (z.B. Chrome, Firefox, Edge).
*   **Python-Version:**
    *   Python 3.x
    *   Tkinter (in der Regel vorinstalliert, andernfalls mit `pip install tkinter` installieren)

## Installation und Ausführung

### HTML-Version

1.  Speichere die Datei `analoguhr.html` in einem Ordner.
2.  Öffne die Datei `analoguhr.html` mit einem Webbrowser.

### Python-Version

1.  Speichere die Datei `analoguhr.py` in einem Ordner.
2.  Öffne ein Terminal oder eine Eingabeaufforderung und navigiere zu dem Ordner, in dem du die Datei gespeichert hast.
3.  Führe die Datei mit dem Befehl `python analoguhr.py` aus.

## Ordnerstruktur

analoguhr/ 
├── analoguhr.html 
├── analoguhr.py 
└── colors.ini (nur Python-Version)

## Konfiguration (Python-Version)

Die Farbkonfiguration wird in der Datei `colors.ini` gespeichert.  Hier ist ein Beispiel für den Inhalt der Datei:

```ini
[Colors]
background = #FFFFFF
face = #EEEEEE
hands = #000000
digits = #000000
date = #000000
```

Du kannst die Werte in dieser Datei ändern, um das Aussehen der Uhr anzupassen.

Bekannte Probleme
Die HTML-Version benötigt möglicherweise Anpassungen, um in älteren Browsern korrekt angezeigt zu werden.
Die Python-Version benötigt möglicherweise zusätzliche Berechtigungen, um akustische Signale abzuspielen (abhängig vom Betriebssystem).
Die genaue Darstellung des Datums kann je nach Systemkonfiguration variieren.
Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert.

Kontakt
[Dieter Eckstein]
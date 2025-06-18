<br/>

<p align="center">
  <img src="design/graphics/svg/xcore_full_green.svg" width=350px alt="">
    <br/><br/>
    <b>eine einfache modulare Anwendung, die verschiedene Funktionalitäten in Form von Modulen bereitstellt</b>
</p>

<p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/badge/Code-MIT-yellow.svg" alt=""></a>
    <a href=""><img src="https://img.shields.io/badge/powered%20by-Xeniorn-4770DB" alt=""></a>
    <a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://img.shields.io/badge/Media-CC%20BY%204.0-lightgrey.svg" alt=""></a>
    <a href="https://github.com/x404bjrn"><img src="https://img.shields.io/badge/written%20by-x404bjrn-8A2BE2" alt=""></a>
</p>

---

![DE](https://img.shields.io/badge/DE-green?style=for-the-badge)
[![EN](https://img.shields.io/badge/EN-blue?style=for-the-badge)](res/README_EN.md)

## Übersicht

Das XCORE Framework ist ein modulares, erweiterbares Framework für Python, das dir die zentrale Steuerung, Ausführung und Entwicklung von Automatisierungs-Tools, Sicherheitsmodulen, kreativen Helferskripten und systemnahen Anwendungen ermöglicht – egal ob über CLI, GUI oder Webinterface.



### ✨ Highlights

#### 🔌 Plug-and-Play Module
- Lade, konfiguriere und starte Module nach Metasploit-Prinzip (use, options, run) – lokal oder remote.

#### 🧠 Benutzerfreundlich & mehrsprachig
- Dynamische GUI mit automatischer Widget-Generierung für Moduloptionen, integrierter Übersetzungsunterstützung (i18n) und Benutzerverwaltung.

#### 🌐 Drei Steuer-Interfaces
- CLI für Power-User
- Tkinter-GUI für Desktop
- Webinterface (Flask + React) für Remote-Zugriff und moderne UI

#### 💾 Datenbankgestützte Moduloptionen
- Speichere benutzerdefinierte Einstellungen, lade sie später wieder oder verteile sie zentral.

#### ⚒️ Dev Tools integriert
- Mitgelieferter module_creator, Setpoint-Editor, automatische Lokalisierung und ENV-Setup machen Entwicklung und Deployment effizient und konsistent.

#### Für eine umfassende Dokumentation siehe [DOCUMENTATION_DE.md](docs/DOCUMENTATION_DE.md).

---

## Hauptmerkmale

- **Modularer Aufbau**: Das Framework organisiert Funktionalitäten in verschiedene Modulkategorien wie Scanner, KI, Utilities, OSINT, System, Monitor, Exploitation, Helper, Persistence, Creative und Transfer.
  

- **Mehrere Betriebsmodi**: 
  - **CLI-Modus**: Eine interaktive Kommandozeile für die Ausführung von Modulen
  - **GUI-Modus**: Eine grafische Benutzeroberfläche für die einfache Bedienung
  - **Web-Modus**: Eine Webschnittstelle für den Fernzugriff
  - **Setpoint-Modus**: Ein Konfigurationseditor mit CLI-, GUI- oder Web-Interface


- **Mehrsprachigkeit**: Unterstützung für mehrere Sprachen (aktuell Deutsch und Englisch) mit einer flexiblen Internationalisierungsstruktur.


- **Erweiterbarkeit**: Neue Module können einfach hinzugefügt werden, um die Funktionalität des Frameworks zu erweitern.

---

## Installation

### Voraussetzungen

- Python 3.8 oder höher
- pip (Python-Paketmanager)

### Installation über pip

```bash
pip install xcore_framework
```

### Installation aus dem Quellcode

1. Repository klonen:
   ```bash
   git clone https://github.com/x404bjrn/XCORE.git
   ```

2. In das Verzeichnis wechseln:
   ```bash
   cd XCORE
   ```

3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

4. Installation durchführen:
   ```bash
   pip install -e .
   ```
   oder
   ```bash
   python setup.py install
   ```

---

## 🚀 Schnellstart

### CLI-Modus starten

```bash
xcore --cli
```

### Web-Modus starten

```bash
xcore --web
```

Optionale Parameter:
- `--host`: Host-Adresse (Standard: 127.0.0.1)
- `--port`: Port (Standard: 5000)
- `--debug`: Debug-Modus aktivieren
- `--open-browser`: Browser automatisch öffnen (Standard: aktiviert)

Beispiel:
```bash
xcore --web --host 0.0.0.0 --port 8080 --debug
```

### GUI-Modus starten

```bash
xcore --gui
```

### Setpoint-Modus starten

```bash
xcore --setpoint
```

Optionale Parameter:
- `--interface`: Interface für den Konfigurationseditor (cli, gui, web) (Standard: gui)

Beispiel:
```bash
xcore --setpoint --interface cli
```

---

## Eigene Module erstellen

Das XCORE Framework enthält ein grafisches Werkzeug zum Erstellen von Modulen, das sich unter `dev/tools/module_creator.py` befindet. Dieses Werkzeug vereinfacht den Prozess der Erstellung neuer Module, indem es eine benutzerfreundliche Oberfläche für die Definition von Modulmetadaten, Optionen und Internationalisierungszeichenketten bereitstellt.

Für detaillierte Informationen zur Erstellung eigener Module, siehe den Abschnitt [Modulsystem](docs/DOCUMENTATION_DE.md#modulsystem) in der Dokumentation.

---

## Beitragen

Beiträge zum XCORE Framework sind willkommen! Hier sind einige Möglichkeiten, wie Sie beitragen können:

1. **Fehler melden**: Erstellen Sie ein Issue im GitHub-Repository, wenn Sie einen Fehler finden.
2. **Funktionen vorschlagen**: Haben Sie eine Idee für eine neue Funktion? Erstellen Sie ein Issue mit Ihrem Vorschlag.
3. **Code beitragen**: Forken Sie das Repository, nehmen Sie Ihre Änderungen vor und erstellen Sie einen Pull Request.
4. **Module erstellen**: Erstellen Sie neue Module, um die Funktionalität des Frameworks zu erweitern.

---

## Lizenz

- **Code**: MIT-Lizenz – siehe [LICENSE](LICENSE) für Details
- **Medieninhalte**: CC BY 4.0 - siehe [Creative Commons](https://creativecommons.org/licenses/by/4.0/) für Details

---

## written on the dark side of toast 🍞🌚  
#### © 2025, [Xeniorn](https://xeniorn.de) | [`x404bjrn`](https://github.com/x404bjrn)
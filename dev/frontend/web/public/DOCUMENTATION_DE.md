<br/>
<p align="center">
  <img src="../design/graphics/svg/xcore_full_green.svg" width=350px alt="">
    <br/><br/>
    <b>Eine einfache modulare Anwendung, die verschiedene Funktionalitäten in Form von Modulen bereitstellt</b>
</p>

<p align="center">
    <a href="../LICENSE"><img src="https://img.shields.io/badge/Code-MIT-yellow.svg" alt=""></a>
    <a href=""><img src="https://img.shields.io/badge/powered%20by-Xeniorn-4770DB" alt=""></a>
    <a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://img.shields.io/badge/Media-CC%20BY%204.0-lightgrey.svg" alt=""></a>
    <a href="https://github.com/x404bjrn"><img src="https://img.shields.io/badge/written%20by-x404bjrn-8A2BE2" alt=""></a>
</p>

---

# Dokumentation

## Inhaltsverzeichnis

1. [Einleitung](#einleitung)
2. [Projektübersicht](#projektübersicht)
3. [Installation](#installation)
4. [Projektstruktur](#projektstruktur)
5. [Betriebsmodi](#betriebsmodi)
   - [CLI-Modus](#cli-modus)
   - [GUI-Modus](#gui-modus)
   - [Web-Modus](#web-modus)
   - [Setpoint-Modus](#setpoint-modus)
6. [Modulsystem](#modulsystem)
   - [Modulstruktur](#modulstruktur)
   - [Modulkategorien](#modulkategorien)
   - [Eigene Module erstellen](#eigene-module-erstellen)
   - [Verwendung des Module Creators](#verwendung-des-module-creators)
7. [Internationalisierung](#internationalisierung)
8. [Konfiguration](#konfiguration)
9. [Entwicklung](#entwicklung)
10. [Vision](#vision)
11. [Beitragen](#beitragen)
12. [Lizenz](#lizenz)

---

## Einleitung

Das XCORE Framework ist eine vielseitige, modulare Anwendung, die entwickelt wurde, um eine flexible Plattform für verschiedene Aufgaben durch ein System von Plug-in-Modulen bereitzustellen. Es bietet mehrere Schnittstellen (CLI, GUI, Web), um verschiedene Benutzerpräferenzen und Anwendungsfälle zu berücksichtigen, was es an verschiedene Umgebungen und Anforderungen anpassbar macht.

Diese Dokumentation bietet umfassende Informationen über das XCORE Framework, seine Architektur, Funktionalität und wie es mit benutzerdefinierten Modulen erweitert werden kann.

## Projektübersicht

### Zweck

Das XCORE Framework wurde geschaffen, um eine einheitliche Plattform bereitzustellen, auf der verschiedene Funktionalitäten als Module implementiert und über verschiedene Schnittstellen zugänglich gemacht werden können. Dieser Ansatz ermöglicht:

- **Flexibilität**: Benutzer können die Schnittstelle wählen, die am besten zu ihren Bedürfnissen passt
- **Erweiterbarkeit**: Neue Funktionalitäten können hinzugefügt werden, ohne das Kern-Framework zu modifizieren
- **Modularität**: Komponenten sind isoliert, was das System leichter zu warten und zu erweitern macht
- **Konsistenz**: Gemeinsame Funktionalität wird über Schnittstellen hinweg geteilt

### Hauptmerkmale

- **Modulare Architektur**: Funktionalität ist in Modulen organisiert, die bei Bedarf geladen und ausgeführt werden können
- **Mehrere Schnittstellen**: 
  - Kommandozeilenschnittstelle (CLI) für terminalbasierte Bedienung
  - Grafische Benutzeroberfläche (GUI) für Desktop-Benutzer
  - Webschnittstelle für Fernzugriff
  - Setpoint-Modus für Konfigurationsverwaltung
- **Internationalisierung**: Unterstützung für mehrere Sprachen (derzeit Deutsch und Englisch)
- **Benutzerverwaltung**: Authentifizierung und benutzerspezifische Einstellungen
- **Konfigurationsverwaltung**: Zentralisierte Konfiguration durch Umgebungsvariablen
- **Module Creator Tool**: Grafisches Werkzeug zum Erstellen neuer Module

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

### Paket erstellen

Wenn Sie das Paket erstellen und aus der Wheel-Datei installieren möchten:

1. Build-Paket installieren:
   ```bash
   pip install build
   ```

2. Paket erstellen:
   ```bash
   python -m build
   ```

3. Wheel-Datei installieren:
   ```bash
   pip install dist/*.whl
   ```

## Projektstruktur

Das XCORE Framework ist in mehrere Schlüsselverzeichnisse organisiert:

```
xcore_framework/
├── config/             # Konfigurationsdateien
│   ├── i18n/           # Internationalisierungsdateien
│   └── ...
├── core/               # Kernfunktionalität
│   ├── commander.py    # CLI-Implementierung
│   ├── module_loader.py # Modul-Ladesystem
│   ├── module_base.py  # Basisklasse für Module
│   └── ...
├── database/           # Datenbankfunktionalität
├── gui/                # Grafische Benutzeroberfläche
│   ├── gui.py          # Haupt-GUI-Implementierung
│   └── ...
├── modules/            # Modulverzeichnisse
│   ├── ai/             # KI-Module
│   ├── creative/       # Kreative Module
│   ├── ...
│   └── template/       # Modulvorlagen
├── setpoint/           # Konfigurationseditor
│   ├── setpoint_cli.py # CLI-Schnittstelle für Setpoint
│   ├── setpoint_gui.py # GUI-Schnittstelle für Setpoint
│   ├── setpoint_web.py # Web-Schnittstelle für Setpoint
│   └── ...
├── web/                # Webschnittstelle
│   ├── app/            # Flask-Anwendung
│   └── ...
├── .env                # Umgebungsvariablen
└── main.py             # Haupteinstiegspunkt
```

Zusätzlich befinden sich die Entwicklungswerkzeuge und der Frontend-Code in:

```
dev/
├── tools/
│   ├── module_creator.py # Werkzeug zum Erstellen von Modulen
│   └── ...
└── frontend/
    └── web/              # Web-Frontend (React)
        ├── src/          # Quellcode
        └── ...
```

## Betriebsmodi

Das XCORE Framework bietet vier Hauptbetriebsmodi, die jeweils eine andere Schnittstelle für die Interaktion mit der Funktionalität des Frameworks bereitstellen.

### CLI-Modus

Der Kommandozeilenschnittstellen-Modus (CLI) bietet eine textbasierte Schnittstelle für die Interaktion mit dem XCORE Framework. Er ist ideal für Serverumgebungen, Automatisierungsskripte oder Benutzer, die terminalbasierte Arbeitsabläufe bevorzugen.

#### CLI-Modus starten

```bash
xcore --cli
```

#### Hauptmerkmale

- Interaktive Kommandozeile mit Tab-Vervollständigung
- Befehle für Modulverwaltung (search, use, list, info)
- Parameterkonfiguration (set, show options)
- Modulausführung (run)
- Benutzerverwaltung (login, logout, create, delete)
- Konfigurationsverwaltung (save_options, load_options)
- Spracheinstellungen (lang)

#### Häufige Befehle

- `search <Suchbegriff>`: Suche nach Modulen, die den Suchbegriff enthalten
- `use <Modulpfad>`: Lade ein Modul zur Verwendung
- `list`: Liste aller verfügbaren Module
- `info`: Zeige Informationen über das aktuelle Modul
- `show options`: Zeige konfigurierbare Parameter für das aktuelle Modul
- `set <Parameter> <Wert>`: Setze einen Parameterwert
- `run`: Führe das aktuelle Modul mit den konfigurierten Parametern aus
- `back`: Verlasse das aktuelle Modul
- `exit`: Beende die CLI

### GUI-Modus

Der Grafische Benutzeroberflächen-Modus (GUI) bietet eine Desktop-Anwendungsschnittstelle für das XCORE Framework. Er ist für Benutzer konzipiert, die eine visuelle Schnittstelle mit Formularen, Schaltflächen und grafischen Elementen bevorzugen.

#### GUI-Modus starten

```bash
xcore --gui
```

#### Hauptmerkmale

- Benutzerfreundliche Desktop-Anwendung
- Visuelle Modulauswahl und -konfiguration
- Formularbasierte Parametereingabe
- Echtzeit-Feedback während der Modulausführung
- Benutzerauthentifizierung über Anmeldeformulare
- Konsistentes Styling und Layout

#### Schnittstellenkomponenten

- Navigationsseitenleiste für Modulkategorien
- Modulauswahlschnittstelle
- Parameterkonfigurationsformulare
- Konsolenausgabeanzeige
- Benutzerauthentifizierungsformulare

### Web-Modus

Der Webschnittstellen-Modus bietet eine browserbasierte Schnittstelle für das XCORE Framework. Er ermöglicht Fernzugriff auf die Funktionalität des Frameworks und ist ideal für verteilte Teams oder den Zugriff auf das Framework von verschiedenen Geräten aus.

#### Web-Modus starten

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

#### Hauptmerkmale

- Moderne, responsive Webschnittstelle
- RESTful API für Modulverwaltung und -ausführung
- Kategoriebasierte Modulnavigation
- Dynamische Formularerstellung für Modulparameter
- Echtzeit-Feedback während der Modulausführung
- Benutzerauthentifizierung und Sitzungsverwaltung

#### Web-Frontend-Architektur

Das Web-Frontend ist mit modernen Webtechnologien aufgebaut:
- React für die Benutzeroberfläche
- Axios für API-Kommunikation
- Komponentenbasierte Architektur für Wartbarkeit

Schlüsselkomponenten:
- Dashboard: Hauptlayout-Komponente
- XcoreModules: Modulverwaltungskomponente
- CategorySelector: Zur Auswahl von Modulkategorien
- ModuleSelector: Zur Auswahl bestimmter Module
- ModuleDetails: Zur Konfiguration von Modulparametern
- ResultDisplay: Zur Anzeige von Ausführungsergebnissen

#### Web-Backend-Architektur

Das Web-Backend ist mit Flask aufgebaut:
- RESTful API-Endpunkte für Modulverwaltung
- Integration mit dem Kernmodulsystem
- Benutzerauthentifizierung und Sitzungsverwaltung
- Statisches Datei-Serving für das Frontend

Schlüssel-Endpunkte:
- `/api/modules`: Liste aller verfügbaren Module
- `/api/module/<Modulpfad>/meta`: Metadaten für ein bestimmtes Modul abrufen
- `/api/module/<Modulpfad>/run`: Ein Modul mit Parametern ausführen

### Setpoint-Modus

Der Setpoint-Modus bietet einen Konfigurationseditor für das XCORE Framework. Er ermöglicht Benutzern, Umgebungsvariablen zu ändern, die das Verhalten des Frameworks steuern.

#### Setpoint-Modus starten

```bash
xcore --setpoint
```

Optionale Parameter:
- `--interface`: Schnittstelle für den Konfigurationseditor (cli, gui, web) (Standard: gui)

Beispiel:
```bash
xcore --setpoint --interface cli
```

#### Hauptmerkmale

- Bearbeiten von Umgebungsvariablen, die das Framework steuern
- Mehrere Schnittstellenoptionen (CLI, GUI, Web)
- Validierung von Konfigurationswerten
- Sofortige Anwendung von Konfigurationsänderungen

#### Konfigurationsvariablen

Der Setpoint-Modus ermöglicht die Bearbeitung verschiedener Umgebungsvariablen, darunter:
- `XCORE_FRAMEWORK`: Pfad zum Framework-Verzeichnis
- `XCORE_ENV`: Pfad zur .env-Datei
- `XCORE_CONFIG`: Pfad zum Konfigurationsverzeichnis
- `XCORE_I18N`: Pfad zum Internationalisierungsverzeichnis
- `XCORE_CORE`: Pfad zum Core-Verzeichnis
- `XCORE_MODULES`: Pfad zum Modulverzeichnis
- `XCORE_DATABASE`: Pfad zum Datenbankverzeichnis
- `XCORE_WEB_INTERFACE_DIR`: Pfad zum Webschnittstellen-Verzeichnis
- `XCORE_WEB_INTERFACE_URL`: URL für die Webschnittstelle
- `XCORE_LANGUAGE`: Standardsprache für das Framework

## Modulsystem

Die Funktionalität des XCORE Frameworks ist in Modulen organisiert, die in sich geschlossene Einheiten sind, die spezifische Funktionen implementieren. Das Modulsystem ist erweiterbar konzipiert und ermöglicht es Benutzern, eigene Module zu erstellen und hinzuzufügen.

### Modulstruktur

Jedes Modul im XCORE Framework folgt einer Standardstruktur:

- **Modulklasse**: Eine Python-Klasse, die von `XCoreModule` erbt
- **Metadaten**: Informationen über das Modul (Name, Beschreibung, Autor, Version, etc.)
- **Optionen**: Konfigurierbare Parameter für das Modul
- **Run-Methode**: Die Hauptausführungslogik des Moduls
- **Feedback-Methode**: Für die Ausgabe während der Ausführung

### Modulkategorien

Module sind nach ihrer Funktionalität in Kategorien organisiert:

- **ai**: Module für künstliche Intelligenz und maschinelles Lernen
- **creative**: Module für kreative Anwendungen
- **exploitation**: Module für Sicherheitstests und Exploitation
- **helper**: Hilfsmodule für verschiedene Aufgaben
- **monitor**: Module zur Überwachung von Systemen und Netzwerken
- **osint**: Module für Open Source Intelligence
- **persistence**: Module für Datenpersistenz
- **scanner**: Module zum Scannen von Netzwerken und Systemen
- **system**: Module für Systemoperationen
- **template**: Vorlagen für die Erstellung neuer Module
- **transfer**: Module für Datenübertragung
- **utilities**: Allgemeine Dienstprogramme

### Eigene Module erstellen

Um ein eigenes Modul für das XCORE Framework zu erstellen, können Sie die Vorlage in `xcore_framework/modules/template/modul.py` als Ausgangspunkt verwenden. Jedes Modul muss eine `Module`-Klasse enthalten, die von `XCoreModule` erbt und die erforderlichen Methoden implementiert.

#### Grundlegende Modulstruktur

```python
from xcore_framework.config.i18n import i18n
from xcore_framework.core.module_base import XCoreModule

class Module(XCoreModule):
    def __init__(self):
        super().__init__()

    name = i18n.t("module_name.modul_name")
    description = i18n.t("module_name.modul_desc")
    author = "Ihr Name"
    version = "1.0.0"
    created = "01.01.2025"
    options = {
        "option1": {
            "widget_type": "entry",
            "required": True,
            "default": "default_value",
            "desc": i18n.t("module_name.option_option1_desc")
        }
    }

    def run(self, params: dict, mode="cli", gui_console=None) -> dict | None:
        self.mode = mode
        self.console_widget = gui_console
        self.feedback([i18n.t("module_name.modul_headline")])

        try:
            for key in self.options:
                val = params.get(key, self.options[key].get("default"))
                self.feedback([f"{key}: {val}"])

            # Hauptlogik des Moduls hier

            self.feedback([i18n.t("module_name.modul_done_message")])
            return {"success": True, "output": self.output, "data": self.results}

        except Exception as e:
            msg = i18n.t("module_name.modul_error", error=e)
            self.feedback([msg])
            return {"success": False, "error": msg, "output": [msg]}
```

#### Moduloptionen

Moduloptionen definieren die konfigurierbaren Parameter für ein Modul. Jede Option hat mehrere Eigenschaften:

- **widget_type**: Der Typ des Eingabe-Widgets (entry, checkbox, radiobutton, etc.)
- **required**: Ob die Option erforderlich ist
- **default**: Der Standardwert für die Option
- **desc**: Eine Beschreibung der Option
- **values**: Für radiobutton- und listbox-Typen die verfügbaren Werte
- **min/max**: Für scale- und spinbox-Typen die Minimal- und Maximalwerte

#### Internationalisierung

Module sollten das Internationalisierungssystem für benutzerseitige Zeichenketten verwenden. Dies ermöglicht die Verwendung des Moduls in verschiedenen Sprachen ohne Codeänderungen.

#### Modulplatzierung

Benutzerdefinierte Module sollten im entsprechenden Kategorieverzeichnis unter `xcore_framework/modules/` platziert werden. Ein Modul für Bildverarbeitung könnte beispielsweise in `xcore_framework/modules/creative/` platziert werden.

### Verwendung des Module Creators

Das XCORE Framework enthält ein grafisches Werkzeug zum Erstellen von Modulen, das sich unter `dev/tools/module_creator.py` befindet. Dieses Werkzeug vereinfacht den Prozess der Erstellung neuer Module, indem es eine benutzerfreundliche Oberfläche für die Definition von Modulmetadaten, Optionen und Internationalisierungszeichenketten bereitstellt.

#### Module Creator starten

Um den Module Creator zu starten, führen Sie aus:

```bash
python dev/tools/module_creator.py
```

#### Hauptmerkmale

- **Grafische Oberfläche**: Kein manuelles Schreiben von Code erforderlich
- **Modulmetadaten**: Name, Beschreibung, Autor und Version definieren
- **Optionsverwaltung**: Moduloptionen hinzufügen, bearbeiten und entfernen
- **Widget-Typ-Auswahl**: Aus verschiedenen Eingabe-Widget-Typen wählen
- **Internationalisierungsunterstützung**: Automatisch Übersetzungsdateien generieren
- **Code-Generierung**: Modulcode basierend auf den definierten Metadaten und Optionen generieren

#### Verwendung des Module Creators

1. **Modulmetadaten eingeben**:
   - Modulname: Der Name des Moduls (verwendet für den Modulpfad)
   - Beschreibung: Eine kurze Beschreibung des Moduls
   - Autor: Ihr Name oder Ihre Organisation
   - Version: Die Modulversion (Standard: 1.0.0)
   - Speicherpfad: Wo die generierte Moduldatei gespeichert werden soll

2. **Moduloptionen hinzufügen**:
   - Name: Der Optionsname (im Code verwendet)
   - Standard: Der Standardwert
   - Beschreibung: Eine Beschreibung der Option
   - Widget-Typ: Der Typ des Eingabe-Widgets
   - Erforderlich: Ob die Option erforderlich ist
   - Zusätzliche Eigenschaften basierend auf dem Widget-Typ (Werte, Min/Max, etc.)

3. **Übersetzungssätze hinzufügen**:
   - Sätze eingeben, die automatisch zu den Übersetzungsdateien hinzugefügt werden
   - Diese Sätze werden über das i18n-System zugänglich sein

4. **Modul generieren**:
   - Auf "Modul generieren" klicken, um die Moduldatei und Übersetzungsdateien zu erstellen
   - Das Modul wird im angegebenen Pfad gespeichert
   - Übersetzungsdateien werden in den entsprechenden Sprachverzeichnissen erstellt

#### Übersetzungsunterstützung

Der Module Creator generiert automatisch Übersetzungsdateien für Deutsch und Englisch. Er verwendet die Google Translate API, um Zeichenketten von Deutsch nach Englisch zu übersetzen, wodurch sichergestellt wird, dass Ihr Modul für Benutzer beider Sprachen zugänglich ist.

## Internationalisierung

Das XCORE Framework enthält ein umfassendes Internationalisierungssystem (i18n), das die Verwendung der Anwendung in verschiedenen Sprachen ermöglicht. Derzeit werden Deutsch und Englisch unterstützt.

### Sprachdateien

Übersetzungszeichenketten werden in JSON-Dateien in den Verzeichnissen `xcore_framework/config/i18n/<Sprachcode>/` gespeichert. Jedes Modul oder jede Komponente kann eine eigene Übersetzungsdatei haben.

### Verwendung von Übersetzungen

Um Übersetzungen im Code zu verwenden, importieren Sie das i18n-Objekt und verwenden Sie die `t`-Methode:

```python
from xcore_framework.config.i18n import i18n

# Eine Übersetzungszeichenkette abrufen
übersetzte_zeichenkette = i18n.t("schlüssel.unterschlüssel")

# Eine Übersetzung mit Variablenersetzung abrufen
übersetzte_zeichenkette = i18n.t("schlüssel.unterschlüssel", variable=wert)
```

### Ändern der Sprache

Um die Sprache zur Laufzeit zu ändern, verwenden Sie die `set_language`-Methode:

```python
from xcore_framework.config.i18n import i18n

# Zu Englisch wechseln
i18n.set_language('en')

# Zu Deutsch wechseln
i18n.set_language('de')
```

### Neue Übersetzungen hinzufügen

Um Übersetzungen für ein neues Modul hinzuzufügen:

1. Erstellen Sie JSON-Dateien in den Sprachverzeichnissen
2. Fügen Sie Übersetzungsschlüssel und -werte für jede Sprache hinzu
3. Verwenden Sie die Schlüssel in Ihrem Modulcode

Das Module Creator-Tool kann diesen Prozess für neue Module automatisieren.

## Konfiguration

Das XCORE Framework verwendet Umgebungsvariablen für die Konfiguration. Diese Variablen können in der `.env`-Datei oder über den Setpoint-Modus festgelegt werden.

### Umgebungsvariablen

Zu den wichtigsten Umgebungsvariablen gehören:

- `XCORE_FRAMEWORK`: Pfad zum Framework-Verzeichnis
- `XCORE_ENV`: Pfad zur .env-Datei
- `XCORE_CONFIG`: Pfad zum Konfigurationsverzeichnis
- `XCORE_I18N`: Pfad zum Internationalisierungsverzeichnis
- `XCORE_CORE`: Pfad zum Core-Verzeichnis
- `XCORE_MODULES`: Pfad zum Modulverzeichnis
- `XCORE_DATABASE`: Pfad zum Datenbankverzeichnis
- `XCORE_WEB_INTERFACE_DIR`: Pfad zum Webschnittstellen-Verzeichnis
- `XCORE_WEB_INTERFACE_URL`: URL für die Webschnittstelle
- `XCORE_LANGUAGE`: Standardsprache für das Framework

### Konfigurationsverwaltung

Der Setpoint-Modus bietet eine benutzerfreundliche Schnittstelle zur Verwaltung dieser Konfigurationsvariablen. Siehe den Abschnitt [Setpoint-Modus](#setpoint-modus) für Details.

## Entwicklung

### Einrichten einer Entwicklungsumgebung

1. Repository klonen
2. Abhängigkeiten installieren
3. Umgebungsvariablen einrichten
4. Anwendung im gewünschten Modus ausführen

### Entwicklungsworkflow

1. Änderungen am Code vornehmen
2. Änderungen im entsprechenden Modus testen
3. Bei Bedarf Dokumentation aktualisieren
4. Pull-Request einreichen

### Neue Funktionen hinzufügen

Neue Funktionen sollten wann immer möglich als Module implementiert werden. Dies hält das Kern-Framework sauber und wartbar.

## Vision

Das XCORE Framework ist ein Projekt mit großem Entwicklungspotenzial. Diese Vision skizziert zukünftige Entwicklungsmöglichkeiten und Verbesserungen, die im Laufe der Zeit umgesetzt werden könnten.

### Websicherheit

- Implementierung fortschrittlicher Sicherheitsmaßnahmen für die Webschnittstelle
- HTTPS-Unterstützung mit automatischer Zertifikatsverwaltung
- Verbesserte Authentifizierung und Autorisierung
- Schutz vor gängigen Webangriffsvektoren (XSS, CSRF, SQL-Injection)
- Sicherheitsaudits und Penetrationstests

### Webkomponenten-Optimierung

- Leistungsoptimierung der React-Komponenten
- Implementierung von Code-Splitting und Lazy Loading
- Verbesserung der Benutzererfahrung durch optimierte Ladezeiten
- Responsive Design-Verbesserungen für verschiedene Geräte
- Barrierefreiheit nach WCAG-Standards

### SCSS/CSS-Optimierung

- Umstellung auf SCSS für bessere Wartbarkeit
- Implementierung eines konsistenten Design-Systems
- Optimierung der CSS-Selektoren für bessere Leistung
- Reduzierung der CSS-Dateigröße durch Minimierung
- Verbesserte Animationen und Übergänge

### GUI-Entwicklung in PyQT

- Neuimplementierung der GUI mit PyQT für verbesserte Leistung
- Konsistentes Design zwischen allen Betriebssystemen
- Erweiterte Benutzeroberflächen-Funktionen
- Verbesserte Grafikunterstützung
- Anpassbare Themes und Layouts

### Erweiterte Speicher- und Ladefunktionen

- Integration der Speicher- und Ladefunktionen in alle Betriebsmodi
- Unterstützung für verschiedene Dateiformate (JSON, YAML, XML)
- Automatische Sicherung und Wiederherstellung von Sitzungen
- Cloud-Synchronisierung von Konfigurationen und Ergebnissen
- Versionierung von gespeicherten Daten

### Modulexport und -integration

- Export von Modulen als eigenständige Service-Units
- Systemintegration von Modulen für automatisierte Ausführung
- Kombination verschiedener Module zu komplexen Workflows
- API-Schnittstellen für externe Anwendungen
- Containerisierung von Modulen für einfache Bereitstellung

### Persönliche Anmerkung

Das XCORE Framework ist ein Projekt, das aus Freude an der Entwicklung entstanden ist und nicht in einem beruflichen Kontext entwickelt wird. Es gibt sicherlich viel Optimierungspotenzial in verschiedenen Bereichen des Projekts, und ich bin für jede Rückmeldung und Hilfe dankbar.

Als Hobbyprojekt entwickelt sich das Framework in einem Tempo, das mit meiner verfügbaren Zeit vereinbar ist. Ich freue mich über Beiträge, Vorschläge und Feedback von der Community, um das Projekt kontinuierlich zu verbessern und zu erweitern.

## Beitragen

Beiträge zum XCORE Framework sind willkommen! Hier sind einige Möglichkeiten, wie Sie beitragen können:

1. **Fehler melden**: Erstellen Sie ein Issue im GitHub-Repository, wenn Sie einen Fehler finden
2. **Funktionen vorschlagen**: Haben Sie eine Idee für eine neue Funktion? Erstellen Sie ein Issue mit Ihrem Vorschlag
3. **Code beitragen**: Forken Sie das Repository, nehmen Sie Ihre Änderungen vor und erstellen Sie einen Pull-Request
4. **Module erstellen**: Erstellen Sie neue Module, um die Funktionalität des Frameworks zu erweitern
5. **Dokumentation verbessern**: Helfen Sie, die Dokumentation zu verbessern, um das Framework zugänglicher zu machen

## Lizenz

- **Code**: MIT-Lizenz – siehe [LICENSE](../LICENSE) für Details
- **Medieninhalte**: CC BY 4.0 – siehe [Creative Commons](https://creativecommons.org/licenses/by/4.0/) für Details

---

## written on the dark side of toast 🍞🌚  
#### © 2025, [Xeniorn](https://xeniorn.de) | [`x404bjrn`](https://github.com/x404bjrn)

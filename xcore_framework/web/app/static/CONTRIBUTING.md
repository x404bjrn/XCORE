![DE](https://img.shields.io/badge/DE-green?style=for-the-badge)
[![EN](https://img.shields.io/badge/EN-blue?style=for-the-badge)](https://github.com/x404bjrn/XCORE/blob/main/docs/CONTRIBUTING_EN.md)

# 🤝 Beitrag leisten zu XCORE-Framework

---

Vielen Dank, dass du dich für einen Beitrag zum **XCORE-Framework** interessierst!  
Dieses Projekt befindet sich noch in der aktiven Entwicklung – jede Hilfe ist willkommen, egal ob Code, Tests, Doku oder einfach nur Feedback!

---

## 📋 Inhaltsverzeichnis

1. [Wie du beitragen kannst](#-wie-du-beitragen-kannst)
2. [Grundregeln](#-grundregeln)
3. [Lokales Setup](#-lokales-setup)
4. [Issues & Pull Requests](#-issues--pull-requests)
5. [Code-Stil](#-code-stil)
6. [Kontakt](#-kontakt)

---

## ✅ Wie du beitragen kannst

Du kannst auf verschiedene Arten mithelfen:

- 🔧 **Fehler melden** (`Bug Reports`)
- 💡 **Feature-Vorschläge** einreichen
- 🛠️ **Code beisteuern** (Module, Verbesserungen)
- 🧪 **Tests schreiben**
- 📚 **Dokumentation verbessern**
- 🌍 **Übersetzungen hinzufügen**

---

## 📌 Grundregeln

- Sei freundlich und respektvoll – egal auf welcher Plattform.
- Nutze die `issues`, um Ideen, Fehler oder Fragen zu diskutieren.
- Schreibe klare, nachvollziehbare Commits (z. B. mit `feat:`, `fix:`, `docs:` Prefix).
- Halte dich an den Stil des Projekts – der Code soll für andere verständlich bleiben.

---

## 🛠️ Lokales Setup

Falls du lokal beitragen willst:


### Projekt klonen
```
git clone https://github.com/x404bjrn/XCORE.git
cd XCORE
```

### Empfohlen: PDM (Python Dependency Manager)
PDM ist das bevorzugte Tool für die Verwaltung von Abhängigkeiten in diesem Projekt. Es bietet eine bessere Isolierung, genauere Abhängigkeitsverwaltung und vereinfacht die Entwicklungsworkflows.

#### PDM installieren (falls noch nicht vorhanden)
```
pip install pdm
```

#### Abhängigkeiten mit PDM installieren
```
pdm install
```

#### PDM-Umgebung aktivieren
```
# Für eine Shell-Sitzung
pdm run <command>

# Oder eine neue Shell mit aktivierter PDM-Umgebung starten
pdm shell
```

#### Nützliche PDM-Befehle
```
pdm add <package>        # Neue Abhängigkeit hinzufügen
pdm remove <package>     # Abhängigkeit entfernen
pdm update               # Alle Abhängigkeiten aktualisieren
pdm run tests            # Tests ausführen
pdm run export-req       # requirements.txt generieren
```

### Alternative: Klassische virtuelle Umgebung
Falls du PDM nicht verwenden möchtest:
```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### (Optional) Frontend einrichten
```
cd dev/frontend/web
npm install
npm run dev
```

## 🔄 Issues & Pull Requests

- Erstelle ein Issue, bevor du größere Änderungen vornimmst.
- Forke das Repo und arbeite in einem separaten Branch (`feature/dein-thema`).
- Schreibe eine aussagekräftige Beschreibung zum PR.
- Vermeide unnötige Commits wie `fix typo` oder `test123`.
- Teste deine Änderungen lokal.

## 🎨 Code-Stil

- Python: PEP8-konform (z. B. via `black`, `mypy`, `flake8`)
- React: möglichst konsistent, einfache Komponentenstruktur
- Schreibe Kommentare, wenn dein Code nicht selbsterklärend ist
- Variablen & Funktionen bitte auf Englisch benennen

## 📬 Kontakt

Wenn du Fragen hast oder Feedback geben möchtest, melde dich gern:

- GitHub Issues oder Discussions
- Mail: [void@insomnialegion.xyz](mailto:void@insomnialegion.xyz)

Danke fürs Mitwirken! 🚀
Gemeinsam machen wir XCORE zu einem mächtigen und smarten Framework für CLI, GUI und Web.

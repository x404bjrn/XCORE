# 📦 Changelog

## 0.1.0a3 (2025-06-23)

### 📝 Dokumentation

* aktualisiere Dokumentation ([67e6754](https://github.com/x404bjrn/XCORE/commit/67e6754e4048ed9662693fb57575df958c5b3284))
* entferne duplizierten Dokumentationseintrag aus CHANGELOG ([66450bd](https://github.com/x404bjrn/XCORE/commit/66450bddb060e2a0ca44fa3a8eb3ba293d417d7e))
* zweisprachiger Verhaltenskodex und Beitragsrichtlinien hinzugefügt ([d1d6d9d](https://github.com/x404bjrn/XCORE/commit/d1d6d9d5f63c401e629fdba7456ec18b53c65625))

### ✨ Features

* **cli:** erweitere Banner um neue Module und Versionsanzeige
* **database:** füge Methode `get_all_users` hinzu
* **design:** SCSS-Architektur, CSS-Stylesheets, SVG-Logo für Webinterface
* **devcontainer:** Dockerfile + Konfiguration hinzugefügt
* **frontend:** Footer, Navbar, neue Seiten, Sidelist, Webinterface-Basisstruktur, Modul-Komponenten
* **gui:** grafische Benutzeroberfläche + dynamische Widget-Erstellung
* **i18n:** deutsche und englische Konfigurationen
* **main:** CLI, GUI und Web-Support
* **modules:** neue Struktur mit dynamischen Optionen, Template-Modul
* **release:** Versionen aktualisiert (0.1.0a1 → 0.1.0a2 → 0.1.0), Integration in `__init__.py`
* **scripts:** Dokumentkopie, Versions-Sync, Automatisierung
* **setpoint:** CLI/GUI/Web Integration
* **test:** Tests für DatabaseManager, I18nManager, ModuleLoader
* **tools:** GUI-Modulgenerator für XCORE
* **web:** Backend-Infrastruktur + Ladezeitoptimierung

### 🧹 Refactoring

* **cli/banner:** Docstrings, i18n-Schlüssel
* **cli/commands:** Erweiterung von Befehlen (`save`, `load`)
* **cli/i18n:** bessere Konsistenz
* **core:** Fehlerbehandlung, Docstrings
* **i18n:** Struktur verbessert, alte Dateien entfernt
* **main:** Funktionsnamen und Argumente vereinheitlicht
* **setpoint:** Funktionsnamen für alle Interfaces angeglichen

---

## 0.1.0a2 (2025-06-19)

### 📝 Dokumentation

* README.md aktualisiert
* Verlinkungen in README und Dokumentation optimiert

---

## 0.1.0a0 (2025-06-18)

### 📝 Dokumentation

* Dokumentation auf Deutsch und Englisch hinzugefügt

### ✨ Features

* **cli:** Willkommensbanner
* **context:** AuthContext, ThemeContext
* **core:** CLI-Shell, DB-Manager
* **design:** ASCII-Art, Favicon, SCSS, Logo
* **frontend:** Basiskomponenten und Struktur
* **gui:** Anmelde-/Registrierungsmaske
* **modules:** Modulstruktur, Template
* **scripts:** Pyproject-Version, Doc-Kopie
* **web:** Grund-API, Modul-Preloading
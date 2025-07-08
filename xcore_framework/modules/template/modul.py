# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
from xcore_framework.config.i18n import i18n
from xcore_framework.core.module_base import XCoreModule


class Module(XCoreModule):
    """
    Repräsentiert ein Modul zur dynamischen Konfiguration und Verarbeitung von Parametern.

    Das Modul bietet eine flexible Schnittstelle zur Erfassung, Validierung und Verarbeitung
    von Konfigurationsparametern in verschiedenen Modi wie CLI und GUI. Es vereinfacht die
    dynamische Anpassung von Verhaltensweisen durch unterschiedliche Parameteroptionen,
    wie Texteingabe, Schieberegler und Auswahllisten. Durch die Möglichkeit der Fehlerbehandlung
    und Rückmeldungen ist es für eine Vielzahl von Anwendungen geeignet.

    Attributes:
        name: Der Name des Moduls. Wird durch Internationalisierung abgeleitet.
        description: Beschreibung des Moduls, die den Funktionsumfang angibt.
        author: Der Autor des Moduls.
        version: Die aktuelle Moduldarstellungsversion.
        created: Das Erstellungsdatum des Moduls.
        options: Ein Wörterbuch, welches die verfügbaren Konfigurationsparameter und
            ihre Eigenschaften wie Typ, Standardwerte und Beschreibungen definiert.
    """

    def __init__(self):
        """
        Repräsentiert einen Initialisierungskonstruktor für eine Klasse, der die
        Basisklasse aufruft.
        """
        super().__init__()

        # Logger initialisieren
        self.init_logging(name=i18n.t("template_modul.modul_name"))

    name = i18n.t("template_modul.modul_name")
    description = i18n.t("template_modul.modul_desc")
    author = "Björn Häusermann | x404bjrn"
    version = "2.0.0"
    created = "28.05.2025"
    options = {
        "example_entry": {
            "widget_type": "entry",
            "required": True,
            "default": "default text",
            "desc": i18n.t("template_modul.modul_option_example_entry_desc"),
        },
        "enable_feature": {
            "widget_type": "checkbox",
            "required": False,
            "default": "False",
            "desc": i18n.t("template_modul.modul_option_enable_feature_desc"),
        },
        "color_choice": {
            "widget_type": "radiobutton",
            "required": False,
            "default": "Blau",
            "values": ["Rot", "Grün", "Blau"],
            "desc": i18n.t("template_modul.modul_option_color_choice_desc"),
        },
        "security_level": {
            "widget_type": "listbox",
            "required": False,
            "default": "Mittel",
            "values": ["Niedrig", "Mittel", "Hoch"],
            "desc": i18n.t("template_modul.modul_option_security_level_desc"),
        },
        "thread_count": {
            "widget_type": "spinbox",
            "required": False,
            "default": 3,
            "min": 1,
            "max": 10,
            "desc": i18n.t("template_modul.modul_option_thread_count_desc"),
        },
        "size_percentage": {
            "widget_type": "scale",
            "required": False,
            "default": 50,
            "min": 0,
            "max": 100,
            "desc": i18n.t("template_modul.modul_option_size_percentage_desc"),
        },
        "config_path": {
            "widget_type": "fileexplorer",
            "required": False,
            "default": "",
            "desc": i18n.t("template_modul.modul_option_config_path_desc"),
        },
    }

    def run(self, params: dict, mode="cli", gui_console=None) -> dict | None:
        """
        Führt die Hauptlogik des Moduls aus und setzt Parameter entsprechend den übergebenen
        Einstellungen. Bietet Unterstützung sowohl für CLI- als auch für GUI-Modi.

        Args:
            params (dict): Ein Wörterbuch von Parametern, das die Einstellungen für
                die Modulausführung enthält.
            mode (str): Optionale Angabe des Ausführungsmodus. Standardmäßig "cli".
            gui_console: Optionale GUI-Konsole für Textausgabe. Standardmäßig None.

        Returns:
            dict | None: Gibt ein Wörterbuch zurück, das den Erfolg, mögliche Fehlermeldungen,
                Ausgaben und Ergebnisse enthält, oder None, wenn keine Ergebnisse vorliegen.

        Raises:
            Exception: Wenn ein unerwarteter Fehler während der Modulausführung auftritt.
        """
        # Modul Logging
        self.log("Modul gestartet")

        # Ausführungsmodus
        self.mode = mode

        # Textausgabeobjekt des GUI
        self.console_widget = gui_console

        # Modul-Überschrift / Headline
        self.feedback([i18n.t("template_modul.modul_headline")])

        # Modulhauptroutinen Bereich (Beispielaktion)
        try:
            self.feedback(["🧪 start demo-mode.."])
            for key in self.options:
                # Holen der Parameter-Werte
                val = params.get(key, self.options[key].get("default"))
                self.feedback([f"{key}: {val}"])

        # Fehlerbehandlung
        except Exception as e:
            msg = i18n.t("template_modul.modul_error", error=e)
            self.feedback([msg])

            # Fehler Logging
            self.log(msg, level="error")

            return {"success": False, "error": msg, "output": [msg]}

        # Ergebnis / Abschluss (Modulskript Ende) Bereich
        self.feedback([i18n.t("template_modul.modul_done_message")])
        self.log("Modul wurde ausgeführt")

        print()
        return {"success": True, "output": self.output, "data": self.results}

# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
from xcore_framework.config.formatting import strip_ansi
from xcore_framework.core.logger import setup_logger


class XCoreModule:
    """
    Repräsentiert ein Kernmodul mit Logging-, Feedback- und Betriebsmodi-Funktionalitäten.

    Diese Klasse bietet grundlegende Funktionen für Protokollierung und Feedback-Mechanismen
    basierend auf verschiedenen Betriebsarten (CLI, Web, GUI). Sie dient als Basis, um die
    Kommunikation zwischen unterschiedlichen Modulen und Benutzerschnittstellen zu verwalten.

    Attributes:
        name (str): Der Name des Moduls zur Identifizierung in den Protokollen.
        logger: Logger-Instanz für die Protokollierung von Nachrichten.
        output (list): Liste für die Speicherung der Ausgabe, z. B. für den Web-Modus.
        results (list): Liste zur Speicherung und Weitergabe von Web-Ergebnissen.
        mode (str): Betriebsmodus des Moduls ('cli', 'web', 'gui').
        console_widget: Widget für GUI-Interaktionen zur Anzeige von Ausgaben.
    """

    def __init__(self):
        self.name = None
        self.logger = None
        self.output = []
        self.results = []
        self.mode = ""
        self.console_widget = None


    def init_logging(self, name):
        """
        Initialisiert das Logging für das angegebene Modul und erstellt einen Logger.

        Das Modul wird mit einem benannten Logger eingerichtet. Der Logger wird verwendet,
        um Debugging-Informationen und weitere Log-Einträge für das spezifizierte Modul
        zu verwalten.

        Args:
            name: Der Name des Moduls, das geloggt werden soll. Wird zur Identifikation
                  des Loggers verwendet.
        """
        self.name = strip_ansi(name)
        self.logger = setup_logger(self.name, con_handler=False)
        self.logger.debug(f"Initialisiere Modul {self.name}")


    def log(self, msg, level="info"):
        """
        Schreibt eine Protokollnachricht mit dem angegebenen Niveau.

        Die Methode ermöglicht das Protokollieren von Nachrichten auf verschiedenen
        Protokollstufen, um die Zustände und Ereignisse in der Anwendung festzuhalten.

        Args:
            msg: Die Nachricht, die protokolliert werden soll.
            level: Das Protokollstufen-Level für die Nachricht. Standard ist "info".
        """
        # ANSI Formatierungen vom String entfernen
        msg = strip_ansi(msg)

        if level == "debug":
            self.logger.debug(msg)

        elif level == "warning":
            self.logger.warning(msg)

        elif level == "error":
            self.logger.error(msg)

        else:
            self.logger.info(msg)


    def feedback(self, output: list = None, result: dict = None):
        """
        Führt eine Feedback-Funktionalität durch, abhängig von der Betriebsart (CLI, Web, GUI)
        und verarbeitet die gelieferte Ausgabe bzw. Ergebnisse entsprechend.

        Wenn `output` bereitgestellt wird, wird diese abhängig vom Modus auf der Konsole
        ausgegeben und für Web- oder GUI-Modi verarbeitet. ANSI-Formatierungen werden bei
        Bedarf entfernt. Wenn `result` bereitgestellt wird und der Modus auf 'web' gesetzt ist,
        wird das Ergebnis an die Webschnittstelle übergeben.

        Args:
            output (list): Eine Liste von Zeichenketten, die als Ausgabe verarbeitet werden
                           sollen. Jede Zeichenkette repräsentiert eine einzelne Zeile
                           der Ausgabe.
            result (dict): Ein optionales Wörterbuch, das Ergebnisdaten enthält, die für den
                           Web-Modus weitergegeben werden sollen.
        """
        if output is not None:
            for line in output:
                # Konsolenausgabe CLI (auch im Web- & GUI-Modus)
                print(line)

                # Löschen der ANSI-Formatierung (für Web- & GUI-Modus)
                line = strip_ansi(line)

                # Web (ResultDisplay)
                if self.mode == "web":
                    self.output.append(line)

                # GUI (ResultDisplay)
                elif self.mode == "gui" and self.console_widget is not None:
                    self.console_widget.configure(state="normal")
                    self.console_widget.insert("end", line + "\n")
                    self.console_widget.update()
                    self.console_widget.see("end")  # automatisch scrollen
                    self.console_widget.configure(state="disabled")

        if result is not None and self.mode == "web":
            # Web (Ergebnisübergabe)
            self.results.append(result)

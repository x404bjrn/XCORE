# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
from xcore_framework.config.formatting import strip_ansi


class XCoreModule:
    """
    Eine Basisklasse für die Verwaltung von Modulen im CLI-, GUI- und Web-Modus.

    Die Klasse stellt Mechanismen bereit, um Ausgaben und Ergebnisdaten je nach
    Modus (CLI, GUI oder Web) zu verarbeiten und auszugeben. Dabei wird die Ausgabe
    im Web-Modus entsprechend formatiert, und GUI-Komponenten können angepasst werden.
    Die Klasse ermöglicht eine flexible Handhabung von Ausgabetypen und stellt die
    Integration mit verschiedenen Benutzerschnittstellen bereit.

    Attribute:
    - output: Liste der verarbeiteten Ausgaben (nur relevant im Web-Modus).
    - results: Liste der im Web-Modus gespeicherten Ergebnisdaten.
    - mode: Modus der Anwendung (z. B. "web", "gui" oder leer für CLI).
    - console_widget: Referenz auf ein Widget zur Konsolenausgabe im GUI-Modus.
    """

    def __init__(self):
        self.output = []
        self.results = []
        self.mode = ""
        self.console_widget = None

    def feedback(self, output: list = None, result: dict = None):
        """
        Sendet Rückmeldungen im CLI- und/oder Web-Modus.

        Diese Methode verarbeitet eine Liste von Ausgaben und/oder ein Ergebnisobjekt.
        Wenn eine Ausgabe angegeben wird, wird jeder Eintrag in der Liste ausgegeben
        und gegebenenfalls im Web-Modus entsprechend behandelt.
        Ebenso wird ein übergebenes Ergebnis im Web-Modus gespeichert.

        :param output: Liste mit Ausgaben, die ggf. verarbeitet und ausgegeben werden sollen
        :type output: list, optional
        :param result: Ergebnisdaten, die ggf. im Web-Modus gespeichert werden sollen
        :type result: dict, optional
        :return: Es wird kein Wert zurückgegeben
        :rtype: None
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

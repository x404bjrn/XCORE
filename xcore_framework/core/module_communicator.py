# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
from xcore_framework.config.formatting import strip_ansi


class ResultFeedbackSystem:
    def __init__(self):
        self.output = []
        self.results = []
        self.mode = ""
        self.console_widget = None


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

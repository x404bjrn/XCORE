# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import argparse
import webbrowser
import subprocess
import sys

from xcore_framework.core.initializer import initialize
from xcore_framework.config.env import DIRECTORY_WEB_INTERFACE_DIR
from xcore_framework.config.i18n import i18n
from xcore_framework.config.banner import show_banner


class CustomHelp(argparse.ArgumentParser):
    """
    Eine benutzerdefinierte Erweiterung von argparse.ArgumentParser.

    Diese Klasse ersetzt die Standardhilfefunktion durch eine angepasste
    Ausgabe. Die neue Hilfsfunktion fügt eine zusätzliche benutzerdefinierte
    Nachricht hinzu, bevor die reguläre Hilfeausgabe der Basisklasse angezeigt
    wird. Sie kann in Anwendungen verwendet werden, um die Benutzerfreundlichkeit
    durch individuellere Hilfetexte zu verbessern.

    Attributes:
        Keine besonderen Attribute definiert.

    Methods:
        print_help(*args, **kwargs):
            Überschreibt die Hilfsmethode, um eine benutzerdefinierte Nachricht
            vor der Standardausgabe der Basisklasse hinzuzufügen.
    """

    def print_help(self, *args, **kwargs):
        print(i18n.t("main.help_title"))
        super().print_help(*args, **kwargs)


def start_web(host="127.0.0.1", port=5000, debug=True, open_browser=True):
    """
    Startet die Web-Schnittstelle unter einem angegebenen Host und Port. Die Methode erlaubt es,
    den Modus (Debug) zu konfigurieren und optional einen Webbrowser mit der Schnittstellen-URL
    zu öffnen. Es wird das Flask-Server-Skript ausgeführt, das die API bereitstellt.

    :param host: Die Host-Adresse, unter der der Dienst erreichbar ist.
    :param port: Der Port, auf dem der Dienst verfügbar ist.
    :param debug: Aktiviert den Debug-Modus, wenn True.
    :param open_browser: Öffnet standardmäßig nach dem Start der Schnittstelle einen Webbrowser.
    :return: Keiner. Der Prozess wird gestartet und gewartet, bis er beendet wird.
    """
    initialize()
    run_path = os.path.join(DIRECTORY_WEB_INTERFACE_DIR, "run.py")
    cmd = [sys.executable, run_path]

    if debug:
        cmd.append("--debug")
    if host != "127.0.0.1":
        cmd.append("--host")
        cmd.append(host)
    if port != 5000:
        cmd.append("--port")
        cmd.append(f"{port}")

    # Starte Flask Server
    process = subprocess.Popen(cmd)

    # Browser öffnen (optional)
    if open_browser:
        webbrowser.open(f"http://{host}:{port}")
    process.wait()


def start_cli():
    """
    Startet die Kommandozeilenschnittstelle (CLI) mithilfe der Funktion `start_cli`
    aus dem Modul `xcore_framework.core.commander`.

    Diese Funktion dient als Startpunkt für die CLI und ruft die zugrundeliegende
    Implementierung auf, die im Framework enthalten ist.

    :return: None
    """
    from xcore_framework.core.commander import start_cli

    initialize()
    start_cli()


def start_gui():
    """
    Startet die grafische Benutzeroberfläche (GUI) der Anwendung.

    Zusammenfassung:
    Diese Funktion importiert und ruft die `start_gui`-Funktion aus dem Modul
    `xcore_framework.gui.gui` auf, um die grafische Benutzeroberfläche zu initialisieren
    und zu starten.

    Raises:
    ImportError: Wird ausgelöst, wenn das Modul `xcore_framework.gui.gui` nicht gefunden
    werden kann.
    """
    from xcore_framework.gui.gui import start_gui

    initialize()
    start_gui()


def start_setpoint(mode="gui"):
    """
    Führt den Start einer Setpoint-Konfiguration basierend auf dem angegebenen Modus aus.

    Diese Funktion ermöglicht es, basierend auf dem ausgewählten Modus (CLI, GUI oder Web)
    die entsprechende Setpoint-Konfiguration zu initialisieren.
    Wird ein ungültiger Modus übergeben, wird eine Fehlermeldung ausgegeben.

    Args:
        mode (str): Der Modus der Konfiguration. Unterstützte Werte sind "cli", "gui" und "web".
            Der Standardwert ist "gui".

    Raises:
        ImportError: Wenn der Import des entsprechenden Moduls fehlschlägt.
        Exception: Bei Ausführung eines nicht unterstützten Modus.
    """
    initialize()
    if mode == "cli":
        from xcore_framework.setpoint.setpoint_cli import start_cli_setpoint

        start_cli_setpoint()
    elif mode == "gui":
        from xcore_framework.setpoint.setpoint_gui import start_gui_setpoint

        start_gui_setpoint()
    elif mode == "web":
        from xcore_framework.setpoint.setpoint_web import start_web_setpoint

        start_web_setpoint()
    else:
        print(i18n.t("main.invalid_mode", mode))


def main():
    """
    Parst und verarbeitet Befehlszeilenargumente für verschiedene Betriebsmodi der Anwendung.
    Je nach angegebenem Modus (CLI, Web, GUI, Setpoint) wird der entsprechende Teil der
    Anwendung gestartet. Zusätzliche Optionen können über spezifische Argumente für die
    einzelnen Modi konfiguriert werden.

    Arguments:
        --cli (bool): Aktiviert den CLI-Modus. Wird dieser Modus gewählt, sind keine weiteren
                      Argumente erlaubt.
        --web (bool): Aktiviert den Web-Modus. Zugelassene zusätzliche Argumente in diesem
                      Modus sind --host, --port, --debug und --open-browser.
        --host (str, optional): Definiert die Host-Adresse für die Webanwendung. Standard ist
                                '127.0.0.1'.
        --port (int, optional): Definiert den Port für die Webanwendung. Standard ist 5000.
        --debug (bool, optional): Aktiviert den Debug-Modus für die Webanwendung.
        --open-browser (bool, optional): Öffnet den Standard-Webbrowser automatisch beim Start
                                          der Anwendung im Web-Modus.
        --gui (bool): Aktiviert den GUI-Modus.
        --setpoint (bool): Aktiviert den Setpoint-Modus. Nur das Argument --interface ist in
                           diesem Modus erlaubt.
        --interface (bool, optional): Legt das Interface für den Konfigurationseditor fest,
                                      der im Setpoint-Modus verwendet wird. Standard ist "gui".

    Raises:
        ArgumentError: Falls ungültige oder inkompatible Argumentkombinationen übergeben werden,
                       wird ein Fehler ausgegeben.

    Returns:
        None
    """
    # Banner anzeigen
    show_banner("xcore_banner")

    # ArgumenteParser initialisieren und konfigurieren
    parser = CustomHelp(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=i18n.t("main.help_desc"),
    )
    # Modus-Argumente
    mode_group = parser.add_argument_group(
        i18n.t("main.arg_mode_group_title"), i18n.t("main.arg_mode_group_desc")
    )
    mode_group.add_argument(
        "--cli", action="store_true", help=i18n.t("main.arg_cli_desc")
    )
    mode_group.add_argument(
        "--web", action="store_true", help=i18n.t("main.arg_web_desc")
    )
    mode_group.add_argument(
        "--gui", action="store_true", help=i18n.t("main.arg_gui_desc")
    )
    mode_group.add_argument(
        "--setpoint", action="store_true", help=i18n.t("main.arg_setpoint_desc")
    )

    # Nur für Web-Modus relevant
    # Flask Verbindungseinstellungen
    web_group = parser.add_argument_group(
        i18n.t("main.arg_web_group_title"), i18n.t("main.arg_web_group_desc")
    )
    web_group.add_argument(
        "--host", default="127.0.0.1", help=i18n.t("main.arg_host_desc")
    )
    web_group.add_argument(
        "--port", type=int, default=5000, help=i18n.t("main.arg_port_desc")
    )
    web_group.add_argument(
        "--debug", action="store_true", help=i18n.t("main.arg_debug_desc")
    )
    # Webbrowser öffnen beim Start (Web-Modus)
    web_group.add_argument(
        "--open-browser",
        default=True,
        action="store_true",
        help=i18n.t("main.arg_open_browser_desc"),
    )

    # Nur für den Setpoint-Modus relevant
    # Interface Variante zur Darstellung des Konfigurations-Editors
    setpoint_group = parser.add_argument_group(
        i18n.t("main.arg_setpoint_group_title"), i18n.t("main.arg_setpoint_group_desc")
    )
    setpoint_group.add_argument(
        "--interface",
        choices=["cli", "gui", "web"],
        default="gui",
        help=i18n.t("main.arg_interface_desc"),
    )

    args = parser.parse_args()

    # MODUS: CLI / Konsole
    if args.cli:
        # keine weiteren Argumente erlaubt
        if (
            args.host != "127.0.0.1"
            or args.port != 5000
            or args.debug
            or not args.open_browser
            or args.interface != "gui"
        ):
            parser.error(i18n.t("main.fail_start_cli_msg"))
        print(i18n.t("main.start_cli_msg"))
        start_cli()

    # MODUS: WEBSERVER
    elif args.web:
        # --interface darf NICHT gesetzt sein
        if args.interface != "gui":
            parser.error(i18n.t("main.fail_start_web_msg"))
        host = args.host
        port = args.port
        debug = args.debug
        open_browser = args.open_browser
        print(i18n.t("main.start_web_msg", host=host, port=port))
        start_web(host=host, port=port, debug=debug, open_browser=open_browser)

    # MODUS: SETPOINT
    elif args.setpoint:
        # Nur --interface erlaubt (alle anderen müssen default sein)
        if (
            args.host != "127.0.0.1"
            or args.port != 5000
            or args.debug
            or not args.open_browser
        ):
            parser.error(i18n.t("main.fail_start_setpoint_msg"))
        mode = args.interface or "gui"
        print(i18n.t("main.start_setpoint_msg", mode=mode.upper()))
        start_setpoint(mode=mode)

    # MODUS: GUI
    elif args.gui:
        print(i18n.t("main.start_gui_msg"))
        start_gui()


if __name__ == "__main__":
    main()

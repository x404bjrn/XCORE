# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import sys
import argparse
import platform

from xcore_framework.core.initializer import initialize
from xcore_framework.core.commander import start_cli

from xcore_framework.config.env import DIRECTORY_WEB_INTERFACE_DIR
from xcore_framework.config.i18n import i18n
from xcore_framework.config.banner import show_banner


class CustomHelp(argparse.ArgumentParser):
    """
    Eine benutzerdefinierte Erweiterung von argparse.ArgumentParser.

    Diese Klasse ersetzt die Standardhilfefunktion durch eine angepasste
    Ausgabe. Die neue Hilfsfunktion fügt eine zusätzliche benutzerdefinierte
    Nachricht hinzu, bevor die reguläre Hilfeausgabe der Basisklasse angezeigt
    wird.
    """

    def print_help(self, *args, **kwargs):
        print(i18n.t("main.help_title") + "\n")
        super().print_help(*args, **kwargs)


def start_web_mode(host="127.0.0.1", port=5000, debug=True, open_browser=True):
    initialize()

    if platform.system() == "Windows":
        from waitress import serve
        from xcore_framework.web.app import create_app

        app = create_app()

        if debug:
            # Entwicklermodus (Debug-Mode) mit Flask starten
            app.run(host=host, port=port, debug=debug, use_reloader=False)
        else:
            # Produktiv mit waitress auf dem Windowssystem
            serve(app, host=host, port=port, threads=4, connection_limit=100)
    else:
        # Alternativ (auf anderen OS) mit gunicorn starten
        import subprocess

        subprocess.run(["gunicorn", "-w", "4", "-b", f"{host}:{port}", "xcore_framework.web.app:create_app()"])

    # Browser öffnen (optional)
    if open_browser:
        import webbrowser
        webbrowser.open(f"http://{host}:{port}")


def start_cli_mode():
    """
    Startet die Kommandozeilenschnittstelle (CLI).
    """
    initialize()
    start_cli()


def start_gui_mode():
    """
    Startet die grafische Benutzeroberfläche (GUI) der Anwendung.
    """
    from xcore_framework.gui.gui import start_gui
    initialize()
    start_gui()


def start_setpoint_mode(interface="cli"):
    """
    Führt den Start eines Setpoints basierend auf der angegebenen Interfacevariante aus.

    Diese Funktion ermöglicht es, basierend auf der ausgewählten Interface
    Variante (CLI, GUI oder Web) das entsprechende Setpoint-Objekt zu initialisieren.
    Wird eine ungültige Interfacevariante übergeben, wird eine Fehlermeldung ausgegeben.

    Args:
        interface (str): Der Modus der Konfigurationsoberflächendarstellung.
                         Unterstützte Werte sind "cli", "gui" und "web".
                         Der Standardwert ist "cli".
    Raises:
        Exception: Bei Ausführung einer nicht unterstützten Interfacevariante.
    """
    initialize()

    if interface == "cli":
        from xcore_framework.setpoint.setpoint_cli import start_setpoint_cli

        # Startet Setpoint im CLI- / Konsolen-Modus
        start_setpoint_cli()

    elif interface == "gui":
        from xcore_framework.setpoint.setpoint_gui import start_setpoint_gui

        # Startet Setpoint im GUI-Modus
        start_setpoint_gui()

    elif interface == "web":
        from xcore_framework.setpoint.setpoint_web import start_setpoint_web

        # Startet Setpoint im Web-Modus
        start_setpoint_web()

    else:
        print(i18n.t("main.invalid_interface", interface=interface))


def main():
    """
    Parst und verarbeitet Befehlszeilenargumente für verschiedene Betriebsmodi der Anwendung.
    Je nach angegebenem Modus (CLI, Web, GUI, Setpoint) wird der entsprechende Teil der
    Anwendung gestartet. Zusätzliche Optionen können über spezifische Argumente für die
    einzelnen Modi konfiguriert werden.

    Arguments:
        --cli (bool): Aktiviert den CLI-Modus.
                      Wird dieser Modus gewählt, sind keine weiteren Argumente erlaubt.

        --web (bool): Aktiviert den Web-Modus.
                      Zugelassene zusätzliche Argumente in diesem Modus sind:
                      --host, --port, --debug, --open-browser.

        --host (str, optional): Definiert die Host-Adresse für die Webanwendung.
                                Standard ist '127.0.0.1' (localhost).

        --port (int, optional): Definiert den Port für die Webanwendung.
                                Standard ist 5000.

        --debug (bool, optional): Aktiviert den Debug-Modus für die Webanwendung.

        --open-browser (bool, optional): Öffnet den Standard-Webbrowser automatisch beim
                                         Start der Anwendung im Web-Modus.

        --gui (bool): Aktiviert den GUI-Modus.

        --setpoint (bool): Aktiviert den Setpoint-Modus.
                           Nur das Argument --interface ist in diesem Modus erlaubt.

        --interface (bool, optional): Legt das Interface für den Konfigurationseditor fest,
                                      der im Setpoint-Modus verwendet wird.
                                      Standard ist "cli".

    Raises:
        ArgumentError: Falls ungültige oder inkompatible Argumentkombinationen übergeben werden,
                       wird ein Fehler ausgegeben.
    """

    # (XCORE) Banner anzeigen
    show_banner("xcore_banner")

    # ArgumenteParser initialisieren und konfigurieren
    parser = CustomHelp(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=i18n.t("main.help_desc"),
    )

    # Argumentgruppe der Betriebsmodi ________________________________________________________
    mode_group = parser.add_argument_group(
        i18n.t("main.arg_group_mode_title"), i18n.t("main.arg_group_mode_desc")
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

    # Argumentgruppe für Konfigurationen des Web-Modus _______________________________________
    web_group = parser.add_argument_group(
        i18n.t("main.arg_group_web_title"), i18n.t("main.arg_group_web_desc")
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
    # Webbrowser öffnen beim Start des Web-Modus
    web_group.add_argument(
        "--open-browser",
        action="store_true",
        help=i18n.t("main.arg_open_browser_desc"),
    )

    # Argumentgruppe für die Konfiguration des Setpoint-Modus ________________________________
    setpoint_group = parser.add_argument_group(
        i18n.t("main.arg_group_setpoint_title"), i18n.t("main.arg_group_setpoint_desc")
    )
    # Darstellungsvariante für den Konfigurationseditor (Setpoint)
    setpoint_group.add_argument(
        "--interface",
        choices=["cli", "gui", "web"],
        default="cli",
        help=i18n.t("main.arg_interface_desc"),
    )

    args = parser.parse_args()

    # ARGUMENT AUSWERTUNG ====================================================================
    # MODUS: CLI / Konsole ___________________________________________________________________
    if args.cli:
        # keine weiteren Argumente erlaubt
        if (
            args.host != "127.0.0.1"
            or args.port != 5000
            or args.debug
            or args.open_browser
            or args.interface != "cli"
        ):
            parser.error(i18n.t("main.fail_start_cli_msg"))

        print(i18n.t("main.start_cli_msg"))
        start_cli_mode()

    # MODUS: WEB _____________________________________________________________________________
    elif args.web:
        # --interface darf NICHT gesetzt sein
        if args.interface != "cli":
            parser.error(i18n.t("main.fail_start_web_msg"))

        host = args.host
        port = args.port
        debug = args.debug
        open_browser = args.open_browser

        print(i18n.t("main.start_web_msg", host=host, port=port))
        start_web_mode(host=host, port=port, debug=debug, open_browser=open_browser)

    # MODUS: SETPOINT ________________________________________________________________________
    elif args.setpoint:
        # Nur --interface erlaubt (alle anderen müssen default sein)
        if (
            args.host != "127.0.0.1"
            or args.port != 5000
            or args.debug
            or args.open_browser
        ):
            parser.error(i18n.t("main.fail_start_setpoint_msg"))

        interface = args.interface or "cli"
        print(i18n.t("main.start_setpoint_msg", interface=interface.upper()))
        start_setpoint_mode(interface=interface)

    # MODUS: GUI _____________________________________________________________________________
    elif args.gui:
        # keine weiteren Argumente erlaubt
        if (
            args.host != "127.0.0.1"
            or args.port != 5000
            or args.debug
            or args.open_browser
            or args.interface != "cli"
        ):
            parser.error(i18n.t("main.fail_start_gui_msg"))

        print(i18n.t("main.start_gui_msg"))
        start_gui_mode()

    # TODO: Weiterer Modus (TUI - Terminal User Interface) geplant
    # TODO: Anzeige der Dokumentation soll über ein Argument realisiert werden


if __name__ == "__main__":
    main()

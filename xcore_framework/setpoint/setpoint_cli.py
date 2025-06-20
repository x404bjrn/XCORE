# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
# TODO:CLI-Setpoint weiter ausarbeiten (Hiermit nur Basis geschaffen)
from dotenv import dotenv_values

from xcore_framework.config.env import DIRECTORY_ENV
from xcore_framework.config.i18n import i18n
from xcore_framework.config.banner import show_banner
from xcore_framework.setpoint.setpoint_logic import save_config


def start_setpoint_cli():
    """
    Startet das interaktive Command-Line-Interface (CLI) für
    die Verwaltung der Setpoint-Konfiguration.

    Diese Funktion zeigt die aktuellen Konfigurationen an,
    ermöglicht dem Nutzer deren Anpassung und
    speichert die Änderungen. Der Benutzer hat die Möglichkeit,
    die CLI jederzeit zu beenden, indem
    er einen bestimmten Abbruchbefehl eingibt. Die Funktion liest
    die Konfiguration aus einer
    Umgebungsdatei aus, validiert die Eingabe des Nutzers und
    speichert die aktualisierten Werte.

    Raises:
        ValueError: Wird ausgelöst, wenn die Benutzereingabe
        für die Auswahl eines Indexes keine gültige
        Ganzzahl ist und die Eingabe auch nicht einem gültigen
        Abbruchbefehl entspricht.
    """
    show_banner("setpoint_cli_banner")
    while True:
        config = dotenv_values(DIRECTORY_ENV)
        keys = list(config.keys())
        print(i18n.t("setpoint_cli.current_config"))

        for i, key in enumerate(keys):
            print(f"[{i}] {key} = {config[key]}")
        print()
        choice = input(i18n.t("setpoint_cli.which_index"))

        try:
            choice = int(choice)
        except ValueError:
            if choice.lower() in ("q", "quit", "back", "exit"):
                break
            print(i18n.t("setpoint_cli.invalid_input"))

        if 0 <= choice < len(keys):
            key1 = keys[choice]
            new_value = input(i18n.t("setpoint_cli.new_value", key1=key1)).strip()
            save_config({key1: new_value})
            print(
                i18n.t(
                    "setpoint_cli.value_change_success", key1=key1, new_value=new_value
                )
            )
        else:
            print(i18n.t("setpoint_cli.invalid_index"))

    print(i18n.t("setpoint_cli.config_completed"))

# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os

from datetime import datetime

from xcore_framework.config.i18n import i18n
from xcore_framework.config.env import ensure_env_file
from xcore_framework.config.db import ensure_db_file
from xcore_framework.config.rte import check_runtimes

# TODO: Laufzeitdaten/dateien in .xcore Verzeichnis und getrennt von Code auszugliedern
XCORE_BASE_DIRECTORY = os.path.expanduser("~/.xcore/")
INIT_CHECKFILE_PATH = os.path.join(XCORE_BASE_DIRECTORY, ".init.xcore")


def initialize():
    """
    Initialisiert XCORE Framework.
    Einrichtung des Anwendungsverzeichnisses und generieren
    von .env-Datei und Datenbank bei Erststart.
    """
    # Prüfen ob das XCORE Framework Anwendungsverzeichnis (für Laufzeitdaten) schon existiert
    if not os.path.exists(XCORE_BASE_DIRECTORY):
        print(
            i18n.t("system.init_dir_not_found"),
        )
        try:
            os.makedirs(XCORE_BASE_DIRECTORY, exist_ok=True)
            print(
                i18n.t("system.init_dir_created", path=XCORE_BASE_DIRECTORY),
            )
        except Exception as e:
            print(
                i18n.t("system.init_dir_created_error", error=e),
            )

    if not os.path.exists(INIT_CHECKFILE_PATH):
        print(i18n.t("system.init"))

        try:
            # .env prüfen/anlegen
            ensure_env_file()

            # Datenbank prüfen/anlegen
            ensure_db_file()

            # Prüfen ob erforderliche Laufzeitumgebungen existieren
            # (Wenn nicht, dann downloaden und ablegen)
            check_runtimes()

            # Prüfen ob XCORE Arbeitsverzeichnis (der Module) existiert
            if not os.path.exists(os.path.join(XCORE_BASE_DIRECTORY, "workspace")):
                os.makedirs(os.path.join(XCORE_BASE_DIRECTORY, "workspace"), exist_ok=True)
                # TODO Statt Print LOGGER einarbeiten
                print(
                    i18n.t("system.init_module_dir_created", path=os.path.join(XCORE_BASE_DIRECTORY, "workspace")),
                )

            # INFO: Hier weitere Initialisierungen bei Bedarf hinzufügen
            # ...

            # Legt Datei mit init-Marker an, als Kennzeichnung für abgeschlossene Initialisierung
            with open(INIT_CHECKFILE_PATH, "w", encoding="utf-8") as f:
                f.write(f"{datetime.now()} = init_ok")
                f.close()

            print(i18n.t("system.init_success"))

        except Exception as e:
            print(i18n.t("system.init_error", e=e))

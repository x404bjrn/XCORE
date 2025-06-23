# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
from xcore_framework.config.i18n import i18n
from xcore_framework.config.env import ensure_env_file
from xcore_framework.config.db import ensure_db_file

import os
from datetime import datetime


INIT_CHECKFILE_PATH = os.path.join(os.path.dirname(__file__), "..", ".init.xcore")


def initialize():
    """ Initialisiert .env-Datei und Datenbank bei Erststart. """
    if not os.path.exists(INIT_CHECKFILE_PATH):
        print(i18n.t("system.init"))

        try:
            # .env prüfen/anlegen
            ensure_env_file()

            # Datenbank prüfen/anlegen
            ensure_db_file()

            # INFO: Hier weitere Initialisierungen bei Bedarf hinzufügen
            # ...

            # Legt Datei mit init-Marker an, als Kennzeichnung für abgeschlossene Initialisierung
            with open(INIT_CHECKFILE_PATH, "w", encoding="utf-8") as f:
                f.write(f"{datetime.now()} = init_ok")
                f.close()

            print(i18n.t("system.init_success"))

        except Exception as e:
            print(i18n.t("system.init_error", e=e))

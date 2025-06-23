# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os

from xcore_framework.core.database_manager import DatabaseManager
from xcore_framework.config.i18n import i18n


# Basisverzeichnis definieren
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "database", "database.db")


def ensure_db_file(path=DB_PATH):
    """
    Überprüft, ob eine Datenbankdatei existiert, und erstellt diese bei Bedarf.
    Es wird außerdem eine Benutzer-Tabelle in der Datenbank erstellt.

    Args:
        path (str): Der Pfad zur Datenbankdatei, die überprüft werden soll.
            Standardwert ist der in DB_PATH definierte Pfad.
    """
    if os.path.exists(path):
        print(i18n.t("config.db_file_exists"))
        return

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    # Erstellt neue Datenbank
    print(i18n.t("config.init_new_db"))
    xcore_db = DatabaseManager()

    # Erstelle User-Table
    xcore_db.init_user_table()

    # Erstelle User-Content-Table
    xcore_db.init_content_table()

    # INFO: Hier weitere Table Initialisierungen bei Bedarf hinzufügen
    # ...

    print(i18n.t("config.init_new_db_success", path=path))

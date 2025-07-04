# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import locale
from dotenv import load_dotenv, set_key

from xcore_framework.config.i18n import i18n


# Basisverzeichnis definieren
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")


def set_env_key(key, value):
    """
    Eine Funktion, die einen spezifischen Umgebungsvariablen-Schlüssel und dessen
    Wert in einer .env-Datei speichert oder aktualisiert. Sie stellt sicher, dass
    die Datei existiert, bevor sie den Schlüssel setzt.
    Falls die Datei nicht existiert, wird sie erstellt.

    Args:
        key (str): Der Name des Umgebungsvariablen-Schlüssels, der gesetzt oder
                   aktualisiert werden soll.
        value (str): Der Wert, der dem Schlüssel zugewiesen werden soll.

    Returns:
        bool: TRUE, wenn erfolgreich,
              FALSE, wenn ein Fehler aufgetreten ist
    """
    try:
        if not os.path.exists(DOTENV_PATH):
            ensure_env_file()

        set_key(DOTENV_PATH, key, value)
        os.environ[key] = value  # Aktualisiere auch die aktuelle Umgebung
        return True
    except Exception as e:
        print(f"Fehler beim Setzen des Umgebungsschlüssels: {e}")
        return False


def ensure_env_file(path=DOTENV_PATH):
    """
    Prüft auf das Vorhandensein einer `.env`-Datei am angegebenen Pfad. Falls keine
    `.env`-Datei existiert, wird eine Standardkonfiguration erstellt und gespeichert.
    Anschließend wird die `.env`-Datei geladen, um Umgebungsvariablen zu initialisieren.

    :param path: Der Pfad, an dem die `.env`-Datei gesucht oder erstellt werden soll.
    :type path: str
    :return: Gibt nichts zurück. Führt die Initialisierung der Umgebungsvariablen durch.
    :rtype: None
    """
    if os.path.exists(path):
        load_dotenv(path)
        return

    print(i18n.t("config.init_new_env"))

    # INFO: Hier weitere .env Eintrags-Initialisierungen bei Bedarf hinzufügen
    # ...
    default_env = [
        # Verzeichnisse
        f"DIRECTORY_FRAMEWORK={BASE_DIR}",
        f"DIRECTORY_LOGGING={os.path.join(BASE_DIR, 'logs')}",
        f"DIRECTORY_ENV={os.path.join(BASE_DIR, '.env')}",
        f"DIRECTORY_CONFIG={os.path.dirname(os.path.abspath(__file__))}",
        f"DIRECTORY_I18N={os.path.join(BASE_DIR, 'config', 'i18n')}",
        f"DIRECTORY_CORE={os.path.join(BASE_DIR, 'core')}",
        f"DIRECTORY_MODULES={os.path.join(BASE_DIR, 'modules')}",
        f"DIRECTORY_DATABASE={os.path.join(BASE_DIR, 'database')}",
        f"DIRECTORY_GUI={os.path.join(BASE_DIR, 'gui')}",
        f"DIRECTORY_WEB_INTERFACE_DIR={os.path.join(BASE_DIR, 'web')}",
        # Einstellungen (für benutzernahe Einstellungen)
        f"SETTING_LANGUAGE={locale.getlocale()[0][:2] if locale.getlocale()[0] else 'en'}",
        "SETTING_WEB_INTERFACE_URL=http://0.0.0.0:5000",
        # Konfigurationen (für technische Konfigurationen)
        # CONFIGURATION_ ...
        # Fonts (GUI)
        f"FONT_FIRACODE_BOLD={os.path.join(BASE_DIR, 'gui', 'fonts', 'FiraCode-Bold.ttf')}",
        f"FONT_FIRACODE_LIGHT={os.path.join(BASE_DIR, 'gui', 'fonts', 'FiraCode-Light.ttf')}",
        f"FONT_FIRACODE_MEDIUM={os.path.join(BASE_DIR, 'gui', 'fonts', 'FiraCode-Medium.ttf')}",
        f"FONT_FIRACODE_REGULAR={os.path.join(BASE_DIR, 'gui', 'fonts', 'FiraCode-Regular.ttf')}",
        f"FONT_FIRACODE_SEMIBOLD={os.path.join(BASE_DIR, 'gui', 'fonts','FiraCode-SemiBold.ttf')}",
        f"FONT_FIRACODE_VARIABLEFONT_WGHT={os.path.join(BASE_DIR, 'gui', 'fonts', 'FiraCode-VariableFont_wght.ttf')}",
        f"FONT_ORBITRON_BLACK={os.path.join(BASE_DIR, 'gui', 'fonts', 'Orbitron-Black.ttf')}",
        f"FONT_ORBITRON_BOLD={os.path.join(BASE_DIR, 'gui', 'fonts', 'Orbitron-Bold.ttf')}",
        f"FONT_ORBITRON_EXTRABOLD={os.path.join(BASE_DIR, 'gui', 'fonts', 'Orbitron-ExtraBold.ttf')}",
        f"FONT_ORBITRON_MEDIUM={os.path.join(BASE_DIR, 'gui', 'fonts', 'Orbitron-Medium.ttf')}",
        f"FONT_ORBITRON_REGULAR={os.path.join(BASE_DIR, 'gui', 'fonts', 'Orbitron-Regular.ttf')}",
        f"FONT_ORBITRON_SEMIBOLD={os.path.join(BASE_DIR, 'gui', 'fonts', 'Orbitron-SemiBold.ttf')}",
        f"FONT_ORBITRON_VARIABLEFONT_WGHT={os.path.join(BASE_DIR, 'gui', 'fonts', 'Orbitron-VariableFont_wght.ttf')}",
        f"FONT_RUSSOONE_REGULAR={os.path.join(BASE_DIR, 'gui', 'fonts', 'RussoOne-Regular.ttf')}",
        f"FONT_WDXLLUBRIFONTTC_REGULAR={os.path.join(BASE_DIR, 'gui', 'fonts', 'WDXLLubrifontTC-Regular.ttf')}",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(default_env))

    print(i18n.t("config.init_new_env_success", path=path))
    load_dotenv(DOTENV_PATH)


# Erstelle Default/Standard-ENV, falls nicht vorhanden
ensure_env_file()

# Zugriff auf ENV-Variablen
# Anwendungsverzeichnisse _____________________________________________________
DIRECTORY_FRAMEWORK = os.getenv("DIRECTORY_FRAMEWORK")
DIRECTORY_LOGGING = os.getenv("DIRECTORY_LOGGING")
DIRECTORY_ENV = os.getenv("DIRECTORY_ENV")
DIRECTORY_CONFIG = os.getenv("DIRECTORY_CONFIG")
DIRECTORY_I18N = os.getenv("DIRECTORY_I18N")
DIRECTORY_CORE = os.getenv("DIRECTORY_CORE")
DIRECTORY_MODULES = os.getenv("DIRECTORY_MODULES")
DIRECTORY_DATABASE = os.getenv("DIRECTORY_DATABASE")
DIRECTORY_GUI = os.getenv("DIRECTORY_GUI")
DIRECTORY_WEB_INTERFACE_DIR = os.getenv("DIRECTORY_WEB_INTERFACE_DIR")

# Anwendungseinstellungen / Benutzerkonfigurationen ___________________________
SETTING_LANGUAGE = os.getenv("SETTING_LANGUAGE")
SETTING_WEB_INTERFACE_URL = os.getenv("SETTING_WEB_INTERFACE_URL")

# Verwendete Fonts (Schriftarten) _____________________________________________
FONT_PACKAGE = {
    "FIRACODE_BOLD": os.getenv("FONT_FIRACODE_BOLD"),
    "FIRACODE_LIGHT": os.getenv("FONT_FIRACODE_LIGHT"),
    "FIRACODE_MEDIUM": os.getenv("FONT_FIRACODE_MEDIUM"),
    "FIRACODE_REGULAR": os.getenv("FONT_FIRACODE_REGULAR"),
    "FIRACODE_SEMIBOLD": os.getenv("FONT_FIRACODE_SEMIBOLD"),
    "FIRACODE_VARIABLEFONT_WGHT": os.getenv("FONT_FIRACODE_VARIABLEFONT_WGHT"),
    "ORBITRON_BLACK": os.getenv("FONT_ORBITRON_BLACK"),
    "ORBITRON_BOLD": os.getenv("FONT_ORBITRON_BOLD"),
    "ORBITRON_EXTRABOLD": os.getenv("FONT_ORBITRON_EXTRABOLD"),
    "ORBITRON_MEDIUM": os.getenv("FONT_ORBITRON_MEDIUM"),
    "ORBITRON_REGULAR": os.getenv("FONT_ORBITRON_REGULAR"),
    "ORBITRON_SEMIBOLD": os.getenv("FONT_ORBITRON_SEMIBOLD"),
    "ORBITRON_VARIABLEFONT_WGHT": os.getenv("FONT_ORBITRON_VARIABLEFONT_WGHT"),
    "RUSSOONE_REGULAR": os.getenv("FONT_RUSSOONE_REGULAR"),
    "WDXLLUBRIFONTTC_REGULAR": os.getenv("FONT_WDXLLUBRIFONTTC_REGULAR"),
}

# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
from dotenv import set_key, load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")


def save_config(data: dict):
    """
    Speichert Konfigurationsdaten in einer Umgebungsdatei.

    Diese Funktion speichert die übergebenen Konfigurationsdaten in einer Datei,
    die sich im durch die Konstante `ENV_PATH` angegebenen Pfad befindet. Existiert
    die Datei nicht, wird sie erstellt. Die Schlüssel in den Daten werden in
    Großbuchstaben umgewandelt, bevor sie gespeichert werden.

    Args:
        data (dict): Ein Dictionary, das die Konfigurationsdaten enthält. Die
        Schlüssel sind die Konfigurationsnamen, und die Werte sind die jeweiligen
        Konfigurationsinhalte.

    Raises:
        KeyError: Wenn eines der Schlüssel-Wert-Paare nicht gesetzt werden kann.
    """
    if not os.path.exists(ENV_PATH):
        open(ENV_PATH, "a").close()

    for key, value in data.items():
        set_key(ENV_PATH, key.upper(), value)


def load_config() -> dict:
    """
    Lädt die Konfigurationswerte aus einer .env-Datei und gibt sie als Wörterbuch
    zurück. Es werden nur Umgebungsvariablen berücksichtigt, die in
    Großbuchstaben geschrieben sind.

    Raises:
        Kein Fehler wird in diesem Code explizit ausgelöst. Fehler können jedoch
        auftreten, wenn die Datei im Pfad `ENV_PATH` nicht vorhanden ist, fehlerhaft
        ist oder keine Leseberechtigung besteht.

    Returns:
        Ein Wörterbuch, das die geladenen Konfigurationswerte enthält, wobei die
        Schlüssel den Großbuchstaben-Schlüssel der Umgebungsvariablen und die Werte
        deren zugehörigen Inhalte sind.
    """
    load_dotenv(ENV_PATH)
    return {key: os.getenv(key) for key in os.environ if key.isupper()}

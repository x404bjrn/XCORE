# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import logging

from logging.handlers import RotatingFileHandler

from xcore_framework.config.env import DIRECTORY_LOGGING, LOG_FILE_XCORE


def setup_logger(name: str, file_handler=True, con_handler=True):
    """
    Richtet einen Logger mit optionalen Handlers für Datei und Konsole ein.

    Die Funktion erstellt den Logger mit einem bestimmten Namen und erlaubt,
    einen Datei-Handler mit Rotationsmechanismus wie auch einen Konsolen-Handler
    für Ausgabe zu konfigurieren. Es wird außerdem sichergestellt, dass das
    Logging-Verzeichnis existiert, bevor Handler initialisiert werden.

    Args:
        name (str): Name des Loggers.
        file_handler (bool): Aktiviert/Deaktiviert den Datei-Handler.
        con_handler (bool): Aktiviert/Deaktiviert den Konsolen-Handler.

    Returns:
        logging.Logger: Der konfigurierte Logger mit den angegebenen Handlers.
    """
    if not os.path.exists(DIRECTORY_LOGGING):
        os.makedirs(DIRECTORY_LOGGING, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        if file_handler:
                # File Handler mit Rotation (5x max 1MB)
                file_handler = RotatingFileHandler(LOG_FILE_XCORE, maxBytes=1_000_000, backupCount=5)
                file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                ))

        if con_handler:
            # Optional: Konsolen-Handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(
                '%(name)s - %(levelname)s - %(message)s'
            ))

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

    return logger

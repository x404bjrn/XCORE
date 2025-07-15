# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import logging

from logging.handlers import RotatingFileHandler

from xcore_framework.config.env import DIRECTORY_LOGGING


def setup_logger(name: str, file_handler=True, con_handler=False):
    if not os.path.exists(DIRECTORY_LOGGING):
        os.makedirs(DIRECTORY_LOGGING, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Check: Hat der Logger bereits einen passenden FileHandler?
    log_path = os.path.join(DIRECTORY_LOGGING, f"{name}.log")
    has_file_handler = any(
        isinstance(h, RotatingFileHandler)
        and h.baseFilename == os.path.abspath(log_path)
        for h in logger.handlers
    )

    if file_handler and not has_file_handler:
        file_log_handler = RotatingFileHandler(
            log_path, maxBytes=1_000_000, backupCount=5, encoding="utf-8"
        )
        file_log_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(file_log_handler)

    if con_handler:
        # Prüfen, ob schon ein StreamHandler existiert
        if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter("%(name)s - %(levelname)s - %(message)s")
            )
            logger.addHandler(console_handler)

    # INFO: DEBUG_DEV Kommentar (Kann auskommentiert werden wenn nicht benötigt)
    # print(f"[DEBUG] Logger {name} initialized with handlers: {[type(h).__name__ for h in logger.handlers]}")

    return logger

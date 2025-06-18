# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os

# 'Basisverzeichnis' / Hauptverzeichnis (Anwendungsverzeichnis)
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "wabbalubbadubdub"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        basedir, "..", "database", "database.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

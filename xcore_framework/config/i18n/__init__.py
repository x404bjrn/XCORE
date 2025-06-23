# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import locale
from dotenv import load_dotenv

from .i18n_manager import I18nManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, "..", "..", ".env")

if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)
    XCORE_LANGUAGE = os.getenv("SETTING_LANGUAGE")
else:
    locale_info = locale.getlocale()[0]
    XCORE_LANGUAGE = locale_info[:2] if locale_info else "en"

# Globale Instanz
i18n = I18nManager(lang=XCORE_LANGUAGE, base_path=os.path.join(BASE_DIR))

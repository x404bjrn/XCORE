# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import json
import shutil
import pytest

from xcore_framework.config.i18n.i18n_manager import I18nManager


@pytest.fixture
def i18n_test_env(tmp_path):
    i18n_dir = tmp_path / "i18n"
    de_dir = i18n_dir / "de"
    en_dir = i18n_dir / "en"

    de_dir.mkdir(parents=True)
    en_dir.mkdir(parents=True)

    # Beispielübersetzungen
    with open(de_dir / "common.json", "w", encoding="utf-8") as f:
        json.dump({"greeting": "Hallo, {name}!"}, f)

    with open(en_dir / "common.json", "w", encoding="utf-8") as f:
        json.dump({"greeting": "Hello, {name}!"}, f)

    yield str(i18n_dir)  # Rückgabe des Basispfads als String

    # Aufräumen
    shutil.rmtree(i18n_dir, ignore_errors=True)


def test_default_language_load(i18n_test_env):
    i18n = I18nManager(lang="de", base_path=i18n_test_env)
    assert i18n.t("common.greeting", name="Björn") == "Hallo, Björn!"


def test_language_switch(i18n_test_env):
    i18n = I18nManager(lang="de", base_path=i18n_test_env)
    i18n.set_language("en")
    assert i18n.t("common.greeting", name="Xenia") == "Hello, Xenia!"


def test_missing_translation_key(i18n_test_env):
    i18n = I18nManager(lang="de", base_path=i18n_test_env)
    assert i18n.t("common.unknownkey") == "[common.unknownkey]"


def test_invalid_key_format(i18n_test_env):
    i18n = I18nManager(lang="de", base_path=i18n_test_env)
    assert i18n.t("wrongformatkey") == "wrongformatkey"


def test_set_unsupported_language(i18n_test_env):
    i18n = I18nManager(lang="de", base_path=i18n_test_env)
    result = i18n.set_language("fr")
    assert result is False
    # Sprache sollte unverändert bleiben
    assert i18n.lang == "de"

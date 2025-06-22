# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import shutil
import tempfile
import textwrap
import pytest

from xcore_framework.core.module_loader import ModuleLoader


@pytest.fixture
def real_module_environment():
    # Temporäres Modulverzeichnis erzeugen
    temp_dir = tempfile.mkdtemp()

    # Beispielmodul 1: test_hello_module.py
    module_code = textwrap.dedent("""
        class Module:
            def __init__(self):
                self.name = "Hello"
            def greet(self):
                return "Hello from real module"
    """)
    module_path = os.path.join(temp_dir, "test_hello_module.py")
    with open(module_path, "w") as f:
        f.write(module_code)

    yield temp_dir
    shutil.rmtree(temp_dir)


def test_module_loader_with_real_module(monkeypatch, real_module_environment):
    # Patch: das echte Modulverzeichnis vorgeben
    loader = ModuleLoader()
    loader.module_base = real_module_environment

    # Suche nach dem Modul
    results = loader.search_modules("hello")
    assert len(results) == 1
    assert results[0] == "test_hello_module"

    # Modul laden
    mod = loader.load_module("test_hello_module")
    assert mod is not None
    assert hasattr(mod, "name")
    assert mod.name == "Hello"
    assert mod.greet() == "Hello from real module"

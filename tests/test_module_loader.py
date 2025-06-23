# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import tempfile
import textwrap
import shutil
import pytest

from xcore_framework.core.module_loader import ModuleLoader


@pytest.fixture
def temp_module_dir():
    temp_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(temp_dir, "subdir"), exist_ok=True)

    # Modul mit Keyword
    with open(os.path.join(temp_dir, "test_keyword.py"), "w") as f:
        f.write(
            textwrap.dedent(
                """\
            class Module:
                def __init__(self):
                    self.name = "TestModule"
        """
            )
        )

    # Modul ohne Keyword
    with open(os.path.join(temp_dir, "random.py"), "w") as f:
        f.write("")

    # init-Datei
    with open(os.path.join(temp_dir, "__init__.py"), "w") as f:
        f.write("")

    # Unterverzeichnis mit Treffern
    with open(os.path.join(temp_dir, "subdir", "another_keyword_module.py"), "w") as f:
        f.write(
            textwrap.dedent(
                """\
            class Module:
                def __init__(self):
                    self.name = "AnotherTestModule"
        """
            )
        )

    yield temp_dir
    shutil.rmtree(temp_dir)


def test_search_modules_finds_matching_files(monkeypatch, temp_module_dir):
    loader = ModuleLoader()
    loader.module_base = temp_module_dir
    results = loader.search_modules("keyword")

    assert len(results) == 2
    assert "test_keyword" in results
    assert "subdir/another_keyword_module" in results


def test_search_modules_ignores_init(monkeypatch, temp_module_dir):
    loader = ModuleLoader()
    loader.module_base = temp_module_dir
    results = loader.search_modules("__init__")

    assert "__init__" not in [os.path.basename(path) for path in results]


def test_load_module_returns_instance(monkeypatch, temp_module_dir):
    loader = ModuleLoader()
    loader.module_base = temp_module_dir
    module = loader.load_module("test_keyword")

    assert module is not None
    assert hasattr(module, "name")
    assert module.name == "TestModule"


def test_load_module_returns_none_if_not_found(monkeypatch, temp_module_dir):
    loader = ModuleLoader()
    loader.module_base = temp_module_dir
    module = loader.load_module("nonexistent_module")

    assert module is None

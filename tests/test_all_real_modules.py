# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import re
import pytest

from xcore_framework.core.module_loader import ModuleLoader
from xcore_framework.core.module_base import XCoreModule


def get_default_params(module):
    params = {}
    for key, opt in module.options.items():
        params[key] = opt.get("default")
    return params


def validate_module_structure(mod, path):
    required_attrs = {
        "name": str,
        "description": str,
        "author": str,
        "version": str,
        "created": str,
        "options": dict,
    }

    for attr, expected_type in required_attrs.items():
        assert hasattr(mod, attr), f"❌ Modul '{path}' fehlt Attribut '{attr}'."
        value = getattr(mod, attr)
        assert isinstance(
            value, expected_type
        ), f"❌ Modul '{path}': '{attr}' ist kein {expected_type.__name__}."
        if expected_type == str:
            assert value.strip() != "", f"❌ Modul '{path}': '{attr}' ist leer."

    # Versionsformat prüfen
    assert re.match(
        r"^\d+\.\d+\.\d+.*$", mod.version
    ), f"❌ Modul '{path}': version '{mod.version}' ist kein semantisches Format."

    # Created-Datum z. B. im Format dd.mm.yyyy (flexibel anpassbar)
    assert re.match(
        r"^\d{2}\.\d{2}\.\d{4}$", mod.created
    ), f"❌ Modul '{path}': created '{mod.created}' ist kein gültiges Datum."


def validate_options_structure(options, path):
    for key, opt in options.items():
        assert isinstance(
            opt, dict
        ), f"❌ Option '{key}' in Modul '{path}' ist kein dict."

        assert (
            "widget_type" in opt
        ), f"❌ Option '{key}' in Modul '{path}' hat kein 'widget_type'."
        assert isinstance(
            opt["widget_type"], str
        ), f"❌ Option '{key}' in Modul '{path}': 'widget_type' ist kein string."

        # prüft empfohlene Felder
        if "desc" in opt:
            assert isinstance(
                opt["desc"], str
            ), f"❌ Option '{key}' in Modul '{path}': 'desc' ist kein string."

        if "required" in opt:
            assert isinstance(
                opt["required"], bool
            ), f"❌ Option '{key}' in Modul '{path}': 'required' ist kein bool."

        if "default" in opt:
            pass  # Optionaler Typ-Test je nach widget_type möglich

        if "values" in opt:
            assert isinstance(
                opt["values"], list
            ), f"❌ Option '{key}' in Modul '{path}': 'values' ist keine Liste."

        for unknown in set(opt.keys()) - {
            "widget_type",
            "required",
            "default",
            "desc",
            "values",
            "min",
            "max",
        }:
            assert (
                False
            ), f"❌ Option '{key}' in Modul '{path}' enthält unbekannten Schlüssel '{unknown}'."


@pytest.mark.parametrize("keyword", [""])  # Alle Module durchsuchen
def test_all_modules(keyword):
    loader = ModuleLoader()
    modules = loader.search_modules(keyword)

    assert modules, "❌ Keine Module gefunden."

    errors = []

    for path in modules:
        try:
            mod = loader.load_module(path)
            assert mod is not None, f"❌ Modul '{path}' konnte nicht geladen werden."
            assert isinstance(
                mod, XCoreModule
            ), f"❌ Modul '{path}' erbt nicht von XCoreModule."

            validate_module_structure(mod, path)
            validate_options_structure(mod.options, path)

            params = get_default_params(mod)
            result = mod.run(params)

            assert isinstance(
                result, dict
            ), f"❌ Modul '{path}': run() gibt kein dict zurück."
            assert (
                result.get("success", False) is True
            ), f"❌ Modul '{path}' meldet kein success=True."
            assert "output" in result, f"❌ Modul '{path}' hat keine 'output'-Liste."

            print(f"✅ {path} OK")

        except AssertionError as e:
            errors.append(str(e))
        except Exception as e:
            errors.append(f"💥 Ausnahme in Modul '{path}': {e}")

    if errors:
        print("\n==== !!! Fehlerhafte Module !!! ====")
        for err in errors:
            print(err)
        pytest.fail(f"{len(errors)} Modul(e) schlugen fehl. Siehe oben.")

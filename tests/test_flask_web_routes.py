# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import pytest
import sys

from flask import Flask
from unittest.mock import MagicMock, patch

# Importiere benötigte Objekte/Blueprint
from xcore_framework.web.app.modules import modules

sys.modules["modules"] = modules


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(modules)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_list_modules_success(client):
    mock_module = MagicMock()
    mock_module.name = "Testmodul"
    mock_module.description = "Beschreibung"

    with (
        patch("xcore_framework.web.app.modules.loader") as mock_loader,
        patch("xcore_framework.web.app.modules.strip_ansi", side_effect=lambda x: x),
    ):
        mock_loader.search_modules.return_value = ["category1/mod1", "category2/mod2"]
        mock_loader.load_module.side_effect = [mock_module, mock_module]

        resp = client.get("/api/modules")
        assert resp.status_code == 200

        data = resp.get_json()
        assert "category1" in data or "category2" in data
        for category, mods in data.items():
            assert isinstance(mods, list)
            for mod in mods:
                assert "name" in mod and "description" in mod


def test_list_modules_error(client):
    with patch("xcore_framework.web.app.modules.loader") as mock_loader:
        mock_loader.search_modules.side_effect = Exception("Fehler!")
        resp = client.get("/api/modules")
        assert resp.status_code == 500
        data = resp.get_json()
        assert "error" in data


def test_get_module_meta_found(client):
    mock_module = MagicMock()
    mock_module.name = "MetaModul"
    mock_module.description = "MetaBeschreibung"
    mock_module.options = {"foo": 1}
    mod_attrs = {"author": "Autor", "version": "1.0", "created": "2024-01-01"}
    for k, v in mod_attrs.items():
        setattr(mock_module, k, v)

    with (
        patch("xcore_framework.web.app.modules.loader") as mock_loader,
        patch("xcore_framework.web.app.modules.strip_ansi", side_effect=lambda x: x),
    ):
        mock_loader.load_module.return_value = mock_module
        resp = client.get("/api/module/testmod/meta")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["name"] == "MetaModul"
        assert data["author"] == "Autor"
        assert data["options"] == {"foo": 1}


def test_get_module_meta_not_found(client):
    with patch("xcore_framework.web.app.modules.loader") as mock_loader:
        mock_loader.load_module.return_value = None
        resp = client.get("/api/module/nichtda/meta")
        assert resp.status_code == 404
        data = resp.get_json()
        assert "error" in data


def test_get_module_meta_error(client):
    with patch("xcore_framework.web.app.modules.loader") as mock_loader:
        mock_loader.load_module.side_effect = Exception("Fehler!")
        resp = client.get("/api/module/testerror/meta")
        assert resp.status_code == 500
        data = resp.get_json()
        assert "error" in data


def test_run_module_success(client):
    mock_module = MagicMock()
    mock_module.run.return_value = {"erfolg": True}

    with patch("xcore_framework.web.app.modules.loader") as mock_loader:
        mock_loader.load_module.return_value = mock_module
        resp = client.post("/api/module/foo/run", json={"p1": "v1"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data == {"erfolg": True}
        mock_module.run.assert_called_with({"p1": "v1"}, mode="web")


def test_run_module_not_found(client):
    with patch("xcore_framework.web.app.modules.loader") as mock_loader:
        mock_loader.load_module.return_value = None
        resp = client.post("/api/module/nichtda/run")
        assert resp.status_code == 404
        data = resp.get_json()
        assert "error" in data


def test_run_module_error(client):
    mock_module = MagicMock()
    mock_module.run.side_effect = Exception("Fehler bei Ausführung")
    with patch("xcore_framework.web.app.modules.loader") as mock_loader:
        mock_loader.load_module.return_value = mock_module
        resp = client.post("/api/module/testerror/run", json={"foo": "bar"})
        assert resp.status_code == 500
        data = resp.get_json()
        assert "error" in data

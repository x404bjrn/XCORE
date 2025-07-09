# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import json
import traceback

from flask import request, jsonify, Blueprint, current_app

# XCORE Framework Module Loader
from xcore_framework.core.module_loader import ModuleLoader
from xcore_framework.config.formatting import strip_ansi


modules = Blueprint("modules", __name__)

loader = ModuleLoader()


@modules.route("/api/modules", methods=["GET"])
def list_modules():
    """
    Bietet eine API-Endpunkt-Funktionalität an, um eine Liste von verfügbaren Modulen zu erhalten.
    Die Methode gruppiert die Module nach Kategorien, lädt die Module und extrahiert dabei relevante
    Informationen wie den Modulnamen und die Beschreibung.

    :param loader: Ein Modul-Lademechanismus, der die Suche und das
                   Laden von Modulen ermöglicht.
    :return: Eine JSON-Repräsentation einer baumartigen Struktur,
             die die geladenen Module nach Kategorien gruppiert und für
             jedes Modul Informationen wie Pfad, Name und Beschreibung enthält.
             Im Falle eines Fehlers wird eine JSON-Antwort mit Fehlermeldung
             und HTTP-Statuscode 500 zurückgegeben.
    """
    try:
        tree = {}
        for path in loader.search_modules(""):  # alle Module laden
            category = path.split("/")[0]
            mod = loader.load_module(path)

            if not mod:
                continue

            if category not in tree:
                tree[category] = []

            tree[category].append(
                {
                    "path": path,
                    "name": strip_ansi(mod.name),
                    "description": strip_ansi(mod.description),
                }
            )
        return jsonify(tree)

    except Exception:
        return jsonify({"error": traceback.format_exc()}), 500


@modules.route("/api/module/<path:module_path>/meta", methods=["GET"])
def get_module_meta(module_path):
    """
    Stellt Metadaten eines Moduls über eine API-Schnittstelle bereit.

    Ruft die Metadaten eines bestimmten Moduls ab, das durch seinen Pfad
    identifiziert wird, und gibt sie im JSON-Format zurück. Die möglichen
    Metadaten umfassen Name, Beschreibung, Autor, Versionsnummer,
    Erstellungszeitpunkt und verfügbare Optionen des Moduls. Wenn das Modul nicht
    gefunden wird, wird ein HTTP-Fehler 404 zurückgegeben. Im Falle von
    unerwarteten Fehlern wird ein allgemeiner HTTP-Fehler 500 zurückgegeben.

    :param module_path: Der Pfad des zu ladenden Moduls
    :type module_path: str
    :return: Eine JSON-Antwort mit den Metadaten des Moduls oder einer
             entsprechenden Fehlermeldung
    :rtype: flask.Response
    :raises flask.HTTPException: Bei nicht gefundenem Modul (404)
    :raises flask.HTTPException: Bei unerwarteten Fehlern (500)
    """
    try:
        mod = loader.load_module(module_path)
        if not mod:
            return jsonify({"error": "Modul nicht gefunden"}), 404

        return jsonify(
            {
                "name": strip_ansi(mod.name),
                "description": strip_ansi(mod.description),
                "author": strip_ansi(getattr(mod, "author", "Unbekannt")),
                "version": strip_ansi(getattr(mod, "version", "n/a")),
                "created": getattr(mod, "created", "n/a"),
                "options": mod.options,
            }
        )
    except Exception:
        return jsonify({"error": traceback.format_exc()}), 500


@modules.route("/api/module/<path:module_path>/run", methods=["POST"])
def run_module(module_path):
    """
    Ruft ein definiertes Modul basierend auf dem angegebenen Pfad auf und führt es mit den
    übergebenen Parametern aus. Die Funktion behandelt Fehler, die bei der Verarbeitung auftreten,
    und gibt eine entsprechende JSON-Antwort zurück.

    :param module_path: Der Pfad des auszuführenden Moduls als String, der relativ zur Ladeumgebung
        des `loader` liegt.
    :type module_path: str

    :return: Eine JSON-Antwort, die entweder das Ergebnis der Modulausführung enthält oder
        eine Fehlermeldung bei einem aufgetretenen Fehler sowie den entsprechenden HTTP-Statuscode.
    :rtype: flask.Response
    """
    try:
        mod = loader.load_module(module_path)
        if not mod:
            return jsonify({"error": "Modul nicht gefunden"}), 404

        params = request.json or {}
        result = mod.run(params, mode="web")

        return jsonify(result)

    except Exception:
        return jsonify({"error": traceback.format_exc()}), 500


@modules.route("/api/module/<path:module_path>/save-options", methods=["POST"])
def save_module_options(module_path):
    try:
        mod = loader.load_module(module_path)
        if not mod:
            return jsonify({"error": "Modul nicht gefunden"}), 404

        db_manager = current_app.db_manager

        if not db_manager.get_user():
            return jsonify({"error": "Kein Benutzer angemeldet"}), 403

        options = request.json.get("options", {})
        designation = f"options::{mod.name}"
        content = json.dumps(options)
        success = db_manager.save_content(content, designation=designation)

        return jsonify({"success": success})

    except Exception:
        return jsonify({"error": traceback.format_exc()}), 500


@modules.route("/api/module/<path:module_path>/load-options", methods=["GET"])
def load_module_options(module_path):
    try:
        mod = loader.load_module(module_path)
        if not mod:
            return jsonify({"error": "Modul nicht gefunden"}), 404

        db_manager = current_app.db_manager

        if not db_manager.get_user():
            return jsonify({"error": "Kein Benutzer angemeldet"}), 403

        designation = f"options::{mod.name}"
        for _, content in db_manager.load_content(designation_filter=designation):
            return jsonify({"options": json.loads(content)})

        return jsonify({"options": None})  # nichts gespeichert

    except Exception:
        return jsonify({"error": traceback.format_exc()}), 500

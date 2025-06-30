# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os

from flask import Blueprint, render_template, jsonify, redirect, current_app
from flask_login import login_required, current_user
from .models import User

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """
    Rendert die Startseite der Anwendung.

    Diese Funktion überprüft den Debug-Modus der Anwendung und leitet den Benutzer
    bei aktivierter Debug-Umgebung zu einer bestimmten URL weiter. In der
    Produktivumgebung wird die Standard-Startseite gerendert.

    :returns: Eine HTTP-Umleitung zu einer alternativen URL im Debug-Modus
        oder die gerenderte Startseite im Produktionsmodus.
    :rtype: werkzeug.wrappers.Response
    """
    if current_app.debug:
        print("-- [ D E B U G - M O D E ] --")
        return redirect("http://localhost:5173/")
    return render_template("index.html")


@main.route("/api/config", methods=["GET"])
def api_config():
    """
    Stellt eine API-Endpunkt-Funktion bereit, um Konfigurationseinstellungen aus
    Umgebungsvariablen zu laden und im JSON-Format zurückzugeben. Diese Funktion
    ermöglicht es, spezifische Konfigurationswerte wie Sprache und andere
    Einstellungen dynamisch abzurufen

    Die zurückgegebene JSON-Datenstruktur enthält die folgenden Schlüssel:
    - 'lang': Die eingestellte Sprache, standardmäßig 'de', wenn nicht festgelegt.
    - 'other_setting': Eine weitere Konfigurationseinstellung, standardmäßig 'foo',
      wenn nicht festgelegt.
    """
    return jsonify({
        "lang": os.getenv("VITE_LANG", "de"),
        "other_setting": os.getenv("VITE_OTHER_SETTING", "foo"),
    })


@main.route("/api/user", methods=["GET"])
def api_user():
    """
    Stellt einen API-Endpunkt bereit, um Informationen über die aktuell
    authentifizierte Benutzerinstanz abzurufen. Gibt Nutzerinformationen
    zurück, falls ein Benutzer authentifiziert ist. Andernfalls wird der
    Status, dass kein Benutzer eingeloggt ist, übermittelt.

    :raises AttributeError: Falls ein angefordertes Benutzerattribut fehlt,
        aber aufgerufen wurde.
    :raises RuntimeError: Falls kein `current_user` Objekt im Kontext
        verfügbar ist.

    :return: Ein JSON-Objekt, das entweder Informationen zum aktuell
        authentifizierten Benutzer enthält, sofern vorhanden, oder den
        Zustand, dass kein Benutzer eingeloggt ist.
    :rtype: flask.Response
    """
    # Wenn Authentifiziert
    if current_user.is_authenticated:
        return jsonify(
            {
                "logged_in": True,
                "id": current_user.id,
                "username": current_user.username,
            }
        )
    else:
        # Wenn nicht authentifiziert, FALSE
        return jsonify({"logged_in": False})


@main.route("/api/users", methods=["GET"])
@login_required
def get_all_users():
    """
    Diese Funktion stellt eine API-Endpunkt-Implementierung dar, die eine Liste aller Benutzer
    in JSON-Format zurückgibt. Für den Zugriff auf diesen Endpunkt ist eine Authentifizierung
    erforderlich, die durch den `@login_required`-Decorator sichergestellt wird.

    :raises SQLAlchemyError: Wenn eine Datenbankabfrage fehlschlägt.
    :raises RuntimeError: Wenn die Benutzerobjekte nicht korrekt serialisiert werden können.
    :param method: HTTP-Methoden, die für diesen Endpunkt erlaubt sind, in diesem Fall GET.
    :type method: list[str]
    :return: Eine JSON-Liste aller Benutzer, wobei jeder Benutzer durch seine ID, E-Mail,
             Benutzernamen und Namen repräsentiert wird.
    :rtype: flask.Response
    """
    users = User.query.all()
    return jsonify(
        [
            {
                "id": user.id,
                "username": user.username,
            }
            for user in users
        ]
    )

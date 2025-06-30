# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
from flask import Blueprint, redirect, url_for, request, jsonify
from .models import db, User
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/api/login", methods=["POST"])
def api_login():
    """
    Authentifiziert einen Benutzer und ermöglicht den Login über die API.

    Diese Funktion verarbeitet Anmeldedaten, die im JSON-Format übermittelt werden,
    und prüft die übergebenen Benutzerinformationen. Wenn die Anmeldung erfolgreich
    ist, wird der Benutzer eingeloggt und eine Antwort mit der Erfolgsmeldung
    zurückgegeben. Bei fehlerhaften Anmeldedaten wird eine Fehlermeldung mit
    entsprechendem Statuscode gesendet.

    :param data: JSON-Daten, die die Anmeldedaten "username" und "password" enthalten.
    :type data: dict
    :param username: Der Benutzername, der aus den Anmeldedaten extrahiert wird.
    :type username: str
    :param password: Das Passwort, das aus den Anmeldedaten extrahiert wird.
    :type password: str
    :param user: Die aus der Datenbank abgerufene Benutzerinstanz, die zum angegebenen
                 Benutzernamen gehört.
    :type user: User
    :raises KeyError: Wenn die JSON-Daten keinen Benutzernamen oder kein Passwort enthalten.
    :raises ValueError: Wenn die Anmeldedaten ungültig sind.
    :raises TypeError: Bei fehlerhaftem JSON-Datenformat.

    :return: Eine JSON-Antwort mit einer Erfolgsmeldung und dem Benutzernamen, falls
             der Login erfolgreich ist. Bei fehlerhaften Anmeldedaten wird eine
             Fehlermeldung und der Statuscode 401 zurückgegeben.
    :rtype: flask.Response
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login erfolgreich", "username": user.username})
    else:
        return jsonify({"message": "Login fehlgeschlagen"}), 401


@auth.route("/api/logout")
@login_required
def api_logout():
    """
    Behandelt die API-Abmeldung eines angemeldeten Benutzers.

    Diese Funktion beendet die aktuelle Benutzeranmeldung und leitet den
    Benutzer zur Haupt-API-Benutzerseite weiter. Sie stellt sicher, dass
    die Abmeldung nur für authentifizierte Benutzer verfügbar ist.

    :return: Eine Umleitung zur Haupt-API-Benutzerseite.
    :rtype: flask.wrappers.Response
    """
    logout_user()
    return redirect(url_for("main.api_user"))


@auth.route("/api/register", methods=["POST"])
def api_register():
    """
    Handle die Registrierung eines neuen Benutzers durch die Verarbeitung
    einer HTTP-POST-Anfrage. Überprüft, ob die erforderlichen Daten vorliegen,
    ob der Benutzername verfügbar ist, und erstellt einen neuen Benutzer
    im System. Im Erfolgsfall erfolgt eine Weiterleitung zu einer
    definierten Zielseite.

    :raises ValueError: Wird ausgelöst, falls die Eingangsdaten unvollständig sind
        oder ein Benutzername bereits vorhanden ist.
    :param flask.Request request: Die HTTP-Anfrage, die die Registrierungsdaten
        enthält. Erwartet eine JSON-Nutzlast mit den Schlüsseln "username"
        und "password".
    :return: Eine HTTP-Antwort: entweder ein JSON-Fehlerobjekt oder eine
        erfolgreiche Weiterleitungsantwort.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Pflichtfelder fehlen"}), 400

    if User.query.filter((User.username == username)).first():
        return jsonify({"error": "Benutzername bereits vergeben"}), 409

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password=hashed_pw, salt="salt")
    db.session.add(new_user)
    db.session.commit()

    # Nach erfolgreicher Registrierung Weiterleitung zur Startseite
    return redirect(url_for("main.api_user"))

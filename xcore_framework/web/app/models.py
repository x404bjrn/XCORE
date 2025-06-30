# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    Repräsentiert einen Benutzer innerhalb einer Datenbank.

    Die User-Klasse speichert Benutzerdaten wie den Benutzernamen
    und das Passwort, die für die Identifizierung und Authentifizierung
    von Benutzern innerhalb einer Anwendung verwendet werden. Sie
    integriert sich in SQLAlchemy für die Datenbankverwaltung und
    Flask-Login für Benutzerverwaltung.

    :ivar id: Die eindeutige ID des Benutzers in der Datenbank.
    :type id: int
    :ivar username: Der Benutzername des registrierten Benutzers.
        Muss eindeutig sein.
    :type username: str
    :ivar password: Das verschlüsselte Passwort des Benutzers.
    :type password: str
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    salt = db.Column(db.String(128), nullable=True)


def init_db():
    db.create_all()

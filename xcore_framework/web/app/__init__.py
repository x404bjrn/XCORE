# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os

from flask import Flask
from flask_login import LoginManager
from .models import db, User
from xcore_framework.web.config import Config
from flask_cors import CORS

from xcore_framework.config.env import DIRECTORY_DATABASE
from xcore_framework.config.i18n import i18n
from xcore_framework.core.database_manager import DatabaseManager


def create_app():
    app = Flask(
        __name__,
        instance_path=DIRECTORY_DATABASE,
        instance_relative_config=True,
        static_folder="static",
        template_folder="templates",
    )
    CORS(app, supports_credentials=True)

    # Anwendungskonfigurationen
    app.config.from_object(Config)

    # Sicherstellen, dass der "instance" Ordner existiert
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path, exist_ok=True)

    # Initialisierung der Datenbank
    db_file_path = os.path.join(app.instance_path, "database.db")
    print(i18n.t("database.path", path=db_file_path))

    db.init_app(app)
    with app.app_context():
        try:
            if not os.path.exists(db_file_path):
                print(i18n.t("database.no_exist"))
                db.create_all(bind_key=None)
            else:
                print(i18n.t("database.found"))
        except Exception as e:
            print(i18n.t("database.init_error", e=e))
        print()

    # Login-Manager initialisieren
    login_manager = LoginManager()
    login_manager.login_view = "auth.api_login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # DB Manager global einhängbar machen
    app.db_manager = DatabaseManager()

    # Registrierte Blueprints
    from .auth import auth

    app.register_blueprint(auth)

    from .main import main

    app.register_blueprint(main)

    from .modules import modules

    app.register_blueprint(modules)

    return app

# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import pytest
from werkzeug.security import check_password_hash

from xcore_framework.core.database_manager import DatabaseManager


@pytest.fixture
def setup_database(tmp_path):
    db_path = tmp_path / "database.db"
    db_manager = DatabaseManager(db_path=tmp_path)
    db_manager.init_user_table()
    db_manager.init_content_table()
    yield db_manager
    db_manager.close()


def test_connect(setup_database):
    db = setup_database
    db.connect()
    assert db.conn is not None
    assert db.cursor is not None


def test_create_user(setup_database):
    db = setup_database
    db.create_user("testuser", "password123")
    db.connect()
    db.cursor.execute("SELECT * FROM users WHERE username = ?", ("testuser",))
    user = db.cursor.fetchone()
    assert user is not None
    assert user[1] == "testuser"
    assert check_password_hash(user[2], "password123")


def test_delete_user(setup_database):
    db = setup_database
    db.create_user("testuser", "password123")
    result = db.delete_user("testuser", "password123")
    assert result is True
    db.connect()
    db.cursor.execute("SELECT * FROM users WHERE username = ?", ("testuser",))
    user = db.cursor.fetchone()
    assert user is None


def test_login_user(setup_database):
    db = setup_database
    db.create_user("testuser", "password123")
    result = db.login("testuser", "password123")
    assert result is True
    assert db.logged_in_user == "testuser"
    assert db.session_key is not None


def test_duplicate_user(setup_database):
    db = setup_database
    db.create_user("testuser", "password123")
    result = db.create_user("testuser", "newpassword456")  # Sollte fehlschlagen
    assert result is False
    db.connect()
    db.cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", ("testuser",))
    count = db.cursor.fetchone()[0]
    assert count == 1


def test_logout_user(setup_database):
    db = setup_database
    db.create_user("testuser", "password123")
    db.login("testuser", "password123")
    db.logout()
    assert db.logged_in_user is None
    assert db.session_key is None


def test_save_and_load_content(setup_database):
    db = setup_database
    db.create_user("testuser", "password123")
    db.login("testuser", "password123")
    secret = "Dies ist ein geheimer Text"
    designation = "Notiz"
    db.save_content(secret, designation)
    result = db.load_content()
    assert len(result) == 1
    assert result[0][0] == designation
    assert result[0][1] == secret


def test_save_and_load_content_filtered(setup_database):
    db = setup_database
    db.create_user("testuser", "password123")
    db.login("testuser", "password123")
    db.save_content("Notiz A", "Notiz")
    db.save_content("Passwort X", "Passwort")
    result_notizen = db.load_content("Notiz")
    result_pass = db.load_content("Passwort")
    assert len(result_notizen) == 1
    assert result_notizen[0][1] == "Notiz A"
    assert result_pass[0][1] == "Passwort X"


def test_delete_database(setup_database):
    db = setup_database
    db.create_user("testuser", "password123")
    db.delete()
    assert not os.path.exists(db.db_path)

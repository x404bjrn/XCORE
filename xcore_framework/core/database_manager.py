# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import sqlite3
import base64

from werkzeug.security import check_password_hash, generate_password_hash
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

from xcore_framework.config.env import DIRECTORY_DATABASE
from xcore_framework.config.i18n import i18n


class DatabaseManager:
    """ Verwaltet eine SQLite-Datenbank mit Benutzer- und Inhaltstabellen. """

    def __init__(self, db_path=DIRECTORY_DATABASE):
        """
        Repräsentiert eine Klasse, die eine Verbindung zu einer SQLite-Datenbank herstellt
        und verwaltet, einschließlich grundlegender Benutzerauthentifizierung und
        Sitzungshandhabung.

        Attributes:
        db_path: Pfad zur SQLite-Datenbankdatei.
        conn: Verbindung zum SQLite-Datenbankobjekt.
        cursor: Cursorobjekt für die Ausführung von SQL-Abfragen.
        logged_in_user: Name des aktuell angemeldeten Benutzers.
        session_key: Schlüssel zur Identifizierung der aktuellen Benutzersitzung.
        user_salt: Salz-Wert des aktuell angemeldeten Benutzers für die Verschlüsselung.
        """
        self.db_path = os.path.join(db_path, "database.db")
        self.conn = None
        self.cursor = None
        self.logged_in_user = None
        self.session_key = None
        self.user_salt = None


    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        """
        Leitet einen kryptografischen Schlüssel von einem Passwort und einem Salt ab.

        Dies ist eine statische Methode, die ein Passwort und einen Salt verwendet, um mithilfe
        eines Key Derivation Function (KDF) einen sicheren, base64-kodierten Schlüssel zu erzeugen.

        Parameters:
            password (str): Das Passwort, das zur Ableitung des Schlüssels verwendet wird.
            salt (bytes): Der Salt, der zur Ableitung des Schlüssels verwendet wird.

        Returns:
            bytes: Der abgeleitete und base64-kodierte Schlüssel.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend(),
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))


    def encrypt_for_user(self, plaintext: str) -> str:
        """
        Verschlüsselt einen Klartext für den Benutzer unter Verwendung eines Sitzungsschlüssels.

        Die Methode verwendet den Sitzungsschlüssel zur Erstellung eines Fernet-Objekts
        und führt damit die Verschlüsselung des übergebenen Klartextes durch.

        Args:
        plaintext: Ein Klartext-String, der verschlüsselt werden soll.

        Returns:
        Ein String, der den verschlüsselten Text repräsentiert.

        Raises:
        ValueError: Wenn kein Sitzungsschlüssel vorhanden ist, entweder weil der Benutzer
        nicht eingeloggt ist oder weil der Schlüssel fehlt.
        """
        if not self.session_key:
            raise ValueError(i18n.t("database.no_encryption_key_found"))
        f = Fernet(self.session_key)
        return f.encrypt(plaintext.encode()).decode()


    def decrypt_for_user(self, encrypted_text: str) -> str:
        """
        Entschlüsselt einen verschlüsselten Text für den Benutzer.

        Diese Methode entschlüsselt einen gegebenen verschlüsselten Text mithilfe des
        aktuellen Sitzungsschlüssels, der vom Benutzer bereitgestellt oder während der
        Sitzung generiert wurde. Wenn kein Sitzungsschlüssel vorhanden ist, wird eine
        Fehlermeldung ausgelöst.

        Parameters:
            encrypted_text: str
                Der zu Entschlüsselnde verschlüsselte Text.

        Returns:
            str
                Der entschlüsselte Text im Klartext.

        Raises:
            ValueError
                Wenn kein Sitzungsschlüssel verfügbar ist.
        """
        if not self.session_key:
            raise ValueError(i18n.t("database.no_encryption_key_found"))
        f = Fernet(self.session_key)
        return f.decrypt(encrypted_text.encode()).decode()


    def connect(self):
        """
        Verbindet sich mit der SQLite-Datenbank, falls noch keine Verbindung besteht.

        Die Methode erstellt den Datenbankordner, falls dieser nicht existiert,
        und verbindet sich anschließend mit der SQLite-Datenbank, die durch den Pfad `db_path`
        definiert ist. Nach der erfolgreichen Verbindung wird ein Cursor-Objekt erstellt.
        Dieses ermöglicht die Ausführung von SQL-Abfragen.

        :raises sqlite3.Error: Falls es während der Verbindung zur SQLite-Datenbank
            zu einem Problem kommt.
        """
        if not self.conn:
            try:
                dir_path = os.path.dirname(self.db_path)
                if not os.path.exists(dir_path):
                    os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
                self.conn = sqlite3.connect(self.db_path)
                self.cursor = self.conn.cursor()
                print(i18n.t("database.connected", path=self.db_path))

            except sqlite3.Error:
                print(i18n.t("database.connection_error"))


    def close(self):
        """
        Schließt die aktive Verbindung zur Datenbank.

        Diese Methode überprüft, ob eine aktive Verbindung zur Datenbank besteht.
        Falls vorhanden, wird die Verbindung geschlossen, und sowohl die Verbindungs-
        als auch die Cursor-Objekte werden auf `None` gesetzt. Zusätzlich wird eine
        entsprechende Nachricht ausgegeben, um den Abschluss der Aktion zu bestätigen.

        :return: Kein Rückgabewert
        :rtype: None
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            print(i18n.t("database.disconnected"))


    def delete(self):
        """
        Löscht die Datenbankdatei, falls sie existiert, und schließt die Verbindung zur Datenbank.

        Diese Methode überprüft, ob die Datei an der angegebenen Datenbankpfad-Position existiert.
        Falls die Datei existiert, wird sie entfernt, und es erfolgt eine entsprechende Ausgabe.
        Falls die Datei nicht existiert, wird eine Meldung ausgegeben, dass keine Datenbank
        zum Löschen gefunden wurde.

        :rtype: None
        """
        self.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(i18n.t("database.deleted", path=self.db_path))
        else:
            print(i18n.t("database.no_found"))


    def init_user_table(self):
        """
        Initialisiert die Benutzertabelle in der Datenbank.

        Diese Methode erstellt eine Tabelle mit dem Namen 'users', falls diese noch
        nicht existiert. Die Tabelle enthält Felder für eine eindeutige ID, den
        Benutzernamen, das Passwort und einen individuellen Salt-Wert für die Verschlüsselung.
        Besteht die Tabelle bereits, wird keine neue erstellt.

        :raises sqlite3.Error: Wirft einen Fehler, falls ein Problem beim Zugriff auf
            die Datenbank oder beim Erstellen der Tabelle auftritt.
        :return: Gibt nichts zurück.
        """
        self.connect()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """
        )
        self.conn.commit()
        print(i18n.t("database.users_table_created"))
        self.close()


    def init_content_table(self):
        """
        Initialisiert die Tabelle für Benutzerinhalte in der Datenbank, wenn sie
        noch nicht existiert.

        Die Methode stellt sicher, dass die Tabelle 'user_contents' in der
        Datenbank erstellt wird. Diese Tabelle enthält Informationen über
        Benutzernamen und verschlüsselte Inhalte. Nach der erfolgreichen
        Erstellung wird die Änderung gespeichert und eine Bestätigungsmeldung
        ausgegeben.

        Arguments:
            Es werden keine Argumente an die Methode übergeben.

        Raises:
            Die Methode selbst löst keine Ausnahmen aus, aber mögliche
            Datenbank- oder Verbindungsfehler könnten an anderer Stelle
            auftreten.
        """
        self.connect()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_contents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                designation TEXT NOT NULL,
                encrypted_content TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
            )
        """
        )
        self.conn.commit()
        print(i18n.t("database.user_content_table_created"))
        self.close()

    def create_user(self, username, password):
        """
        Erstellt einen neuen Benutzer in der Datenbank.

        Diese Methode fügt einen neuen Benutzer mit dem angegebenen Benutzernamen und
        Passwort-Hash in die Tabelle 'users' der Datenbank ein. Für jeden Benutzer wird
        ein einzigartiger Salt-Wert generiert, der für die Verschlüsselung verwendet wird.
        Falls der Benutzername bereits existiert, wird ein entsprechender Hinweis ausgegeben.

        :param username: Der Benutzername des neuen Benutzers. Muss einzigartig sein.
        :type username: str
        :param password: Das Passwort des neuen Benutzers, das gehashed in der
            Datenbank gespeichert wird.
        :type password: str
        :return: True bei Erfolg, False bei Fehler.
        :rtype: bool
        """
        self.connect()
        password_hash = generate_password_hash(password)

        # Generiere einen zufälligen Salt für den Benutzer
        import os

        salt = base64.b64encode(os.urandom(16)).decode("utf-8")

        try:
            self.cursor.execute(
                "INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",
                (username, password_hash, salt),
            )
            self.conn.commit()
            print(i18n.t("database.user_created", username=username))
            self.close()
            return True

        except sqlite3.IntegrityError:
            print(i18n.t("database.already_exists", username=username))
            self.close()
            return False


    def delete_user(self, username, password):
        """
        Löscht einen Benutzer aus der Datenbank, wenn die Anmeldeinformationen korrekt sind.

        Beendet die Löschoperation, wenn versucht wird, den aktuellen Benutzer zu löschen.
        Verbindet sich mit der Datenbank, prüft die Existenz des Benutzers und verifiziert
        das zugehörige Passwort. Löscht den Benutzer aus der Datenbank, wenn die Prüfung
        erfolgreich ist.

        Args:
            username (str): Der Benutzername des zu löschenden Kontos.
            password (str): Das mit dem Benutzerkonto verknüpfte Passwort.

        Returns:
            bool: Gibt True zurück, wenn das Benutzerkonto erfolgreich gelöscht wurde,
                  andernfalls False.
        """
        if self.logged_in_user == username:
            print(i18n.t("database.user_delete_failed"))
            return False

        self.connect()
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        if user:
            stored_hash = user[2]
            if check_password_hash(stored_hash, password):
                self.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
                self.conn.commit()
                print(i18n.t("database.user_deleted", username=username))
                self.close()
                return True
            else:
                print(i18n.t("database.password_failed"))
                self.close()
                return False
        else:
            print(i18n.t("database.user_not_found"))
            self.close()
            return False


    def login(self, username, password):
        """
        Authentifiziert einen Benutzer durch Überprüfung der Anmeldedaten gegen eine Datenbank.

        Die Methode überprüft, ob ein Benutzer mit dem bereitgestellten Benutzernamen in der
        Datenbank existiert. Wenn ja, wird das gespeicherte Passwort-Hash überprüft, um die
        Identität zu verifizieren. Bei erfolgreicher Authentifizierung werden relevante
        Sitzungsinformationen wie der Sitzungs-Token generiert und zugewiesen.

        Args:
            username (str): Der Benutzername des Benutzers, der sich anmelden möchte.
            password (str): Das Passwort des Benutzers in unverschlüsselter Form.

        Returns:
            bool: True, wenn die Anmeldung erfolgreich war, andernfalls False.

        Raises:
            Keine.
        """
        self.connect()
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

        user = self.cursor.fetchone()

        if user:
            stored_hash = user[2]
            user_salt = user[3]  # Salt aus der Datenbank lesen

            if check_password_hash(stored_hash, password):
                self.logged_in_user = username
                self.user_salt = user_salt
                # Salt aus Base64-String in Bytes umwandeln
                salt_bytes = base64.b64decode(user_salt.encode("utf-8"))
                self.session_key = self._derive_key(password, salt_bytes)
                print(i18n.t("database.login_success", username=username))
                self.close()
                return True

            else:
                print(i18n.t("database.password_failed"))
                self.close()
                return False
        else:
            print(i18n.t("database.user_not_found"))
            self.close()
            return False


    def logout(self):
        """
        Loggt den aktuell angemeldeten Benutzer aus.

        Zusammenfassung:
        Diese Methode dient dazu, den aktuell angemeldeten Benutzer aus dem System
        auszuloggen. Nach erfolgreichem Ausloggen werden die angemeldete Benutzer-Variable,
        der Sitzungsschlüssel und der Benutzer-Salt zurückgesetzt, um anzuzeigen, dass
        kein Benutzer mehr authentifiziert ist.

        :return: Gibt keinen Rückgabewert zurück.
        :rtype: None
        """
        print(i18n.t("database.logged_out", logged_in_user=self.logged_in_user))
        self.logged_in_user = None
        self.session_key = None
        self.user_salt = None


    def save_content(self, content: str, designation: str = "default") -> bool:
        """
        Speichert einen verschlüsselten Inhalt für den angemeldeten Benutzer in der Datenbank.

        Abschnitt "summary" beschreibt die allgemeine Funktionalität der Methode.
        Die Methode überprüft, ob ein Benutzer angemeldet ist und ob ein Verschlüsselungsschlüssel
        verfügbar ist. Ist dies gegeben, wird der angegebene Inhalt verschlüsselt und in
        der Datenbank gespeichert. Der Erfolg der Speicherung wird zurückgegeben.

        Parameter:
            content: str
                Der unverschlüsselte Inhalt, der gespeichert werden soll.
            designation: str
                Eine optionale Beschreibung oder Bezeichnung für den zu speichernden Inhalt.
                Standardmäßig 'default'.

        Rückgabewert:
            bool
                Gibt True zurück, wenn der Inhalt erfolgreich gespeichert wurde, oder False,
                wenn die Operation fehlschlägt.

        Fehlermeldungen:
            Gibt in der Konsole Fehlermeldungen aus, wenn kein Benutzer angemeldet ist oder
            kein Verschlüsselungsschlüssel gefunden wurde.
        """
        if not self.logged_in_user:
            print(i18n.t("database.no_login_user"))
            return False

        if not self.session_key:
            print(i18n.t("database.no_encryption_key_found"))
            return False

        self.connect()

        encrypted = self.encrypt_for_user(content)

        # Prüfen, ob Eintrag schon existiert
        self.cursor.execute(
            "SELECT id FROM user_contents WHERE username = ? AND designation = ?",
            (self.logged_in_user, designation)
        )
        existing = self.cursor.fetchone()

        if existing:
            # Update des vorhandenen Eintrags
            self.cursor.execute(
                "UPDATE user_contents SET encrypted_content = ? WHERE id = ?",
                (encrypted, existing[0])
            )
        else:
            # Neuer Eintrag
            self.cursor.execute(
                "INSERT INTO user_contents (username, designation, encrypted_content) VALUES (?, ?, ?)",
                (self.logged_in_user, designation, encrypted)
            )

        self.conn.commit()
        print(i18n.t("database.content_save_success", logged_in_user=self.logged_in_user))

        self.close()
        return True

        #self.cursor.execute(
        #    "INSERT INTO user_contents (username, designation, encrypted_content) VALUES (?, ?, ?)",
        #    (self.logged_in_user, designation, encrypted),
        #)
        #self.conn.commit()
        #print(
        #    i18n.t("database.content_save_success", logged_in_user=self.logged_in_user)
        #)
        #
        #self.close()
        #return True


    def load_content(self, designation_filter: str = None) -> list:
        """
        Lädt Inhalte aus der Datenbank in Abhängigkeit von einem optionalen Filter und
        entschlüsselt sie.

        Args:
            designation_filter: Optional. Ein Filter, der den Inhalt nach der angegebenen
            Bezeichnung einschränkt.

        Returns:
            Eine Liste von Tupeln, wobei jedes Tupel eine Bezeichnung und den entschlüsselten
            Inhalt enthält. Falls die Entschlüsselung fehlschlägt, enthält das Tupel
            stattdessen eine Fehlermeldung.

        Raises:
            Keine spezifischen Fehler werden durch diese Funktion direkt ausgelöst.
            Allerdings kann ein generisches Exception-Objekt durch die
            Entschlüsselungsmethode auftreten.
        """
        if not self.logged_in_user:
            print(i18n.t("database.no_login_user"))
            return []

        self.connect()

        if designation_filter:
            self.cursor.execute(
                "SELECT designation, encrypted_content "
                "FROM user_contents "
                "WHERE username = ? "
                "AND designation = ?",
                (self.logged_in_user, designation_filter),
            )
        else:
            self.cursor.execute(
                "SELECT designation, encrypted_content "
                "FROM user_contents "
                "WHERE username = ?",
                (self.logged_in_user,),
            )

        rows = self.cursor.fetchall()
        contents = []

        for designation, enc in rows:
            try:
                decrypted = self.decrypt_for_user(enc)
                contents.append((designation, decrypted))

            except Exception as e:
                contents.append(
                    (designation, i18n.t("database.decryption_failed", e=str(e)))
                )

        self.close()
        return contents


    def get_user(self):
        """
        Gibt den aktuell angemeldeten Benutzer zurück.

        Diese Methode ermöglicht den Abruf des Benutzers, der derzeit im System angemeldet
        ist. Sie wird häufig verwendet, um Benutzerinformationen für die aktuelle Sitzung
        oder Interaktionen mit dem Benutzer zu erhalten.

        :return: Der aktuell angemeldete Benutzer.
        :rtype: object
        """
        return self.logged_in_user


    def get_all_users(self) -> list:
        """
        Ruft alle Benutzer aus der Datenbank ab.

        Diese Methode verbindet sich mit der Datenbank (falls noch nicht verbunden)
        und führt eine Abfrage auf die Tabelle 'users' aus, um alle Benutzernamen
        zurückzugeben.

        Returns:
            list: Eine Liste aller Benutzernamen als Strings.
        """
        self.connect()
        self.cursor.execute("SELECT username FROM users ORDER BY username ASC")
        rows = self.cursor.fetchall()
        self.close()
        return [row[0] for row in rows]

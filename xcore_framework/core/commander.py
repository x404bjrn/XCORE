# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import cmd

from xcore_framework.config.banner import show_banner, show_basic_banner
from xcore_framework.config.i18n import i18n
from xcore_framework.config.formatting import formatter, strip_ansi
from xcore_framework.config.env import set_env_key

from xcore_framework.core.module_loader import ModuleLoader
from xcore_framework.core.database_manager import DatabaseManager

try:
    import readline
except ImportError:
    print(i18n.t("system.notice_autocomplete"))


class XCoreShell(cmd.Cmd):
    """
    Repräsentiert eine interaktive Shell für die Verwaltung und Ausführung von
    Modulen. Die Shell bietet Funktionen wie Laden, Konfigurieren und
    Ausführen von Modulen sowie dynamische Eingabehilfe und Autovervollständigung.

    :ivar intro: Die Begrüßungsnachricht, die beim Starten der Shell angezeigt wird.
    :type intro: str
    :ivar completekey: Der Schlüssel für die Autovervollständigung.
    :type completekey: str
    :ivar loader: Ein `ModuleLoader` Objekt zum Laden und Verwalten von Modulen.
    :type loader: ModuleLoader
    :ivar current_module: Das aktuell geladene Modul.
    :type current_module: Optional[Module]
    :ivar options: Eine Sammlung von Modulparametern und ihren Werten.
    :type options: Dict[str, Any]
    """

    intro = i18n.t("system.cli_welcome")
    completekey = "tab"

    @property
    def doc_header(self):
        """ Anzeige des 'help' Headers. """
        return i18n.t("header.help")

    def __init__(self):
        """
        Initialisiert die Shell-Umgebung und bereitet das Laden von Modulen vor.
        Setzt das aktuelle Modul, die Moduloptionen und den Modul-Loader.
        """
        super().__init__()
        self.db = DatabaseManager()
        self.loader = ModuleLoader()
        self.current_module = None
        self.options = {}

    @property
    def prompt(self):
        """ Rückgabe des Prompts. """
        return i18n.t(
            "system.cli_prompt",
            current_module=self.current_module.name if self.current_module else "xcore",
        )

    def default(self, line):
        """ Fehlermeldung für unbekannte Befehle. """
        self.stdout.write(i18n.t("system.error_unknown_command", line=line) + "\n")

    def do_search(self, arg):
        """
        Durchsucht verfügbare Module nach einem Suchbegriff.
        Gibt eine Liste aller Module aus, deren Name den übergebenen Begriff enthält.
        """
        results = self.loader.search_modules(arg)

        # Ausgabe der Suchergebnisse (Banner)
        show_basic_banner(i18n.t("header.search_results"))

        for module in results:
            print(i18n.t("module.found", module=module))

        print("╚" + ("═" * 58) + "╝\n")

    @staticmethod
    def help_search():
        """ Dynamischen Hilfetext für `search` bereitstellen. """
        print(i18n.t("help.search"))

    def complete_search(self, text, line, begidx, endidx):
        """
        Autovervollständigung von `search`.
        Vorschläge basierend auf vorhandenen Modulen
        """
        return [m for m in self.loader.search_modules("") if m.startswith(text)]

    def do_use(self, path):
        """
        Lädt ein Modul anhand seines Pfads.
        Nach dem Laden wird das Modul aktiviert und seine Optionen stehen zur Verfügung.
        """
        module = self.loader.load_module(path)
        if module:
            self.current_module = module
            self.options = {k: v["default"] for k, v in module.options.items()}
            print(i18n.t("module.loaded", module=module.name))

        else:
            print(i18n.t("module.not_found"))

    @staticmethod
    def help_use():
        """ Dynamischen Hilfetext für `use` bereitstellen. """
        print(i18n.t("help.use"))

    def complete_use(self, text, line, begidx, endidx):
        """
        Autovervollständigung von `use`.
        Vorschläge basierend auf vorhandenen Modulen
        """
        return [m for m in self.loader.search_modules("") if m.startswith(text)]

    def do_list(self, arg):
        """
        Zeigt eine Übersicht aller verfügbaren Module mit Kurzbeschreibung.
        """
        modules = self.loader.search_modules("")
        if not modules:
            print(i18n.t("module.no_modules_found"))
            return

        # Ausgabe der XCORE Modulliste (Banner)
        show_basic_banner(i18n.t("header.module_list"))

        for mod_path in sorted(modules):
            mod = self.loader.load_module(mod_path)
            if mod:
                print("  {LBE}▶{X} {name}\n    - {desc}".format(
                    name=f"{mod.name:<30}", desc=f"{mod.description[:49]}...", **formatter))

        print("╚" + ("═" * 58) + "╝\n")

    @staticmethod
    def help_list():
        """ Dynamischen Hilfetext für `list` bereitstellen. """
        print(i18n.t("help.list"))

    def do_info(self, arg):
        """
        Zeigt Metadaten (Autor, Version, Beschreibung etc.) eines Moduls an.
        Bei leerem Argument wird das aktuell geladene Modul verwendet.
        """
        if arg:
            module = self.loader.load_module(arg)
            if not module:
                print(i18n.t("module.not_found"))
                return

        elif self.current_module:
            module = self.current_module

        else:
            print(i18n.t("module.no_module"))
            return

        # Ausgabe der Modulinformationen (Banner)
        show_banner("cli_module_info_banner",
                    name=module.name,
                    desc=module.description,
                    author=getattr(module, "author", "Unbekannt"),
                    version=getattr(module, "version", "1.0.0"),
                    created=getattr(module, "created", "n/a")
                    )

    @staticmethod
    def help_info():
        """ Dynamischen Hilfetext für `info` bereitstellen. """
        print(i18n.t("help.info"))

    def complete_info(self, text, line, begidx, endidx):
        """
        Autovervollständigung von `info`.
        Vorschläge basierend auf vorhandenen Modulen
        """
        return [m for m in self.loader.search_modules("") if m.startswith(text)]

    def do_show(self, arg):
        """
        Zeigt Informationen.
        'show options' - alle konfigurierbaren Parameter des geladenen Moduls werden angezeigt.
        'show users' - alle registrierten Benutzer werden angezeigt.
        """
        if arg.strip() == "options" and self.current_module:
            # Ausgabe der Moduloptionen (Banner)
            show_basic_banner(i18n.t("header.module_options"))

            for name, meta in self.current_module.options.items():
                current_value = self.options.get(name, "")
                default_value = meta.get("default", "")
                is_required = meta.get("required", False)
                description = meta.get("desc", "")
                space = "" if current_value else " "

                # Ausgabe der Moduloption (Banner)
                show_banner("cli_module_options_banner",
                            label=name,
                            required=is_required,
                            default=default_value,
                            current=current_value or "(nicht gesetzt)",
                            space=space,
                            desc=description)

        elif arg.strip() == "users":
            # Auslesen aller Benutzer aus der Datenbank
            all_users = self.db.get_all_users()

            # Ausgabe der registrierten Benutzer (Liste)
            show_basic_banner(i18n.t("header.user_list"), color=formatter["LGN"])

            for user in all_users:
                print("   {LBE}▶{X} {LYW}{user}{X}".format(user=user, **formatter))

            print("╚" + ("═" * 58) + "╝\n")

        else:
            print(i18n.t("module.invalid_show"))

    @staticmethod
    def help_show():
        """ Dynamischen Hilfetext für `show` bereitstellen. """
        print(i18n.t("help.show"))

    @staticmethod
    def complete_show(text, line, begidx, endidx):
        """
        Autovervollständigung von `show`.
        Vorschläge basierend auf vorhandenen Optionen
        """
        return ["options"] if "options".startswith(text) else []

    def do_set(self, line):
        """
        Setzt einen Parameterwert für das aktuelle Modul.
        Syntax: set <Parameter> <Wert>
        """
        if not self.current_module:
            print(i18n.t("module.no_module"))
            return

        try:
            key, value = line.split(maxsplit=1)

            if key in self.options:
                self.options[key] = value
                print(i18n.t("module.set_success", parameter=key, value=value))

            else:
                print(i18n.t("module.invalid_option"))

        except ValueError:
            print(i18n.t("module.set_usage"))

    @staticmethod
    def help_set():
        """ Dynamischen Hilfetext für `set` bereitstellen. """
        print(i18n.t("help.set"))

    def complete_set(self, text, line, begidx, endidx):
        """
        Autovervollständigung von `set`.
        Vorschläge basierend auf vorhandenen Parametern
        """
        return [k for k in self.options.keys() if k.startswith(text)]

    def do_run(self, arg):
        """
        Führt das aktuell geladene Modul mit den gesetzten Parametern aus.
        Vor der Ausführung wird geprüft, ob alle Pflichtparameter gesetzt sind.
        """
        if not self.current_module:
            print(i18n.t("module.no_module"))
            return

        missing = [
            k
            for k, v in self.current_module.options.items()
            if v["required"] and not self.options.get(k)
        ]

        if missing:
            print(i18n.t("module.missing_fields", fields=", ".join(missing)))
            return

        self.current_module.run(self.options)

    @staticmethod
    def help_run():
        """ Dynamischen Hilfetext für `run` bereitstellen. """
        print(i18n.t("help.run"))

    def do_back(self, arg):
        """
        Beendet das aktuell geladene Modul und kehrt zum vorherigen Zustand zurück.
        """
        if self.current_module:
            print(i18n.t("module.module_closed", module=self.current_module.name))
            self.current_module = None
            self.options = {}

        else:
            print(i18n.t("module.no_active_module"))

    @staticmethod
    def help_back():
        """ Dynamischen Hilfetext für `back` bereitstellen. """
        print(i18n.t("help.back"))

    @staticmethod
    def do_lang(arg):
        """
        Ändert die Anzeigesprache der CLI.
        Übergibt einen Sprachcode (z. B. 'de' oder 'en'), um die Sprache umzustellen.
        """
        if i18n.set_language(arg.strip()):
            # Setzt Eintrag in Umgebungsvariable
            set_env_key("XCORE_LANGUAGE", arg.strip())
            print(i18n.t("system.language_changed", lang=arg.strip()))

        else:
            print(i18n.t("system.language_not_supported"))

    @staticmethod
    def help_lang():
        """ Dynamischen Hilfetext für `lang` bereitstellen. """
        print(i18n.t("help.lang"))

    def do_user(self, arg):
        """
        Verarbeitet Benutzerbefehle, wie das Erstellen, Löschen, Anmelden, Abmelden von Benutzern und
        die Abfrage des aktuellen Benutzerstatus. Je nach eingegebenem Befehl analysiert die Methode
        den Input, führt die entsprechende Datenbankoperation aus und gibt eine Bestätigung oder
        Fehlermeldung aus.

        Diese Methode unterstützt die folgenden Befehle:
        - "create": Erstellen eines neuen Benutzers.
        - "delete": Löschen eines Benutzers.
        - "status": Überprüfung, welcher Benutzer aktuell angemeldet ist.

        Falls der eingegebene Befehl nicht gültig ist, wird eine Fehlermeldung auf der Konsole ausgegeben.
        """
        print()
        parts = arg.strip().split()

        if not parts:
            print(i18n.t("system.error_invalid_user_command"))
            print()
            return

        command = parts[0]
        args = parts[1:]

        if command == "create":
            if len(args) != 2:
                print("{LMA}Syntax{X}: {LYW}user create{X} <{LBE}benutzername{X}> <{LGN}passwort{X}>".format(**formatter))
            else:
                username, password = args
                self.db.create_user(username, password)

        elif command == "delete":
            if len(args) != 2:
                print("{LMA}Syntax{X}: {LYW}user delete{X} <{LBE}benutzername{X}> <{LGN}passwort{X}>".format(**formatter))
            else:
                username, password = args
                self.db.delete_user(username, password)

        elif command == "status":
            user = self.db.get_user()
            if user:
                print(i18n.t("database.login_as", user=user))
            else:
                print(i18n.t("database.no_login_user"))

        # INFO: Hier können weitere Unterbefehle für den 'user' Befehl hinzugefügt werden..
        else:
            print(i18n.t("system.error_invalid_user_command"))
        print()

    @staticmethod
    def help_user():
        """ Dynamischen Hilfetext für `user` bereitstellen. """
        print(i18n.t("help.user"))

    def do_login(self, arg):
        """
        Login für einen Benutzer.
        Syntax: user_login <name> <passwort>
        """
        print()
        try:
            username, password = arg.split()
            self.db.login(username, password)

        except ValueError:
            print("{LMA}Syntax{X}: {LYW}user login{X} "
                  "<{LBE}benutzername{X}> <{LGN}passwort{X}>".format(
                    **formatter))
        print()

    @staticmethod
    def help_login():
        """ Dynamischen Hilfetext für `login` bereitstellen. """
        print(i18n.t("help.login"))

    def do_logout(self, arg):
        """ Loggt den aktuellen Benutzer aus. """
        print()
        self.db.logout()
        print()

    @staticmethod
    def help_logout():
        """ Dynamischen Hilfetext für `logout` bereitstellen. """
        print(i18n.t("help.logout"))

    def do_save(self, arg):
        """
        Verarbeitet den 'save'-Befehl für die aktuelle Instanz. Der Befehl kann je nach
        Eingabe spezifische Unteroperationen ausführen, wie z. B. das Speichern von
        Optionseinstellungen einer aktuellen Modulinstanz in einer Datenbank.

        Args:
            arg (str): Der Eingabeparameter für den 'save'-Befehl. Dieser enthält
                       die spezifischen Unterbefehle und Optionen,
                       die verarbeitet werden sollen.

        Raises:
            KeyError: Kann ausgelöst werden, wenn ein Zugriff auf nicht vorhandene
                      Schlüssel innerhalb der gespeicherten Optionen erfolgt.
            ValueError: Kann ausgelöst werden, wenn der JSON-Dump fehlschlägt
                        oder ungültige Daten verarbeitet werden.
        """
        print()
        parts = arg.strip().split()

        if not parts:
            print(i18n.t("system.error_invalid_save_command"))
            print()
            return

        command = parts[0]
        #args = parts[1:] <- wenn benötigt kann ent-kommentiert werden..

        if command == "options":
            if not self.current_module:
                print(i18n.t("module.no_module"))
                print()
                return

            if not self.db.get_user():
                print(i18n.t("database.no_login_user"))
                print()
                return

            designation = f"options::{strip_ansi(self.current_module.name)}"
            try:
                import json

                content = json.dumps(self.options)
                success = self.db.save_content(content, designation=designation)
                if success:
                    print(i18n.t("database.options_saved", module=self.current_module.name))
            except Exception as e:
                print(i18n.t("database.options_save_failed", e=str(e)))

        # INFO: Hier können weitere Unterbefehle für den 'save' Befehl hinzugefügt werden..
        else:
            print(i18n.t("system.error_invalid_save_command"))
        print()

    @staticmethod
    def help_save():
        """ Dynamischen Hilfetext für `save` bereitstellen. """
        print(i18n.t("help.save"))

    def do_load(self, arg):
        """
        Lädt bestimmte Inhalte oder Einstellungen basierend auf dem übergebenen Argument
        und dem aktuellen Kontext des Systems, wie dem aktuellen Modul und Benutzerdaten.
        Diese Methode verarbeitet spezifische Unterbefehle, prüft den Status des Systems
        und interagiert mit einer Datenbank, um gespeicherte Inhalte zu laden.

        Args:
            arg (str): Der Befehl und optionale Parameter, die verarbeitet werden sollen.
                       Dieser wird analysiert, um spezifische Operationen wie das Laden
                       von gespeicherten Optionen durchzuführen.

        Raises:
            ValueError: Wird möglicherweise intern ausgelöst, wenn bestimmte Inhalte oder
                        Operationen nicht korrekt verarbeitet werden können
                        (z. B. fehlerhafte JSON-Daten). Diese Ausnahme wird jedoch
                        intern behandelt und nicht explizit weitergegeben.
        """
        print()
        parts = arg.strip().split()

        if not parts:
            print(i18n.t("system.error_invalid_load_command"))
            print()
            return

        command = parts[0]
        #args = parts[1:] <- wenn benötigt kann ent-kommentiert werden..

        if command == "options":
            if not self.current_module:
                print(i18n.t("module.no_module"))
                print()
                return

            if not self.db.get_user():
                print(i18n.t("database.no_login_user"))
                print()
                return

            designation = f"options::{strip_ansi(self.current_module.name)}"
            import json

            for name, content in self.db.load_content(designation_filter=designation):
                try:
                    loaded = json.loads(content)
                    self.options.update(loaded)
                    print(
                        i18n.t("database.options_loaded", module=self.current_module.name)
                    )
                    print()
                    return
                except Exception as e:
                    print(i18n.t("database.options_load_failed", e=str(e)))
                    print()
                    return
            print(i18n.t("database.no_saved_options", module=self.current_module.name))

        # INFO: Hier können weitere Unterbefehle für den 'load' Befehl hinzugefügt werden..
        else:
            print(i18n.t("system.error_invalid_load_command"))
        print()

    @staticmethod
    def help_load():
        """ Dynamischen Hilfetext für `load` bereitstellen. """
        print(i18n.t("help.load"))

    @staticmethod
    def do_exit(arg):
        """ Beendet das Programm. """
        print(i18n.t("system.cli_goodbye"))
        return True

    @staticmethod
    def help_exit():
        """ Dynamischen Hilfetext für `exit` bereitstellen. """
        print(i18n.t("help.exit"))


def start_cli():
    """ Startet den XCORE CLI-Modus (XCore-Shell). """
    show_banner(banner="cli_banner")

    shell = XCoreShell()
    shell.cmdloop()

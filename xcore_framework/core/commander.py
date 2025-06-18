# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import cmd

from xcore_framework.config.banner import show_banner
from xcore_framework.config.i18n import i18n
from xcore_framework.config.formatting import formatter, strip_ansi
from xcore_framework.core.module_loader import ModuleLoader
from xcore_framework.core.database_manager import DatabaseManager

try:
    import readline
except ImportError:
    print(i18n.t("notice.autocomplete"))


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

    intro = i18n.t("welcome.xcore_cli")
    completekey = "tab"

    @property
    def doc_header(self):
        """
        Dynamisch den Header basierend auf der aktuellen Sprache zurückgeben.
        """
        return i18n.t("help.header")

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
        """
        Dynamisch den Prompt basierend auf der aktuellen Sprache zurückgeben.
        """
        return i18n.t(
            "prompt.xcore_cli",
            current_module=self.current_module.name if self.current_module else "xcore",
        )

    def default(self, line):
        """
        Fehlermeldung für unbekannte Befehle.
        """
        self.stdout.write(i18n.t("unknown.command", line=line) + "\n")

    def do_search(self, arg):
        """
        Durchsucht verfügbare Module nach einem Suchbegriff.
        Gibt eine Liste aller Module aus, deren Name den übergebenen Begriff enthält.
        """
        results = self.loader.search_modules(arg)
        print()
        for module in results:
            print(i18n.t("module.found", module=module))
        print()

    @staticmethod
    def help_search():
        """Dynamischen Hilfetext für `search` bereitstellen."""
        print(i18n.t("help.search"))

    def complete_search(self, text, line, begidx, endidx):
        """
        Autovervollständigung von `search`.
        """
        # Vorschläge basierend auf vorhandenen Modulen
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
        """Dynamischen Hilfetext für `use` bereitstellen."""
        print(i18n.t("help.use"))

    def complete_use(self, text, line, begidx, endidx):
        """
        Autovervollständigung von `use`.
        """
        # Vorschläge basierend auf vorhandenen Modulen
        return [m for m in self.loader.search_modules("") if m.startswith(text)]

    def do_list(self, arg):
        """
        Zeigt eine Übersicht aller verfügbaren Module mit Kurzbeschreibung.
        """
        modules = self.loader.search_modules("")
        if not modules:
            print(i18n.t("module.no_modules_found"))
            return

        print(i18n.t("list.module_header"))
        print("=" * 60)
        for mod_path in sorted(modules):
            mod = self.loader.load_module(mod_path)
            if mod:
                print(f"{mod.name:<30} - {mod.description[:40]}")
        print("=" * 60)
        print()

    @staticmethod
    def help_list():
        """Dynamischen Hilfetext für `list` bereitstellen."""
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

        print(i18n.t("info.header"))
        print("=" * 60)
        print(i18n.t("info.name", name=module.name))
        print(i18n.t("info.description", desc=module.description))
        print(i18n.t("info.author", author=getattr(module, "author", "Unbekannt")))
        print(i18n.t("info.version", version=getattr(module, "version", "1.0.0")))
        print(i18n.t("info.created", created=getattr(module, "created", "n/a")))
        print("=" * 60)
        print()

    @staticmethod
    def help_info():
        """Dynamischen Hilfetext für `info` bereitstellen."""
        print(i18n.t("help.info"))

    def complete_info(self, text, line, begidx, endidx):
        """
        Autovervollständigung von `info`.
        """
        # Vorschläge basierend auf vorhandenen Modulen
        return [m for m in self.loader.search_modules("") if m.startswith(text)]

    def do_show(self, arg):
        """
        Zeigt Informationen zum aktuellen Modul.
        Mit 'show options' werden alle konfigurierbaren Parameter des geladenen Moduls angezeigt.
        """
        if arg.strip() == "options" and self.current_module:
            print(i18n.t("options.header"))
            print("=" * 60)
            for name, meta in self.current_module.options.items():
                current_value = self.options.get(name, "")
                default_value = meta.get("default", "")
                is_required = meta.get("required", False)
                description = meta.get("desc", "")
                space = "" if current_value else " "

                print(i18n.t("options.label", name=name))
                print(i18n.t("options.required", required=is_required))
                print(i18n.t("options.default", default=default_value))
                print(
                    i18n.t(
                        "options.current",
                        current=current_value or "(nicht gesetzt)",
                        space=space,
                    )
                )
                print(i18n.t("options.desc", desc=description))
                print(i18n.t("options.divider"))
            print()
        else:
            print(i18n.t("module.invalid_show"))

    @staticmethod
    def help_show():
        """Dynamischen Hilfetext für `show` bereitstellen."""
        print(i18n.t("help.show"))

    @staticmethod
    def complete_show(text, line, begidx, endidx):
        """
        Autovervollständigung von `show`.
        """
        # Vorschläge basierend auf vorhandenen Optionen
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
        """Dynamischen Hilfetext für `set` bereitstellen."""
        print(i18n.t("help.set"))

    def complete_set(self, text, line, begidx, endidx):
        """
        Autovervollständigung von `set`.
        """
        # Vorschläge basierend auf vorhandenen Parametern
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
        """Dynamischen Hilfetext für `run` bereitstellen."""
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
        """Dynamischen Hilfetext für `back` bereitstellen."""
        print(i18n.t("help.back"))

    @staticmethod
    def do_lang(arg):
        """
        Ändert die Anzeigesprache der CLI.
        Übergibt einen Sprachcode (z. B. 'de' oder 'en'), um die Sprache umzustellen.
        """
        if i18n.set_language(arg.strip()):
            # Setzt Eintrag in Umgebungsvariable
            from xcore_framework.config.env import set_env_key

            set_env_key("XCORE_LANGUAGE", arg.strip())
            print(i18n.t("language.changed", lang=arg.strip()))
        else:
            print(i18n.t("language.not_supported"))

    @staticmethod
    def help_lang():
        """Dynamischen Hilfetext für `lang` bereitstellen."""
        print(i18n.t("help.lang"))

    def do_user_create(self, arg):
        """
        Legt einen Benutzer an.
        Syntax: user_create <name> <passwort>
        """
        print()
        try:
            username, password = arg.split()
            self.db.create_user(username, password)
        except ValueError:
            print(
                "{LBE}Syntax{X}: user_create <benutzername> <passwort>".format(
                    **formatter
                )
            )
        print()

    @staticmethod
    def help_user_create():
        """Dynamischen Hilfetext für `user_create` bereitstellen."""
        print(i18n.t("help.user_create"))

    def do_user_delete(self, arg):
        """
        Entfernt (Löscht) einen Benutzer.
        Syntax: user_delete <name> <passwort>
        """
        print()
        try:
            username, password = arg.split()
            self.db.delete_user(username, password)
        except ValueError:
            print(
                "{LBE}Syntax{X}: user_delete <benutzername> <passwort>".format(
                    **formatter
                )
            )
        print()

    @staticmethod
    def help_user_delete():
        """Dynamischen Hilfetext für `user_delete` bereitstellen."""
        print(i18n.t("help.user_delete"))

    def do_user_login(self, arg):
        """
        Login für einen Benutzer.
        Syntax: user_login <name> <passwort>
        """
        print()
        try:
            username, password = arg.split()
            self.db.login(username, password)
        except ValueError:
            print(
                "{LBE}Syntax{X}: user_login <benutzername> <passwort>".format(
                    **formatter
                )
            )
        print()

    @staticmethod
    def help_user_login():
        """Dynamischen Hilfetext für `user_login` bereitstellen."""
        print(i18n.t("help.user_login"))

    def do_user_logout(self, arg):
        """
        Loggt den aktuellen Benutzer aus.
        """
        print()
        self.db.logout()
        print()

    @staticmethod
    def help_user_logout():
        """Dynamischen Hilfetext für `user_logout` bereitstellen."""
        print(i18n.t("help.user_logout"))

    def do_user_status(self, arg):
        """
        Zeigt den aktuellen Login-Status.
        """
        print()
        user = self.db.get_user()
        if user:
            print(i18n.t("database.login_as", user=user))
        else:
            print(i18n.t("database.no_login_user"))
        print()

    @staticmethod
    def help_user_status():
        """Dynamischen Hilfetext für `user_status` bereitstellen."""
        print(i18n.t("help.user_status"))

    def do_save_options(self, arg):
        """
        Speichert die aktuellen Optionen für das aktuelle Modul in der Datenbank.
        Die Methode prüft vor dem Speichervorgang, ob ein aktuelles Modul und ein
        eingeloggter Benutzer vorhanden sind. Falls diese Bedingungen nicht erfüllt sind,
        wird ein entsprechender Hinweis ausgegeben. Im Erfolgsfall werden die Optionen des
        Moduls als JSON-String in der Datenbank gespeichert. Tritt ein Fehler während des
        Speichervorgangs auf, wird dieser behandelt und eine Fehlermeldung
        ausgegeben.
        """
        print()
        if not self.current_module:
            print(i18n.t("module.no_module"))
            return

        if not self.db.get_user():
            print(i18n.t("database.no_login_user"))
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
        print()

    @staticmethod
    def help_save_options():
        """Dynamischen Hilfetext für `save_options` bereitstellen."""
        print(i18n.t("help.save_options"))

    def do_load_options(self, arg):
        """
        Lädt die Optionen für das aktuell ausgewählte Modul aus der Datenbank und
        aktualisiert die internen Einstellungen. Gibt entsprechende Meldungen zu
        den Ladevorgängen aus.
        """
        print()
        if not self.current_module:
            print(i18n.t("module.no_module"))
            return

        if not self.db.get_user():
            print(i18n.t("database.no_login_user"))
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
                return
            except Exception as e:
                print(i18n.t("database.options_load_failed", e=str(e)))
                return
        print(i18n.t("database.no_saved_options", module=self.current_module.name))
        print()

    @staticmethod
    def help_load_options():
        """Dynamischen Hilfetext für `load_options` bereitstellen."""
        print(i18n.t("help.load_options"))

    @staticmethod
    def do_exit(arg):
        """
        Beendet das Programm.
        """
        print(i18n.t("goodbye.bye"))
        return True

    @staticmethod
    def help_exit():
        """Dynamischen Hilfetext für `exit` bereitstellen."""
        print(i18n.t("help.exit"))


def start_cli():
    """
    Startet die XCore-Shell (CLI).
    """
    show_banner()
    shell = XCoreShell()
    shell.cmdloop()

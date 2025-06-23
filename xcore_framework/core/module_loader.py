# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import importlib.util
import os

from xcore_framework.config.env import DIRECTORY_MODULES


class ModuleLoader:
    """
    Eine Klasse zur Verwaltung und zum Laden von Modulen.

    Die Klasse ermöglicht es, Module anhand von Schlüsselwörtern in einem definierten
    Modulbasisverzeichnis zu suchen. Zudem können gefundene Module anhand ihres Pfades
    geladen werden. Die Module müssen Python-Dateien sein und einer spezifischen
    Namenskonvention folgen.

    :ivar module_base: Basisverzeichnis, in dem nach Modulen gesucht wird.
    :type module_base: str
    """

    def __init__(self):
        try:
            self.module_base = DIRECTORY_MODULES

        except Exception:
            # Fallback Modulpfad
            self.module_base = os.path.join(os.path.dirname(__file__), "..", "modules")

    def search_modules(self, keyword):
        """
        Sucht innerhalb eines Basisverzeichnisses nach Python-Modulen, deren Dateinamen ein
        bestimmtes Schlüsselwort enthalten. Diese Methode traversiert rekursiv alle
        Unterverzeichnisse, filtert Dateien, die mit `.py` enden und das Schlüsselwort
        enthalten, und gibt die übereinstimmenden Pfadnamen ohne `.py`-Endung zurück.
        Dateien mit dem Namen `__init__.py` werden bewusst ignoriert.

        :param keyword: Das Schlüsselwort, nach dem im Dateinamen gesucht wird.
        :type keyword: str
        :return: Eine Liste von relativen Pfaden zu den Python-Modulen, die das Schlüsselwort im
                 Dateinamen enthalten, ohne die `.py`-Dateiendung.
        :rtype: list[str]
        """
        matches = []
        for root, dirs, files in os.walk(self.module_base):
            for file in files:
                if file.endswith(".py") and keyword.lower() in file.lower():
                    if file.endswith("__init__.py"):
                        continue
                    rel_path = os.path.relpath(
                        os.path.join(root, file), self.module_base
                    )
                    matches.append(rel_path.replace(os.sep, "/")[:-3])  # ohne .py
        return matches

    def load_module(self, path):
        """
        Lädt ein Modul basierend auf dem bereitgestellten Pfad aus einem spezifischen Verzeichnis.
        Der Pfad wird relativ zur Basis des modulspezifischen Verzeichnisses interpretiert
        und die Datei wird anhand der .py-Endung lokalisiert und geladen.

        Falls die Datei nicht existiert, wird None zurückgegeben.
        Andernfalls wird das geladene Modul importiert und dessen Instanz zurückgegeben.

        :param path: Der Pfad zur zu ladenden Moduldatei, relativ zum Basisverzeichnis.
                     Teile des Pfads sollten mit '/' getrennt sein.
        :type path: str
        :return: Eine Instanz des geladenen Moduls oder None, falls die Datei nicht gefunden wird.
        :rtype: typing.Optional[object]
        """
        full_path = os.path.join(self.module_base, *path.split("/")) + ".py"

        if not os.path.isfile(full_path):
            return None

        spec = importlib.util.spec_from_file_location("mod", full_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        return mod.Module()

# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
# TODO: Pakete / Modul installationen (npm, pip etc. - ermöglichen und sinnvoll einarbeiten)
import os
import json
import platform

from typing import Optional

from xcore_framework.config.env import DIRECTORY_WORKSPACE, DIRECTORY_MODULES
from xcore_framework.config.formatting import strip_ansi
from xcore_framework.core.logger import setup_logger


def get_current_os() -> str:
    system = platform.system().lower()
    if "windows" in system:
        return "windows"
    elif "darwin" in system:
        return "osx"
    elif "linux" in system:
        return "linux"
    else:
        return "unknown"


def is_module_os_compatible(meta: dict) -> bool:
    current_os = get_current_os()
    os_list = meta.get("os")

    if not os_list:
        # Kein OS definiert → Modul gilt als global kompatibel
        return True

    if isinstance(os_list, str):
        os_list = [os_list]

    return current_os in [entry.lower() for entry in os_list]


class Xmod:
    def __init__(self, data: dict):
        self.data = data
        self.meta = data.get("meta", {})
        self.options = data.get("options", {})
        self.sections = data.get("sections", [])

        # Deklariere und initialisiere globales Arbeitsverzeichnis
        self.workdir = DIRECTORY_WORKSPACE

        # Initialisiere Logger Objekt
        self.logger = None
        self.init_logging()


    @classmethod
    def load(cls, path: str) -> "Xmod":
        with open(path, "r", encoding="utf-8") as f:
            return cls(json.load(f))


    def init_logging(self):
        self.logger = setup_logger(strip_ansi(self.get_name()).replace("/", "_"), con_handler=False)
        self.logger.debug(f"Initialisiere Modul '{self.get_name()}..'")


    def log(self, msg, level="info"):
        msg = strip_ansi(msg)
        if level == "debug":
            self.logger.debug(msg)
        elif level == "warning":
            self.logger.warning(msg)
        elif level == "error":
            self.logger.error(msg)
        else:
            self.logger.info(msg)


    def log_exec_info(self, state: dict, section_id: str):
        exec_info = state.get("__exec__", {})

        if not exec_info.get("success"):
            # Direkt Fehler abfangen und im Log protokollieren
            self.log(f"❌ Fehler in Section <{section_id}>: {exec_info.get('stderr')}", level="error")

        elif exec_info.get("success"):
            # Erfolgreiche Ausführung der Section im Log protokollieren
            self.log(f"✅ Section <{section_id}> erfolgreich ausgeführt")

        self.log(f"🔙 Rückgabecode: {exec_info.get('returncode')}")


    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)


    def is_valid(self) -> bool:
        return all(k in self.data for k in ["meta", "options", "sections"])


    def get_name(self) -> str:
        return self.meta.get("name", "n/a")


    def get_description(self) -> str:
        return self.meta.get("description", "")


    def get_author(self) -> str:
        return self.meta.get("author", "n/a")


    def get_version(self) -> str:
        return self.meta.get("version", "n/a")


    def get_created(self) -> str:
        return self.meta.get("created", "n/a")


    def get_category(self) -> str:
        return self.meta.get("category", "n/a")


    def get_os(self) -> str:
        return self.meta.get("os", "n/a")


    def get_languages(self) -> list[str]:
        return list({s.get("language", "n/a") for s in self.sections})


    def get_section_by_id(self, section_id: str) -> Optional[dict]:
        return next((s for s in self.sections if s.get("id") == section_id), None)


    def add_section(self, section: dict) -> None:
        self.sections.append(section)


    def add_option(self, key: str, option: dict) -> None:
        self.options[key] = option


    def to_dict(self) -> dict:
        return {
            "meta": self.meta,
            "options": self.options,
            "sections": self.sections
        }


    def run(self, params: dict, initial_state: Optional[dict] = None, mode="cli", gui_console=None) -> dict:
        self.log("▶️ Methode 'run' wird gestartet")
        state = initial_state or {}

        from xcore_framework.core.runtime_executor import XCoreRuntimeExecutor
        runtime_executor = XCoreRuntimeExecutor(working_dir=self.workdir)

        for section in self.sections:
            self.log(f"🚀 lade 'section' <{section['id']}>")

            # Section für Section ausführen mit jeweiligem Runtime (Interpreter)
            state = runtime_executor.execute(section, params, state, mode, gui_console)
            self.log_exec_info(state, section['id'])

            # INFO: Ausgabe der Ausführungsinformationen (Wenn nicht gewünscht, dann auskommentieren)
            print_exec_info(state)

        self.log("⏹️ Methode 'run' abgeschlossen")
        return state


def print_exec_info(state):
    info = state.get("__exec__", {})
    print("✅ Erfolgreich:", info.get("success"))
    print("📤 stdout:", info.get("stdout"))
    print("📥 stderr:", info.get("stderr"))
    print("⏎ Rückgabecode:", info.get("returncode"))
    print()


def load_xmod(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_module(rel_path: str, base_dir=DIRECTORY_MODULES, as_instance=False):
    path = os.path.abspath(os.path.join(base_dir, rel_path + ".xmod"))
    if os.path.exists(path):
        if as_instance:
            return Xmod.load(path)
        else:
            return load_xmod(path)
    return None


def get_all_modules(base_dir=DIRECTORY_MODULES):
    found = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".xmod"):
                try:
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        content = json.load(f)

                        meta = content.get("meta", {})
                        if not is_module_os_compatible(meta):
                            continue  # überspringen, wenn OS inkompatibel

                        modulname = meta.get("name", os.path.splitext(file)[0])
                        relative_root = os.path.relpath(root, base_dir)
                        found.append((relative_root, modulname))

                except Exception as e:
                    print(f"Fehler beim Lesen von {file}: {e}")
    return found


def search_modules(keyword: str, base_dir=DIRECTORY_MODULES):
    keyword = keyword.lower()
    results = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".xmod"):
                try:
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        content = json.load(f)

                        meta = content.get("meta", {})
                        if not is_module_os_compatible(meta):
                            continue

                        name = meta.get("name", "")
                        desc = meta.get("description", "")
                        cat = meta.get("category", "")
                        author = meta.get("author", "")

                        if any(keyword in val.lower() for val in [name, desc, cat, author]):
                            relative_root = os.path.relpath(root, base_dir)
                            results.append((relative_root, name))

                except Exception as e:
                    print(f"Fehler beim Lesen von {file}: {e}")
    return results

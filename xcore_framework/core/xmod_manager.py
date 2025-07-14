# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import json
import tempfile
import subprocess
import importlib.util

from typing import Optional

from xcore_framework.config.env import RUNTIME_PACKAGE, DIRECTORY_MODULES
from xcore_framework.config.formatting import strip_ansi
from xcore_framework.core.logger import setup_logger


class Xmod:
    def __init__(self, data: dict):
        self.data = data
        self.meta = data.get("meta", {})
        self.options = data.get("options", {})
        self.sections = data.get("sections", [])

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
        self.log("Methode 'run' wird gestartet")
        state = initial_state or {}

        for section in self.sections:
            self.log(f"lade 'section' <{section['id']}>")
            state = run_section(section, params, state, mode, gui_console)
            self.log(f"'section' <{section['id']}> abgeschlossen")

        self.log("Methode 'run' abgeschlossen")
        return state


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
                        modulname = content.get("meta", {}).get("name", os.path.splitext(file)[0])
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


def run_section(section, params, state, mode="cli", gui_console=None):
    lang = section["language"]
    code = section["code"]

    if lang == "python":
        return run_python_section(code, params, state, mode, gui_console)

    elif lang == "java":
        return run_java_section(code, params, state)

    elif lang == "bash":
        return run_bash_section(code, params, state)

    elif lang == "powershell":
        return run_powershell_section(code, params, state)

    else:
        raise ValueError(f"Nicht unterstützte Sprache: {lang}")


def run_bash_section(code: str, params: dict, state: dict):
    tempdir = tempfile.mkdtemp()
    bash_file = os.path.join(tempdir, "script.sh")
    param_file = os.path.join(tempdir, "params.json")
    state_file = os.path.join(tempdir, "state.json")

    with open(bash_file, "w", encoding="utf-8") as f:
        f.write(code)

    os.chmod(bash_file, 0o755)

    with open(param_file, "w") as f:
        json.dump(params, f)

    with open(state_file, "w") as f:
        json.dump(state, f)

    subprocess.run([
        "bash",
        bash_file,
        param_file,
        state_file
    ], check=True)

    with open(state_file) as f:
        return json.load(f)


def run_powershell_section(code: str, params: dict, state: dict):
    tempdir = tempfile.mkdtemp()
    ps1_file = os.path.join(tempdir, "script.ps1")
    param_file = os.path.join(tempdir, "params.json")
    state_file = os.path.join(tempdir, "state.json")

    with open(ps1_file, "w", encoding="utf-8") as f:
        f.write(code)

    with open(param_file, "w") as f:
        json.dump(params, f)

    with open(state_file, "w") as f:
        json.dump(state, f)

    subprocess.run([
        "powershell",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        ps1_file,
        param_file,
        state_file
    ], check=True)

    with open(state_file) as f:
        return json.load(f)


def run_python_section(code: str, params: dict, state: dict, mode="cli", gui_console=None):
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as temp:
        temp.write(code + "\n\nresult = run(params, state)")
        temp_path = temp.name

    spec = importlib.util.spec_from_file_location("mod", temp_path)
    mod = importlib.util.module_from_spec(spec)

    # Übergabe von Variablen
    mod.params = params
    mod.state = state
    mod.mode = mode
    mod.gui_console = gui_console

    spec.loader.exec_module(mod)
    os.unlink(temp_path)

    return mod.result


def run_java_section(code: str, params: dict, state: dict):
    # Temporäre Datei schreiben
    tempdir = tempfile.mkdtemp()
    java_file = os.path.join(tempdir, "RenameFiles.java")

    with open(java_file, "w", encoding="utf-8") as f:
        f.write(code)

    # Kompilieren
    subprocess.run([
        rf"{RUNTIME_PACKAGE['DIRECTORY_RUNTIMES']}\java\jdk-20.0.2+9\bin\javac.exe",
        java_file
    ], check=True)

    # Daten über temporäre JSON-Dateien austauschen
    with open(os.path.join(tempdir, "params.json"), "w") as f:
        json.dump(params, f)

    with open(os.path.join(tempdir, "state.json"), "w") as f:
        json.dump(state, f)

    # Java ausführen (z. B. mit Übergabe von Dateipfaden)
    subprocess.run([
        rf"{RUNTIME_PACKAGE['DIRECTORY_RUNTIMES']}\java\jdk-20.0.2+9\bin\java.exe",
        "-cp",
        tempdir,
        "RenameFiles",
        os.path.join(tempdir, "params.json"),
        os.path.join(tempdir, "state.json")
    ], check=True)

    # Ergebnisse wieder einlesen
    with open(os.path.join(tempdir, "state.json")) as f:
        return json.load(f)

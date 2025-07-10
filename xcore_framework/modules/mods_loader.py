
# INFO: Das ist nur ein Testmodul zum Aufbau der neuen Modulladefunktionen
# TODO: Fertigstellen

import json, tempfile, subprocess, importlib.util, os
from xcore_framework.config.env import RUNTIME_PACKAGE

def load_xmod(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_section(section, params, state):
    lang = section["language"]
    code = section["code"]

    if lang == "python":
        return run_python_section(code, params, state)
    elif lang == "java":
        return run_java_section(code, params, state)
    else:
        raise ValueError(f"Nicht unterstützte Sprache: {lang}")

def run_python_section(code: str, params: dict, state: dict):
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as temp:
        temp.write(code + "\n\nresult = run(params, state)")
        temp_path = temp.name

    spec = importlib.util.spec_from_file_location("mod", temp_path)
    mod = importlib.util.module_from_spec(spec)
    mod.params = params
    mod.state = state
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
    subprocess.run([rf"{RUNTIME_PACKAGE['DIRECTORY_RUNTIMES']}\java\jdk-20.0.2+9\bin\javac.exe", java_file], check=True)

    # Daten über temporäre JSON-Dateien austauschen
    with open(os.path.join(tempdir, "params.json"), "w") as f:
        json.dump(params, f)
    with open(os.path.join(tempdir, "state.json"), "w") as f:
        json.dump(state, f)

    # Java ausführen (z. B. mit Übergabe von Dateipfaden)
    subprocess.run([rf"{RUNTIME_PACKAGE['DIRECTORY_RUNTIMES']}\java\jdk-20.0.2+9\bin\java.exe", "-cp", tempdir, "RenameFiles", os.path.join(tempdir, "params.json"), os.path.join(tempdir, "state.json")], check=True)

    # Ergebnisse wieder einlesen
    with open(os.path.join(tempdir, "state.json")) as f:
        return json.load(f)

# def run_java_section(code: str, params: dict, state: dict):
#     import shutil
#
#     tempdir = tempfile.mkdtemp()
#     java_file = os.path.join(tempdir, "RenameFiles.java")
#     with open(java_file, "w", encoding="utf-8") as f:
#         f.write(code)
#
#     # Kompilieren
#     compile_proc = subprocess.run(
#         [r"C:\Users\Admin\Desktop\XCORE\xcore_framework\runtimes\java\jdk-20.0.2+9\bin\javac.exe", java_file],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True
#     )
#     print("JAVAC STDOUT:\n", compile_proc.stdout)
#     print("JAVAC STDERR:\n", compile_proc.stderr)
#
#     # JSON-Dateien schreiben
#     with open(os.path.join(tempdir, "params.json"), "w") as f:
#         json.dump(params, f)
#     with open(os.path.join(tempdir, "state.json"), "w") as f:
#         json.dump(state, f)
#
#     # Ausführen mit Ausgabe
#     exec_proc = subprocess.run(
#         [
#             r"C:\Users\Admin\Desktop\XCORE\xcore_framework\runtimes\java\jdk-20.0.2+9\bin\java.exe",
#             "-cp", tempdir,
#             "RenameFiles",
#             os.path.join(tempdir, "params.json"),
#             os.path.join(tempdir, "state.json")
#         ],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         text=True
#     )
#     print("JAVA STDOUT:\n", exec_proc.stdout)
#     print("JAVA STDERR:\n", exec_proc.stderr)
#
#     with open(os.path.join(tempdir, "state.json")) as f:
#         return json.load(f)

# Beispielnutzung
xmod = load_xmod("file_renamer.xmod")
params = {
    "target_folder": os.path.abspath("./tmp/"),
    "prefix": "neu_"
}
state = {}

for section in xmod["sections"]:
    state = run_section(section, params, state)
    print(state)
    # TODO: Hier weiter machen.. funzt noch nicht richtig
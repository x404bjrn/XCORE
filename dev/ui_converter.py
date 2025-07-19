# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import subprocess


def compile_ui_file(input_path, output_path):
    cmd = ["pyside6-uic", input_path, "-o", output_path]

    try:
        subprocess.run(cmd, check=True)
        print(f"[✅] Kompiliert: {input_path} → {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"[❌] Fehler beim Kompilieren: {input_path}")
        print(e)


def compile_ui_folder(source_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".ui"):
                input_file = os.path.join(root, file)
                base_name = os.path.splitext(file)[0] + "_ui.py"
                output_file = os.path.join(output_dir, base_name)
                compile_ui_file(input_file, output_file)


if __name__ == "__main__":
    # Kompilieren von UIs für den Module-Editor
    compile_ui_folder("ui/module_editor", "../xcore_framework/editor/ui")

    # Kompilieren von UIs für den GUI-Mode von XCORE
    compile_ui_folder("ui/xcore_gui_mode", "../xcore_framework/gui/ui")

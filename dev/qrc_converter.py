# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import subprocess


def compile_qrc_file(input_path, output_path):
    cmd = ["pyside6-rcc", input_path, "-o", output_path]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ QRC kompiliert: {input_path} → {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler bei {input_path}")
        print(e)


def compile_qrc_folder(source_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".qrc"):
                input_file = os.path.join(root, file)
                base_name = os.path.splitext(file)[0] + "_rc.py"
                output_file = os.path.join(output_dir, base_name)
                compile_qrc_file(input_file, output_file)


if __name__ == "__main__":
    # Kompilieren von UI Ressourcen (QRC)
    compile_qrc_folder("qrc", "src/generated")

# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import subprocess
import os
import shutil

# sucht npx im Systempfad
NPX_PATH = shutil.which("npx")

# Pfade definieren
base_dir = os.path.dirname(__file__)
scss_input = os.path.abspath(os.path.join(base_dir, "../design/scss/main.scss"))

css_output_design = os.path.abspath(os.path.join(base_dir, "../design/css/main.min.css"))
css_output_react = os.path.abspath(os.path.join(base_dir, "../dev/frontend/web/src/styles/main.min.css"))

def compile_with_dart_sass():
    try:
        # Sass-Befehl zusammenbauen
        command = [
            NPX_PATH, "sass",
            scss_input,
            css_output_design,
            "--style=compressed",
            "--no-source-map"
        ]

        print(f"[*] Kompiliere SCSS → CSS mit Dart-Sass (Design)...")
        print(f"[*] Eingabe: {scss_input}")
        print(f"[*] Ausgabe: {css_output_design}")

        print("[✓] Kompilierung [1/2] erfolgreich!")

        subprocess.run(command, check=True)

        command = [
            NPX_PATH, "sass",
            scss_input,
            css_output_react,
            "--style=compressed",
            "--no-source-map"
        ]

        print(f"[*] Kompiliere SCSS → CSS mit Dart-Sass (React Frontend)...")
        print(f"[*] Eingabe: {scss_input}")
        print(f"[*] Ausgabe: {css_output_react}")

        subprocess.run(command, check=True)

        print("[✓] Kompilierung [2/2] erfolgreich!")

    except subprocess.CalledProcessError as e:
        print(f"[x] Fehler beim Kompilieren:\n{e}")

    except FileNotFoundError:
        print("[x] Fehler: Stelle sicher, dass Node.js und Dart-Sass (npx sass) installiert sind!")

if __name__ == "__main__":
    compile_with_dart_sass()

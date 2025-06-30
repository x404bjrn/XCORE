# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import shutil


# Basisverzeichnis ermitteln (wo das Skript ausgeführt wird)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Zu kopierende Dateien und ihre Pfade relativ zum Basisverzeichnis
files_to_copy = {
    "CHANGELOG.md": "CHANGELOG.md",
    "DOCUMENTATION_DE.md": os.path.join("docs", "DOCUMENTATION_DE.md"),
    "DOCUMENTATION_EN.md": os.path.join("docs", "DOCUMENTATION_EN.md"),
    "LICENSE": "LICENSE",
    "README.md": "README.md",
    "README_EN.md": os.path.join("docs", "README_EN.md"),
    "CONTRIBUTING.md": "CONTRIBUTING.md",
    "CONTRIBUTING_EN.md": os.path.join("docs", "CONTRIBUTING_EN.md"),
    "CODE_OF_CONDUCT.md": "CODE_OF_CONDUCT.md",
    "CODE_OF_CONDUCT_EN.md": os.path.join("docs", "CODE_OF_CONDUCT_EN.md"),
}

# Zielverzeichnisse
target_dirs = [
    os.path.join(BASE_DIR, "dev", "frontend", "web", "public"),
    os.path.join(BASE_DIR, "xcore_framework", "docs"),
]

# Kopiervorgang
for filename, relative_path in files_to_copy.items():
    source_path = os.path.join(BASE_DIR, relative_path)

    if not os.path.exists(source_path):
        print(f"[!] Datei nicht gefunden: {source_path}")
        continue

    for target_dir in target_dirs:
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, filename)

        try:
            shutil.copy2(source_path, target_path)
            print(f"[+] Kopiert: {filename} → {target_path}")
        except Exception as e:
            print(f"[!] Fehler beim Kopieren von {filename}: {e}")

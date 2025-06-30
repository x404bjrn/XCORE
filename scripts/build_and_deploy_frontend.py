# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import shutil
import subprocess

from pathlib import Path


# Pfade definieren
frontend_dir = Path("../dev/frontend/web").resolve()
dist_dir = frontend_dir / "dist"
templates_dir = Path("../xcore_framework/web/app/templates").resolve()
static_dir = Path("../xcore_framework/web/app/static").resolve()


def run_command(command, cwd):
    print(f"[*] 🚀 Führe Befehl aus: {command} (im Verzeichnis {cwd})")
    result = subprocess.run(command, cwd=cwd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"[!] ❌ Befehl fehlgeschlagen: {command}")


def clear_directory(path):
    print(f"[*] 🧹 Leere Verzeichnis: {path}")
    for item in path.iterdir():
        if item.name == ".gitignore":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def copy_dist_files():
    print("[*] 📁 Kopiere index.html nach Templates...")
    index_file = dist_dir / "index.html"
    shutil.copy(index_file, templates_dir / "index.html")

    print("[*] 📁 Kopiere restliche Dateien nach Static...")
    for item in dist_dir.iterdir():
        if item.name == "index.html":
            continue
        target = static_dir / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy(item, target)


def main():
    if not frontend_dir.exists():
        raise FileNotFoundError(f"[!] Frontend-Verzeichnis nicht gefunden: {frontend_dir}")

    # Schritt 1: npm install & build
    run_command("npm install", cwd=frontend_dir)
    run_command("npm run build", cwd=frontend_dir)

    # Schritt 2: Zielverzeichnisse leeren
    clear_directory(templates_dir)
    clear_directory(static_dir)

    # Schritt 3: Dateien kopieren
    copy_dist_files()

    # Schritt 4: dist-Verzeichnis entfernen
    print(f"[*] 🗑️ Entferne dist-Verzeichnis: {dist_dir}")
    shutil.rmtree(dist_dir)

    print("[+] ✅ Build und Deployment erfolgreich abgeschlossen!")


if __name__ == "__main__":
    main()

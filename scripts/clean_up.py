# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import shutil


# Basisverzeichnis festlegen (Projekt-Root-Dir)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Liste der Pfade, die geprüft und ggf. gelöscht werden sollen
# INFO: Hier erweitern, wenn weitere Dateien oder Verzeichnisse bereinigt werden sollen
paths_to_check = [
    f"{BASE_DIR}/*.egg-info",
    f"{BASE_DIR}/dist",
    f"{BASE_DIR}/build",
    f"{BASE_DIR}/xcore_framework/.env",
    f"{BASE_DIR}/xcore_framework/database",
    f"{BASE_DIR}/dev/frontend/web/dist"
]


def find_existing_paths(paths):
    """ Überprüfen, ob Dateien oder Verzeichnisse existieren """
    existing = []
    for path in paths:
        # Unterstützung für Muster mit *
        if "*" in path:
            # z.B. ./something/*.egg-info
            paths_found = [p for p in os.listdir(os.path.dirname(path)) if p.endswith('.egg-info')]
            for p in paths_found:
                full_path = os.path.join(BASE_DIR, p)
                if os.path.exists(full_path):
                    existing.append(full_path)
        else:
            if os.path.exists(path):
                existing.append(path)
    return existing


# Löschvorgang
def delete_paths(paths):
    """ Löschen der Dateien oder Verzeichnisse """
    for path in paths:
        try:
            if os.path.isfile(path):
                os.remove(path)
                print(f"[✓] Datei gelöscht: {path}")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                print(f"[✓] Verzeichnis gelöscht: {path}")
            else:
                print(f"[!] Unbekannter Pfadtyp: {path}")
        except Exception as e:
            print(f"[!] Fehler beim Löschen von {path}: {e}")


def main():
    """
    Hauptfunktion zur Bereinigung von Dateien oder Verzeichnissen.

    Diese Funktion prüft eine vorgegebene Liste von Pfaden, ob sie existieren.
    Falls relevante Dateien oder Verzeichnisse gefunden werden,
    informiert sie den Benutzer und fragt nach einer Bestätigung,
    ob diese gelöscht werden sollen.
    Je nach Antwort werden die Dateien/Verzeichnisse entweder gelöscht
    oder die Operation abgebrochen.
    """
    existing_paths = find_existing_paths(paths_to_check)

    if not existing_paths:
        print("[*] Keine zu löschenden Dateien oder Verzeichnisse gefunden.")
        return

    print("[*] Folgende Dateien/Verzeichnisse wurden gefunden und können gelöscht werden:")
    for p in existing_paths:
        print(f"  {p}")

    confirm = input("[?] Möchten Sie diese Dateien/Verzeichnisse wirklich löschen? (j/n): ").lower()
    if confirm == 'j':
        delete_paths(existing_paths)
        print("[+] Bereinigung abgeschlossen.")
    else:
        print("[x] Abgebrochen. Es wurde nichts gelöscht.")


if __name__ == "__main__":
    main()

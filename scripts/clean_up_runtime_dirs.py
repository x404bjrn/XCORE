# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import shutil


# Basisverzeichnis definieren (Projekt-Root-Verzeichnis)
BASE_DIR = os.path.expanduser('~/.xcore/')

# Die vier Runtime-Verzeichnisse, deren Inhalte gelöscht werden sollen
runtime_dirs = [
    os.path.join(BASE_DIR, "runtimes", "bash"),
    os.path.join(BASE_DIR, "runtimes", "node"),
    os.path.join(BASE_DIR, "runtimes", "java"),
    os.path.join(BASE_DIR, "runtimes", "powershell"),
]


def clear_directory_contents(directory):
    """
    Entfernt den Inhalt eines angegebenen Verzeichnisses.
    Es werden alle Dateien, symbolischen Links und Unterverzeichnisse im Verzeichnis gelöscht.
    Falls das Verzeichnis nicht existiert, wird eine entsprechende Meldung ausgegeben.
    Fehler während des Löschprozesses werden ebenfalls protokolliert.

    Args:
        directory (str): Der Pfad zu dem Verzeichnis, dessen Inhalt gelöscht werden soll.
    """
    if not os.path.isdir(directory):
        print(f"[!] Verzeichnis existiert nicht: {directory}")
        return

    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
                print(f"[✓] Datei gelöscht: {path}")

            elif os.path.isdir(path):
                shutil.rmtree(path)
                print(f"[✓] Verzeichnis gelöscht: {path}")

        except Exception as e:
            print(f"[!] Fehler beim Löschen von {path}: {e}")


def main():
    """
    Führt eine Bereinigung von Verzeichnisinhalten durch basierend auf Benutzereingaben.

    Die Funktion zeigt zunächst die Verzeichnisse an, die geleert werden sollen,
    und fragt den Benutzer, ob diese Operation durchgeführt werden soll.
    Bei Bestätigung werden die Inhalte der Verzeichnisse bereinigt.

    Raises:
        ValueError: Wird ausgelöst, wenn der Benutzer eine ungültige Eingabe angibt oder
                    wenn beim Bereinigen der Verzeichnisse ein Fehler auftritt.
    """
    print("[*] Folgende Verzeichnisse werden inhaltlich geleert:")
    for d in runtime_dirs:
        print(f"  {d}")

    confirm = input("[?] Möchten Sie diese Verzeichnisinhalte wirklich löschen? (j/n): ").strip().lower()
    if confirm != 'j':
        print("[x] Abgebrochen. Es wurde nichts gelöscht.")
        return

    for directory in runtime_dirs:
        print(f"[*] Bereinige Inhalt von: {directory}")
        clear_directory_contents(directory)

    print("[+] Alle angegebenen Verzeichnisinhalte wurden bereinigt.")


if __name__ == "__main__":
    main()

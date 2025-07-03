# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import click
import subprocess

from pathlib import Path


@click.command()
@click.argument("cmd", nargs=-1)
@click.argument("cwd")
def main(cmd, cwd):
    click.echo("[*] starte Ausführung...")
    click.echo(f"[*] Eingabe Befehle   : {cmd}")
    click.echo(f"[*] Arbeitsverzeichnis: {cwd}")

    # Arbeitsverzeichnis Path-Objekt erstellen
    cwd_path = Path(str(cwd)).resolve()

    # Prüfen, ob Verzeichnispfad existiert
    if not cwd_path.exists():
        raise FileNotFoundError(f"[!] Verzeichnis nicht gefunden: {cwd_path}")

    # Befehlsausführung
    result = subprocess.run(cmd, cwd=cwd_path, shell=True)

    if result.returncode != 0:
        raise RuntimeError(f"[!] Befehl fehlgeschlagen: {cmd}")


if __name__ == "__main__":
    main()

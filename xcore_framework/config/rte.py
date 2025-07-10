# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import subprocess


def check_java_runtime():
    """
    Überprüft die Java-Laufzeitumgebung, indem Java-Runtime- und Compiler-Binärdateien
    abgerufen werden und anschließend die Java-Version ausgeführt wird.

    Returns:
        None

    Raises:
        subprocess.CalledProcessError: Wenn der Aufruf von `subprocess.run` fehlschlägt.
    """
    from xcore_framework.core.runtime_manager import JavaRuntimeManager

    manager = JavaRuntimeManager()
    java_bin, javac_bin = manager.get_binary()
    print(f"[✅] Java JDK gefunden unter:\n{java_bin}")
    print("[*] Teste Java-Version Kommando...")
    subprocess.run([java_bin, "-version"])


def check_node_runtime():
    """
    Überprüft die Existenz und Funktionalität des Node.js-Interpreters im System.

    Zusammenfassung:
    Die Funktion ruft das NodeRuntimeManager-Objekt auf, um den Pfad des Node.js-Binaries
    zu ermitteln. Anschließend bestätigt sie, dass der Node.js-Interpreter gefunden wurde
    und führt einen Testbefehl zur Versionsprüfung aus.

    Raises:
        RuntimeError: Wenn der Node.js Binary-Pfad nicht ermittelt werden kann oder das
                      Node.js-Version-Kommando fehlschlägt.
    """
    from xcore_framework.core.runtime_manager import NodeRuntimeManager

    manager = NodeRuntimeManager()
    node_bin = manager.get_binary()
    print(f"[✅] Node.js-Interpreter gefunden unter:\n{node_bin}")
    print("[*] Teste Node.js-Version Kommando...")
    subprocess.run([node_bin, "--version"])


def check_bash_runtime():
    """
    Überprüft die Laufzeitumgebung für Bash, ermittelt den Pfad zum Bash-Binary
    und testet die Bash-Version, um sicherzustellen, dass der Interpreter
    ordnungsgemäß verfügbar und funktionsfähig ist.

    Ermittelt den Bash-Interpreter durch den `BashRuntimeManager`, gibt
    dessen Pfad aus und führt das `--version` Kommando aus, um die verfügbare
    Version zu überprüfen.

    Raises:
        Alle möglichen Fehler oder Ausnahmen können während der Laufzeit im Datenabruf
        oder der Bash-Ausführung auftreten.
    """
    from xcore_framework.core.runtime_manager import BashRuntimeManager

    manager = BashRuntimeManager()
    bash_bin = manager.get_binary()
    print(f"[✅] Bash-Interpreter gefunden unter:\n{bash_bin}")
    print("[*] Teste Bash-Interpreter-Version Kommando...")
    subprocess.run([bash_bin, "--version"])


def check_powershell_runtime():
    """
    Prüft die Verfügbarkeit des PowerShell-Interpreters und dessen Version.

    Diese Funktion verwendet den PowerShellRuntimeManager, um die Binary des
    PowerShell-Interpreters zu ermitteln, gibt den Pfad zur Binary aus und führt
    einen Testbefehl aus, um die Version des Interpreters anzuzeigen.

    Raises:
        Exception: Wenn der PowerShellRuntimeManager keinen Interpreter finden kann
                   oder die Binary nicht verfügbar ist.
    """
    from xcore_framework.core.runtime_manager import PowerShellRuntimeManager

    manager = PowerShellRuntimeManager()
    ps_bin = manager.get_binary()
    print(f"[✅] PowerShell-Interpreter gefunden unter:\n{ps_bin}")
    print("[*] Teste PowerShell-Version Kommando...")
    subprocess.run([ps_bin, "-Command", "$PSVersionTable.PSVersion"])


def check_runtimes():
    """
    Prüft die Verfügbarkeit und Funktionalität verschiedener Laufzeitumgebungen.

    Diese Funktion ruft nacheinander Prüfmethoden für mehrere Laufzeitumgebungen auf,
    um sicherzustellen, dass diese ordnungsgemäß installiert und einsatzbereit sind.

    Raises:
        Exception: Eine Ausnahme wird ausgelöst, falls eine der Prüfungen fehlschlägt.
    """
    check_bash_runtime()
    check_java_runtime()
    check_node_runtime()
    check_powershell_runtime()

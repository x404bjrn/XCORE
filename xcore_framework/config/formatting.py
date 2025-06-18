# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import colorama
import re

# Regex-Pattern für ANSI-Escape-Sequenzen
ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def strip_ansi(text: str) -> str:
    """
    Entfernt ANSI-Escape-Sequenzen aus einem gegebenen Text. Dies kann verwendet
    werden, um Terminal-Farbcodes oder andere Steuersequenzen zu bereinigen,
    die durch ANSI-Escape-Codes definiert wurden. (Für Webapp Ausgaben)

    :param text: Der Eingabetext, der bereinigt werden soll.
    :type text: str
    :return: Der bereinigte Text ohne ANSI-Escape-Sequenzen.
    :rtype: str
    """
    return ANSI_ESCAPE.sub("", text)


# Konsolenfarben
colorama.init()
CCOLOR = {
    "LRD": colorama.Fore.LIGHTRED_EX,
    "RD": colorama.Fore.RED,
    "LGN": colorama.Fore.LIGHTGREEN_EX,
    "GN": colorama.Fore.GREEN,
    "LYW": colorama.Fore.LIGHTYELLOW_EX,
    "YW": colorama.Fore.YELLOW,
    "LBE": colorama.Fore.LIGHTBLUE_EX,
    "BE": colorama.Fore.BLUE,
    "LMA": colorama.Fore.LIGHTMAGENTA_EX,
    "MA": colorama.Fore.MAGENTA,
    "X": colorama.Style.RESET_ALL,
}

# Statusboxen
STATUS_BOX = {
    "SUCCESS": f"{CCOLOR['LYW']}[{CCOLOR['LGN']}+{CCOLOR['LYW']}]{CCOLOR['X']}",
    "NEUTRAL": f"{CCOLOR['LYW']}[{CCOLOR['YW']}*{CCOLOR['LYW']}]{CCOLOR['X']}",
    "FAIL": f"{CCOLOR['LYW']}[{CCOLOR['LRD']}!{CCOLOR['X']}{CCOLOR['LYW']}]{CCOLOR['X']}",
    "CHECK": f"{CCOLOR['LYW']}[{CCOLOR['LGN']}✓{CCOLOR['LYW']}]{CCOLOR['X']}",
    "UNCHECK": f"{CCOLOR['LYW']}[{CCOLOR['LRD']}x{CCOLOR['LYW']}]{CCOLOR['X']}",
}

# Vollständiges Formatierungsobjekt
formatter = {}
formatter.update(CCOLOR)
formatter.update(STATUS_BOX)

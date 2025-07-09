# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
# TODO: Fertigstellen (Erstes Modul)
import subprocess
import platform

from xcore_framework.config.i18n import i18n
from xcore_framework.core.module_base import XCoreModule


class Module(XCoreModule):

    def __init__(self):
        super().__init__()

        # Logger initialisieren
        self.init_logging(name=i18n.t("scanner_nmap.modul_name"))

    # Modulinformationen
    name = i18n.t("scanner_nmap.modul_name")
    description = i18n.t("scanner_nmap.modul_desc")
    author = "x404bjrn"
    version = "0.1.0"
    created = "04.07.2025"
    options = {
        "target": {
            "desc": i18n.t("scanner_nmap.modul_option_target_desc"),
            "required": True,
            "default": "127.0.0.1",
            "widget_type": "entry",
        },
        "ports": {
            "desc": i18n.t("scanner_nmap.modul_option_ports_desc"),
            "required": False,
            "default": "",
            "widget_type": "entry",
        },
        "service_detection": {
            "desc": i18n.t("scanner_nmap.modul_option_service_detection_desc"),
            "required": False,
            "default": False,
            "widget_type": "checkbox",
        },
        "os_detection": {
            "desc": i18n.t("scanner_nmap.modul_option_os_detection_desc"),
            "required": False,
            "default": False,
            "widget_type": "checkbox",
        },
        "ping_skip": {
            "desc": i18n.t("scanner_nmap.modul_option_ping_skip_desc"),
            "required": False,
            "default": False,
            "widget_type": "checkbox",
        },
    }

    @staticmethod
    def _detect_nmap() -> str:
        """Findet das nmap-Binary plattformübergreifend."""
        system = platform.system().lower()
        candidates = ["nmap.exe", "nmap"] if system.startswith("win") else ["nmap"]

        for nmap_bin in candidates:
            try:
                res = subprocess.run(
                    [nmap_bin, "--version"], capture_output=True, text=True, timeout=5
                )
                if res.returncode == 0 and "Nmap version" in res.stdout:
                    return nmap_bin
            except Exception:
                continue
        return ""

    def run(self, params: dict, mode="cli", gui_console=None) -> dict | None:
        self.log("Modul gestartet")

        # Ausführungsmodus
        self.mode = mode

        # Textausgabeobjekt des GUI
        self.console_widget = gui_console

        # Modul-Überschrift / Headline
        self.feedback([i18n.t("scanner_nmap.modul_headline")])

        # Modulhauptroutine
        target = params.get("target")
        ports = params.get("ports")
        flags = []

        if params.get("service_detection"):
            flags.append("-sV")

        if params.get("os_detection"):
            flags.append("-O")

        if params.get("ping_skip"):
            flags.append("-Pn")

        if ports:
            flags += ["-p", ports]

        # OS und nmap-Binary ermitteln
        nmap_bin = self._detect_nmap()
        if not nmap_bin:
            self.feedback([i18n.t("scanner_nmap.modul_nmap_binary_not_found")])
            print()
            return {"success": True, "output": self.output, "data": self.results}

        command = [nmap_bin] + flags + [target]
        self.feedback([i18n.t("scanner_nmap.modul_nmap_cmd", cmd=" ".join(command))])

        try:
            result = subprocess.run(command, capture_output=True, text=True)

            # Ergebnisrückgabe
            self.feedback([result.stdout])

            if result.stderr:
                msg = i18n.t("scanner_nmap.modul_error", error=result.stderr)
                self.feedback([msg])

                # Fehler Logging
                self.log(msg, level="error")

                return {"success": False, "error": msg, "output": [msg]}

        except Exception as e:
            msg = i18n.t("scanner_nmap.modul_error", error=e)
            self.feedback([msg])

            # Fehler Logging
            self.log(msg, level="error")

            return {"success": False, "error": msg, "output": [msg]}

        print()
        return {"success": True, "output": self.output, "data": self.results}

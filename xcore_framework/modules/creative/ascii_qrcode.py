# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
# Diese Datei / Dieses Modul wurde mithilfe des XCORE 'Modul-Creator' erstellt
# This file / module was created using the XCORE 'Module Creator'
# ─────────────────────────────────────────────────────────────────────────────
import qrcode

from io import StringIO

from xcore_framework.config.i18n import i18n
from xcore_framework.core.module_base import XCoreModule


class Module(XCoreModule):
    def __init__(self):
        super().__init__()
        self.init_logging(name=i18n.t("creative_ascii_qrcode.modul_name"))

    name = i18n.t("creative_ascii_qrcode.modul_name")
    description = i18n.t("creative_ascii_qrcode.modul_desc")
    author = "x404bjrn"
    version = "1.0.0"
    created = "08.07.2025"
    options = {
        "text": {
            "widget_type": "entry",
            "required": True,
            "default": "https://github.com/x404bjrn/XCORE",
            "desc": i18n.t("creative_ascii_qrcode.modul_option_text_desc"),
        },
    }

    def run(self, params: dict, mode="cli", gui_console=None) -> dict | None:
        self.log("Modul gestartet")
        self.mode = mode
        self.console_widget = gui_console
        self.feedback([i18n.t("creative_ascii_qrcode.modul_headline")])

        try:
            text = params.get("text", self.options["text"].get("default"))
            self.feedback([i18n.t("creative_ascii_qrcode.custom_484210")])
            qr = qrcode.QRCode(border=1)
            qr.add_data(text)
            qr.make(fit=True)
            buffer = StringIO()
            qr.print_ascii(out=buffer)
            self.feedback(output=["\n" + buffer.getvalue()])

            self.feedback([i18n.t("creative_ascii_qrcode.modul_done_message")])
            self.log(i18n.t("creative_ascii_qrcode.modul_done_message"))
            print()

            return {"success": True, "output": self.output, "data": self.results}

        except Exception as e:
            # Fehlerbehandlung in Hauptroutine
            msg = i18n.t("creative_ascii_qrcode.modul_error", error=e)
            self.feedback([msg])
            self.log(msg, level="error")
            print()

            return {"success": False, "error": msg, "output": [msg]}

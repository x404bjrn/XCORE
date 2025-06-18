# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
from xcore_framework.config.i18n import i18n
from xcore_framework.core.module_base import XCoreModule

from collections import Counter
import os


class Module(XCoreModule):
    def __init__(self):
        super().__init__()

    name = i18n.t("system_bash_history_stats.modul_name")
    description = i18n.t("system_bash_history_stats.modul_desc")
    author = "Björn Häusermann | x404bjrn"
    version = "2.0.1"
    created = "28.05.2025"
    options = {
        "history_path": {
            "widget_type": "fileexplorer",
            "required": False,
            "default": "~/.bash_history",
            "desc": i18n.t("system_bash_history_stats.option_history_path_desc"),
        }
    }

    def run(self, params: dict, mode="cli", gui_console=None) -> dict | None:
        self.mode = mode
        self.console_widget = gui_console

        # Headline
        self.feedback([i18n.t("system_bash_history_stats.modul_headline")])

        path = os.path.expanduser(
            params.get("history_path", self.options["history_path"].get("default"))
        )

        if not os.path.exists(path):
            msg = i18n.t("system_bash_history_stats.file_not_found", path=path)
            self.feedback(["\n" + msg + "\n"])
            return {"success": False, "error": msg, "output": [msg]}

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = [line.strip().split()[0] for line in f if line.strip()]

        counts = Counter(lines)
        self.feedback(["\n" + i18n.t("system_bash_history_stats.most_cmd")])

        for cmd, count in counts.most_common(10):
            line = f"{cmd:<15} {count}x"
            self.feedback(output=[line], result={"command": cmd, "count": count})

        print()
        return {"success": True, "output": self.output, "data": self.results}

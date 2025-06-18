# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import sys
from xcore_framework.web.app import create_app

app = create_app()

if __name__ == "__main__":
    debug_mode = "--debug" in sys.argv
    port = 5000
    host = "0.0.0.0"

    if "--port" in sys.argv:
        port = sys.argv[sys.argv.index("--port") + 1]
    if "--host" in sys.argv:
        host = sys.argv[sys.argv.index("--host") + 1]

    print()
    print(
        "XCORE Web Interface:\n"
        "---------------------------------------------\n"
        f"HOST : {host}\n"
        f"PORT : {port}\n"
        f"DEBUG: {str(debug_mode)}\n"
        "---------------------------------------------"
    )
    print()
    app.run(host=host, port=port, debug=debug_mode, use_reloader=False)

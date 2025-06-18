# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
# TODO: Web-Setpoint weiter ausarbeiten (Hiermit nur Basis geschaffen)
from flask import Flask, render_template_string, request, redirect, url_for
from dotenv import dotenv_values, set_key

from xcore_framework.config.env import DIRECTORY_ENV


def start_web_setpoint():
    """
    Startet eine Flask-Web-Anwendung zur Konfiguration und Bearbeitung von Umgebungsvariablen
    basierend auf einer .env-Datei des XCORE-Frameworks. Nutzer können Konfigurationsschlüssel
    auswählen, deren Werte ändern und speichern. Die Änderungen werden direkt in die
    .env-Datei übernommen.

    Funktionen:
        - Lädt die Umgebungskonfiguration basierend auf `XCORE_ENV`.
        - Bietet eine Web-Oberfläche zur Anzeige und Bearbeitung der Konfigurationsschlüssel und
          -werte.
        - Unterstützt das Speichern der Änderungen und aktualisiert die Werte in der
          .env-Datei.

    Section(s):
        - `XCORE_ENV` muss korrekt definiert und auf die entsprechende .env-Datei zeigen.
        - Die Webanwendung wird lokal auf Port 5001 ausgeführt, für Debugging aktiviert.

    Returns:
        None
    """
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def config():
        config = dotenv_values(DIRECTORY_ENV)
        message = ""

        if request.method == "POST":
            key = request.form.get("key")
            value = request.form.get("value", "").strip()

            if key and value:
                set_key(DIRECTORY_ENV, key, value)
                message = f"✅ {key} wurde aktualisiert."
                return redirect(url_for("config", message=message))

        # Wieder laden nach Speicherung
        config = dotenv_values(DIRECTORY_ENV)
        return render_template_string(
            """
            <!DOCTYPE html>
            <html lang="de">
            <head>
                <meta charset="UTF-8">
                <title>XCORE Web Konfiguration (Setpoint)</title>
                <style>
                    body {
                        font-family: sans-serif;
                        padding: 2em;
                        background: #111;
                        color: #eee;
                        }
                    select,
                    input[type=text],
                    button {
                        margin: 0.5em 0;
                        padding: 0.5em;
                        width: 300px;
                        }
                    label {
                        display: block;
                        margin-top: 1em;
                        font-weight: bold;
                        }
                    .success {
                        color: #0f0;
                        }
                </style>
            </head>
            <body>
                <h2>XCORE Web-Konfiguration (.env)</h2>

                <form method="post">
                    <label for="key">Eintrag auswählen:</label>
                    <select name="key" id="key" onchange="this.form.submit()">
                        <option value="">-- Auswahl --</option>
                        {% for k in config.keys() %}
                            <option value="{{ k }}" {% if k == request.form.get('key') %}
                                    selected{% endif %}>{{ k }}
                            </option>
                        {% endfor %}
                    </select>

                    {% if request.form.get('key') %}
                        <label for="value">Wert für '{{ request.form.get('key') }}':</label>
                        <input type="text" name="value" id="value"
                            value="{{ config[request.form.get('key')] }}"
                        >
                        <br>
                        <button type="submit">Speichern</button>
                    {% endif %}
                </form>

                {% if message %}
                    <p class="success">{{ message }}</p>
                {% endif %}
            </body>
            </html>
        """,
            config=config,
            message=request.args.get("message", ""),
            request=request,
        )

    app.run(debug=True, port=5001)

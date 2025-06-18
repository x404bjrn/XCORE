# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
# TODO: 'activecolors' und weitere Widget-Formatierungen einarbeiten
import tkinter as tk
from tkinter import filedialog, ttk

BACKGROUND_COLOR = "#1C033E"
INNER_COLOR = "#E7D684"


def create_widget_by_meta(parent, name, meta):
    """
    Diese Hilfsfunktion dient zur dynamischen Erstellung von Widgets anhand
    von Optionen, die in Modulen übergeben werden (options = {...}). Die Funktion
    basiert auf dem Schlüssel "widget_type" und erstellt automatisch passende
    Eingabefelder für die GUI.

    Unterstützte Typen:
        - entry         : Einfaches Textfeld (StringVar)
        - checkbox      : Checkbox (BooleanVar)
        - radiobutton   : Radiobutton-Auswahl (StringVar, mit "values"-Liste)
        - listbox       : Listbox-Auswahl (StringVar, mit "values"-Liste)
        - spinbox       : Zahlenwahl (StringVar, mit "min" / "max")
        - scale         : Slider (IntVar, mit "min" / "max")
        - fileexplorer  : Eingabe mit Datei-Auswahl-Dialog (StringVar)

    Jeder erzeugte Widget-Container enthält zusätzlich ein `.var`-Attribut zur
    späteren Werteauswertung in der GUI.

    Verwendung:
        widget = create_widget_by_meta(parent_frame, "host", option_dict)
        wert = widget.var.get()
    """
    widget_type = meta.get("widget_type", "entry")
    default = meta.get("default", "")
    widget = None

    if widget_type == "entry":
        var = tk.StringVar(value=str(default))
        widget = tk.Entry(parent, textvariable=var, bg=INNER_COLOR)
        widget.var = var
        widget.pack(fill="x")

    elif widget_type == "checkbox":
        var = tk.BooleanVar(value=str(default).lower() == "true")
        widget = tk.Checkbutton(parent, variable=var, bg=BACKGROUND_COLOR, fg="black")
        widget.var = var
        widget.pack(anchor="w", pady=5)

    elif widget_type == "radiobutton":
        var = tk.StringVar(value=str(default))
        frame = tk.Frame(parent, bg=BACKGROUND_COLOR)
        for val in meta.get("values", []):
            rb = tk.Radiobutton(
                frame,
                text=val,
                variable=var,
                value=val,
                bg=BACKGROUND_COLOR,
                selectcolor="black",
                fg="white",
                anchor="w",
            )
            rb.pack(anchor="w")
        frame.pack(anchor="w", pady=5)
        frame.var = var
        widget = frame

    elif widget_type == "listbox":
        var = tk.StringVar(value=str(default))
        values = meta.get("values", [])

        combo = ttk.Combobox(parent, textvariable=var, values=values, state="readonly")
        combo.set(default if default in values else (values[0] if values else ""))
        combo.pack(fill="x")

        combo.var = var
        widget = combo

    elif widget_type == "spinbox":
        var = tk.StringVar(value=str(default))
        widget = tk.Spinbox(
            parent,
            from_=meta.get("min", 0),
            to=meta.get("max", 100),
            textvariable=var,
            bg=INNER_COLOR,
        )
        widget.var = var
        widget.pack(fill="x")

    elif widget_type == "scale":
        var = tk.IntVar(value=int(default))
        widget = tk.Scale(
            parent,
            from_=meta.get("min", 0),
            to=meta.get("max", 100),
            orient="horizontal",
            variable=var,
            bg=BACKGROUND_COLOR,
            fg="white",
        )
        widget.var = var
        widget.pack(fill="x")

    elif widget_type == "fileexplorer":
        var = tk.StringVar(value=str(default))
        container = tk.Frame(parent, bg=BACKGROUND_COLOR)
        entry = tk.Entry(container, textvariable=var, bg=INNER_COLOR)
        entry.pack(fill="x", side="left", expand=True)

        def browse_file():
            file_path = filedialog.askopenfilename()
            if file_path:
                var.set(file_path)

        btn = tk.Button(container, text="...", command=browse_file)
        btn.pack(side="right")

        container.pack(fill="x")
        container.var = var
        widget = container

    else:
        var = tk.StringVar(value=str(default))
        widget = tk.Entry(parent, textvariable=var)
        widget.var = var
        widget.pack(fill="x")

    return widget

# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
# TODO: GUI-Setpoint weiter ausarbeiten (Hiermit nur Basis geschaffen)
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from dotenv import dotenv_values

from xcore_framework.config.env import DIRECTORY_ENV
from xcore_framework.setpoint.setpoint_logic import save_config


def start_gui_setpoint():
    """
    Startet eine grafische Benutzeroberfläche (GUI) zur Verwaltung von
    Konfigurationswerten in einer .env-Datei.
    """
    config = dotenv_values(DIRECTORY_ENV)

    def on_entry_select(event=None):
        key = entry_selector.get()
        current_value = config.get(key, "")
        path_entry.delete(0, tk.END)
        path_entry.insert(0, current_value)

    def durchsuchen():
        pfad = filedialog.askdirectory()
        if pfad:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, pfad)

    def speichern():
        key = entry_selector.get()
        pfad = path_entry.get().strip()
        if key and pfad:
            save_config({key: pfad})
            status_label.config(
                text=f"✅ '{key}' wurde aktualisiert.", foreground="green"
            )
        else:
            messagebox.showerror("Fehler", "Bitte Eintrag wählen und Pfad angeben.")

    # Root-Fenster
    root = tk.Tk()
    root.title("🛠XCORE Setpoint-Konfiguration")
    root.geometry("500x280")
    root.resizable(False, False)

    # Stil-Setup
    style = ttk.Style()
    style.theme_use("clam")

    container = ttk.Frame(root, padding=20)
    container.pack(expand=True, fill="both")

    # .env-Key Auswahl
    ttk.Label(container, text="🔑 Eintrag auswählen:").grid(
        row=0, column=0, sticky="w", pady=(0, 5)
    )
    entry_selector = ttk.Combobox(
        container, values=list(config.keys()), state="readonly", width=50
    )
    entry_selector.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    entry_selector.bind("<<ComboboxSelected>>", on_entry_select)

    # Pfad-Eingabe
    ttk.Label(container, text="📁 Pfad bearbeiten:").grid(row=2, column=0, sticky="w")
    path_entry = ttk.Entry(container, width=40)
    path_entry.grid(row=3, column=0, sticky="ew", pady=(0, 5))
    ttk.Button(container, text="Durchsuchen", command=durchsuchen).grid(
        row=3, column=1, padx=(5, 0)
    )

    # Buttons
    ttk.Button(container, text="💾 Speichern", command=speichern).grid(
        row=4, column=0, columnspan=2, pady=(15, 10)
    )

    # Statusanzeige
    status_label = ttk.Label(container, text="", foreground="green")
    status_label.grid(row=5, column=0, columnspan=2)

    root.mainloop()

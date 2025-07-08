# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk
import os
import datetime
import json

from tkinter import ttk, messagebox
from translate import Translator as AltTranslator

from xcore_framework.config.env import DIRECTORY_I18N, DIRECTORY_MODULES, SETTING_LANGUAGE
from xcore_framework import __version__


options = []
translations = []
SAVE_LOCATIONS = {
    "ai": os.path.join(DIRECTORY_MODULES, "ai"),
    "creative": os.path.join(DIRECTORY_MODULES, "creative"),
    "exploitation": os.path.join(DIRECTORY_MODULES, "exploitation"),
    "helper": os.path.join(DIRECTORY_MODULES, "helper"),
    "monitor": os.path.join(DIRECTORY_MODULES, "monitor"),
    "osint": os.path.join(DIRECTORY_MODULES, "osint"),
    "persistence": os.path.join(DIRECTORY_MODULES, "persistence"),
    "scanner": os.path.join(DIRECTORY_MODULES, "scanner"),
    "system": os.path.join(DIRECTORY_MODULES, "system"),
    "template": os.path.join(DIRECTORY_MODULES, "template"),
    "transfer": os.path.join(DIRECTORY_MODULES, "transfer"),
    "utilities": os.path.join(DIRECTORY_MODULES, "utilities")
}


def add_option():
    """
    Fügt eine neue Option zu einer Liste von Optionen hinzu,
    basierend auf den Benutzereingaben in einer GUI. Die Funktion überprüft die
    Eingabewerte, validiert sie und erstellt ein entsprechendes Optionsobjekt,
    das zur globalen Liste hinzugefügt wird. Zusätzlich wird eine visuelle
    Darstellung der hinzugefügten Option aktualisiert.

    Args:
        Keine Argumente benötigt (verwendet globale Variablen,
        die durch Benutzereingaben in der GUI gesetzt werden).

    Raises:
        ValueError: Wird ausgelöst, wenn die Min- oder Max-Werte für
        "scale" oder "spinbox" ungültig (nicht konvertierbar in Integer)
        sind.

        messagebox.showerror: Zeigt einen Fehlerdialog an,
        wenn wesentliche Validierungsbedingungen der Eingaben nicht erfüllt werden
        (z. B. leerer Parametername).
    """
    name = entry_name.get().strip()
    required = var_required.get()
    default = entry_default.get().strip()
    desc = entry_desc.get().strip()
    widget_type = widget_type_var.get()
    values = entry_values.get().strip()

    if not name:
        messagebox.showerror("Fehler", "Parametername darf nicht leer sein.")
        return

    option = {
        "name": name,
        "required": required,
        "default": default,
        "desc": desc,
        "widget_type": widget_type
    }

    if widget_type in ["radiobutton", "listbox"]:
        option["values"] = [v.strip() for v in values.split(",") if v.strip()]

    elif widget_type in ["scale", "spinbox"]:
        try:
            option["min"] = int(entry_min.get())
            option["max"] = int(entry_max.get())
        except ValueError:
            messagebox.showerror("Fehler", "Min/Max muss bei scale/spinbox gesetzt werden.")
            return

    options.append(option)
    listbox.insert(tk.END, f"{name} ({widget_type}) - {desc}")
    clear_option_entries()


def clear_option_entries():
    """
    Löscht den Inhalt sämtlicher Eingabefelder und setzt den Wert einer Kontrollbox zurück.

    Diese Funktion löscht die Inhalte in mehreren Eingabefeldern und setzt den Wert einer
    Checkbox zurück. Sie wird verwendet, um die Eingabemasken für eine neue oder
    leere Eingabe zu initialisieren.
    """
    entry_name.delete(0, tk.END)
    entry_default.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    entry_values.delete(0, tk.END)
    entry_min.delete(0, tk.END)
    entry_max.delete(0, tk.END)
    var_required.set(False)


def remove_selected_option():
    """
    Entfernt die aktuell ausgewählte Option aus einer Liste und aktualisiert die
    Optionen Auswahl im Listenfeld entsprechend.
    """
    index = listbox.curselection()
    if index:
        idx = index[0]
        del options[idx]
        listbox.delete(idx)


def add_translation():
    """
    Fügt eine neue Übersetzung zur Liste der Übersetzungen hinzu.

    Hauptziel dieser Funktion ist es, eine vom Benutzer eingegebene Übersetzung
    zur Sammlung hinzuzufügen und dabei die GUI entsprechend zu aktualisieren.
    """
    satz = entry_translation.get().strip()
    if satz:
        translations.append(satz)
        listbox_translations.insert(tk.END, satz)
        entry_translation.delete(0, tk.END)


def export_translation_json(base_path, module_name, module_desc, options, sentences, json_base_path=DIRECTORY_I18N):
    """
    Generiert und exportiert JSON-Dateien mit Übersetzungen aus gegebenen Eingabedaten.
    Diese Funktion generiert Übersetzungsdateien im JSON-Format für ein spezifisches Modul.
    Die Übersetzungen werden sowohl vom Deutschen ins Englische als auch umgekehrt durchgeführt,
    abhängig von der Spracheinstellung (SETTING_LANGUAGE). Es werden zwei .json-Dateien erstellt:
    eine für die Ausgangssprache und eine für die Zielsprache. Die zu übersetzenden Inhalte
    umfassen Modulinformationen, Optionen und benutzerdefinierte Sätze.

    Die Dateien werden in spezifische Unterverzeichnisse des definierten json_base_path
    gespeichert ('de', 'en') und deren Struktur wird automatisch erzeugt,
    falls sie nicht existiert.

    Args:
        base_path (str): Der Basispfad des Moduls, dessen Inhalte übersetzt werden sollen.
        module_name (str): Der Name des zu exportierenden Moduls.
        module_desc (str): Die Beschreibung des Moduls.
        options (list[dict]): Eine Liste von Optionen mit Beschreibung.
                              Jede Option wird durch ein Dictionary repräsentiert,
                              das mindestens die Schlüssel 'name' und 'desc' enthält.
        sentences (list[str]): Eine Liste von Sätzen, die übersetzt werden sollen.
        json_base_path (str, optional): Der Basispfad für die Ausgabe der JSON-Dateien.
                                        Der Standardwert ist 'DIRECTORY_I18N'.
    """
    full_module_name = os.path.split(base_path)[-1] + "/" + module_name
    translations_from = {
        "modul_name": "{LGN}" + full_module_name + "{X}",
        "modul_desc": module_desc,
        "modul_headline": "\n{LBE}" + module_name.upper().replace("_", " ") + "{X}\n",
        "modul_done_message": ("{SUCCESS} " + f"'{full_module_name}' ") + ("completed..." if SETTING_LANGUAGE == "en" else "abgeschlossen..."),
        "modul_error": "{FAIL} {error}"
    }

    for opt in options:
        translations_from[f"modul_option_{opt['name']}_desc"] = opt["desc"]

    for satz in sentences:
        key = "custom_" + str(abs(hash(satz)))[:6]
        translations_from[key] = satz

    # Alternativer Übersetzer
    from_language = "de"
    to_language = "en"

    if SETTING_LANGUAGE == "en":
        from_language = "en"
        to_language = "de"

    # DEBUG Print
    #print(f"Übersetzung von {from_language} nach {to_language}")
    translator = AltTranslator(from_lang=from_language, to_lang=to_language)

    translations_to = {}
    for key, value in translations_from.items():
        try:
            translations_to[key] = translator.translate(value)
        except Exception:
            translations_to[key] = value + " (translation error)"

    os.makedirs(os.path.join(json_base_path, "de"), exist_ok=True)
    os.makedirs(os.path.join(json_base_path, "en"), exist_ok=True)

    with open(os.path.join(json_base_path, from_language, f"{full_module_name.replace('/', '_')}.json"), "w", encoding="utf-8") as f:
        json.dump(translations_from, f, indent=2, ensure_ascii=False)

    with open(os.path.join(json_base_path, to_language, f"{full_module_name.replace('/', '_')}.json"), "w", encoding="utf-8") as f:
        json.dump(translations_to, f, indent=2, ensure_ascii=False)


def generate_module():
    """
    Generiert ein Modulskript basierend auf Benutzerangaben und speichert es an einem
    definierten Speicherort. Die generierte Datei beinhaltet Konfigurationen, Metadaten
    und eine Standardstruktur für die Implementierung der Modul-Funktionalitäten.

    Parameters:
        Keine direkt übergebenen Parameter, nutzt globale Variablen und Eingabefelder
        (z. B. `entry_module_name`, `entry_module_desc`, `entry_module_author`,
        `entry_save_path`), um Benutzereingaben zu verarbeiten.

    Raises:
        Zeigt Fehlermeldungen in Messagebox-Dialogen, falls Eingabevalidierung
        fehlschlägt (z. B. wenn Pflichtfelder leer bleiben).

    Effects:
        Speichert die generierte Datei am angegebenen Speicherort (falls gültig).
        Initialisiert eine weitere Übersetzungsdatei für das Modul.
        Informiert den Benutzer über den Erfolg oder Misserfolg des Prozesses.
    """
    name = entry_module_name.get().strip()
    desc = entry_module_desc.get().strip()
    author = entry_module_author.get().strip()
    version = entry_module_version.get().strip()

    selected_key = save_path_var.get()
    base_path = SAVE_LOCATIONS.get(selected_key)

    if not base_path:
        messagebox.showerror("Fehler", "Ungültiger Speicherort ausgewählt.")
        return

    path = os.path.join(base_path, f"{name.replace('/', '_')}.py")

    if not name or not desc or not author or not path:
        messagebox.showerror("Fehler", "Alle Pflichtfelder müssen ausgefüllt sein.")
        return

    mod_id = os.path.split(base_path)[-1] + "_" + name.replace("/", "_")
    now = datetime.datetime.now().strftime("%d.%m.%Y")
    indent = " " * 4

    code = f"""# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
# Diese Datei / Dieses Modul wurde mithilfe des XCORE 'Modul-Creator' erstellt
# This file / module was created using the XCORE 'Module Creator'
# ─────────────────────────────────────────────────────────────────────────────
from xcore_framework.config.i18n import i18n
from xcore_framework.core.module_base import XCoreModule

class Module(XCoreModule):
{indent}def __init__(self):
{indent*2}super().__init__()
{indent*2}self.init_logging(name=i18n.t("{mod_id}.modul_name"))

{indent}name = i18n.t("{mod_id}.modul_name")
{indent}description = i18n.t("{mod_id}.modul_desc")
{indent}author = "{author}"
{indent}version = "{version or "1.0.0"}"
{indent}created = "{now}"
{indent}options = {{
"""

    for opt in options:
        code += f'{indent*2}"{opt["name"]}": {{\n'
        code += f'{indent*3}"widget_type": "{opt["widget_type"]}",\n'
        code += f'{indent*3}"required": {opt["required"]},\n'
        code += f'{indent*3}"default": "{opt["default"]}",\n'
        if "values" in opt:
            code += f'{indent*3}"values": {opt["values"]},\n'
        if "min" in opt:
            code += f'{indent*3}"min": {opt["min"]},\n'
        if "max" in opt:
            code += f'{indent*3}"max": {opt["max"]},\n'
        code += f'{indent*3}"desc": i18n.t("{mod_id}.modul_option_{opt["name"]}_desc")\n'
        code += f"{indent*2}}},\n"

    code += f"{indent}}}\n\n"

    code += f"""{indent}def run(self, params: dict, mode="cli", gui_console=None) -> dict | None:
{indent*2}self.log("Modul gestartet")    
{indent*2}self.mode = mode
{indent*2}self.console_widget = gui_console
{indent*2}self.feedback([i18n.t("{mod_id}.modul_headline")])

{indent*2}try:
{indent*3}# Hier [HAUPTROUTINE] eintragen...
{indent*3}# ...

"""
    for satz in translations:
        code += f"{indent * 3}# i18n.t('{mod_id}.custom_{str(abs(hash(satz)))[:6]}')" + f" | {satz}" + "\n"

    code += f"""
{indent*3}self.feedback([i18n.t("{mod_id}.modul_done_message")])
{indent*3}self.log(i18n.t("{mod_id}.modul_done_message"))
{indent*3}print()

{indent*3}return {{"success": True, "output": self.output, "data": self.results}}

{indent*2}except Exception as e:
{indent*3}# Fehlerbehandlung in Hauptroutine
{indent*3}msg = i18n.t("{mod_id}.modul_error", error=e)
{indent*3}self.feedback([msg])
{indent*3}self.log(msg, level="error")
{indent*3}print()

{indent*3}return {{"success": False, "error": msg, "output": [msg]}}
"""

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

    # Übersetzen
    export_translation_json(base_path, name, desc, options, translations)

    # Fertig generiert
    messagebox.showinfo("Erfolg", f"Modul gespeichert unter:\n{path}")


# GUI Dialog Darstellung ================================
root = tk.Tk()
root.title(f"XCORE - Modulgenerator - {__version__}")
root.geometry("880x700")

ttk.Label(root, text="Modulname").pack()
entry_module_name = ttk.Entry(root, width=80)
entry_module_name.pack()

ttk.Label(root, text="Beschreibung").pack()
entry_module_desc = ttk.Entry(root, width=80)
entry_module_desc.pack()

ttk.Label(root, text="Autor").pack()
entry_module_author = ttk.Entry(root, width=80)
entry_module_author.insert(0, "x404bjrn")
entry_module_author.pack()

ttk.Label(root, text="Version").pack()
entry_module_version = ttk.Entry(root, width=80)
entry_module_version.insert(0, "1.0.0")
entry_module_version.pack()

ttk.Label(root, text="Speicherort").pack()
save_path_var = tk.StringVar(value=list(SAVE_LOCATIONS.keys())[0])
ttk.Combobox(root, textvariable=save_path_var, values=list(SAVE_LOCATIONS.keys()), width=60, state="readonly").pack()

ttk.Separator(root).pack(pady=6, fill="x")
ttk.Label(root, text="Option hinzufügen").pack()

frame_opt = ttk.Frame(root)
frame_opt.pack(pady=4)

entry_name = ttk.Entry(frame_opt, width=12)
entry_name.pack(side="left", padx=2)
entry_name.insert(0, "name")

entry_default = ttk.Entry(frame_opt, width=12)
entry_default.pack(side="left", padx=2)
entry_default.insert(0, "default")

entry_desc = ttk.Entry(frame_opt, width=30)
entry_desc.pack(side="left", padx=2)
entry_desc.insert(0, "description")

widget_type_var = tk.StringVar(value="entry")
ttk.Combobox(frame_opt, textvariable=widget_type_var, values=[
    "entry", "checkbox", "radiobutton", "listbox", "scale", "spinbox", "fileexplorer"],
             width=12).pack(side="left", padx=2)

entry_values = ttk.Entry(frame_opt, width=12)
entry_values.pack(side="left", padx=2)
entry_values.insert(0, "Wert1,Wert2")

entry_min = ttk.Entry(frame_opt, width=4)
entry_min.pack(side="left")
entry_min.insert(0, "min")
entry_max = ttk.Entry(frame_opt, width=4)
entry_max.pack(side="left")
entry_max.insert(0, "max")

var_required = tk.BooleanVar()
ttk.Checkbutton(frame_opt, text="Pflicht", variable=var_required).pack(side="left", padx=2)

ttk.Button(root, text="Option hinzufügen", command=add_option).pack()
ttk.Button(root, text="Ausgewählte Option entfernen", command=remove_selected_option).pack(pady=4)

listbox = tk.Listbox(root, width=100, height=8)
listbox.pack(pady=6)

ttk.Separator(root).pack(pady=6, fill="x")
ttk.Label(root, text="Übersetzungssätze (werden automatisch i18n.t() zugeordnet)").pack()

entry_translation = ttk.Entry(root, width=60)
entry_translation.pack(pady=2)
ttk.Button(root, text="Satz hinzufügen", command=add_translation).pack()

listbox_translations = tk.Listbox(root, width=100, height=4)
listbox_translations.pack(pady=6)

ttk.Button(root, text="Modul generieren", command=generate_module).pack(pady=10)

root.mainloop()

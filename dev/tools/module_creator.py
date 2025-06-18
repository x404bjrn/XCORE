# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
# TODO: Tests und Fertigstellen
# INFO: Befindet sich noch in der Testphase!..
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import datetime
import json
from googletrans import Translator

from xcore_framework.config.env import DIRECTORY_I18N

options = []
translations = []

def add_option():
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
    entry_name.delete(0, tk.END)
    entry_default.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    entry_values.delete(0, tk.END)
    entry_min.delete(0, tk.END)
    entry_max.delete(0, tk.END)
    var_required.set(False)

def remove_selected_option():
    index = listbox.curselection()
    if index:
        idx = index[0]
        del options[idx]
        listbox.delete(idx)

def add_translation():
    satz = entry_translation.get().strip()
    if satz:
        translations.append(satz)
        listbox_translations.insert(tk.END, satz)
        entry_translation.delete(0, tk.END)

def export_translation_json(module_name, module_desc, options, sentences, json_base_path=DIRECTORY_I18N):
    translator = Translator()

    translations_de = {
        "modul_name": "{LGN}" + module_name + "{X}",
        "modul_desc": module_desc,
        "modul_headline": f"[{module_name}] gestartet",
        "modul_done_message": f"[{module_name}] erfolgreich abgeschlossen",
        "modul_error": "Fehler aufgetreten: {error}"
    }

    for opt in options:
        translations_de[f"option_{opt['name']}_desc"] = opt["desc"]

    for satz in sentences:
        key = "custom_" + str(abs(hash(satz)))[:6]
        translations_de[key] = satz

    translations_en = {}
    for key, value in translations_de.items():
        try:
            translations_en[key] = translator.translate(value, src='de', dest='en').text
        except Exception:
            translations_en[key] = value + " (translation error)"

    os.makedirs(os.path.join(json_base_path, "de"), exist_ok=True)
    os.makedirs(os.path.join(json_base_path, "en"), exist_ok=True)

    with open(os.path.join(json_base_path, "de", f"{module_name.replace('/', '_')}.json"), "w", encoding="utf-8") as f:
        json.dump(translations_de, f, indent=2, ensure_ascii=False)

    with open(os.path.join(json_base_path, "en", f"{module_name.replace('/', '_')}.json"), "w", encoding="utf-8") as f:
        json.dump(translations_en, f, indent=2, ensure_ascii=False)

def generate_module():
    name = entry_module_name.get().strip()
    desc = entry_module_desc.get().strip()
    author = entry_module_author.get().strip()
    version = entry_module_version.get().strip()
    path = entry_save_path.get().strip()

    if not name or not desc or not author or not path:
        messagebox.showerror("Fehler", "Alle Pflichtfelder müssen ausgefüllt sein.")
        return

    mod_id = name.replace("/", "_")
    now = datetime.datetime.now().strftime("%d.%m.%Y")
    indent = " " * 4

    code = f"""# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
from xcore_framework.config.i18n import i18n
from xcore_framework.core.module_base import XCoreModule

class Module(XCoreModule):
{indent}def __init__(self):
{indent*2}super().__init__()

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
        code += f'{indent*3}"desc": i18n.t("{mod_id}.option_{opt["name"]}_desc")\n'
        code += f"{indent*2}}},\n"

    code += f"{indent}}}\n\n"

    code += f"""{indent}def run(self, params: dict, mode="cli", gui_console=None) -> dict | None:
{indent*2}self.mode = mode
{indent*2}self.console_widget = gui_console
{indent*2}self.feedback([i18n.t("{mod_id}.modul_headline")])

{indent*2}try:
{indent*3}for key in self.options:
{indent*4}val = params.get(key, self.options[key].get("default"))
{indent*4}self.feedback([f"{{key}}: {{val}}"])

{indent*3}self.feedback([i18n.t("{mod_id}.modul_done_message")])
{indent*3}return {{"success": True, "output": self.output, "data": self.results}}

{indent*2}except Exception as e:
{indent*3}msg = i18n.t("{mod_id}.modul_error", error=e)
{indent*3}self.feedback([msg])
{indent*3}return {{"success": False, "error": msg, "output": [msg]}}
"""

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

    export_translation_json(name, desc, options, translations)
    messagebox.showinfo("Erfolg", f"Modul gespeichert unter:\n{path}")

def browse_path():
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
    if file_path:
        entry_save_path.delete(0, tk.END)
        entry_save_path.insert(0, file_path)

root = tk.Tk()
root.title("XCORE Modulgenerator")
root.geometry("880x700")

ttk.Label(root, text="Modulname").pack()
entry_module_name = ttk.Entry(root, width=80)
entry_module_name.pack()

ttk.Label(root, text="Beschreibung").pack()
entry_module_desc = ttk.Entry(root, width=80)
entry_module_desc.pack()

ttk.Label(root, text="Autor").pack()
entry_module_author = ttk.Entry(root, width=80)
entry_module_author.insert(0, "Björn Häusermann | x404bjrn")
entry_module_author.pack()

ttk.Label(root, text="Version").pack()
entry_module_version = ttk.Entry(root, width=80)
entry_module_version.insert(0, "1.0.0")
entry_module_version.pack()

ttk.Label(root, text="Speicherpfad").pack()
entry_save_path = ttk.Entry(root, width=80)
entry_save_path.pack()
ttk.Button(root, text="Durchsuchen", command=browse_path).pack()

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
    "entry", "checkbox", "radiobutton", "listbox", "scale", "spinbox", "fileexplorer"], width=12).pack(side="left", padx=2)

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


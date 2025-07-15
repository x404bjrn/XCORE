# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
# TODO: Fertigstellen / erweitern / optimieren
import json
import tkinter as tk

from tkinter import ttk, filedialog, messagebox
from tkcode import CodeEditor

from xcore_framework.editor.module_templates import SECTION_TEMPLATES


class ScrollableFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        canvas = tk.Canvas(self, height=300)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class ModuleCreatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XCORE Modul Generator")
        self.sections = []

        self.build_gui()


    def build_gui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Linker Bereich (Meta + Optionen)
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="y", padx=(0, 10))

        frm_meta = ttk.LabelFrame(left_frame, text="Metadaten")
        frm_meta.pack(fill="x", pady=5)

        self.meta_entries = {}
        for label in ["name", "description", "author", "version", "created", "category"]:
            row = ttk.Frame(frm_meta)
            row.pack(fill="x", padx=5, pady=2)
            ttk.Label(row, text=label.title(), width=12).pack(side="left")
            entry = ttk.Entry(row)
            entry.pack(fill="x", expand=True)
            self.meta_entries[label] = entry

        # OS-Auswahl für Modul-Metas
        os_row = ttk.Frame(frm_meta)
        os_row.pack(fill="x", padx=5, pady=2)
        ttk.Label(os_row, text="OS", width=15).pack(side="left")
        self.os_vars = {
            "windows": tk.BooleanVar(),
            "linux": tk.BooleanVar(),
            "osx": tk.BooleanVar()
        }
        for os_name, var in self.os_vars.items():
            cb = ttk.Checkbutton(os_row, text=os_name, variable=var)
            cb.pack(side="left")


        self.options_frame = ttk.LabelFrame(left_frame, text="Modul Optionen")
        self.options_frame.pack(fill="x", pady=5)
        self.option_entries = []

        # Labels für Option-Spalten
        header = ttk.Frame(self.options_frame)
        header.pack(fill="x", padx=5, pady=(0, 2))

        for name in ["Name", "Widget", "Required", "Default", "Description", "Type"]:
            lbl = ttk.Label(header, text=name, width=12, anchor="center")
            lbl.pack(side="left", padx=2)

        ttk.Button(self.options_frame, text="Neue Option", command=self.add_option).pack(pady=5)

        # Rechter Bereich (Sections)
        self.sections_container = ttk.LabelFrame(main_frame, text="Code Sections")
        self.sections_container.pack(side="right", fill="both", expand=True)

        self.scrollable = ScrollableFrame(self.sections_container)
        self.scrollable.pack(fill="both", expand=True)
        ttk.Button(self.sections_container, text="Neue Section", command=self.add_section).pack(pady=5)

        actions = ttk.Frame(self.root)
        actions.pack(pady=10)
        ttk.Button(actions, text="Modul generieren", command=self.generate_module).pack(side="left", padx=5)
        ttk.Button(actions, text="Modul laden", command=self.load_module).pack(side="left", padx=5)


    def add_option(self):
        row = ttk.Frame(self.options_frame)
        row.pack(fill="x", padx=5, pady=2)

        fields = {}

        # Name
        fields["name"] = ttk.Entry(row, width=10)
        fields["name"].pack(side="left", padx=2)

        # Widget-Typ Dropdown
        fields["widget_type"] = ttk.Combobox(row, values=[
            "entry", "checkbox", "radiobutton", "listbox", "spinbox", "scale", "fileexplorer"
        ], width=12)
        fields["widget_type"].pack(side="left", padx=2)

        # Required (true/false)
        fields["required"] = ttk.Entry(row, width=5)
        fields["required"].pack(side="left", padx=2)

        # Default-Wert
        fields["default"] = ttk.Entry(row, width=10)
        fields["default"].pack(side="left", padx=2)

        # Beschreibung
        fields["desc"] = ttk.Entry(row, width=20)
        fields["desc"].pack(side="left", padx=2)

        # Typ Dropdown
        fields["type"] = ttk.Combobox(row, values=[
            "string", "int", "float", "bool", "list", "dict", "any"
        ], width=8)
        fields["type"].pack(side="left", padx=2)

        # Farbfeld (automatisch angepasst nach Auswahl)
        color_label = tk.Label(row, text="", width=2, background="#f2f2f2")
        color_label.pack(side="left", padx=2)

        def update_color(*_):
            color_map = {
                "string": "#e6f7ff",
                "int": "#fff7e6",
                "float": "#f9e6ff",
                "bool": "#e6ffe6",
                "list": "#fff0f5",
                "dict": "#f0fff0",
                "any": "#f2f2f2"
            }
            selected = fields["type"].get().lower()
            color_label.configure(background=color_map.get(selected, "#ffffff"))

        fields["type"].bind("<<ComboboxSelected>>", update_color)

        self.option_entries.append(fields)
        self.resize_to_fit()


    def resize_to_fit(self):
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        self.root.geometry(f"{width+225}x{height}")


    def add_section(self, data=None):
        section_frame = ttk.LabelFrame(self.scrollable.scrollable_frame, text=f"Section {len(self.sections)+1}")
        section_frame.pack(fill="x", expand=True, padx=5, pady=5)

        id_row = ttk.Frame(section_frame)
        id_row.pack(fill="x", padx=5, pady=2)
        ttk.Label(id_row, text="ID", width=10).pack(side="left")
        id_entry = ttk.Entry(id_row)
        id_entry.pack(fill="x", expand=True)

        lang_row = ttk.Frame(section_frame)
        lang_row.pack(fill="x", padx=5, pady=2)
        ttk.Label(lang_row, text="Language", width=10).pack(side="left")

        lang_cb = ttk.Combobox(lang_row, values=list(SECTION_TEMPLATES.keys()), width=15)
        lang_cb.set("python")
        lang_cb.pack(side="left")

        desc_row = ttk.Frame(section_frame)
        desc_row.pack(fill="x", padx=5, pady=2)
        ttk.Label(desc_row, text="Description", width=10).pack(side="left")
        desc_entry = ttk.Entry(desc_row)
        desc_entry.pack(fill="x", expand=True)

        editor = CodeEditor(section_frame, language="python", height=12, width=80, highlighter="dracula", blockcursor=True)
        editor.pack(fill="x", expand=True, padx=5, pady=5)

        # Callback: Wenn Sprache geändert wird, aktualisiere Code
        def on_lang_change(event=None):
            lang = lang_cb.get()
            template = SECTION_TEMPLATES.get(lang, "")
            editor.delete("1.0", tk.END)
            editor.insert("1.0", template)

        lang_cb.bind("<<ComboboxSelected>>", on_lang_change)

        section = {
            "frame": section_frame,
            "id": id_entry,
            "language": lang_cb,
            "description": desc_entry,
            "code_widget": editor
        }

        self.sections.append(section)

        # Initialdaten setzen (z. B. beim Laden eines bestehenden Moduls)
        if data:
            id_entry.insert(0, data.get("id", ""))
            lang_cb.set(data.get("language", "python"))
            desc_entry.insert(0, data.get("description", ""))
            editor.insert("1.0", data.get("code", ""))
        else:
            # Wenn neu: Basis-Template einsetzen
            on_lang_change()

            # Fenstergröße automatisch anpassen
            self.resize_to_fit()


    def generate_module(self):
        meta = {k: v.get() for k, v in self.meta_entries.items()}

        # OS-Auswahl übernehmen
        meta["os"] = [os_name for os_name, var in self.os_vars.items() if var.get()]

        options = {}
        for opt in self.option_entries:
            name = opt["name"].get()
            if name:
                options[name] = {
                    "widget_type": opt["widget_type"].get(),
                    "required": opt["required"].get().lower() == "true",
                    "default": opt["default"].get(),
                    "desc": opt["desc"].get(),
                    "type": opt["type"].get()
                }

        sections = []
        for sec in self.sections:
            sections.append({
                "id": sec["id"].get(),
                "language": sec["language"].get(),
                "description": sec["description"].get(),
                "code": sec["code_widget"].get("1.0", "end-1c")
            })

        mod = {
            "meta": meta,
            "options": options,
            "sections": sections
        }

        path = filedialog.asksaveasfilename(defaultextension=".xmod", filetypes=[("XMOD Dateien", "*.xmod"), ("JSON", "*.json")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(mod, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Erfolg", f"Modul gespeichert unter:\n{path}")


    def load_module(self):
        path = filedialog.askopenfilename(filetypes=[("XMOD Dateien", "*.xmod"), ("JSON", "*.json")])
        if not path:
            return

        with open(path, "r", encoding="utf-8") as f:
            mod = json.load(f)

        for key, entry in self.meta_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, mod.get("meta", {}).get(key, ""))

        for os_name, var in self.os_vars.items():
            var.set(os_name in mod.get("meta", {}).get("os", []))

        for opt_fields in self.option_entries:
            for field in opt_fields.values():
                field.master.destroy()
        self.option_entries.clear()

        for name, opt in mod.get("options", {}).items():
            self.add_option()
            self.option_entries[-1]["name"].insert(0, name)
            self.option_entries[-1]["widget_type"].insert(0, opt.get("widget_type", ""))
            self.option_entries[-1]["required"].insert(0, str(opt.get("required", False)))
            self.option_entries[-1]["default"].insert(0, opt.get("default", ""))
            self.option_entries[-1]["desc"].insert(0, opt.get("desc", ""))
            self.option_entries[-1]["type"].set(opt.get("type", ""))

            # Farbe direkt setzen
            self.option_entries[-1]["type"].event_generate("<<ComboboxSelected>>")

        for sec in self.sections:
            sec["frame"].destroy()
        self.sections.clear()

        for section in mod.get("sections", []):
            self.add_section(section)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModuleCreatorGUI(root)
    root.mainloop()

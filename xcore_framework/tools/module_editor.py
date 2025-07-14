# TODO: NOCH NICHT ABGSCHLOSSEN!!! Not yet completed!!!
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcode import CodeEditor

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
        frm_meta = ttk.LabelFrame(self.root, text="Metadaten")
        frm_meta.pack(fill="x", padx=10, pady=5)

        self.meta_entries = {}
        for label in ["name", "description", "author", "version", "created", "category"]:
            row = ttk.Frame(frm_meta)
            row.pack(fill="x", padx=5, pady=2)
            ttk.Label(row, text=label.title(), width=15).pack(side="left")
            entry = ttk.Entry(row)
            entry.pack(fill="x", expand=True)
            self.meta_entries[label] = entry

        self.options_frame = ttk.LabelFrame(self.root, text="Modul Optionen")
        self.options_frame.pack(fill="x", padx=10, pady=5)
        self.option_entries = []
        ttk.Button(self.options_frame, text="Neue Option", command=self.add_option).pack(pady=5)

        self.sections_container = ttk.LabelFrame(self.root, text="Code Sections")
        self.sections_container.pack(fill="both", expand=True, padx=10, pady=5)

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
        for name in ["name", "widget_type", "required", "default", "desc"]:
            entry = ttk.Entry(row, width=12)
            entry.pack(side="left", padx=2)
            fields[name] = entry
        self.option_entries.append(fields)

    def add_section(self, data=None):
        section_frame = ttk.LabelFrame(self.scrollable.scrollable_frame, text=f"Section {len(self.sections)+1}")
        section_frame.pack(fill="both", expand=True, padx=5, pady=5)

        id_row = ttk.Frame(section_frame)
        id_row.pack(fill="x", padx=5, pady=2)
        ttk.Label(id_row, text="ID", width=10).pack(side="left")
        id_entry = ttk.Entry(id_row)
        id_entry.pack(fill="x", expand=True)

        lang_row = ttk.Frame(section_frame)
        lang_row.pack(fill="x", padx=5, pady=2)
        ttk.Label(lang_row, text="Language", width=10).pack(side="left")
        lang_cb = ttk.Combobox(lang_row, values=["python", "java", "powershell", "node"], width=15)
        lang_cb.set("python")
        lang_cb.pack(side="left")

        desc_row = ttk.Frame(section_frame)
        desc_row.pack(fill="x", padx=5, pady=2)
        ttk.Label(desc_row, text="Description", width=10).pack(side="left")
        desc_entry = ttk.Entry(desc_row)
        desc_entry.pack(fill="x", expand=True)

        editor = CodeEditor(section_frame, language="python", height=12, width=80, highlighter="dracula", blockcursor=True)
        editor.pack(padx=5, pady=5)

        section = {
            "frame": section_frame,
            "id": id_entry,
            "language": lang_cb,
            "description": desc_entry,
            "code_widget": editor
        }

        self.sections.append(section)

        if data:
            id_entry.insert(0, data.get("id", ""))
            lang_cb.set(data.get("language", "python"))
            desc_entry.insert(0, data.get("description", ""))
            editor.insert("1.0", data.get("code", ""))

    def generate_module(self):
        meta = {k: v.get() for k, v in self.meta_entries.items()}
        options = {}
        for opt in self.option_entries:
            name = opt["name"].get()
            if name:
                options[name] = {
                    "widget_type": opt["widget_type"].get(),
                    "required": opt["required"].get().lower() == "true",
                    "default": opt["default"].get(),
                    "desc": opt["desc"].get()
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
                json.dump(mod, f, indent=2)
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

        for sec in self.sections:
            sec["frame"].destroy()
        self.sections.clear()

        for section in mod.get("sections", []):
            self.add_section(section)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModuleCreatorGUI(root)
    root.mainloop()

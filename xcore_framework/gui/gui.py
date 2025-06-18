# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import tkinter as tk
import os
import ctypes
from functools import partial
from PIL import ImageTk, Image
from tkinter import ttk, messagebox

from xcore_framework.core.module_loader import ModuleLoader
from xcore_framework.gui.widget_factory import create_widget_by_meta
from xcore_framework.core.database_manager import DatabaseManager
from xcore_framework.config.env import DIRECTORY_GUI, SETTING_LANGUAGE, FONT_PACKAGE
from xcore_framework.config.i18n import i18n


def load_custom_fonts(*font_paths):
    """
    Lädt benutzerdefinierte Schriftarten ins System, wenn das Betriebssystem Windows ist.

    Es werden Pfade zu Schriftdateien erwartet und bei erfolgreichem Laden
    der Schriftarten in das Betriebssystem registriert. Wenn ein Pfad ungültig
    ist oder die Datei nicht existiert, wird eine Warnung ausgegeben.

    Arguments:
        font_paths: Die Schlüsselwortargumente repräsentieren die Pfade zu den
            Schriftdateien, die geladen werden sollen.

    Raises:
        KeyError: Falls Schlüssel in den übergebenen `font_paths` nicht korrekt
            verarbeitet werden können.
    """
    if os.name == "nt":
        for font_path in font_paths:
            if os.path.exists(font_path):
                ctypes.windll.gdi32.AddFontResourceExW(font_path, 0x10, 0)
            else:
                print(f"[!] Font nicht gefunden: {font_path}")


def refresh_entry_content(input_field, content):
    """
    Aktualisiert den Inhalt eines Eingabefelds mit einem Standardtext, falls das Feld leer ist.
    Dies kann zur Bereitstellung von Platzhaltern für Eingabefelder verwendet werden.

    Args:
        input_field: Eingabefeld, dessen Inhalt überprüft und aktualisiert werden soll.
        content: Standardtext, der im Eingabefeld eingefügt werden soll, falls dieses leer ist.
    """
    if input_field.get() == "":
        input_field.config(fg="grey")
        input_field.insert(0, content)


class XCoreGUI:
    """
    Diese Klasse stellt die grafische Benutzeroberfläche für die Anmeldung und
    Registrierung in einer Anwendung bereit.

    Die Klasse wird verwendet, um verschiedene GUI-Komponenten wie Eingabefelder,
    Buttons und Fenster für die Benutzerinteraktion zu erstellen und zu verwalten.
    Außerdem kümmert sie sich um das Layout und die Logik des Anmelde- und
    Registrierungsflusses.
    """

    def __init__(self, master_userform, dsize, dcoords, dimages):
        """
        Initialisiert eine Anmeldedialog-Klasse mit Benutzeroberflächenelementen und Funktionen.

        Die Klasse erstellt und verwaltet grafische Elemente und Ereignisse für die
        Benutzeranmeldung (Signin) und Registrierung (Signup). Sie enthält auch Buttons und
        Eingabefelder, die mit verschiedenen Ereignis-Handlern verbunden sind.
        Zusätzlich werden die Dialogfenstergröße, Titel und andere visuelle Aspekte konfiguriert.

        Attributes:
            _master                     Hauptfenster-Instanz der Benutzeroberfläche.
            _dsize                      Größe der Dialogfenster für verschiedene Ansichten.
            _dcoords                    Bildschirm-Koordinaten zur Positionierung der Fenster.
            _dimages                    Bilder und Icons für visuelle Elemente der
                                        Benutzeroberfläche.
            db                          Instanz eines Datenbankmanagers für Backend-Operationen.
            loader                      Instanz eines Modulladers für zusätzliche Module und
                                        Funktionalitäten.
            current_module              Aktuelles Modul, das geladen ist.
            option_widgets              Widgets-Container für Moduloptionen.

            module_var                  Variablen für Modulauswahl.
            module_box                  UI-Komponente zur Anzeige von Modulen.
            options_frame               Rahmen für Moduloptionen.
            run_button                  Button für das Ausführen von Modulen.
            console_output              Konsolenfenster für Ausgabe.
            clear_button                Button zum Leeren des Konsolenfensters.
            clear_btn_label             Beschriftung für den Clear-Button.
            run_btn_label               Beschriftung für den Run-Button.
            options_container           Container für die Anordnung von Optionen.

            _username_signup_input      Eingabefeld für Benutzernamen beim Registrieren.
            _password_signup_input      Eingabefeld für Passwort beim Registrieren.

            _frame_signin_data_area     Rahmen für Benutzereingaben beim Anmelden.
            _frame_btn_area             Rahmen für verschiedene Button-Aktionen.
            _user_icon                  Icon für Benutzername-Feld.
            _password_icon              Icon für Passwort-Feld.
            _username_signin_input      Eingabefeld für Benutzernamen beim Anmelden.
            _password_signin_input      Eingabefeld für das Passwort beim Anmelden.
            _login_btn                  Login-Button Aktionselement.
            _login_btn_label            Label für den Login-Button.
            _register_btn               Button für die Registrierung (Sign up).
            _without_passw_btn          Button für die Anmeldung ohne Passwort.

        Args:
            master_userform (Tk): Hauptfenster der Tkinter-Anwendung.
            dsize (dict): Größeninformationen für verschiedene Dialogfenster.
            dcoords (dict): Koordinateninformationen für Fensterpositionierungen.
            dimages (dict): Bilddateien für Icons und andere UI-Elemente.
        """
        self._master = master_userform
        self._dsize = dsize
        self._dcoords = dcoords
        self._dimages = dimages
        self.db = DatabaseManager()
        self.loader = ModuleLoader()
        self.current_module = None
        self.option_widgets = {}

        # Initialisieren der Modul 'Objekte' (für Modul Dialog Fenster)
        self.module_var = None
        self.module_box = None
        self.options_frame = None
        self.run_button = None
        self.console_output = None
        self.clear_button = None
        self.clear_btn_label = None
        self.run_btn_label = None
        self.options_container = None

        # Initialisieren (Leer) der Button-Felder für den Signup-Prozess.
        self._username_signup_input = None
        self._password_signup_input = None

        # Dialog Fenster (Signin) - Aufbau ________________________________________________________
        self._master.title(i18n.t("gui.dlg_title_signin"))
        self._master.geometry(
            f"{self._dsize['signin'][0]}x"
            f"{self._dsize['signin'][1]}+"
            f"{self._dcoords['x_pos_signin']}+"
            f"{self._dcoords['y_pos_signin']}"
        )
        self._master.resizable(False, False)
        self._master.iconphoto(
            False,
            tk.PhotoImage(file=os.path.join(DIRECTORY_GUI, "icons", "ico_dialog.png")),
        )

        # Frames __________________________________________________________________________________
        self._frame_signin_data_area = tk.Frame(
            self._master, bd=0, relief="flat", bg="#0B0B0B"
        )
        self._frame_signin_data_area.place(x=10, y=270, width=200, height=55)

        self._frame_btn_area = tk.Frame(self._master, bd=0, relief="flat", bg="#040403")
        self._frame_btn_area.place(x=10, y=335, width=200, height=90)

        # Icons für Eingabefelder _________________________________________________________________
        # Benutzer / User
        self._user_icon = tk.Label(
            self._frame_signin_data_area, image=self._dimages["img_user"], bg="#0B0B0B"
        )
        self._user_icon.place(x=8, y=5)

        # Passwort / Password
        self._password_icon = tk.Label(
            self._frame_signin_data_area,
            image=self._dimages["img_password"],
            bg="#0B0B0B",
        )
        self._password_icon.place(x=8, y=32)

        # Eingabefelder (Signin) __________________________________________________________________
        # Benutzername (Signin)
        self._username_signin_input = tk.Entry(
            self._frame_signin_data_area, bd=2, relief="sunken", fg="grey"
        )
        self._username_signin_input.place(x=37, y=5, width=153, height=22)
        self._username_signin_input.insert(
            0, i18n.t("gui.entry_username_signin_default")
        )

        # → Events
        self._username_signin_input.bind(
            "<Button-1>",
            lambda e: (
                self._username_signin_input.delete(0, tk.END),
                self._username_signin_input.config(fg="black"),
            ),
        )
        self._username_signin_input.bind(
            "<FocusOut>",
            lambda e: refresh_entry_content(
                self._username_signin_input, i18n.t("gui.entry_username_signin_refresh")
            ),
        )

        # Passwort (Signin)
        self._password_signin_input = tk.Entry(
            self._frame_signin_data_area, bd=2, relief="sunken", fg="grey", show="*"
        )
        self._password_signin_input.place(x=37, y=32, width=153, height=22)
        self._password_signin_input.insert(
            0, i18n.t("gui.entry_password_signin_default")
        )

        # → Events
        self._password_signin_input.bind(
            "<Button-1>",
            lambda e: (
                self._password_signin_input.delete(0, tk.END),
                self._password_signin_input.config(fg="black"),
            ),
        )
        self._password_signin_input.bind(
            "<FocusOut>",
            lambda e: refresh_entry_content(
                self._password_signin_input, i18n.t("gui.entry_password_signin_refresh")
            ),
        )

        # Login Button ____________________________________________________________________________
        self._login_btn = tk.Button(
            self._frame_btn_area, image=self._dimages["img_green_btn"]
        )
        self._login_btn.place(x=100, y=20, anchor="center")
        self._login_btn.config(
            bd=0,
            bg="#040403",
            activebackground="#040403",
            command=partial(self.user_signin),
        )

        # Login Button Label
        self._login_btn_label = tk.Label(
            self._login_btn,
            text=i18n.t("gui.btn_signin_label"),
            bg="#167336",
            fg="white",
            font=["Orbitron", "12"],
        )
        self._login_btn_label.place(relx=0.5, rely=0.5, anchor="center")

        # Login Button Events
        self._login_btn.bind(
            "<Enter>",
            lambda e: self._set_btn_state(
                self._login_btn, self._login_btn_label, "hover", "green"
            ),
        )
        self._login_btn.bind(
            "<Leave>",
            lambda e: self._set_btn_state(
                self._login_btn, self._login_btn_label, "normal", "green"
            ),
        )
        self._login_btn.bind(
            "<ButtonPress-1>",
            lambda e: self._set_btn_state(
                self._login_btn, self._login_btn_label, "pressed", "green"
            ),
        )
        self._login_btn.bind(
            "<ButtonRelease-1>",
            lambda e: self._set_btn_state(
                self._login_btn, self._login_btn_label, "hover", "green"
            ),
        )

        # Events auf Label → weiterleiten an Button
        self._login_btn_label.bind(
            "<Enter>", lambda e: self._login_btn.event_generate("<Enter>")
        )
        self._login_btn_label.bind(
            "<Leave>", lambda e: self._login_btn.event_generate("<Leave>")
        )
        self._login_btn_label.bind(
            "<ButtonPress-1>",
            lambda e: self._login_btn.event_generate("<ButtonPress-1>"),
        )
        self._login_btn_label.bind(
            "<ButtonRelease-1>",
            lambda e: self._login_btn.event_generate("<ButtonRelease-1>"),
        )

        # Signup / Registrieren Button (Link) _____________________________________________________
        self._register_btn = tk.Button(
            self._frame_btn_area, text=i18n.t("gui.btn_open_dlg_signup")
        )
        self._register_btn.place(x=100, y=50, anchor="center")
        self._register_btn.config(
            bd=0,
            fg="grey",
            bg="#040403",
            activebackground="#040403",
            activeforeground="#FFE491",
            command=partial(self.signup_dialog),
        )

        # → Events
        self._register_btn.bind(
            "<Enter>", lambda e: self._register_btn.config(fg="white")
        )
        self._register_btn.bind(
            "<Leave>", lambda e: self._register_btn.config(fg="grey")
        )

        # 'Ohne Anmeldung weiter' Button (Link) ___________________________________________________
        self._without_passw_btn = tk.Button(
            self._frame_btn_area, text=i18n.t("gui.btn_open_without_password")
        )
        self._without_passw_btn.place(x=100, y=70, anchor="center")
        self._without_passw_btn.config(
            bd=0,
            fg="grey",
            bg="#040403",
            activebackground="#040403",
            activeforeground="#FFE491",
            command=partial(self.module_screen),
        )

        # → Events
        self._without_passw_btn.bind(
            "<Enter>", lambda e: self._without_passw_btn.config(fg="white")
        )
        self._without_passw_btn.bind(
            "<Leave>", lambda e: self._without_passw_btn.config(fg="grey")
        )

    def signup_dialog(self):
        """
        Erstellt und zeigt ein Dialogfenster für die Benutzerregistrierung.

        Dieses Fenster dient dazu, neue Benutzerkonten anzulegen. Es enthält Eingabefelder
        für die Eingabe eines Benutzernamens und eines Passworts sowie einen Button, um den
        Registrierungsvorgang abzuschließen. Zusätzliche visuelle Elemente, wie Icons und
        Hintergrundbilder, sind integriert, um die Benutzererfahrung zu verbessern.
        """
        # Dialog Fenster (Signup) - Aufbau ________________________________________________________
        master_signup = tk.Toplevel(self._master, takefocus=True)
        master_signup.focus_set()
        master_signup.title(i18n.t("gui.dlg_title_signup"))
        master_signup.geometry(
            f"{self._dsize['signup'][0]}x"
            f"{self._dsize['signup'][1]}+"
            f"{self._dcoords['x_pos_signup']}+"
            f"{self._dcoords['y_pos_signup']}"
        )
        master_signup.iconphoto(
            False,
            tk.PhotoImage(file=os.path.join(DIRECTORY_GUI, "icons", "ico_dialog.png")),
        )
        master_signup.resizable(False, False)

        # Background
        register_background = tk.Canvas(
            master_signup, bg="#050505", bd=0, highlightthickness=0, relief="flat"
        )
        register_background.pack(fill="both", expand=1)
        register_background.create_image(
            0, 0, anchor="nw", image=self._dimages["img_register"]
        )

        # Frames __________________________________________________________________________________
        # Frame für Eingabefelder der Benutzerdaten
        frame_userdata_register_area = tk.Frame(
            master_signup, bd=0, relief="flat", bg="#0B0B0B"
        )
        frame_userdata_register_area.place(x=188, y=60, width=195, height=100)

        # Frame für Button Bereich
        frame_button_area = tk.Frame(master_signup, bd=0, relief="flat", bg="#040403")
        frame_button_area.place(x=180, y=180, width=208, height=33)

        # Icons für Eingabefelder _________________________________________________________________
        # Benutzer / User
        user_icon = tk.Label(
            frame_userdata_register_area, image=self._dimages["img_user"], bg="#0B0B0B"
        )
        user_icon.place(x=0, y=15)

        # Passwort / Password
        password_icon = tk.Label(
            frame_userdata_register_area,
            image=self._dimages["img_password"],
            bg="#0B0B0B",
        )
        password_icon.place(x=0, y=65)

        # Eingabefelder (Signup) __________________________________________________________________
        # Benutzername (Signup)
        self._username_signup_input = tk.Entry(
            frame_userdata_register_area, bd=2, relief="sunken", fg="grey"
        )
        self._username_signup_input.place(x=30, y=15, width=160, height=22)
        self._username_signup_input.insert(
            0, i18n.t("gui.entry_username_signup_default")
        )

        # Events
        self._username_signup_input.bind(
            "<Button-1>",
            lambda e: (
                self._username_signup_input.delete(0, tk.END),
                self._username_signup_input.config(fg="black"),
            ),
        )
        self._username_signup_input.bind(
            "<FocusOut>",
            lambda e: refresh_entry_content(
                self._username_signup_input, i18n.t("gui.entry_username_signup_refresh")
            ),
        )

        # Passwort (Signup)
        self._password_signup_input = tk.Entry(
            frame_userdata_register_area, bd=2, relief="sunken", fg="grey"
        )
        self._password_signup_input.place(x=30, y=65, width=160, height=22)
        self._password_signup_input.insert(
            0, i18n.t("gui.entry_password_signup_default")
        )

        # Events
        self._password_signup_input.bind(
            "<Button-1>",
            lambda e: (
                self._password_signup_input.delete(0, tk.END),
                self._password_signup_input.config(fg="black"),
            ),
        )
        self._password_signup_input.bind(
            "<FocusOut>",
            lambda e: refresh_entry_content(
                self._password_signup_input, i18n.t("gui.entry_password_signup_refresh")
            ),
        )

        # Signup Button (Benutzer anlegen) ________________________________________________________
        signup_btn = tk.Button(frame_button_area, image=self._dimages["img_green_btn"])
        signup_btn.pack(fill="both", side="right")
        signup_btn.config(
            bd=0,
            bg="#040403",
            activebackground="#040403",
            command=partial(self.user_signup),
        )

        # Signup Button Label
        signup_btn_label = tk.Label(
            signup_btn,
            text=i18n.t("gui.btn_signup_label"),
            bg="#167336",
            fg="white",
            font=["Orbitron", "12"],
        )
        signup_btn_label.place(relx=0.5, rely=0.5, anchor="center")

        # Signup Button Events
        signup_btn.bind(
            "<Enter>",
            lambda e: self._set_btn_state(
                signup_btn, signup_btn_label, "hover", "green"
            ),
        )
        signup_btn.bind(
            "<Leave>",
            lambda e: self._set_btn_state(
                signup_btn, signup_btn_label, "normal", "green"
            ),
        )
        signup_btn.bind(
            "<ButtonPress-1>",
            lambda e: self._set_btn_state(
                signup_btn, signup_btn_label, "pressed", "green"
            ),
        )
        signup_btn.bind(
            "<ButtonRelease-1>",
            lambda e: self._set_btn_state(
                signup_btn, signup_btn_label, "hover", "green"
            ),
        )

        # Events auf Label → weiterleiten an Button
        signup_btn_label.bind("<Enter>", lambda e: signup_btn.event_generate("<Enter>"))
        signup_btn_label.bind("<Leave>", lambda e: signup_btn.event_generate("<Leave>"))
        signup_btn_label.bind(
            "<ButtonPress-1>", lambda e: signup_btn.event_generate("<ButtonPress-1>")
        )
        signup_btn_label.bind(
            "<ButtonRelease-1>",
            lambda e: signup_btn.event_generate("<ButtonRelease-1>"),
        )

    def user_signin(self):
        """
        Authentifiziert einen Benutzer mit angegebenen Anmeldeinformationen.

        Diese Methode überprüft die vom Benutzer eingegebenen Anmeldeinformationen aus den
        Eingabefeldern für Benutzername und Passwort. Wenn die Authentifizierung erfolgreich ist,
        wird die Ansicht zur nächsten Modulansicht gewechselt. Im Falle eines Fehlers wird
        eine Fehlermeldung mit dem Hinweis auf ungültige Anmeldedaten angezeigt.

        Args:
            self: Das Instanzobjekt der Klasse.

        Raises:
            messagebox.Error: Wenn die Authentifizierung fehlschlägt, wird ein Fehlerdialog
            mit der entsprechenden Nachricht angezeigt.
        """
        user = self._username_signin_input.get()
        pw = self._password_signin_input.get()
        if self.db.login(user, pw):
            self.module_screen()
        else:
            messagebox.showerror(
                i18n.t("gui.login_error"), i18n.t("gui.login_error_msg")
            )

    def user_signup(self):
        """
        Führt die Benutzerregistrierung basierend auf den Eingaben des Benutzers durch.
        Überprüft, ob der Benutzername verfügbar ist, und erstellt einen neuen Benutzer,
        wenn dieser noch nicht existiert.

        Args:
            self: Das Instanzobjekt der Klasse.

        Raises:
            messagebox.showerror: Bei einem fehlgeschlagenen Registrierungsversuch wird
            ein Fehlerdialog angezeigt, der angibt, dass der Benutzername bereits existiert.
        """
        user = self._username_signup_input.get()
        pw = self._password_signup_input.get()
        if self.db.create_user(user, pw):
            self.module_screen()
        else:
            messagebox.showerror(
                i18n.t("gui.signup_error"), i18n.t("gui.signup_error_msg")
            )

    def clear_console(self):
        """
        Löscht den gesamten Inhalt der Konsolenausgabe und setzt die
        Konsole in einen nicht bearbeitbaren Zustand.
        """
        self.console_output.configure(state="normal")
        self.console_output.delete(1.0, tk.END)
        self.console_output.configure(state="disabled")

    def module_screen(self):
        """
        Initialisiert und gestaltet die Benutzeroberfläche für die Modul-Auswahl in der Anwendung.
        Die Methode setzt die grundsätzliche visuelle Struktur, Interaktionselemente und Events
        für das Modul-Management und die Konsolenanzeige.

        Attributes:
            _master (tk.Tk): Wurzel-Widget des aktuellen Fensters.
            _dsize (dict): Gibt die Dimensionen des Fensters an.
            _dcoords (dict): Koordinateninformationen für die Positionierung des Fensters.
            _dimages (dict): Enthält die Bildressourcen für Buttons.
            loader (object): Objekt, um Module zu laden und zu durchsuchen.
            module_var (tk.StringVar): Variable zum Speichern der Auswahl im Modul-Dropdown.
            module_box (ttk.Combobox): Dropdown zur Auswahl von Modulen.
            options_container (tk.Frame): Container zur Anzeige der Modul-Optionen.
            options_frame (tk.Frame): Inneres Frame im scrollbaren Bereich für Modul-Optionen.
            run_button (tk.Button): Button zur Ausführung des gewählten Moduls.
            run_btn_label (tk.Label): Beschriftung des Run-Buttons.
            console_output (tk.Text): Anzeigefeld für Konsolenausgaben.
            clear_button (tk.Button): Button, um die Konsole zu leeren.
            clear_btn_label (tk.Label): Beschriftung des Clear-Buttons.

        Raises:
            Keine spezifischen Fehler werden geworfen.

        Args:
            self: Standardargument zur Übergabe der Instanz des Objekts an die Methode.

        Returns:
            None
        """
        self.clear()

        # Dialog Aufbau ___________________________________________________________________________
        self._master.title(i18n.t("gui.dlg_title_module"))
        self._master.geometry(
            f"{self._dsize['module'][0]}x"
            f"{self._dsize['module'][1]}+"
            f"{self._dcoords['x_pos_module']}+"
            f"{self._dcoords['y_pos_module']}"
        )
        self._master.resizable(True, False)
        self._master.config(bg="#050505")

        # Label - 'Wähle ein Modul'
        tk.Label(
            self._master,
            text=i18n.t("gui.choose_module"),
            bg="#050505",
            fg="white",
            font=["Orbitron", "12"],
        ).pack(ipady=10)

        # Modul-Box / Combobox (Dropdown) _________________________________________________________
        self.module_var = tk.StringVar()
        self.module_box = ttk.Combobox(self._master, textvariable=self.module_var)
        self.module_box["values"] = self.loader.search_modules("")
        self.module_box.bind("<<ComboboxSelected>>", self.load_module_options)
        self.module_box.config(
            background="#050505", foreground="white", font=["Orbitron", "10"]
        )
        self.module_box.pack()

        # Scrollbarer Bereich → Frame → Canvas → Scrollbar + inneres Frame ________________________
        self.options_container = tk.Frame(
            self._master, bg="#1C033E", height=200, relief="sunken", bd=5
        )
        self.options_container.pack(fill="x", padx=8, pady=8)
        self.options_container.pack_propagate(False)

        canvas = tk.Canvas(
            self.options_container,
            bg="#1C033E",
            highlightthickness=0,
            highlightbackground="#333",
        )

        scrollbar = ttk.Scrollbar(
            self.options_container, orient="vertical", command=canvas.yview
        )

        self.options_frame = tk.Frame(canvas, bg="#1C033E")
        self.options_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.options_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=8)
        scrollbar.pack(side="right", fill="y")

        def resize_options_frame(event):
            """
            Dynamische Breite.
            """
            canvas.itemconfig("options_window", width=event.width)

        canvas.bind("<Configure>", resize_options_frame)
        canvas_frame = canvas.create_window(
            (0, 0), window=self.options_frame, anchor="nw", tags="options_window"
        )

        self.options_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        def _on_mousewheel(event):
            """
            Scrollen mit dem Mausrad.
            """
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.options_frame.bind(
            "<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel)
        )
        self.options_frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Run Button (Modul ausführen) ____________________________________________________________
        self.run_button = tk.Button(
            self._master,
            image=self._dimages["img_green_btn"],
            command=self.run_module,
            bg="#050505",
            activebackground="#050505",
            bd=0,
        )
        self.run_button.pack(pady=(5, 10))

        # Run Button Label
        self.run_btn_label = tk.Label(
            self.run_button,
            text=i18n.t("gui.run_module"),
            bg="#167336",
            fg="white",
            font=["Orbitron", "12"],
        )
        self.run_btn_label.place(relx=0.5, rely=0.5, anchor="center")

        # Run Button Events
        self.run_button.bind(
            "<Enter>",
            lambda e: self._set_btn_state(
                self.run_button, self.run_btn_label, "hover", "green"
            ),
        )
        self.run_button.bind(
            "<Leave>",
            lambda e: self._set_btn_state(
                self.run_button, self.run_btn_label, "normal", "green"
            ),
        )
        self.run_button.bind(
            "<ButtonPress-1>",
            lambda e: self._set_btn_state(
                self.run_button, self.run_btn_label, "pressed", "green"
            ),
        )
        self.run_button.bind(
            "<ButtonRelease-1>",
            lambda e: self._set_btn_state(
                self.run_button, self.run_btn_label, "hover", "green"
            ),
        )

        # Events auf Label → weiterleiten an Button
        self.run_btn_label.bind(
            "<Enter>", lambda e: self.run_button.event_generate("<Enter>")
        )
        self.run_btn_label.bind(
            "<Leave>", lambda e: self.run_button.event_generate("<Leave>")
        )
        self.run_btn_label.bind(
            "<ButtonPress-1>",
            lambda e: self.run_button.event_generate("<ButtonPress-1>"),
        )
        self.run_btn_label.bind(
            "<ButtonRelease-1>",
            lambda e: self.run_button.event_generate("<ButtonRelease-1>"),
        )

        # Konsolenbereich _________________________________________________________________________
        # Label
        tk.Label(
            self._master,
            text=i18n.t("gui.console_print"),
            bg="#050505",
            fg="#dbc247",
            font=["Orbitron", "12"],
        ).pack(pady=(10, 0))

        # Output Display
        self.console_output = tk.Text(
            self._master, height=10, bg="black", fg="lime", insertbackground="white"
        )
        self.console_output.pack(fill="both", expand=True, padx=10, pady=(0, 5))
        self.console_output.configure(state="disabled")

        # Konsole Clear Button ____________________________________________________________________
        self.clear_button = tk.Button(
            self._master,
            image=self._dimages["img_red_btn"],
            command=self.clear_console,
            bg="#050505",
            activebackground="#050505",
            bd=0,
        )
        self.clear_button.pack(pady=(5, 10))

        # Clear Button Label
        self.clear_btn_label = tk.Label(
            self.clear_button,
            text=i18n.t("gui.console_clear"),
            bg="#CD1B1B",
            fg="white",
            font=["Orbitron", "12"],
        )
        self.clear_btn_label.place(relx=0.5, rely=0.5, anchor="center")

        # Clear Button Events
        self.clear_button.bind(
            "<Enter>",
            lambda e: self._set_btn_state(
                self.clear_button, self.clear_btn_label, "hover", "red"
            ),
        )
        self.clear_button.bind(
            "<Leave>",
            lambda e: self._set_btn_state(
                self.clear_button, self.clear_btn_label, "normal", "red"
            ),
        )
        self.clear_button.bind(
            "<ButtonPress-1>",
            lambda e: self._set_btn_state(
                self.clear_button, self.clear_btn_label, "pressed", "red"
            ),
        )
        self.clear_button.bind(
            "<ButtonRelease-1>",
            lambda e: self._set_btn_state(
                self.clear_button, self.clear_btn_label, "hover", "red"
            ),
        )

        # Events auf Label → weiterleiten an Button
        self.clear_btn_label.bind(
            "<Enter>", lambda e: self.clear_button.event_generate("<Enter>")
        )
        self.clear_btn_label.bind(
            "<Leave>", lambda e: self.clear_button.event_generate("<Leave>")
        )
        self.clear_btn_label.bind(
            "<ButtonPress-1>",
            lambda e: self.clear_button.event_generate("<ButtonPress-1>"),
        )
        self.clear_btn_label.bind(
            "<ButtonRelease-1>",
            lambda e: self.clear_button.event_generate("<ButtonRelease-1>"),
        )

    def load_module_options(self, event):
        """
        Lädt die Moduloptionen basierend auf einem ausgewählten Modul und erstellt
        grafische Widgets zur Anzeige und Bearbeitung der Optionen.
        Die Methode ist aufgerufen, wenn ein Ereignis ausgelöst wird
        (z. B. eine Benutzerinteraktion).

        Parameters:
            event: object
                Das Ereignisobjekt, das ausgelöst wurde.

        Raises:
            Keine speziellen Ausnahmefälle sind definiert für diesen Code.
        """
        self.clear_frame(self.options_frame)
        self.option_widgets.clear()

        mod_id = self.module_var.get()
        mod = self.loader.load_module(mod_id)
        if not mod:
            return

        self.current_module = mod

        for name, meta in mod.options.items():
            label = tk.Label(
                self.options_frame,
                text=meta.get("desc", name),
                bg="#1C033E",
                fg="white",
                font=["Fira Code", "10"],
            )
            label.pack(anchor="w")

            widget = create_widget_by_meta(self.options_frame, name, meta)
            self.option_widgets[name] = widget

    def run_module(self):
        """
        Führt das aktuelle Modul aus, falls vorhanden, und zeigt den Ausführungsstatus an.

        Die Methode lädt die aktuellen Parameterwerte aus Widgets, führt das aktuelle Modul
        aus und verarbeitet das Ergebnis. Erfolgreiche Ausführungen führen zu einer
        Informationsmeldung, während Fehler mit einer Fehlermeldung angezeigt werden.

        Args:
            Keine Argumente

        Raises:
            Exception: Wenn während der Modulausführung ein Fehler auftritt.
        """
        if not self.current_module:
            return

        self.clear_console()

        values = {}
        for name, widget in self.option_widgets.items():
            val = widget.var.get()
            values[name] = val if not isinstance(val, bool) else str(val)
        try:
            result = self.current_module.run(
                values, mode="gui", gui_console=self.console_output
            )
            if result.get("success"):
                messagebox.showinfo(
                    i18n.t("gui.notify_title_success"),
                    i18n.t("gui.notify_success_content"),
                )
            else:
                messagebox.showerror(
                    i18n.t("gui.notify_title_fail"),
                    result.get("error", i18n.t("gui.notify_fail_content")),
                )
        except Exception as e:
            messagebox.showerror(i18n.t("gui.notify_title_fail"), str(e))

    def _set_btn_state(self, btn_object, label_object, state, color):
        """
        Setzt den Zustand eines Buttons und eines zugehörigen Labels basierend auf dem
        angegebenen Zustand und der Farbe. Der Zustand beeinflusst das Aussehen sowohl
        des Buttons als auch des Labels, indem diese entsprechend neu konfiguriert werden.

        Args:
            btn_object: Das Button-Objekt, dessen Aussehen angepasst werden soll.
            label_object: Das Label-Objekt, das ebenfalls konfiguriert wird,
                          basierend auf dem Zustand.
            state: Ein String, der den Zustand beschreibt
                   ("hover", "pressed" oder eine andere Angabe).
            color: Ein String, der die gewünschte Farbvariante für den Button angibt.
        """
        if color == "red":
            bg_color = ["#CD1B1B", "#E23E3E", "#FF7C7C"]  # default, hover, pressed
        elif color == "green":
            bg_color = ["#167336", "#21BF58", "#0DE982"]
        else:
            bg_color = ["#167336", "#21BF58", "#0DE982"]

        if state == "hover":
            btn_object.config(image=self._dimages[f"img_{color}_btn_mouseover"])
            label_object.config(bg=bg_color[1], fg="white")
        elif state == "pressed":
            btn_object.config(image=self._dimages[f"img_{color}_btn_press"])
            label_object.config(bg=bg_color[2], fg="black")
        else:
            btn_object.config(image=self._dimages[f"img_{color}_btn"])
            label_object.config(bg=bg_color[0], fg="white")

    def clear(self):
        """
        Entfernt alle untergeordneten Widgets des angegebenen Masters.

        Diese Methode durchsucht und entfernt rekursiv alle Widgets,
        die sich im Master-Widget befinden. Sie bietet eine einfache Möglichkeit,
        den Inhalt eines Layouts komplett zu leeren.

        Raises:
            Keine
        """
        for widget in self._master.winfo_children():
            widget.destroy()

    @staticmethod
    def clear_frame(frame):
        """
        Eine Methode, die alle Widgets innerhalb eines angegebenen Frames entfernt.
        Dies ist nützlich, um die Benutzeroberfläche dynamisch zu aktualisieren oder
        Platz für neue Inhalte zu schaffen. Die Methode wird als statische Methode definiert,
        da sie keine Instanzvariablen oder Attribute benötigt.

        @param frame: Der Frame, aus dem alle Widgets entfernt werden sollen.
            Es handelt sich typischerweise um ein tkinter.Frame-Objekt.
        @type frame: tkinter.Frame

        @rtype: None
        """
        for widget in frame.winfo_children():
            widget.destroy()


def start_gui():
    # Fenstergröße und Position
    # Auslesen der Auflösung des Monitors
    user32_start = ctypes.windll.user32
    monitor_width = user32_start.GetSystemMetrics(0)
    monitor_height = user32_start.GetSystemMetrics(1)

    # Fenstergröße des "Signin" und "Signup" Fensters (width, height)
    dlg_sizes = {"signin": (220, 420), "signup": (400, 227), "module": (600, 600)}

    # Errechnung von Fensterpositionskoordinaten der Mitte des Bildschirms
    dlg_coords = {
        "x_pos_signin": int((monitor_width / 2) - (dlg_sizes["signin"][0] / 2)),
        "y_pos_signin": int((monitor_height / 2) - (dlg_sizes["signin"][1] / 2)),
        "x_pos_signup": int(((monitor_width / 2) - (dlg_sizes["signin"][0] / 2)) - 410),
        "y_pos_signup": int((monitor_height / 2) - (dlg_sizes["signin"][1] / 2)),
        "x_pos_module": int(((monitor_width / 2) - (dlg_sizes["module"][0] / 2)) + 10),
        "y_pos_module": int((monitor_height / 2) - (dlg_sizes["module"][1] / 2)),
    }

    # Fonts laden
    load_custom_fonts(*list(FONT_PACKAGE.values()))

    # Tkinter Root
    root = tk.Tk()

    # Hintergrundfläche
    background = tk.Canvas(
        root, bg="#040403", bd=0, highlightthickness=0, relief="flat"
    )
    background.pack(fill="both", expand=1)

    # Hintergrundbild
    background_picture = tk.PhotoImage(
        file=os.path.join(
            DIRECTORY_GUI, "images", "backgrounds", "signin_background.png"
        )
    )
    background.create_image(0, -10, anchor="nw", image=background_picture)

    # Grafiken Initialisieren
    gui_images_path = os.path.join(DIRECTORY_GUI, "images")
    gui_icons_path = os.path.join(DIRECTORY_GUI, "icons")
    dlg_images = {
        "img_user": ImageTk.PhotoImage(
            Image.open(os.path.join(gui_icons_path, "ico_user.png"))
        ),
        "img_register": ImageTk.PhotoImage(
            Image.open(
                os.path.join(
                    gui_images_path,
                    "backgrounds",
                    f"signup_background_{SETTING_LANGUAGE.upper()}.png",
                )
            )
        ),
        "img_password": ImageTk.PhotoImage(
            Image.open(os.path.join(gui_icons_path, "ico_passw.png"))
        ),
        "img_green_btn": ImageTk.PhotoImage(
            Image.open(
                os.path.join(gui_images_path, "buttons", "btn_green_default.png")
            )
        ),
        "img_green_btn_mouseover": ImageTk.PhotoImage(
            Image.open(
                os.path.join(gui_images_path, "buttons", "btn_green_mouseover.png")
            )
        ),
        "img_green_btn_press": ImageTk.PhotoImage(
            Image.open(
                os.path.join(gui_images_path, "buttons", "btn_green_pressed.png")
            )
        ),
        "img_red_btn": ImageTk.PhotoImage(
            Image.open(os.path.join(gui_images_path, "buttons", "btn_red_default.png"))
        ),
        "img_red_btn_mouseover": ImageTk.PhotoImage(
            Image.open(
                os.path.join(gui_images_path, "buttons", "btn_red_mouseover.png")
            )
        ),
        "img_red_btn_press": ImageTk.PhotoImage(
            Image.open(os.path.join(gui_images_path, "buttons", "btn_red_pressed.png"))
        ),
    }

    XCoreGUI(root, dlg_sizes, dlg_coords, dlg_images)
    root.mainloop()

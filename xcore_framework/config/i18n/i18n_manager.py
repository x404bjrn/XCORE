# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import json

from xcore_framework.config.formatting import formatter

available_languages = ["de", "en"]


class I18nManager:
    """
    Verwaltung der Lokalisierung und Internationalisierung (I18n).

    Bietet Funktionen zum Laden und Verwalten von Übersetzungen für
    verschiedene Sprachen. Ermöglicht die Auswahl der Sprache und bietet
    eine Methode zur Übersetzung von Textschlüsseln.

    :ivar lang: Aktuell ausgewählte Sprache.
    :type lang: str
    :ivar fallback_lang: Standardsprache, falls keine Übersetzungen
        für die ausgewählte Sprache gefunden werden.
    :type fallback_lang: str
    :ivar base_path: Basisverzeichnis, in dem die Übersetzungsdateien
        gespeichert sind.
    :type base_path: str
    :ivar translations: Ein Wörterbuch, das die geladenen Übersetzungen
        für die verschiedenen Kategorien und Schlüssel speichert.
    :type translations: dict
    """

    def __init__(self, lang="de", fallback_lang="en", base_path="i18n"):
        self.lang = lang
        self.fallback_lang = fallback_lang
        self.base_path = base_path
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        """
        Lädt Übersetzungsdaten für die Anwendung und initialisiert diese. Die Methode sorgt
        dafür, dass zuerst die Fallback-Sprache geladen wird. Falls die aktive Sprache nicht
        mit der Fallback-Sprache übereinstimmt, wird zusätzlich die aktive Sprache geladen.

        :raises RuntimeError: Falls die Sprache nicht geladen werden kann.
        :return: Gibt nichts zurück. Initialisiert interne Datenstrukturen.
        """
        self.translations = {}
        self._load_language(self.fallback_lang)  # Fallback zuerst
        if self.lang != self.fallback_lang:
            self._load_language(self.lang)

    def _load_language(self, lang_code):
        """
        Lädt Übersetzungsdateien für eine gegebene Sprachkennung aus dem festgelegten Pfad.
        Die Funktion überprüft, ob der entsprechende Ordner existiert, geht durch alle JSON-Dateien
        im Ordner und aktualisiert die Übersetzungskategorien mit den Inhalten der Dateien.

        :param lang_code: Die Sprachkennung, die verwendet wird, um den Sprachpfad zu bestimmen.
        :type lang_code: str
        :return: Gibt None zurück, wenn das Verzeichnis nicht existiert oder keine
        JSON-Dateien gefunden werden.
        :rtype: None
        """
        lang_path = os.path.join(self.base_path, lang_code)
        if not os.path.isdir(lang_path):
            return

        for filename in os.listdir(lang_path):
            if filename.endswith(".json"):
                category = filename[:-5]
                with open(
                    os.path.join(lang_path, filename), "r", encoding="utf-8"
                ) as f:
                    self.translations.setdefault(category, {}).update(json.load(f))

    def t(self, key, **kwargs):
        """
        Die Funktion stellt eine einfache Übersetzungsmethode bereit, die Zeichenketten anhand
        einer vordefinierten Übersetzungsdatenstruktur findet und optional formatierte Platzhalter
        in den Zeichenketten ersetzt. Ist der angegebene Schlüssel nicht im erwarteten Format oder
        wird der Schlüssel nicht gefunden, wird ein Fallback verwendet.

        :param key: Der Schlüssel der Übersetzung im Format 'kategorie.schlüssel'.
        :type key: str
        :param kwargs: Zusätzliche Schlüsselwortargumente, die verwendet werden, um Platzhalter
            in der übersetzten Zeichenkette zu ersetzen.
        :type kwargs: dict
        :return: Die übersetzte Zeichenkette oder, falls der Schlüssel nicht gefunden wird oder
            ein Fehler auftritt, der ursprüngliche Schlüssel oder ein gekennzeichneter Fallback.
        :rtype: str
        """
        parts = key.split(".")
        if len(parts) != 2:
            return key

        cat, k = parts
        text = self.translations.get(cat, {}).get(k, f"[{key}]")

        try:
            # Hinzufügen von Formatierungsargumenten
            kwargs.update(formatter)
            return text.format(**kwargs)
        except (KeyError, AttributeError):
            return f"[{key}]"

    def set_language(self, lang):
        """
        Legt die Spracheinstellungen für die Anwendung fest.

        Überprüft, ob die angegebene Sprache unterstützt wird. Falls die Sprache
        verfügbar ist, wird sie als aktuelle Sprache eingestellt und die
        Übersetzungen werden entsprechend geladen. Gibt `True` zurück, wenn die
        Sprache erfolgreich gesetzt wurde, und `False`, falls die Sprache nicht
        verfügbar ist.

        :param lang: Eine Zeichenkette, die die Sprache angibt, die festgelegt
                     werden soll. Erwartet wird ein Sprachcode, wie z. B. 'en',
                     'de' oder 'fr'.
        :type lang: str
        :return: `True`, wenn die Sprache erfolgreich gesetzt wurde, andernfalls
                 `False`.
        :rtype: bool
        """
        if lang in available_languages:
            self.lang = lang
            self.load_translations()
            return True
        return False

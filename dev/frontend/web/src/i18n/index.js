// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import i18n from "i18next";
import { initReactI18next } from "react-i18next";

// Übersetzungsdateien importieren
import deModule from "@/i18n/de/module.json";
import deBase from "@/i18n/de/base.json";
import deError from "@/i18n/de/error.json";

import enModule from "@/i18n/en/module.json";
import enBase from "@/i18n/en/base.json";
import enError from "@/i18n/en/error.json";

// Lies die Sprache aus der ENV-Variable
const lang = import.meta.env.VITE_LANG || "de";

i18n
  .use(initReactI18next)
  .init({
    resources: {
      de: {
        module: deModule,
        base: deBase,
        error: deError,
      },
      en: {
        module: enModule,
        base: enBase,
        error: enError,
      },
    },
    lng: lang,
    fallbackLng: "de",
    // → Namespaces + Standard
    ns: ["base", "module", "error"],
    defaultNS: "base",
    interpolation: { escapeValue: false },
  });

export default i18n;

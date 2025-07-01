// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import i18n from "i18next";
import { initReactI18next } from "react-i18next";

// Übersetzungsdateien importieren
import deModule from "@/i18n/de/module.json";
import deBase from "@/i18n/de/base.json";
import deSignin from "@/i18n/de/signin.json";
import deSignup from "@/i18n/de/signup.json";
import deSidelist from "@/i18n/de/sidelist.json";

import enModule from "@/i18n/en/module.json";
import enBase from "@/i18n/en/base.json";
import enSignin from "@/i18n/en/signin.json";
import enSignup from "@/i18n/en/signup.json";
import enSidelist from "@/i18n/en/sidelist.json";

// Lies die Sprache aus der ENV-Variable
const lang = import.meta.env.SETTING_LANGUAGE || "de";

i18n
  .use(initReactI18next)
  .init({
    resources: {
      de: {
        module: deModule,
        base: deBase,
        signin: deSignin,
        signup: deSignup,
        sidelist: deSidelist,
      },
      en: {
        module: enModule,
        base: enBase,
        signin: enSignin,
        signup: enSignup,
        sidelist: enSidelist,
      },
    },
    lng: lang,
    fallbackLng: "de",
    // → Namespaces + Standard
    ns: ["module", "base", "signin", "signup", "sidelist"],
    defaultNS: "base",
    interpolation: { escapeValue: false },
  });

export default i18n;

// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import React from "react";
import { useTranslation } from "react-i18next";

export default function Sidelist({ modules, selectedCategory, onModuleSelect }) {
  const { t } = useTranslation("sidelist");

  return (
    <aside className="sidelist">
        <h1>{t("title_h1")}</h1>
      <ul className="sidelist-menu">
        <li className="sidelist-menu-item">
            <a href="#" onClick={() => onModuleSelect('')} className="sidelist-link">
              {t("btn_list_reset")}
            </a>
        </li>
        {/* Die Module dynamisch anzeigen */}
        {selectedCategory && modules[selectedCategory]?.map((mod) => (
          <li key={mod.path} className="sidelist-menu-item">
            <button
              onClick={() => onModuleSelect(mod.path)}
              className="button-sidelist"
            >
              {mod.name}
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
}

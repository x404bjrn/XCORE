// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import { useTranslation } from "react-i18next";

const ModuleSelector = ({ modules, category, onChange }) => {
    const { t } = useTranslation("module");

    return (
        <div className="select">
            <select onChange={(e) => onChange(e.target.value)}>
                <option value="">{t("choose_category")}</option>
                {modules[category].map(mod => (
                    <option key={mod.path} value={mod.path}>{mod.name}</option>
                ))}
            </select>
        </div>
    );
};

export default ModuleSelector;

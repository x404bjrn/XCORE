// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import { useTranslation } from "react-i18next";

const CategorySelector = ({ modules, onChange }) => {
    const {t} = useTranslation("module");

    return (
        <div className="select">
            <select onChange={(e) => onChange(e.target.value)}>
                <option value="">{t("choose_category")}</option>
                {Object.keys(modules).map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                ))}
            </select>
        </div>
    );
};

export default CategorySelector;

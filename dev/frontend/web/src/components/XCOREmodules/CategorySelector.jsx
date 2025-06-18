// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
const CategorySelector = ({ modules, onChange }) => (
    <>
        <div className="select">
            <select onChange={(e) => onChange(e.target.value)}>
                <option value="">Kategorie wählen..</option>
                {Object.keys(modules).map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                ))}
            </select>
        </div>
    </>
);

export default CategorySelector;

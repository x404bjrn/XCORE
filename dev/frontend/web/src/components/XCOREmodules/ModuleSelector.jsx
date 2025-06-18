// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
const ModuleSelector = ({ modules, category, onChange }) => (
  <>
    <div className="select">
    <select onChange={(e) => onChange(e.target.value)}>
      <option value="">Modul wählen..</option>
      {modules[category].map(mod => (
        <option key={mod.path} value={mod.path}>{mod.name}</option>
      ))}
    </select>
   </div>
  </>
);

export default ModuleSelector;

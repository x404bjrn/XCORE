// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
// TODO: Widgeteinbindung optimieren und Formatierungen updaten
import React from "react";

const renderOptionWidget = (key, opt, value, setParams) => {
  const handleChange = (e) => {
    setParams((prev) => ({ ...prev, [key]: e.target.value }));
  };
  const widgetType = opt.widget_type || "entry";


  switch (widgetType) {
    case "checkbox":
      return (
        <input
          type="checkbox"
          checked={value === true || value === "true"}
          onChange={(e) => setParams((prev) => ({ ...prev, [key]: e.target.checked }))}
        />
      );

    case "radiobutton":
      return (
        <div className="radio-group">
          {opt.values?.map((v) => (
            <label key={v}>
              <input
                type="radio"
                name={key}
                value={v}
                checked={value === v}
                onChange={handleChange}
              />
              {v}
            </label>
          ))}
        </div>
      );

    case "listbox":
      return (
        <select value={value} onChange={handleChange}>
          {opt.values?.map((v) => (
            <option key={v} value={v}>{v}</option>
          ))}
        </select>
      );

    case "spinbox":
      return (
        <input
          type="number"
          value={value}
          min={opt.min ?? 0}
          max={opt.max ?? 100}
          onChange={handleChange}
        />
      );

    case "scale":
      return (
        <input
          type="range"
          value={value}
          min={opt.min ?? 0}
          max={opt.max ?? 100}
          onChange={handleChange}
        />
      );

    case "fileexplorer":
      return (
        <input
          type="file"
          onChange={(e) => setParams((prev) => ({ ...prev, [key]: e.target.files[0]?.name }))}
        />
      );

    default:
      return <input type="text" value={value} onChange={handleChange} />;
  }
};

const tableHeaders = ["Parameter", "Beschreibung", "Wert"];

const ModuleDetails = ({ meta, params, setParams, onRun }) => (
  <div className="module-container">
    <div className="module-header">
      <h2>{meta.name}</h2>
      <p className="description">{meta.description}</p>
      <div className="meta-info">
        <span><strong>Version:</strong> {meta.version}</span>
        <span><strong>Autor:</strong> {meta.author}</span>
      </div>
    </div>

    <div className="options-table">
      <table>
        <thead>
          <tr>
            <th>Parameter</th>
            <th>Beschreibung</th>
            <th>Wert</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(meta.options).map(([key, opt]) => (
            <tr key={key}>
              <td data-label={tableHeaders[0]}><code>{key}</code></td>
              <td data-label={tableHeaders[1]}>{opt.desc}</td>
              <td data-label={tableHeaders[2]}>
                {renderOptionWidget(key, opt, params[key] ?? opt.default, setParams)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>

    <button className="button-module-start" onClick={onRun}>
      🚀 Modul ausführen
    </button>
  </div>
);

export default ModuleDetails;

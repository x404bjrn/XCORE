// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
// TODO: Widgeteinbindung optimieren und Formatierungen updaten
import React from "react";
import { useTranslation } from "react-i18next";

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
          accept=".txt"
          onChange={e => {
            const file = e.target.files[0];
            if (file) {
              const reader = new FileReader();
              reader.onload = ev => {
                setParams(prev => ({ ...prev, [key]: ev.target.result }));
              };
              reader.readAsText(file, "UTF-8");
            }
          }}
        />
      );

    default:
      return <input type="text" value={value} onChange={handleChange} />;
  }
};

const ModuleDetails = ({ meta, params, setParams, onRun }) => {
  const {t} = useTranslation("module");
  const tableHeaders = [
    t("module_details_parameter_th"),
    t("module_details_description_th"),
    t("module_details_value_th")
  ];

  return (
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
            <th>{t("module_details_parameter_th")}</th>
            <th>{t("module_details_description_th")}</th>
            <th>{t("module_details_value_th")}</th>
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
        {t("btn_module_start")}
      </button>
    </div>
  );
};

export default ModuleDetails;

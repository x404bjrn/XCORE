// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CategorySelector from './CategorySelector.jsx';
import ModuleSelector from './ModuleSelector.jsx';
import ModuleDetails from './ModuleDetails.jsx';
import ResultDisplay from './ResultDisplay.jsx';

function XcoreModules({
  modules,
  selectedCategory,
  onCategoryChange,
  selectedModule,
  onModuleChange
}) {
  const [meta, setMeta] = useState(null);
  const [params, setParams] = useState({});
  const [result, setResult] = useState(null);

  useEffect(() => {
    if (selectedModule) {
      axios.get(`/api/module/${selectedModule}/meta`).then(res => {
        const data = res.data;
        setMeta(data);
        const defaults = {};
        for (const key in data.options) {
          defaults[key] = data.options[key].default;
        }
        setParams(defaults);
        setResult(null);
      });
    } else {
      setMeta(null);
      setParams({});
      setResult(null);
    }
  }, [selectedModule]);

  const handleRun = async () => {
    const res = await axios.post(`/api/module/${selectedModule}/run`, params);
    setResult(res.data);
  };

  return (
    <>
      <div className="module-selector-container">
      <CategorySelector
        modules={modules}
        onChange={onCategoryChange}
      />

      {selectedCategory && (
        <ModuleSelector
          modules={modules}
          category={selectedCategory}
          onChange={onModuleChange}
        />
      )}
        </div>

      {meta && (
        <ModuleDetails
          meta={meta}
          params={params}
          setParams={setParams}
          onRun={handleRun}
        />
      )}
      {result && <ResultDisplay result={result} />}
    </>
  );
}

export default XcoreModules;

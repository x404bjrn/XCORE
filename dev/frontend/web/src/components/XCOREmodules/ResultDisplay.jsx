// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import { useRef } from 'react';
import { useTranslation } from "react-i18next";

const ResultDisplay = ({ result }) => {
  const textRef = useRef();
  const { t } = useTranslation("module");

  const handleCopy = () => {
    const content = textRef.current?.innerText;
    if (content) {
      navigator.clipboard.writeText(content);
    }
  };

  return (
    <div className="result-display highlight">
      <button className="copy-btn" onClick={handleCopy}>📋</button>
      <h2 className="glow">{t("result_display_title_h2")}</h2>
      <br />
      <pre ref={textRef}>
        {Array.isArray(result.output) ? result.output.join('\n') : result.output}
      </pre>
    </div>
  );
};

export default ResultDisplay;

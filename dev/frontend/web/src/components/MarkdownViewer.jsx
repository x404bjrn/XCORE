// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import React, { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";

const MarkdownViewer = ({ fileUrl }) => {
  const [content, setContent] = useState("");

  useEffect(() => {
    fetch(fileUrl)
      .then((res) => res.text())
      .then(setContent);
  }, [fileUrl]);

  return (
    <div className="markdown">
      <ReactMarkdown rehypePlugins={[rehypeRaw]}>
        {content}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownViewer;

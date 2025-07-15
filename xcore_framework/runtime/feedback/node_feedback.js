// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
const fs = require("fs");

function stripAnsi(str) {
  return str.replace(
    /[\u001b\u009b][[()#;?]*(?:[0-9]{1,4}(?:;[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]/g,
    ""
  );
}

function feedback(outputLines = [], result = {}, mode = "cli") {
  outputLines.forEach((line) => {
    console.log(line);

    const cleanLine = stripAnsi(line);

    if (mode === "web") {
      fs.appendFileSync("xcore_output_web.log", cleanLine + "\n");
    } else if (mode === "gui") {
      fs.appendFileSync("xcore_output_gui.log", cleanLine + "\n");
    }
  });

  if (mode === "web" && Object.keys(result).length > 0) {
    fs.appendFileSync("xcore_result_web.json", JSON.stringify(result) + "\n");
  }
}

module.exports = { feedback };

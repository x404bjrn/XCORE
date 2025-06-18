// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
const fs = require("fs");
const path = require("path");

// Navigiere aus dem `scripts`-Unterverzeichnis zum Wurzelverzeichnis
const rootDir = path.join(__dirname, "..");

// Pfade zur package.json und pyproject.toml
const packageJsonPath = path.join(rootDir, "package.json");
const setupPyPath = path.join(rootDir, "pyproject.toml");

// Lade Version aus package.json
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));
const newVersion = packageJson.version;

// Lies und aktualisiere pyproject.toml
const setupContent = fs.readFileSync(setupPyPath, "utf8");
const updatedSetupContent = setupContent.replace(
  /version="(\d+\.\d+\.\d+)"/,
  `version="${newVersion}"`
);

// Schreibe die Änderung zurück in pyproject.toml
fs.writeFileSync(setupPyPath, updatedSetupContent);

console.log(`Updated pyproject.toml to version ${newVersion}`);
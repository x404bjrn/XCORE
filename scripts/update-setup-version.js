// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
const fs = require("fs");
const path = require("path");

const rootDir = path.join(__dirname, "..");

const packageJsonPath = path.join(rootDir, "package.json");
const pyprojectPath = path.join(rootDir, "pyproject.toml");
const initFilePath = path.join(rootDir, "xcore_framework", "__init__.py");

const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));
const newVersion = packageJson.version;

// pyproject.toml aktualisieren
let pyproject = fs.readFileSync(pyprojectPath, "utf8");
pyproject = pyproject.replace(/version\s*=\s*"[^\"]+"/, `version = "${newVersion}"`);
fs.writeFileSync(pyprojectPath, pyproject);
console.log(`✅ pyproject.toml aktualisiert: ${newVersion}`);

// __init__.py aktualisieren
let initContent = fs.readFileSync(initFilePath, "utf8");
initContent = initContent.replace(/__version__\s*=\s*"[^\"]+"/, `__version__ = "${newVersion}"`);
fs.writeFileSync(initFilePath, initContent);
console.log(`✅ __init__.py aktualisiert: ${newVersion}`);

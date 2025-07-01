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
const footerPath = path.join(rootDir, "dev", "frontend", "web", "src", "Layout", "Footer.jsx");

const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));
const newVersion = packageJson.version;

// pyproject.toml aktualisieren
let pyproject = fs.readFileSync(pyprojectPath, "utf8");
pyproject = pyproject.replace(/version\s*=\s*"[^\"]+"/, `version = "${newVersion}"`);
fs.writeFileSync(pyprojectPath, pyproject);
console.log(`[+] pyproject.toml aktualisiert: ${newVersion}`);

// __init__.py aktualisieren
let initContent = fs.readFileSync(initFilePath, "utf8");
initContent = initContent.replace(/__version__\s*=\s*"[^\"]+"/, `__version__ = "${newVersion}"`);
fs.writeFileSync(initFilePath, initContent);
console.log(`[+] __init__.py aktualisiert: ${newVersion}`);

// Footer.jsx aktualisieren – gezielt nur bei Marker
let footerContent = fs.readFileSync(footerPath, "utf8");
const versionRegex = /({\/\* VERSION_AUTO_UPDATE \*\/}\s*<Link className="link" to="\/changelog">)v[^\<]+(<\/Link>)/;

if (versionRegex.test(footerContent)) {
  footerContent = footerContent.replace(
    versionRegex,
    `$1v${newVersion}$2`
  );
  fs.writeFileSync(footerPath, footerContent);
  console.log(`[+] Footer.jsx aktualisiert (v${newVersion})`);
} else {
  console.warn("[!]  Marker /* VERSION_AUTO_UPDATE */ nicht gefunden. Keine Änderung vorgenommen.");
}

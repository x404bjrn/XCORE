// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import header_logo from "@/assets/xcore-framework-logo.svg";

export default function Logo() {
  return (
    <div className="logo">
      <a href="/dashboard">
        <img
          src={header_logo}
          alt="XCORE Framework Navbar Logo"
          style={{ height: "3rem" }}
        />
      </a>
    </div>
  );
}

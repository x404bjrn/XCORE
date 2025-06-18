// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import { AuthContext } from "@/context/AuthContext";
import React, {useContext} from "react";
import Logo from "./Logo";

export default function Navbar() {
  const { logout } = useContext(AuthContext);

  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Links: Logo */}
        <div className="navbar-logo">
          <Logo />
        </div>

        <div className="navbar-actions">
          <a
            href="#"
            onClick={(e) => {
              e.preventDefault();
              logout();
            }}
            className="navbar-link"
            rel="noopener"
          >
            Logout
          </a>
        </div>
      </div>
    </nav>
  );
}

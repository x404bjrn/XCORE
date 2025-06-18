// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "@/context/AuthContext";

const Footer = () => {
  const { user, logout } = useContext(AuthContext);

  return (
    <footer className="footer">
      <div className="list">
        <div className="list-item">
          {/* TODO: Link auf Dokumentation hinzufügen */}
          <Link className="link" to="/documentation">
            XCORE Framework Documentation
          </Link>
          {/* TODO: Link auf Support hinzufügen */}
          <Link className="link" to="/support">
            Support
          </Link>
          {/* Bedingte Anzeige: Zeige Logout nur, wenn user eingeloggt ist */}
          {user && (
            <a
              href="#"
              onClick={(e) => {
                e.preventDefault();
                logout();
              }}
              className="link"
              rel="noopener"
            >
              Logout
            </a>
          )}
        </div>
        <div className="list-item">
          <span>
            <b>
            &copy; {new Date().getFullYear()}{" "}
            <a
              href="https://github.com/x404bjrn"
              className="list-item link-green"
              target="_blank"
              rel="noopener noreferrer"
            >
              Xeniorn | x404bjrn
            </a>
            . All rights reserved.
            </b>
          </span>
          {/* TODO: Link auf CHANGELOG hinzufügen */}
          <Link className="link" to="/changelog">
            v0.1.0
          </Link>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

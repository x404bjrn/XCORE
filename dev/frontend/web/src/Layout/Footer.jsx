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
          <Link className="link" to="/documentation">XCORE Framework Documentation</Link>

          <Link className="link" to="/contributing">Contributing</Link>

          {/* VERSION_AUTO_UPDATE */}
          <Link className="link" to="/changelog">v0.1.0a4</Link>

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
              className="link-green"
              target="_blank"
              rel="noopener noreferrer"
            >
              x404bjrn
            </a>
            </b>
          </span>

          <div className="link">
            &nbsp;&nbsp;
            <Link className="link" to="/license">
              <span style={{color: "white"}}>
                <b>MIT License – Use it, hack it, love it.</b>
              </span>
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

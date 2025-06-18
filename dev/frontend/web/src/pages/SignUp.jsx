// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import xcore_framework_logo from "@/assets/xcore-framework-logo.svg";

export default function SignUp() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (res.ok) {
      // Optional: Direkt einloggen oder zur Loginseite
      alert("Registrierung erfolgreich!");
      navigate("/");
      //navigate("/dashboard");
    } else {
      alert(data.error || "Registrierung fehlgeschlagen");
    }
  };

  return (
    <div className="modal hover-zoom">
      <div className="logo-container-xl">
        <img src={xcore_framework_logo} alt="Logo" className="logo"/>
      </div>
      <h1>Registrierung</h1>
      <form onSubmit={handleSubmit} method="POST">
        <div className="form-group">
          <label htmlFor="username">Benutzername</label>
          <input type="text" id="username" name="username" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Benutzername eingeben" required/>
        </div>
        <div className="form-group">
          <label htmlFor="password">Passwort</label>
          <input type="password" id="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Passwort eingeben" required/>
        </div>
        <button type="submit" className="button">Registrieren</button>
      </form>
      <div className="link">
        <Link to="/">Bereits registriert? Zum Login.</Link>
      </div>
    </div>
  );
}

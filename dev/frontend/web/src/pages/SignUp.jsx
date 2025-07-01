// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import xcore_framework_logo from "@/assets/xcore-framework-logo.svg";

export default function SignUp() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { t } = useTranslation("signup");

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
      alert(t("alert_register_success"));
      navigate("/");
      //navigate("/dashboard");
    } else {
      alert(data.error || t("alert_register_failed"));
    }
  };

  return (
    <div className="modal hover-zoom">
      <div className="logo-container-xl">
        <img src={xcore_framework_logo} alt="Logo" className="logo"/>
      </div>
      <h1>{t("title_h1")}</h1>
      <form onSubmit={handleSubmit} method="POST">
        <div className="form-group">
          <label htmlFor="username">{t("input_label_username")}</label>
          <input type="text" id="username" name="username" value={username} onChange={(e) => setUsername(e.target.value)} placeholder={t("input_label_username")} required/>
        </div>
        <div className="form-group">
          <label htmlFor="password">{t("input_label_password")}</label>
          <input type="password" id="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder={t("input_label_username")} required/>
        </div>
        <button type="submit" className="button">{t("btn_register")}</button>
      </form>
      <div className="link">
        <Link to="/">{t("link_to_login")}</Link>
      </div>
    </div>
  );
}

// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import {Link, useNavigate} from "react-router-dom";
import { useState, useContext } from "react";
import { AuthContext } from "@/context/AuthContext";
import xcore_logo from "@/assets/xcore-logo.svg";
import { useTranslation } from "react-i18next";

export default function SignIn() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const { t } = useTranslation("signin");

  const handleLogin = async (e) => {
    e.preventDefault();

    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ username, password }),
    });

    if (res.ok) {
      const userInfo = await fetch("/api/user", { credentials: "include" });
      const userData = await userInfo.json();
      login(
          userData.id,
          userData.username
      );
      navigate("/dashboard");
    } else {
      alert(t("alert_login_failed"));
    }
  };

  return (
    <div className="modal hover-zoom">
      <div className="logo-container">
        <img src={xcore_logo} alt="Logo" className="logo" />
      </div>
      <h1>{t("title_h1")}</h1>
      <form onSubmit={handleLogin} method="POST">
        <div className="form-group">
          <label htmlFor="username">{t("input_label_username")}</label>
          <input type="text" id="username" name="username" value={username} onChange={(e) => setUsername(e.target.value)} placeholder={t("input_placeholder_username")} required/>
        </div>
        <div className="form-group">
          <label htmlFor="password">{t("input_label_password")}</label>
          <input type="password" id="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder={t("input_placeholder_password")} required/>
        </div>
        <button type="submit" className="button">{t("btn_login")}</button>
        <div className="link">
          <Link to="/sign-up">{t("link_to_register")}</Link>
        </div>
      </form>
    </div>
  );
}

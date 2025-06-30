// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import { Routes, Route } from "react-router-dom";
import { useTranslation } from "react-i18next";

import Layout from "@/Layout/Layout";
import SignIn from "@/pages/SignIn";
import React, {Suspense, useEffect} from "react";

// Dynamische Importe
const Dashboard = React.lazy(() => import("@/pages/Dashboard"));
const SignUp = React.lazy(() => import("@/pages/SignUp"));
const MarkdownViewer = React.lazy(() => import("@/components/MarkdownViewer"));

// Route Wrapper für Dateinamen Definitionen je nach Systemsprache
// Dokumentation
function DocumentationRouteWrapper() {
  const { i18n } = useTranslation();
  const fileMap = {
    de: "/static/DOCUMENTATION_DE.md",
    en: "/static/DOCUMENTATION_EN.md",
  };
  const fileUrl = fileMap[i18n.language] || fileMap["de"];

  return <MarkdownViewer fileUrl={fileUrl} />;
}

// Contributing
function ContributingRouteWrapper() {
  const { i18n } = useTranslation();
  const fileMap = {
    de: "/static/CONTRIBUTING.md",
    en: "/static/CONTRIBUTING_EN.md",
  };
  const fileUrl = fileMap[i18n.language] || fileMap["de"];

  return <MarkdownViewer fileUrl={fileUrl} />;
}

function App() {
    const { i18n } = useTranslation();

    useEffect(() => {
      fetch("/api/config", { credentials: "include" })
        .then(res => res.json())
        .then(cfg => {
          if (cfg.lang) {
            i18n.changeLanguage(cfg.lang); // Sprache dynamisch setzen
          }
        });
    }, [i18n]);

    return (
        <Routes>
            <Route element={<Layout />}>
                <Route path="/" element={<SignIn />} />
                <Route
                    path="/sign-up"
                    element={
                        <Suspense fallback={<div>{i18n.t("load", {}, { ns: "base" })}</div>}>
                            <SignUp />
                        </Suspense>
                    }
                />
                <Route
                    path="/dashboard"
                    element={
                        <Suspense fallback={<div>{i18n.t("load", {}, { ns: "base" })}</div>}>
                            <Dashboard />
                        </Suspense>
                    }
                />
                <Route
                    path="/contributing"
                    element={
                        <Suspense fallback={<div>{i18n.t("load", {}, { ns: "base" })}</div>}>
                            <ContributingRouteWrapper />
                        </Suspense>
                    }
                />
                <Route
                    path="/changelog"
                    element={
                        <Suspense fallback={<div>{i18n.t("load", {}, { ns: "base" })}</div>}>
                            <MarkdownViewer fileUrl="/static/CHANGELOG.md" />
                        </Suspense>
                    }
                />
                <Route
                    path="/documentation"
                    element={
                        <Suspense fallback={<div>{i18n.t("load", {}, { ns: "base" })}</div>}>
                            <DocumentationRouteWrapper />
                        </Suspense>
                    }
                />
                <Route
                    path="/license"
                    element={
                        <Suspense fallback={<div>{i18n.t("load", {}, { ns: "base" })}</div>}>
                            <MarkdownViewer fileUrl="/static/LICENSE" />
                        </Suspense>
                    }
                />
            </Route>
        </Routes>
    );
}

export default App;

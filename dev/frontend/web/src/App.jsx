// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import {  Routes, Route } from "react-router-dom";
import Layout from "@/Layout/Layout";
import MarkdownViewer from "@/components/MarkdownViewer";
import SignIn from "@/pages/SignIn";
import SignUp from "@/pages/SignUp";
import Dashboard from "@/pages/Dashboard";

function App() {
    return (
        <Routes>
            <Route element={<Layout />}>
                <Route path="/" element={<SignIn />} />
                <Route path="/sign-up" element={<SignUp />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/contributing" element={<MarkdownViewer fileUrl="/CONTRIBUTING.md" />} />
                <Route path="/changelog" element={<MarkdownViewer fileUrl="/CHANGELOG.md" />} />
                <Route path="/documentation" element={<MarkdownViewer fileUrl="/DOCUMENTATION_DE.md" />} />
                <Route path="/license" element={<MarkdownViewer fileUrl="/LICENSE" />} />
            </Route>
        </Routes>
    );
}

export default App;

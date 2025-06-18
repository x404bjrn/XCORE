// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import {  Routes, Route } from "react-router-dom";
import Layout from "@/Layout/Layout";
import Support from "@/pages/Support";
import Changelog from "@/pages/Changelog";
import Documentation from "@/pages/Documentation";
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
                <Route path="/support" element={<Support />} />
                <Route path="/changelog" element={<Changelog />} />
                <Route path="/documentation" element={<Documentation />} />
            </Route>
        </Routes>
    );
}

export default App;

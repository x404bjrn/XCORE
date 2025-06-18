// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import { Outlet } from "react-router-dom";
import Footer from "@/Layout/Footer";

export default function Layout() {
    return (
        <div className="main-container">
            {/* MAIN */}
            <main>
                <Outlet />
            </main>
            {/* FOOTER */}
            <Footer />
        </div>
    );
}

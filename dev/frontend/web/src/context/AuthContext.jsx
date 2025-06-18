// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import { createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

// eslint-disable-next-line react-refresh/only-export-components
export const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);  // Enthält alle User-Infos
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        fetch("/api/user", {
            credentials: "include",
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.logged_in) {
                    // Speichere alle relevanten Daten im User-State
                    setUser({
                        id: data.id,
                        username: data.username
                    });
                } else {
                    setUser(null);
                }
                setLoading(false);
            });
    }, []);

    const login = (id, username) => {
        // Aktualisierung mit allen Werten
        setUser({ id, username });
    };

    const logout = async () => {
        await fetch("/api/logout", {
            method: "GET",
            credentials: "include",
        });
        setUser(null);
        navigate("/"); // ← zurück zur Login-Seite
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
}

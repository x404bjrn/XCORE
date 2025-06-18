// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
// TODO: Theme-Context in Webinterface einarbeiten - Mit ThemeToggler das wechseln von Themes ermöglichen
import { useContext } from 'react';
import { ThemeContext } from '@/context/ThemeContext.jsx';
import { Moon, Sun } from 'lucide-react';

const ThemeToggleButton = () => {
  const { theme, toggleTheme } = useContext(ThemeContext);
  const isDark = theme === 'xcore-green';

  return (
    <button
      className="theme-toggler-btn m-3"
      onClick={toggleTheme}
      title={`Wechsle zu ${isDark ? 'xcore-purple' : 'xcore-green'} Theme`}
    >
      {isDark ? <Sun size={18} /> : <Moon size={18} />}
    </button>
  );
};

export default ThemeToggleButton;

// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import React, { useEffect, useState } from "react";
import axios from "axios";
import Navbar from "@/components/Navbar/Navbar";
import Sidelist from "@/components/Sidebar/Sidelist";
import XcoreModules from "@/components/XCOREmodules/XcoreModules";

export default function Dashboard() {
  const [modules, setModules] = useState({});
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedModule, setSelectedModule] = useState('');

  useEffect(() => {
    axios.get('/api/modules').then(res => setModules(res.data));
  }, []);

  return (
    <div className="dashboard-layout">
      <Navbar />
      <div className="content-area">
        <div className="sidelist-wrapper">
          <Sidelist
            modules={modules}
            selectedCategory={selectedCategory}
            onModuleSelect={setSelectedModule}
          />
        </div>
        <div className="main-form module-wrapper">
          <XcoreModules
            modules={modules}
            selectedCategory={selectedCategory}
            onCategoryChange={setSelectedCategory}
            selectedModule={selectedModule}
            onModuleChange={setSelectedModule}
          />
        </div>
      </div>
    </div>
  );
}

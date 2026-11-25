import React, { useState } from "react";
import { Navbar } from "./components/Navbar";
import { WorkerPortal } from "./components/WorkerPortal/WorkerPortal";
import { Dashboard } from "./components/ManagementDashboard/Dashboard";
import { WhatsAppSimulator } from "./components/WhatsAppSimulator/WhatsAppSimulator";
import { LanguageProvider } from "./context/LanguageContext";
import { Wifi, BatteryMedium } from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState("worker");
  const [isLowPowerMode, setIsLowPowerMode] = useState(false);

  return (
    <LanguageProvider>
      <div className="min-h-screen bg-slate-100 flex flex-col font-sans selection:bg-amber-300 selection:text-slate-950">
        <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

        <aside aria-label="Device connectivity status" className="bg-slate-950 text-slate-400 text-[11px] font-semibold px-4 py-1 border-b border-slate-800">
          <div className="max-w-5xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="flex items-center gap-1 text-emerald-400">
                <Wifi className="w-3.5 h-3.5" />
                <span>4G Factory Network (Active)</span>
              </span>
              <span className="hidden sm:inline text-slate-600">|</span>
              <span className="hidden sm:inline text-slate-400">Shop Floor Zone 4 Hub</span>
            </div>

            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => setIsLowPowerMode(!isLowPowerMode)}
                className={`flex items-center gap-1 px-1.5 py-0.5 rounded transition ${
                  isLowPowerMode ? "bg-amber-400 text-slate-950 font-bold" : "hover:text-slate-200"
                }`}
              >
                <BatteryMedium className="w-3.5 h-3.5" />
                <span>Low-Power Mode: {isLowPowerMode ? "ON" : "OFF"}</span>
              </button>
            </div>
          </div>
        </aside>

        <main className="flex-1">
          {activeTab === "worker" && <WorkerPortal isLowPowerMode={isLowPowerMode} />}
          {activeTab === "dashboard" && <Dashboard />}
          {activeTab === "whatsapp" && <WhatsAppSimulator />}
        </main>

        <footer className="bg-slate-900 text-slate-400 text-xs py-4 px-4 text-center border-t border-slate-800">
          <p className="font-semibold">
            ShiftMitra AI &copy; 2026 – Multilingual Factory Worker Companion & Accountability Engine.
          </p>
        </footer>
      </div>
    </LanguageProvider>
  );
}

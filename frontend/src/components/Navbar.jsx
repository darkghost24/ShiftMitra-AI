import React from "react";
import { useLanguage } from "../context/LanguageContext";
import { HardHat, BarChart3, MessageSquare, Globe } from "lucide-react";

export const Navbar = ({ activeTab, setActiveTab }) => {
  const { lang, setLang, t } = useLanguage();

  return (
    <header className="sticky top-0 z-50 bg-slate-900 text-white shadow-md">
      <div className="max-w-5xl mx-auto px-4 py-2.5 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center space-x-2">
          <div className="bg-amber-500 p-1.5 rounded-lg text-slate-900 font-bold">
            <HardHat className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-1.5">
              ShiftMitra <span className="text-xs bg-amber-400 text-slate-900 px-1.5 py-0.5 rounded font-bold">AI</span>
            </h1>
            <p className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Factory Voice Companion</p>
          </div>
        </div>

        <div className="flex items-center space-x-1 bg-slate-800 p-1 rounded-xl">
          <button
            onClick={() => setActiveTab("worker")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
              activeTab === "worker" ? "bg-amber-500 text-slate-900 shadow" : "text-slate-300 hover:text-white"
            }`}
          >
            <HardHat className="w-4 h-4" />
            <span className="hidden sm:inline">{t.workerTab}</span>
            <span className="sm:hidden">Worker</span>
          </button>
          <button
            onClick={() => setActiveTab("dashboard")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
              activeTab === "dashboard" ? "bg-amber-500 text-slate-900 shadow" : "text-slate-300 hover:text-white"
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            <span className="hidden sm:inline">{t.dashboardTab}</span>
            <span className="sm:hidden">Dashboard</span>
          </button>
          <button
            onClick={() => setActiveTab("whatsapp")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
              activeTab === "whatsapp" ? "bg-emerald-500 text-white shadow" : "text-slate-300 hover:text-white"
            }`}
          >
            <MessageSquare className="w-4 h-4" />
            <span>WhatsApp</span>
          </button>
        </div>

        <div className="flex items-center space-x-1 text-xs">
          <Globe className="w-4 h-4 text-slate-400 mr-1" />
          {["hi", "bn", "en"].map((l) => (
            <button
              key={l}
              onClick={() => setLang(l)}
              className={`px-2 py-1 rounded font-bold uppercase transition ${
                lang === l ? "bg-amber-400 text-slate-950 font-black" : "text-slate-300 hover:bg-slate-800"
              }`}
            >
              {l === "hi" ? "हिन्दी" : l === "bn" ? "বাংলা" : "ENG"}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
};

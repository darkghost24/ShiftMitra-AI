import React, { useEffect, useState, useMemo } from "react";
import { AlertOctagon, CheckCircle2, FileText, Users, RefreshCw, Filter } from "lucide-react";
import { AnalyticsCharts } from "./AnalyticsCharts";
import { MisunderstoodTopicsTable } from "./MisunderstoodTopicsTable";

export const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedLanguage, setSelectedLanguage] = useState("all");

  const fetchSummary = async () => {
    try {
      const res = await fetch("/api/analytics/summary");
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error("Dashboard Fetch Error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSummary();
    const interval = setInterval(fetchSummary, 6000);
    return () => clearInterval(interval);
  }, []);

  const filteredEvents = useMemo(() => {
    if (!data?.recentEvents) return [];
    return data.recentEvents.filter((ev) => {
      if (selectedLanguage !== "all" && ev.language !== selectedLanguage) return false;
      return true;
    });
  }, [data, selectedLanguage]);

  if (loading || !data) {
    return (
      <div className="p-16 text-center text-slate-500 flex flex-col items-center justify-center gap-3">
        <RefreshCw className="w-8 h-8 animate-spin text-amber-500" />
        <span className="font-bold text-sm text-slate-700">फैक्ट्री डेटा लोड हो रहा है...</span>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Live Factory Monitoring</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight mt-0.5">
            Confusion Logging Dashboard
          </h2>
          <p className="text-xs sm:text-sm text-slate-500">
            Real-time verified comprehension analytics across safety mandates, notices, and payslips
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center gap-1.5 bg-white border border-slate-300 rounded-xl px-2.5 py-1.5 shadow-2xs">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="text-xs font-bold text-slate-800 bg-transparent focus:outline-none cursor-pointer"
            >
              <option value="all">All Languages</option>
              <option value="hi">Hindi (हिन्दी)</option>
              <option value="bn">Bengali (বাংলা)</option>
              <option value="en">English</option>
            </select>
          </div>

          <button
            type="button"
            onClick={fetchSummary}
            className="flex items-center gap-1.5 text-xs font-bold bg-white border border-slate-300 px-3 py-2 rounded-xl shadow-2xs hover:bg-slate-50 text-slate-800 transition active:scale-95"
          >
            <RefreshCw className="w-3.5 h-3.5 text-slate-600" />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3.5 mb-6">
        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs">
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider">Total Scans</div>
          <div className="text-3xl font-black text-slate-900 mt-1.5 flex items-center justify-between">
            {data.totalProcessed}
            <div className="p-2 bg-amber-50 rounded-xl text-amber-600">
              <FileText className="w-5 h-5" />
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs">
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider">Confusion Rate</div>
          <div className="text-3xl font-black text-rose-600 mt-1.5 flex items-center justify-between">
            {data.confusionRate}%
            <div className="p-2 bg-rose-50 rounded-xl text-rose-600">
              <AlertOctagon className="w-5 h-5" />
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs">
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider">First-Time Pass</div>
          <div className="text-3xl font-black text-emerald-600 mt-1.5 flex items-center justify-between">
            {100 - data.confusionRate}%
            <div className="p-2 bg-emerald-50 rounded-xl text-emerald-600">
              <CheckCircle2 className="w-5 h-5" />
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs">
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider">Active Dialects</div>
          <div className="text-3xl font-black text-blue-600 mt-1.5 flex items-center justify-between">
            {Object.keys(data.languageBreakdown || {}).length}
            <div className="p-2 bg-blue-50 rounded-xl text-blue-600">
              <Users className="w-5 h-5" />
            </div>
          </div>
        </div>
      </div>

      <AnalyticsCharts data={data} />
      <MisunderstoodTopicsTable topics={data.topMisunderstoodTopics} recentEvents={filteredEvents} />
    </div>
  );
};

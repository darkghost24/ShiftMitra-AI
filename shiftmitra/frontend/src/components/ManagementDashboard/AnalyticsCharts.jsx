import React from "react";

export const AnalyticsCharts = ({ data }) => {
  const docTypes = Object.entries(data.docTypeBreakdown || {});
  const languages = Object.entries(data.languageBreakdown || {});

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
        <h3 className="font-bold text-slate-800 text-sm mb-4">
          दस्तावेज़ प्रकार और भ्रम दर (Docs Processed vs Clarified)
        </h3>
        <div className="space-y-3">
          {docTypes.map(([type, total]) => {
            const confused = (data.docTypeConfusion && data.docTypeConfusion[type]) || 0;
            const pct = total > 0 ? Math.round((confused / total) * 100) : 0;
            return (
              <div key={type}>
                <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                  <span>{type}</span>
                  <span>{total} docs ({pct}% confused)</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden flex">
                  <div
                    className="bg-emerald-500 h-full"
                    style={{ width: `${100 - pct}%` }}
                    title="Understood"
                  />
                  <div
                    className="bg-rose-500 h-full"
                    style={{ width: `${pct}%` }}
                    title="Needed Clarification"
                  />
                </div>
              </div>
            );
          })}
        </div>
        <div className="flex gap-4 text-[11px] font-bold text-slate-500 mt-4">
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 bg-emerald-500 rounded-full"></span> Understood
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 bg-rose-500 rounded-full"></span> Needed Clarification
          </span>
        </div>
      </div>

      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
        <h3 className="font-bold text-slate-800 text-sm mb-4">
          भाषा उपयोग विश्लेषण (Worker Language Distribution)
        </h3>
        <div className="flex items-center justify-around h-36">
          {languages.map(([langCode, count]) => {
            const langLabel = langCode === "hi" ? "Hindi" : langCode === "bn" ? "Bengali" : "English";
            const color = langCode === "hi" ? "bg-amber-400 text-slate-900" : langCode === "bn" ? "bg-sky-500 text-white" : "bg-purple-500 text-white";
            return (
              <div key={langCode} className="text-center">
                <div className={`w-16 h-16 rounded-2xl mx-auto flex items-center justify-center font-black text-xl shadow-sm ${color}`}>
                  {count}
                </div>
                <span className="text-xs font-bold text-slate-700 block mt-2">{langLabel}</span>
                <span className="text-[10px] text-slate-400">workers queried</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

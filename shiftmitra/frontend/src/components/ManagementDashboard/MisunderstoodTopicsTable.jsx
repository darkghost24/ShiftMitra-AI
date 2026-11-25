import React from "react";
import { AlertTriangle, Download } from "lucide-react";

export const MisunderstoodTopicsTable = ({ topics = [], recentEvents = [] }) => {
  const exportCsv = () => {
    let csvContent = "data:text/csv;charset=utf-8,ID,DocumentType,Language,ClarificationNeeded,MissedPoints,Timestamp\n";
    recentEvents.forEach((ev) => {
      csvContent += `${ev.id},"${ev.documentType}",${ev.language},${ev.clarificationNeeded},"${(ev.missedPoints || []).join(";")}",${ev.timestamp}\n`;
    });
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `shiftmitra_confusion_report_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-bold text-slate-900 text-base">Top Misunderstood Worker Topics</h3>
          <p className="text-xs text-slate-500">Aggregated from Explain-Back comprehension checks</p>
        </div>
        <button
          onClick={exportCsv}
          className="flex items-center gap-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold px-3 py-2 rounded-xl transition"
        >
          <Download className="w-4 h-4" />
          <span>Export CSV</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="border border-slate-200 rounded-xl overflow-hidden">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 font-bold uppercase text-[10px] border-b border-slate-200">
              <tr>
                <th className="p-3">Topic / Rule</th>
                <th className="p-3 text-right">Workers Confused</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {topics.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50">
                  <td className="p-3 font-semibold text-slate-800 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0" />
                    <span className="capitalize">{item.topic.replace("_", " ")}</span>
                  </td>
                  <td className="p-3 text-right font-bold text-rose-600">{item.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="border border-slate-200 rounded-xl overflow-hidden">
          <div className="bg-slate-50 p-2.5 text-[11px] font-bold uppercase text-slate-500 border-b border-slate-200">
            Recent Explain-Back Verifications
          </div>
          <div className="divide-y divide-slate-100 max-h-56 overflow-y-auto">
            {recentEvents.map((ev) => (
              <div key={ev.id} className="p-2.5 flex items-center justify-between text-xs">
                <div>
                  <span className="font-bold text-slate-800">{ev.documentType}</span>
                  <span className="ml-2 text-[10px] uppercase font-semibold text-slate-400">({ev.language})</span>
                </div>
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-black uppercase ${
                    ev.clarificationNeeded ? "bg-rose-100 text-rose-700" : "bg-emerald-100 text-emerald-700"
                  }`}
                >
                  {ev.clarificationNeeded ? "Clarified" : "Understood"}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

import React, { useState, useEffect } from "react";
import { DocumentCapture } from "./DocumentCapture";
import { ExplanationCard } from "./ExplanationCard";
import { ExplainBackLoop } from "./ExplainBackLoop";
import { History, Clock, FileText, ChevronRight, Trash2 } from "lucide-react";
import { useLanguage } from "../../context/LanguageContext";

export const WorkerPortal = () => {
  const { t } = useLanguage();
  const [currentDoc, setCurrentDoc] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    try {
      const saved = localStorage.getItem("shiftmitra_doc_history");
      if (saved) setHistory(JSON.parse(saved));
    } catch (e) {
      console.warn("Could not load history:", e);
    }
  }, []);

  const handleDocumentProcessed = (newDoc) => {
    setCurrentDoc(newDoc);
    setHistory((prevHistory) => {
      const updated = [
        {
          ...newDoc,
          savedAt: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
        },
        ...prevHistory.filter((item) => item.id !== newDoc.id)
      ].slice(0, 8);

      try {
        localStorage.setItem("shiftmitra_doc_history", JSON.stringify(updated));
      } catch (e) {
        console.warn("Could not save history:", e);
      }
      return updated;
    });
  };

  const handleSelectHistoricalDoc = (historicalDoc) => {
    setCurrentDoc(historicalDoc);
    setShowHistory(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleClearHistory = () => {
    setHistory([]);
    localStorage.removeItem("shiftmitra_doc_history");
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-6">
      <DocumentCapture
        onDocumentProcessed={handleDocumentProcessed}
        loading={loading}
        setLoading={setLoading}
      />

      {currentDoc ? (
        <section aria-label="Current document explanation">
          <ExplanationCard doc={currentDoc} />
          <ExplainBackLoop doc={currentDoc} />
        </section>
      ) : (
        !loading && (
          <div className="bg-white/80 border border-dashed border-slate-300 rounded-2xl p-8 text-center text-slate-500 mb-6">
            <FileText className="w-12 h-12 text-slate-300 mx-auto mb-2" />
            <h3 className="text-base font-bold text-slate-700">कोई दस्तावेज़ नहीं चुना गया</h3>
            <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
              ऊपर दिए गए बटन से नोटिस की फोटो लें या तुरंत जांचने के लिए एक नमूना दस्तावेज़ चुनें।
            </p>
          </div>
        )
      )}

      {history.length > 0 && (
        <section className="mt-8 border-t border-slate-200 pt-6">
          <div className="flex items-center justify-between mb-3">
            <button
              type="button"
              onClick={() => setShowHistory(!showHistory)}
              className="flex items-center gap-2 text-sm font-bold text-slate-800 hover:text-amber-600 transition"
            >
              <History className="w-4 h-4 text-amber-500" />
              <span>{t.history || "पुराने दस्तावेज़"} ({history.length})</span>
              <ChevronRight className={`w-4 h-4 transition-transform ${showHistory ? "rotate-90" : ""}`} />
            </button>

            {showHistory && (
              <button
                type="button"
                onClick={handleClearHistory}
                className="text-xs font-semibold text-rose-600 hover:text-rose-700 flex items-center gap-1 transition"
              >
                <Trash2 className="w-3.5 h-3.5" />
                <span>साफ करें (Clear)</span>
              </button>
            )}
          </div>

          {showHistory && (
            <div className="space-y-2 bg-slate-50 p-3 rounded-2xl border border-slate-200">
              {history.map((docItem, idx) => (
                <button
                  key={docItem.id || idx}
                  type="button"
                  onClick={() => handleSelectHistoricalDoc(docItem)}
                  className="w-full text-left bg-white hover:bg-amber-50/60 p-3 rounded-xl border border-slate-200 shadow-2xs flex items-center justify-between gap-3 transition"
                >
                  <div className="flex-1 min-w-0">
                    <span className="text-[10px] font-black uppercase text-amber-700 bg-amber-100 px-2 py-0.5 rounded-md inline-block mb-1">
                      {docItem.category}
                    </span>
                    <h4 className="text-xs font-bold text-slate-900 truncate">
                      {docItem.title}
                    </h4>
                    <p className="text-[11px] text-slate-500 truncate mt-0.5">
                      {docItem.short_summary}
                    </p>
                  </div>
                  <div className="text-right text-[10px] text-slate-400 font-semibold shrink-0 flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    <span>{docItem.savedAt || "हाल ही में"}</span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </section>
      )}
    </div>
  );
};

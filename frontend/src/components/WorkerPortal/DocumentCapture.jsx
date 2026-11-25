import React, { useRef, useState } from "react";
import { Camera, Sparkles, UploadCloud, RefreshCw } from "lucide-react";
import { useLanguage } from "../../context/LanguageContext";

const PRESETS = [
  {
    id: "helmet-safety",
    name: "Safety Helmet & Fine Notice",
    rawHint: "SAFETY NOTICE ZONE 4: All workers must wear ISI helmets. Penalty Rs 500 for first violation."
  },
  {
    id: "oct-payslip",
    name: "Monthly Payslip & OT Breakdown",
    rawHint: "MONTHLY PAYSLIP: Gross Rs 18,350. Basic 14500, Overtime 28hrs Rs 3850. Deductions PF 1740, Mess 650. Net 15822."
  }
];

export const DocumentCapture = ({ onDocumentProcessed, loading, setLoading }) => {
  const { lang, t } = useLanguage();
  const fileInputRef = useRef(null);
  const [selectedFileName, setSelectedFileName] = useState("");

  const triggerUpload = async (file, textHint = "") => {
    setLoading(true);
    try {
      const formData = new FormData();
      if (file) formData.append("image", file);
      formData.append("targetLang", lang);
      formData.append("textHint", textHint);

      const response = await fetch("/api/documents/interpret", {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      if (data.success) {
        onDocumentProcessed(data.explanation);
      } else {
        alert("Could not process notice. Please try again.");
      }
    } catch (err) {
      console.error(err);
      alert("Network error. Backend might be starting up.");
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFileName(file.name);
      triggerUpload(file);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-5 mb-4">
      <h2 className="text-lg font-bold text-slate-800 mb-1 flex items-center gap-2">
        <Camera className="w-5 h-5 text-amber-500" />
        {t.takePhoto}
      </h2>
      <p className="text-xs text-slate-500 mb-4">
        कैमरा से फोटो खींचें या नीचे दिए गए नमूना नोटिस को चुनकर देखें
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={loading}
          className="flex items-center justify-center gap-3 bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-4 px-4 rounded-xl shadow-md active:scale-98 transition text-base"
        >
          {loading ? (
            <RefreshCw className="w-6 h-6 animate-spin text-slate-950" />
          ) : (
            <Camera className="w-6 h-6 text-slate-950" />
          )}
          <span>{loading ? "पहचान हो रही है..." : "फोटो लें या अपलोड करें"}</span>
        </button>

        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept="image/*"
          capture="environment"
          className="hidden"
        />

        <div className="flex flex-col gap-1 justify-center bg-slate-50 border border-slate-200 rounded-xl p-2.5">
          <span className="text-[11px] font-bold uppercase text-slate-400 tracking-wider flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-amber-500" /> तुरंत टेस्ट के लिए नमूना चुनें:
          </span>
          <div className="flex gap-1.5 mt-1">
            {PRESETS.map((p) => (
              <button
                key={p.id}
                onClick={() => triggerUpload(null, p.rawHint)}
                disabled={loading}
                className="flex-1 bg-white hover:bg-slate-100 border border-slate-300 text-slate-800 text-xs py-2 px-2 rounded-lg font-semibold text-left leading-tight truncate shadow-xs transition"
              >
                {p.name}
              </button>
            ))}
          </div>
        </div>
      </div>

      {selectedFileName && (
        <div className="text-xs text-emerald-700 bg-emerald-50 p-2 rounded-lg border border-emerald-200 flex items-center gap-2">
          <UploadCloud className="w-4 h-4" />
          फ़ाइल चुनी गई: <strong>{selectedFileName}</strong>
        </div>
      )}
    </div>
  );
};

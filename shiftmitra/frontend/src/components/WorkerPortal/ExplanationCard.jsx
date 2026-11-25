import React, { useState, useEffect } from "react";
import { Volume2, VolumeX, RotateCcw, CheckCircle2, Gauge, Sparkles, Info } from "lucide-react";
import { IconBadge } from "./IconBadge";
import { speakText, stopSpeech } from "../../utils/speechHelper";
import { useLanguage } from "../../context/LanguageContext";

export const ExplanationCard = ({ doc }) => {
  const { lang, t } = useLanguage();
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(0.9);

  useEffect(() => {
    stopSpeech();
    setIsPlaying(false);
  }, [doc, lang]);

  const handleToggleSpeech = () => {
    if (isPlaying) {
      stopSpeech();
      setIsPlaying(false);
    } else {
      setIsPlaying(true);
      speakText(doc.speech_script, lang, () => setIsPlaying(false));
    }
  };

  const handleReplay = () => {
    stopSpeech();
    setIsPlaying(true);
    speakText(doc.speech_script, lang, () => setIsPlaying(false));
  };

  const toggleSpeed = () => {
    const nextSpeed = playbackSpeed === 0.9 ? 1.1 : playbackSpeed === 1.1 ? 0.75 : 0.9;
    setPlaybackSpeed(nextSpeed);
    if (isPlaying) {
      stopSpeech();
      setIsPlaying(true);
      speakText(doc.speech_script, lang, () => setIsPlaying(false));
    }
  };

  if (!doc) return null;

  return (
    <article className="bg-white rounded-2xl shadow-md border-2 border-amber-300 overflow-hidden mb-6 transition-all">
      <header className="bg-gradient-to-r from-amber-500 via-amber-500 to-amber-600 px-5 py-4 text-slate-950">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex-1 min-w-[240px]">
            <div className="inline-flex items-center gap-1.5 bg-slate-950 text-amber-400 text-[11px] font-black uppercase tracking-wider px-2.5 py-0.5 rounded-full mb-1">
              <Sparkles className="w-3 h-3 text-amber-400" />
              <span>{doc.category || "Official Document"}</span>
            </div>
            <h2 className="text-xl sm:text-2xl font-black text-slate-950 leading-tight">
              {doc.title}
            </h2>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={toggleSpeed}
              title="Change audio playback speed"
              className="bg-amber-400/80 hover:bg-amber-400 text-slate-950 border border-slate-950/20 px-2.5 py-2 rounded-xl text-xs font-bold flex items-center gap-1 transition"
            >
              <Gauge className="w-3.5 h-3.5" />
              <span>{playbackSpeed}x</span>
            </button>

            {isPlaying && (
              <button
                type="button"
                onClick={handleReplay}
                title="Replay Audio"
                className="bg-slate-900 hover:bg-slate-800 text-white p-2.5 rounded-xl text-xs font-bold transition shadow"
              >
                <RotateCcw className="w-4 h-4 text-amber-400" />
              </button>
            )}

            <button
              type="button"
              onClick={handleToggleSpeech}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-xl font-black text-sm shadow-md transition active:scale-95 ${
                isPlaying ? "bg-rose-600 text-white animate-pulse" : "bg-slate-950 text-white hover:bg-slate-900"
              }`}
            >
              {isPlaying ? (
                <>
                  <VolumeX className="w-5 h-5 text-rose-200" />
                  <span>रोकें (Stop)</span>
                </>
              ) : (
                <>
                  <Volume2 className="w-5 h-5 text-amber-400" />
                  <span>{t.listenAudio || "आवाज़ में सुनें"}</span>
                </>
              )}
            </button>
          </div>
        </div>
      </header>

      <div className="p-5">
        <section aria-label="Plain language summary" className="bg-amber-50/90 border-l-4 border-amber-500 p-4 rounded-r-xl mb-6 shadow-xs">
          <div className="flex items-center gap-1.5 text-amber-800 font-bold text-xs uppercase tracking-wider mb-1">
            <Info className="w-4 h-4 text-amber-600" />
            <span>सीधे शब्दों में (Summary)</span>
          </div>
          <p className="text-slate-900 font-bold text-base sm:text-lg leading-relaxed">
            {doc.short_summary}
          </p>
        </section>

        <section aria-label="Key notice points">
          <h3 className="text-xs font-bold uppercase text-slate-400 tracking-wider mb-3">
            मुख्य बातें (Icon-Based Breakdown)
          </h3>
          <div className="space-y-3 mb-6">
            {(doc.key_points || []).map((point, index) => {
              const borderTheme =
                point.type === "danger"
                  ? "bg-rose-50/80 border-rose-200"
                  : point.type === "warning"
                  ? "bg-amber-50/80 border-amber-200"
                  : "bg-emerald-50/80 border-emerald-200";

              return (
                <div key={index} className={`flex items-start gap-3.5 p-3.5 rounded-xl border transition ${borderTheme}`}>
                  <div className="p-2.5 bg-white rounded-xl shadow-xs mt-0.5 shrink-0 border border-slate-100">
                    <IconBadge iconType={point.icon} className="w-6 h-6" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-bold text-slate-900 text-sm sm:text-base leading-snug">
                      {point.title}
                    </h4>
                    <p className="text-xs sm:text-sm text-slate-700 mt-1 leading-relaxed font-medium">
                      {point.desc}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {doc.action_item && (
          <footer className="bg-slate-950 text-white p-4 rounded-xl flex items-start sm:items-center gap-3.5 shadow-xs">
            <div className="p-2 bg-emerald-500/20 text-emerald-400 rounded-lg shrink-0 mt-0.5 sm:mt-0">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <div>
              <span className="text-[11px] font-black uppercase tracking-wider text-amber-400 block mb-0.5">
                {t.actionHeader || "आपको क्या करना है (Action Required):"}
              </span>
              <p className="text-sm sm:text-base font-bold text-slate-100">
                {doc.action_item}
              </p>
            </div>
          </footer>
        )}
      </div>
    </article>
  );
};

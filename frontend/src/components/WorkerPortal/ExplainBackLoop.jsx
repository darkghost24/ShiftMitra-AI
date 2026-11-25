import React, { useState } from "react";
import { Mic, MicOff, CheckCircle, AlertCircle, RefreshCw, Sparkles, Volume2 } from "lucide-react";
import { useLanguage } from "../../context/LanguageContext";
import { speakText } from "../../utils/speechHelper";

export const ExplainBackLoop = ({ doc }) => {
  const { lang, t } = useLanguage();
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [evaluation, setEvaluation] = useState(null);
  const [evaluating, setEvaluating] = useState(false);

  const sampleAnswers = [
    {
      label: "Correct Response",
      text: lang === "hi" 
        ? "अगर ज़ोन 4 में हेलमेट और सेफ्टी जूते नहीं पहने तो 500 रुपये कटेंगे और दोबारा गलती पर 3 दिन काम बंद रहेगा।" 
        : "জোন ৪-এ হেলমেট আর জুতো না পরলে ৫০০ টাকা ফাইন আর পরে ৩ দিনের সাসপেনশন হবে।"
    },
    {
      label: "Confused / Incomplete",
      text: lang === "hi" 
        ? "मुझे लगा सिर्फ पीला हेलमेट पहनना है, पैसे कटने की बात नहीं पता।" 
        : "আমি ভেবেছিলাম শুধু হেলমেট থাকলেই হবে, টাকা কাটার কথা বুঝিনি।"
    }
  ];

  const handleStartListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Browser speech recognition not available. Please use the simulated answer buttons below!");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = lang === "hi" ? "hi-IN" : lang === "bn" ? "bn-IN" : "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setIsRecording(true);
      setTranscript("");
    };

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      setTranscript(text);
      runEvaluation(text);
    };

    recognition.onerror = () => setIsRecording(false);
    recognition.onend = () => setIsRecording(false);
    recognition.start();
  };

  const runEvaluation = async (spokenText) => {
    setEvaluating(true);
    try {
      const res = await fetch("/api/comprehension/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          spokenText,
          expectedConcepts: doc.expected_concepts || ["helmet", "500 fine", "zone 4"],
          lang,
          docType: doc.category
        })
      });

      const data = await res.json();
      setEvaluation(data);

      if (data.feedback) {
        const textToSpeak = data.simplifiedClarification 
          ? `${data.feedback} ${data.simplifiedClarification}`
          : data.feedback;
        speakText(textToSpeak, lang);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setEvaluating(false);
    }
  };

  return (
    <div className="bg-slate-900 text-white rounded-2xl p-5 shadow-lg border border-slate-800">
      <div className="flex items-center gap-2 text-amber-400 mb-2">
        <Sparkles className="w-5 h-5" />
        <h3 className="font-bold text-sm tracking-wide uppercase">Explain-Back Comprehension Loop</h3>
      </div>

      <p className="text-slate-200 font-semibold text-base mb-4">
        {t.comprehensionTitle}
      </p>

      <div className="flex flex-col sm:flex-row items-center gap-3 mb-4">
        <button
          onClick={handleStartListening}
          disabled={isRecording || evaluating}
          className={`w-full sm:w-auto flex-1 flex items-center justify-center gap-3 py-4 px-6 rounded-xl font-black text-base shadow-md transition active:scale-95 ${
            isRecording
              ? "bg-rose-500 text-white animate-pulse"
              : "bg-amber-400 hover:bg-amber-500 text-slate-950"
          }`}
        >
          {isRecording ? <MicOff className="w-6 h-6" /> : <Mic className="w-6 h-6" />}
          <span>{isRecording ? t.listening : t.speakBtn}</span>
        </button>
      </div>

      <div className="bg-slate-800/80 p-3 rounded-xl mb-4 border border-slate-700">
        <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">
          बिना माइक के टेस्ट करें (Simulated test answers):
        </div>
        <div className="flex flex-wrap gap-2">
          {sampleAnswers.map((s, idx) => (
            <button
              key={idx}
              onClick={() => {
                setTranscript(s.text);
                runEvaluation(s.text);
              }}
              className="bg-slate-700 hover:bg-slate-600 text-slate-200 text-xs py-2 px-3 rounded-lg font-medium border border-slate-600 transition text-left"
            >
              <span className="font-bold text-amber-400 mr-1.5">{s.label}:</span>
              "{s.text.slice(0, 32)}..."
            </button>
          ))}
        </div>
      </div>

      {transcript && (
        <div className="bg-slate-800 p-3 rounded-xl text-xs text-slate-300 mb-4 border border-slate-700">
          <span className="font-bold text-amber-400 uppercase text-[10px] block mb-1">आपने कहा (What you said):</span>
          "{transcript}"
        </div>
      )}

      {evaluating && (
        <div className="flex items-center gap-2 text-amber-400 text-sm font-semibold py-2">
          <RefreshCw className="w-4 h-4 animate-spin" />
          <span>समझ की जांच हो रही है... (Checking understanding)</span>
        </div>
      )}

      {evaluation && (
        <div
          className={`p-4 rounded-xl border-2 transition ${
            evaluation.isUnderstood
              ? "bg-emerald-950/70 border-emerald-500 text-emerald-100"
              : "bg-rose-950/70 border-rose-500 text-rose-100"
          }`}
        >
          <div className="flex items-start gap-3">
            {evaluation.isUnderstood ? (
              <CheckCircle className="w-7 h-7 text-emerald-400 shrink-0 mt-0.5" />
            ) : (
              <AlertCircle className="w-7 h-7 text-rose-400 shrink-0 mt-0.5" />
            )}

            <div className="flex-1">
              <h4 className="font-bold text-base">
                {evaluation.isUnderstood ? "सफल समझ (Understood Correctly)" : "स्पष्टीकरण आवश्यक (Needs Clarification)"}
              </h4>
              <p className="text-sm mt-1 font-medium">{evaluation.feedback}</p>

              {evaluation.simplifiedClarification && (
                <div className="mt-3 bg-slate-900/90 p-3 rounded-lg border border-amber-400/50">
                  <div className="text-[11px] font-bold text-amber-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                    <Volume2 className="w-3.5 h-3.5" /> सबसे आसान भाषा में सीखें:
                  </div>
                  <p className="text-xs text-white font-semibold leading-relaxed">
                    {evaluation.simplifiedClarification}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

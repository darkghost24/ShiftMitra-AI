import React, { useState, useRef, useEffect } from "react";
import { Send, Image as ImageIcon, Mic, Play, Pause, CheckCheck, RefreshCw, Paperclip, Smile, MoreVertical, Phone, Video, Sparkles } from "lucide-react";
import { speakText, stopSpeech } from "../../utils/speechHelper";
import { useLanguage } from "../../context/LanguageContext";

export const WhatsAppSimulator = () => {
  const { lang } = useLanguage();
  const chatBottomRef = useRef(null);
  const [playingId, setPlayingId] = useState(null);
  const [inputText, setInputText] = useState("");
  const [sending, setSending] = useState(false);

  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "bot",
      text: "नमस्ते! शिफ्टमित्र व्हाट्सएप सहायक में आपका स्वागत है। आप किसी भी फैक्ट्री नोटिस या सैलरी पर्ची का फोटो यहाँ भेज सकते हैं।",
      timestamp: "09:30 AM"
    }
  ]);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  const handlePlayAudio = (id, textToSpeak) => {
    if (playingId === id) {
      stopSpeech();
      setPlayingId(null);
    } else {
      stopSpeech();
      setPlayingId(id);
      speakText(textToSpeak, lang, () => setPlayingId(null));
    }
  };

  const sendMessage = async (type = "text", customContent = null) => {
    const textToSend = customContent || inputText.trim();
    if (!textToSend && type === "text") return;

    const userMessage = {
      id: Date.now(),
      sender: "user",
      text: textToSend || "📸 [Forwarded Document Photo]",
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText("");
    setSending(true);

    try {
      const res = await fetch("/api/whatsapp/webhook", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          from: "+919876543210",
          messageType: type,
          textContent: userMessage.text,
          language: lang
        })
      });

      const data = await res.json();
      if (data.success) {
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 1,
            sender: "bot",
            text: data.message,
            audioScript: data.audioNoteText,
            timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
          }
        ]);
      }
    } catch (err) {
      console.error("WhatsApp Webhook Error:", err);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="max-w-md mx-auto px-4 py-6">
      <div className="bg-[#efeae2] border-4 border-slate-800 rounded-[32px] overflow-hidden shadow-2xl flex flex-col h-[650px] relative">
        <header className="bg-[#075E54] text-white px-3.5 py-3 flex items-center justify-between shadow-md z-10 shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="w-10 h-10 rounded-full bg-amber-400 text-slate-950 font-black flex items-center justify-center text-sm shadow border-2 border-white/40">
              SM
            </div>
            <div>
              <div className="font-bold text-sm leading-tight flex items-center gap-1.5">
                <span>ShiftMitra Assistant</span>
                <span className="text-[10px] bg-emerald-700/80 text-emerald-200 px-1 rounded">BOT</span>
              </div>
              <div className="text-[11px] text-emerald-100 flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span>Active 24x7 Factory Helpline</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3 text-white/90">
            <Video className="w-4 h-4 cursor-pointer" />
            <Phone className="w-4 h-4 cursor-pointer" />
            <MoreVertical className="w-4 h-4 cursor-pointer" />
          </div>
        </header>

        <div className="flex-1 p-3.5 overflow-y-auto space-y-3">
          {messages.map((m) => (
            <div key={m.id} className={`flex flex-col ${m.sender === "user" ? "items-end" : "items-start"}`}>
              <div
                className={`max-w-[85%] rounded-2xl p-3 shadow-2xs text-xs leading-relaxed relative ${
                  m.sender === "user" ? "bg-[#d9fdd3] text-slate-900 rounded-tr-none" : "bg-white text-slate-900 rounded-tl-none border border-slate-200/60"
                }`}
              >
                <div className="whitespace-pre-wrap font-medium">{m.text}</div>

                {m.audioScript && (
                  <div className="mt-2.5 pt-2 border-t border-slate-100">
                    <button
                      type="button"
                      onClick={() => handlePlayAudio(m.id, m.audioScript)}
                      className={`w-full p-2 rounded-xl flex items-center justify-between gap-2 font-bold transition ${
                        playingId === m.id ? "bg-rose-50 text-rose-700 border border-rose-300" : "bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200"
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        {playingId === m.id ? (
                          <Pause className="w-4 h-4 fill-rose-600 text-rose-600" />
                        ) : (
                          <Play className="w-4 h-4 fill-emerald-600 text-emerald-600" />
                        )}
                        <span>{playingId === m.id ? "ऑडियो रोकें" : "वॉइस नोट सुनें (Play Voice)"}</span>
                      </div>
                      <span className="text-[10px] bg-white/80 px-1.5 py-0.5 rounded text-slate-600">0:24</span>
                    </button>
                  </div>
                )}

                <div className="text-[9px] text-slate-400 text-right mt-1.5 flex items-center justify-end gap-1 font-semibold">
                  <span>{m.timestamp}</span>
                  {m.sender === "user" && <CheckCheck className="w-3.5 h-3.5 text-sky-500" />}
                </div>
              </div>
            </div>
          ))}

          {sending && (
            <div className="flex items-center gap-2 bg-white/80 border border-slate-200 text-slate-600 px-3 py-1.5 rounded-full text-xs font-semibold w-fit">
              <RefreshCw className="w-3.5 h-3.5 animate-spin text-emerald-600" />
              <span>ShiftMitra AI is preparing audio note...</span>
            </div>
          )}

          <div ref={chatBottomRef} />
        </div>

        <div className="bg-slate-200/90 px-3 py-1.5 flex items-center gap-1.5 overflow-x-auto text-[11px] border-t border-slate-300">
          <span className="font-bold text-slate-500 shrink-0 flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-amber-500" /> Test:
          </span>
          <button
            type="button"
            onClick={() => sendMessage("image", "📸 [Forwarded Notice: Zone 4 Helmet Fine Rs. 500]")}
            className="bg-white hover:bg-slate-100 text-slate-800 font-semibold px-2 py-0.5 rounded border border-slate-300 shrink-0 transition"
          >
            Send Safety Notice
          </button>
          <button
            type="button"
            onClick={() => sendMessage("text", "🎙️ [Voice: मुझे समझ आ गया कि बिना हेलमेट 500 रुपये कटेंगे]")}
            className="bg-white hover:bg-slate-100 text-slate-800 font-semibold px-2 py-0.5 rounded border border-slate-300 shrink-0 transition"
          >
            Reply with Voice
          </button>
        </div>

        <footer className="bg-[#f0f2f5] p-2 flex items-center gap-2 border-t border-slate-300">
          <div className="flex items-center gap-1 text-slate-500 pl-1">
            <Smile className="w-5 h-5 cursor-pointer hover:text-slate-700" />
            <Paperclip
              onClick={() => sendMessage("image", "📸 [Attached Photo: Monthly Payslip October]")}
              className="w-5 h-5 cursor-pointer hover:text-slate-700"
              title="Attach Document Photo"
            />
          </div>

          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage("text")}
            placeholder="संदेश लिखें (Type message)..."
            className="flex-1 text-xs bg-white border border-slate-300 rounded-full py-2 px-3.5 focus:outline-none focus:ring-1 focus:ring-emerald-500 font-medium"
          />

          {inputText.trim() ? (
            <button
              type="button"
              onClick={() => sendMessage("text")}
              className="p-2.5 bg-[#00a884] hover:bg-[#008f6f] text-white rounded-full transition shadow"
            >
              <Send className="w-4 h-4" />
            </button>
          ) : (
            <button
              type="button"
              onClick={() => sendMessage("text", "🎙️ [Voice: क्या कैंटीन के पैसे अगले महीने वापस मिलेंगे?]")}
              title="Send Simulated Voice Note"
              className="p-2.5 bg-[#00a884] hover:bg-[#008f6f] text-white rounded-full transition shadow"
            >
              <Mic className="w-4 h-4" />
            </button>
          )}
        </footer>
      </div>
    </div>
  );
};

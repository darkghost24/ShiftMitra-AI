export const speakText = (text, lang = "hi", onEnd = () => {}) => {
  if (!("speechSynthesis" in window)) {
    alert("Speech Synthesis not supported in this browser");
    return;
  }

  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  if (lang === "hi") utterance.lang = "hi-IN";
  else if (lang === "bn") utterance.lang = "bn-IN";
  else utterance.lang = "en-IN";

  utterance.rate = 0.9;
  utterance.pitch = 1.0;

  utterance.onend = () => onEnd();
  utterance.onerror = () => onEnd();

  window.speechSynthesis.speak(utterance);
};

export const stopSpeech = () => {
  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();
  }
};

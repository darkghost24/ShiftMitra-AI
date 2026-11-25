import express from "express";
import { generateExplanation } from "../services/aiService.js";

const router = express.Router();

router.post("/webhook", async (req, res) => {
  const { from = "+919876543210", messageType = "image", textContent = "", language = "hi" } = req.body;

  let replyText = "";
  let audioTranscript = "";

  if (messageType === "image" || textContent.includes("photo") || textContent.includes("Notice")) {
    const explanation = await generateExplanation({
      rawText: "SAFETY NOTICE ZONE 4 HELMET PENALTY 500",
      targetLang: language
    });

    replyText = `📢 *${explanation.title}*\n\n${explanation.short_summary}\n\n👉 *ज़रूरी नियम:* ${explanation.action_item}\n\n🎙️ _नीचे दिए गए ऑडियो संदेश को सुनें। इसके बाद अपना उत्तर भेजें।_`;
    audioTranscript = explanation.speech_script;
  } else {
    replyText = language === "hi" 
      ? "धन्यवाद! आपका वॉइस संदेश मिला। आपका उत्तर सही है। हेलमेट अवश्य पहनें।"
      : "ধন্যবাদ! আপনার ভয়েস মেসেজ পাওয়া গেছে। আপনি নিয়মটি ঠিক বুঝেছেন।";
    audioTranscript = replyText;
  }

  res.json({
    success: true,
    to: from,
    message: replyText,
    audioNoteText: audioTranscript,
    timestamp: new Date().toISOString()
  });
});

export default router;

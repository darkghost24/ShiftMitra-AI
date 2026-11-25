import express from "express";
import multer from "multer";
import { processDocumentOcr } from "../services/ocrService.js";
import { generateExplanation } from "../services/aiService.js";
import { recordAnalyticsEvent } from "./analytics.js";

const upload = multer({ limits: { fileSize: 10 * 1024 * 1024 } });
const router = express.Router();

router.post("/interpret", upload.single("image"), async (req, res) => {
  try {
    const { targetLang = "hi", textHint = "" } = req.body;
    const extractedText = await processDocumentOcr(req.file, textHint);
    const explanation = await generateExplanation({ rawText: extractedText, targetLang });

    recordAnalyticsEvent({
      documentType: explanation.category,
      language: targetLang,
      clarificationNeeded: false,
      rawQuery: explanation.title
    });

    return res.json({
      success: true,
      rawText: extractedText,
      explanation
    });
  } catch (error) {
    console.error("Interpret Error:", error);
    return res.status(500).json({ success: false, error: "Failed to process document" });
  }
});

export default router;

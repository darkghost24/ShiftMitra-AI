import express from "express";
import { evaluateComprehension } from "../services/aiService.js";
import { recordAnalyticsEvent } from "./analytics.js";

const router = express.Router();

router.post("/verify", (req, res) => {
  const { spokenText = "", expectedConcepts = [], lang = "hi", docType = "General" } = req.body;

  const result = evaluateComprehension({ spokenText, expectedConcepts, lang });

  if (!result.isUnderstood) {
    recordAnalyticsEvent({
      documentType: docType,
      language: lang,
      clarificationNeeded: true,
      missedPoints: result.missedConcepts
    });
  }

  return res.json({
    success: true,
    ...result
  });
});

export default router;

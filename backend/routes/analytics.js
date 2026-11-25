import express from "express";

const router = express.Router();

let analyticsStore = [
  { id: "1", documentType: "Safety Notice", language: "hi", clarificationNeeded: true, missedPoints: ["500 fine", "suspension"], timestamp: new Date(Date.now() - 3600000 * 24 * 3).toISOString() },
  { id: "2", documentType: "Safety Notice", language: "bn", clarificationNeeded: true, missedPoints: ["suspension"], timestamp: new Date(Date.now() - 3600000 * 24 * 2).toISOString() },
  { id: "3", documentType: "Payslip Breakdown", language: "hi", clarificationNeeded: false, missedPoints: [], timestamp: new Date(Date.now() - 3600000 * 24).toISOString() },
  { id: "4", documentType: "Payslip Breakdown", language: "bn", clarificationNeeded: true, missedPoints: ["canteen", "pf deduction"], timestamp: new Date(Date.now() - 3600000 * 12).toISOString() },
  { id: "5", documentType: "Safety Notice", language: "hi", clarificationNeeded: false, missedPoints: [], timestamp: new Date().toISOString() }
];

export const recordAnalyticsEvent = (event) => {
  analyticsStore.unshift({
    id: "evt-" + Date.now() + Math.random().toString(36).substr(2, 4),
    documentType: event.documentType || "Safety Notice",
    language: event.language || "hi",
    clarificationNeeded: Boolean(event.clarificationNeeded),
    missedPoints: event.missedPoints || [],
    timestamp: new Date().toISOString()
  });
};

router.get("/summary", (req, res) => {
  const totalProcessed = analyticsStore.length;
  const confusionCount = analyticsStore.filter((item) => item.clarificationNeeded).length;
  const confusionRate = totalProcessed > 0 ? Math.round((confusionCount / totalProcessed) * 100) : 0;

  const docTypeCounts = {};
  const docTypeConfusion = {};
  analyticsStore.forEach((item) => {
    docTypeCounts[item.documentType] = (docTypeCounts[item.documentType] || 0) + 1;
    if (item.clarificationNeeded) {
      docTypeConfusion[item.documentType] = (docTypeConfusion[item.documentType] || 0) + 1;
    }
  });

  const languageCounts = {};
  analyticsStore.forEach((item) => {
    languageCounts[item.language] = (languageCounts[item.language] || 0) + 1;
  });

  const missedTopicMap = {};
  analyticsStore.forEach((item) => {
    (item.missedPoints || []).forEach((pt) => {
      missedTopicMap[pt] = (missedTopicMap[pt] || 0) + 1;
    });
  });

  const topMisunderstoodTopics = Object.entries(missedTopicMap).map(([topic, count]) => ({
    topic,
    count
  })).sort((a, b) => b.count - a.count);

  res.json({
    totalProcessed,
    confusionCount,
    confusionRate,
    docTypeBreakdown: docTypeCounts,
    docTypeConfusion,
    languageBreakdown: languageCounts,
    topMisunderstoodTopics,
    recentEvents: analyticsStore.slice(0, 15)
  });
});

export default router;

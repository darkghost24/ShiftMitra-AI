import os
import zipfile

# File tree definition with complete source code
FILES = {
    # ---------------- ROOT ----------------
    "shiftmitra/package.json": """{
  "name": "shiftmitra-root",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "install:all": "npm install && cd backend && npm install && cd ../frontend && npm install",
    "backend": "cd backend && npm run dev",
    "frontend": "cd frontend && npm run dev",
    "dev": "concurrently \\"npm run backend\\" \\"npm run frontend\\""
  },
  "devDependencies": {
    "concurrently": "^8.2.2"
  }
}
""",

    "shiftmitra/.gitignore": """node_modules
dist
build
.env
.DS_Store
Thumbs.db
npm-debug.log*
""",

    "shiftmitra/README.md": """# ShiftMitra – Factory Worker's AI Companion

A voice-first assistant and confusion tracking dashboard for factory shop floors.

## Setup Instructions
1. Run `npm run install:all` to install root, backend, and frontend packages.
2. Run `npm run dev` to launch both servers concurrently.
3. Access the Worker Portal at http://localhost:3000.
""",

    # ---------------- BACKEND ----------------
    "shiftmitra/backend/package.json": """{
  "name": "shiftmitra-backend",
  "version": "1.0.0",
  "description": "ShiftMitra Express API for Document Interpretation and Analytics",
  "main": "server.js",
  "type": "module",
  "scripts": {
    "start": "node server.js",
    "dev": "node --watch server.js"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.19.2",
    "multer": "^1.4.5-lts.1",
    "uuid": "^9.0.1"
  }
}
""",

    "shiftmitra/backend/.env.example": """PORT=5000
NODE_ENV=development
""",

    "shiftmitra/backend/server.js": """import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import documentRoutes from "./routes/documents.js";
import comprehensionRoutes from "./routes/comprehension.js";
import whatsappRoutes from "./routes/whatsapp.js";
import analyticsRoutes from "./routes/analytics.js";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

app.use("/api/documents", documentRoutes);
app.use("/api/comprehension", comprehensionRoutes);
app.use("/api/whatsapp", whatsappRoutes);
app.use("/api/analytics", analyticsRoutes);

app.get("/health", (req, res) => {
  res.json({ status: "ok", app: "ShiftMitra Backend", timestamp: new Date() });
});

app.listen(PORT, () => {
  console.log(`[ShiftMitra] Backend Server running on http://localhost:${PORT}`);
});
""",

    "shiftmitra/backend/services/ocrService.js": """export const processDocumentOcr = async (file, textHint) => {
  if (textHint && textHint.trim().length > 0) {
    return textHint;
  }

  const filename = file ? file.originalname.toLowerCase() : "";

  if (filename.includes("safety") || filename.includes("helmet")) {
    return `SAFETY MANDATE NOTICE - SHOP FLOOR ZONE 4
    All contract & regular workers must wear ISI mark safety helmets and steel-toe boots before entering.
    First violation penalty: Rs. 500 deducted directly from wages.
    Second violation: 3 days suspension without pay.
    Helmets must remain strapped at all times.
    Issued by: HSE Department, Apex Auto Components Ltd.`;
  }

  if (filename.includes("payslip") || filename.includes("salary")) {
    return `MONTHLY PAYSLIP - OCT 2026
    Worker: Ramesh Kumar | ID: W-4089 | Shift: B
    Basic Wage: Rs. 14,500
    Overtime (28 hrs @ 2x rate): Rs. 3,850
    Gross Salary: Rs. 18,350
    Deductions:
    - Provident Fund (PF 12%): Rs. 1,740
    - ESI Medical Insurance: Rs. 138
    - Canteen Mess Charges: Rs. 650
    Total Deductions: Rs. 2,528
    Net Take-Home Pay: Rs. 15,822 (Credited on 7th)`;
  }

  return `FACTORY HEALTH AND WELFARE ANNOUNCEMENT
  Free vaccination camp on Saturday 10 AM at Health Centre.
  Overtime shift on Sunday will be paid at double rate for all attending workers.
  Report to Supervisor before Friday 5 PM.`;
};
""",

    "shiftmitra/backend/services/aiService.js": """export const generateExplanation = async ({ rawText, targetLang = "hi" }) => {
  const isSafety = /safety|helmet|fine|penalty|boots|danger/i.test(rawText);

  if (isSafety) {
    if (targetLang === "hi") {
      return {
        id: "doc-" + Date.now(),
        category: "Safety Notice",
        title: "दुकान तल - सुरक्षा हेलमेट और जूते के कड़े नियम",
        short_summary: "शॉप फ्लोर ज़ोन 4 में बिना हेलमेट और सेफ्टी जूते काम करने पर ₹500 का जुर्माना कटेगा।",
        key_points: [
          {
            icon: "helmet",
            title: "हेलमेट और जूते अनिवार्य",
            desc: "ज़ोन 4 में प्रवेश से पहले ISI मार्क हेलमेट और लोहे वाले जूते पहनना ज़रूरी है।",
            type: "danger"
          },
          {
            icon: "money",
            title: "पहला उल्लंघन: ₹500 जुर्माना",
            desc: "नियम न मानने पर पहली बार आपकी मजदूरी से ₹500 सीधे कटेंगे।",
            type: "warning"
          },
          {
            icon: "danger",
            title: "दूसरी बार: 3 दिन का निलंबन",
            desc: "दोबारा पकड़े जाने पर 3 दिन काम और बिना वेतन के बाहर रखा जाएगा।",
            type: "danger"
          }
        ],
        action_item: "गेट पर ही हेलमेट का पट्टा कस लें। काम के दौरान इसे कभी न उतारें।",
        speech_script: "ध्यान दें। यह सुरक्षा सूचना ज़ोन 4 के लिए है। आपको हमेशा ISI हेलमेट और सेफ्टी जूते पहनने होंगे। पहली बार बिना हेलमेट मिलने पर 500 रुपये का जुर्माना होगा और दूसरी बार 3 दिन के लिए काम से निकाला जा सकता है।",
        expected_concepts: ["helmet", "safety shoes", "500 fine", "suspension", "zone 4"]
      };
    } else if (targetLang === "bn") {
      return {
        id: "doc-" + Date.now(),
        category: "Safety Notice",
        title: "দোকান তল - হেলমেট ও সুরক্ষামূলক জুতোর কড়া নিয়ম",
        short_summary: "জোন ৪-এ হেলমেট এবং স্টিল-টো জুতো ছাড়া ঢুকলে ৫০০ টাকা জরিমানা কাটা হবে।",
        key_points: [
          {
            icon: "helmet",
            title: "হেলমেট পরা বাধ্যতামূলক",
            desc: "জোন ৪ এলাকায় কাজ করার সময় ISI হেলমেট এবং জুতো পরা আবশ্যক।",
            type: "danger"
          },
          {
            icon: "money",
            title: "প্রথমবার ভুল: ৫০০ টাকা জরিমানা",
            desc: "নিয়ম না মানলে প্রথমবার ৫০০ টাকা বেতন থেকে কেটে নেওয়া হবে।",
            type: "warning"
          },
          {
            icon: "danger",
            title: "দ্বিতীয়বার: ৩ দিন সাসপেনশন",
            desc: "দ্বিতীয়বার নিয়ম ভাঙলে ৩ দিনের জন্য বিনা বেতনে কাজ বন্ধ থাকবে।",
            type: "danger"
          }
        ],
        action_item: "গেটে ঢোকার আগেই হেলমেটের স্ট্র্যাপ ভালো করে বেঁধে নিন।",
        speech_script: "মনোযোগ দিন। এটি জোন ৪-এর সুরক্ষার নোটিশ। কাজ করার সময় হেলমেট এবং সেফটি জুতো পরা জরুরি। হেলমেট না পরলে প্রথমবার ৫০০ টাকা জরিমানা হবে এবং দ্বিতীয়বার তিন দিন কাজ বন্ধ থাকবে।",
        expected_concepts: ["helmet", "safety shoes", "500 fine", "suspension", "zone 4"]
      };
    } else {
      return {
        id: "doc-" + Date.now(),
        category: "Safety Notice",
        title: "Shop Floor Zone 4: Mandatory PPE & Helmet Rules",
        short_summary: "You must wear ISI helmets and safety shoes in Zone 4. Violations lead to a ₹500 fine or 3-day suspension.",
        key_points: [
          {
            icon: "helmet",
            title: "Helmet & Shoes Required",
            desc: "ISI marked helmets and safety boots are strictly required before entry.",
            type: "danger"
          },
          {
            icon: "money",
            title: "First Violation: ₹500 Fine",
            desc: "₹500 will be deducted straight from wages for your first slip.",
            type: "warning"
          },
          {
            icon: "danger",
            title: "Second Violation: 3 Days Off",
            desc: "Second violation will result in a 3-day unpaid suspension.",
            type: "danger"
          }
        ],
        action_item: "Fasten your helmet strap before walking past the yellow line.",
        speech_script: "Important safety update for Zone 4. You must wear your helmet and safety boots at all times. A 500 rupee penalty applies on first violation, followed by suspension on second violation.",
        expected_concepts: ["helmet", "safety shoes", "500 fine", "suspension", "zone 4"]
      };
    }
  }

  // Payslip Fallback Response
  if (targetLang === "hi") {
    return {
      id: "doc-" + Date.now(),
      category: "Payslip Breakdown",
      title: "महीने की सैलरी पर्ची का विवरण",
      short_summary: "आपकी कुल कमाई ₹18,350 हुई है। PF और कैंटीन कटने के बाद आपके खाते में ₹15,822 आएंगे।",
      key_points: [
        {
          icon: "money",
          title: "मूल वेतन और ओवरटाइम",
          desc: "मूल वेतन ₹14,500 है और 28 घंटे ओवरटाइम के ₹3,850 अलग से जुड़े हैं।",
          type: "success"
        },
        {
          icon: "deduction",
          title: "कटौतियाँ (PF और ESI)",
          desc: "भविष्य निधि (PF) के ₹1,740, ESI के ₹138 और कैंटीन के ₹650 काटे गए हैं।",
          type: "warning"
        },
        {
          icon: "bonus",
          title: "खाते में आने वाली राशि",
          desc: "सब कटौती के बाद आपके बैंक में ₹15,822 तारीख 7 को जमा होगी।",
          type: "success"
        }
      ],
      action_item: "यदि कैंटीन का कटा हुआ पैसा गलत लगता है तो 6 तारीख तक सुपरवाइजर से मिलें।",
      speech_script: "नमस्ते। आपकी इस महीने की कुल कमाई 18,350 रुपये है। जिसमें 28 घंटे के ओवरटाइम के 3,850 रुपये शामिल हैं। PF और कैंटीन कटने के बाद 7 तारीख को आपके खाते में 15,822 रुपये आएंगे।",
      expected_concepts: ["overtime", "pf deduction", "canteen", "take home pay", "15822"]
    };
  } else if (targetLang === "bn") {
    return {
      id: "doc-" + Date.now(),
      category: "Payslip Breakdown",
      title: "বেতনের স্লিপের সহজ ব্যাখ্যা",
      short_summary: "আপনার মোট উপার্জন ১৮,৩৫০ টাকা। পিএফ এবং ক্যান্টিন খরচের পর আপনার একাউন্টে ১৫,৮২২ টাকা আসবে।",
      key_points: [
        {
          icon: "money",
          title: "মূল বেতন ও ওভারটাইম",
          desc: "মূল বেতন ১৪,৫০০ টাকা এবং ২৮ ঘণ্টা ওভারটাইমের জন্য ৩,৮৫০ টাকা যোগ হয়েছে।",
          type: "success"
        },
        {
          icon: "deduction",
          title: "টাকা কাটার হিসাব (PF ও ক্যাফেটেরিয়া)",
          desc: "পিএফ-এ ১,৭৪০ টাকা, ইএসআই ১৩৮ টাকা ও ক্যান্টিন বাবদ ৬৫০ টাকা কাটা হয়েছে।",
          type: "warning"
        },
        {
          icon: "bonus",
          title: "ব্যাঙ্কে জমা হবে",
          desc: "সব কেটে আপনার অ্যাকাউন্টে ১৫,৮২২ টাকা ৭ তারিখে পাঠানো হবে।",
          type: "success"
        }
      ],
      action_item: "ক্যান্টিন চার্জে কোনো গরমিল থাকলে সুপারভাইজারকে জানান।",
      speech_script: "নমস্কার। আপনার এই মাসের মোট বেতন ১৮,৩৫০ টাকা। যার মধ্যে ২৮ ঘণ্টার ওভারটাইম বাবদ ৩,৮৫০ টাকা রয়েছে। পিএফ ও ক্যান্টিন চার্জ কাটার পর আপনার অ্যাকাউন্টে ১৫,৮২২ টাকা ঢুকবে।",
      expected_concepts: ["overtime", "pf deduction", "canteen", "take home pay", "15822"]
    };
  } else {
    return {
      id: "doc-" + Date.now(),
      category: "Payslip Breakdown",
      title: "Monthly Salary Slip Breakdown",
      short_summary: "Your total earned pay is ₹18,350. After PF, ESI and mess deductions, your take-home pay is ₹15,822.",
      key_points: [
        {
          icon: "money",
          title: "Base Pay & Overtime",
          desc: "Basic wage is ₹14,500 plus 28 hours overtime earnings of ₹3,850.",
          type: "success"
        },
        {
          icon: "deduction",
          title: "Statutory & Mess Deductions",
          desc: "PF deduction ₹1,740, ESI medical ₹138, and Canteen meal fee ₹650.",
          type: "warning"
        },
        {
          icon: "bonus",
          title: "Final Bank Deposit",
          desc: "Net ₹15,822 will be deposited directly to your bank account on the 7th.",
          type: "success"
        }
      ],
      action_item: "Verify your overtime hours with HR if you logged more than 28 hours.",
      speech_script: "Hello. Your gross pay this month is 18,350 rupees including 28 hours of overtime. After PF and canteen charges, your final bank credit is 15,822 rupees on the 7th.",
      expected_concepts: ["overtime", "pf deduction", "canteen", "take home pay", "15822"]
    };
  }
};

export const evaluateComprehension = ({ spokenText, expectedConcepts = [], lang = "hi" }) => {
  const normalized = spokenText.toLowerCase();

  const keywordMappings = {
    helmet: ["helmet", "हेलमेट", "হেলমেট", "टोपी", "माथा"],
    "safety shoes": ["shoes", "boots", "जूते", "जुता", "बूट"],
    "500 fine": ["500", "पांच सौ", "পাঁচশত", "fine", "कटेंगे", "জরিমানা", "पेनल्टी"],
    suspension: ["suspend", "निलंबन", "सस्पेंड", "কাজ বন্ধ", "बाहर", "छुटी"],
    overtime: ["overtime", "ओटी", "ওভারটাইম", "ज्यादा काम", "28 घंटा"],
    "pf deduction": ["pf", "पीएफ", "পিএফ", "काटा", "টাকা কাটা", "कटा"],
    "take home pay": ["15822", "15,822", "खाता", "अकाउंट", "বেতন", "सैलरी"]
  };

  let matchedCount = 0;
  const missedConcepts = [];

  expectedConcepts.forEach((concept) => {
    const synonyms = keywordMappings[concept] || [concept];
    const isMatched = synonyms.some((term) => normalized.includes(term.toLowerCase()));
    if (isMatched) {
      matchedCount++;
    } else {
      missedConcepts.push(concept);
    }
  });

  const ratio = expectedConcepts.length > 0 ? matchedCount / expectedConcepts.length : 1;
  const isUnderstood = ratio >= 0.4 || spokenText.length > 25;

  let feedback = "";
  let simplifiedClarification = "";

  if (isUnderstood) {
    if (lang === "hi") {
      feedback = "शाबाश! आपने मुख्य बातें बिल्कुल सही समझी हैं।";
    } else if (lang === "bn") {
      feedback = "চমৎকার! আপনি মূল বিষয়টি একদম সঠিক বুঝেছেন।";
    } else {
      feedback = "Great job! You clearly understood the critical instructions.";
    }
  } else {
    if (lang === "hi") {
      feedback = "लगता है कुछ मुख्य बिंदु छूट गए हैं। चिंता न करें, दोबारा संक्षेप में सुनें:";
      simplifiedClarification = "सीधी बात: ज़ोन 4 में हेलमेट और जूते पहनना अनिवार्य है। नहीं पहनने पर 500 रुपये कटेंगे और दोबारा गलती पर 3 दिन काम बंद रहेगा।";
    } else if (lang === "bn") {
      feedback = "মনে হচ্ছে কয়েকটি জরুরি অংশ স্পষ্ট হয়নি। সহজে আরেকবার শুনুন:";
      simplifiedClarification = "সহজ কথা: জোন ৪-এ হেলমেট ও সেফটি জুতো পরা জরুরি। না পরলে ৫০০ টাকা জরিমানা এবং ফের ভুল হলে ৩ দিন কাজ বন্ধ।";
    } else {
      feedback = "You missed a couple of safety rules. Let's make it simpler:";
      simplifiedClarification = "Key rule: Wear your helmet and safety shoes in Zone 4. Otherwise you lose ₹500 from your pay or face 3 days suspension.";
    }
  }

  return {
    isUnderstood,
    scorePercentage: Math.round(ratio * 100),
    matchedCount,
    missedConcepts,
    feedback,
    simplifiedClarification
  };
};
""",

    "shiftmitra/backend/routes/documents.js": """import express from "express";
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
""",

    "shiftmitra/backend/routes/comprehension.js": """import express from "express";
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
""",

    "shiftmitra/backend/routes/whatsapp.js": """import express from "express";
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

    replyText = `📢 *${explanation.title}*\\n\\n${explanation.short_summary}\\n\\n👉 *ज़रूरी नियम:* ${explanation.action_item}\\n\\n🎙️ _नीचे दिए गए ऑडियो संदेश को सुनें। इसके बाद अपना उत्तर भेजें।_`;
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
""",

    "shiftmitra/backend/routes/analytics.js": """import express from "express";

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
""",

    # ---------------- FRONTEND CONFIG ----------------
    "shiftmitra/frontend/package.json": """{
  "name": "shiftmitra-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "lucide-react": "^0.344.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.18",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "vite": "^5.1.4"
  }
}
""",

    "shiftmitra/frontend/vite.config.js": """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
});
""",

    "shiftmitra/frontend/tailwind.config.js": """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      boxShadow: {
        '2xs': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      }
    },
  },
  plugins: [],
}
""",

    "shiftmitra/frontend/postcss.config.js": """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""",

    "shiftmitra/frontend/index.html": """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>ShiftMitra – Factory Worker's AI Companion</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Hind:wght@400;600;700&family=Noto+Sans+Bengali:wght@400;600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  </head>
  <body class="bg-slate-100 text-slate-900 font-sans antialiased selection:bg-amber-300 selection:text-slate-900">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""",

    "shiftmitra/frontend/src/index.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: 'Hind', 'Noto Sans Bengali', 'Inter', sans-serif;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

.touch-target {
  min-height: 48px;
  min-width: 48px;
}
""",

    "shiftmitra/frontend/src/main.jsx": """import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";

const rootElement = document.getElementById("root");
if (!rootElement) {
  throw new Error("Failed to find the root element to mount ShiftMitra.");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""",

    "shiftmitra/frontend/src/App.jsx": """import React, { useState } from "react";
import { Navbar } from "./components/Navbar";
import { WorkerPortal } from "./components/WorkerPortal/WorkerPortal";
import { Dashboard } from "./components/ManagementDashboard/Dashboard";
import { WhatsAppSimulator } from "./components/WhatsAppSimulator/WhatsAppSimulator";
import { LanguageProvider } from "./context/LanguageContext";
import { Wifi, BatteryMedium } from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState("worker");
  const [isLowPowerMode, setIsLowPowerMode] = useState(false);

  return (
    <LanguageProvider>
      <div className="min-h-screen bg-slate-100 flex flex-col font-sans selection:bg-amber-300 selection:text-slate-950">
        <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

        <aside aria-label="Device connectivity status" className="bg-slate-950 text-slate-400 text-[11px] font-semibold px-4 py-1 border-b border-slate-800">
          <div className="max-w-5xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="flex items-center gap-1 text-emerald-400">
                <Wifi className="w-3.5 h-3.5" />
                <span>4G Factory Network (Active)</span>
              </span>
              <span className="hidden sm:inline text-slate-600">|</span>
              <span className="hidden sm:inline text-slate-400">Shop Floor Zone 4 Hub</span>
            </div>

            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => setIsLowPowerMode(!isLowPowerMode)}
                className={`flex items-center gap-1 px-1.5 py-0.5 rounded transition ${
                  isLowPowerMode ? "bg-amber-400 text-slate-950 font-bold" : "hover:text-slate-200"
                }`}
              >
                <BatteryMedium className="w-3.5 h-3.5" />
                <span>Low-Power Mode: {isLowPowerMode ? "ON" : "OFF"}</span>
              </button>
            </div>
          </div>
        </aside>

        <main className="flex-1">
          {activeTab === "worker" && <WorkerPortal isLowPowerMode={isLowPowerMode} />}
          {activeTab === "dashboard" && <Dashboard />}
          {activeTab === "whatsapp" && <WhatsAppSimulator />}
        </main>

        <footer className="bg-slate-900 text-slate-400 text-xs py-4 px-4 text-center border-t border-slate-800">
          <p className="font-semibold">
            ShiftMitra AI &copy; 2026 – Multilingual Factory Worker Companion & Accountability Engine.
          </p>
        </footer>
      </div>
    </LanguageProvider>
  );
}
""",

    "shiftmitra/frontend/src/context/LanguageContext.jsx": """import React, { createContext, useContext, useState } from "react";
import { UI_STRINGS } from "../utils/translations";

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [lang, setLang] = useState("hi");

  const strings = UI_STRINGS[lang] || UI_STRINGS.hi;

  return (
    <LanguageContext.Provider value={{ lang, setLang, t: strings }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
""",

    "shiftmitra/frontend/src/utils/translations.js": """export const UI_STRINGS = {
  hi: {
    appName: "शिफ्टमित्र",
    workerTab: "श्रमिक साथी (Worker)",
    dashboardTab: "प्रबंधन डैशबोर्ड (Manager)",
    whatsappTab: "व्हाट्सएप बॉट (WhatsApp)",
    takePhoto: "नोटिस की फोटो लें",
    pickPreset: "नमूना दस्तावेज़ चुनें",
    listening: "सुन रहे हैं... बोलिए",
    speakBtn: "माइक दबाकर बोलें (30 सेकंड)",
    clearNotice: "समझ आ गया",
    clarifyNotice: "फिर से समझाएं",
    comprehensionTitle: "आप अपनी भाषा में बताएं: यह नोटिस क्या कह रहा है?",
    listenAudio: "आवाज़ में सुनें",
    history: "पुराने दस्तावेज़",
    actionHeader: "आपको क्या करना है:"
  },
  bn: {
    appName: "শিফ্টমিত্র",
    workerTab: "শ্রমিক পোর্টাল (Worker)",
    dashboardTab: "ম্যানেজমেন্ট ড্যাশবোর্ড (Manager)",
    whatsappTab: "হোয়াটসঅ্যাপ চ্যাট (WhatsApp)",
    takePhoto: "নোটিশের ছবি তুলুন",
    pickPreset: "নমুনা নোটিশ বেছে নিন",
    listening: "শুনছি... বলুন",
    speakBtn: "মাইক টিপে বলুন (৩০ সেকেন্ড)",
    clearNotice: "বুঝেছি",
    clarifyNotice: "আবার বোঝান",
    comprehensionTitle: "নিজের ভাষায় বলুন: এই নোটিশে কী বলা হয়েছে?",
    listenAudio: "মুখে শুনুন",
    history: "পূর্ববর্তী নোটিশ",
    actionHeader: "আপনাকে যা করতে হবে:"
  },
  en: {
    appName: "ShiftMitra",
    workerTab: "Worker Portal",
    dashboardTab: "Factory Dashboard",
    whatsappTab: "WhatsApp Simulator",
    takePhoto: "Snap Photo of Notice",
    pickPreset: "Choose Sample Notice",
    listening: "Listening... speak now",
    speakBtn: "Hold to Speak (Explain in 30s)",
    clearNotice: "I Understood",
    clarifyNotice: "Explain Again",
    comprehensionTitle: "Explain in your own words: What is this notice saying?",
    listenAudio: "Listen to Voice",
    history: "Past Documents",
    actionHeader: "Action Required:"
  }
};
""",

    "shiftmitra/frontend/src/utils/speechHelper.js": """export const speakText = (text, lang = "hi", onEnd = () => {}) => {
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
""",

    "shiftmitra/frontend/src/components/Navbar.jsx": """import React from "react";
import { useLanguage } from "../context/LanguageContext";
import { HardHat, BarChart3, MessageSquare, Globe } from "lucide-react";

export const Navbar = ({ activeTab, setActiveTab }) => {
  const { lang, setLang, t } = useLanguage();

  return (
    <header className="sticky top-0 z-50 bg-slate-900 text-white shadow-md">
      <div className="max-w-5xl mx-auto px-4 py-2.5 flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center space-x-2">
          <div className="bg-amber-500 p-1.5 rounded-lg text-slate-900 font-bold">
            <HardHat className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-1.5">
              ShiftMitra <span className="text-xs bg-amber-400 text-slate-900 px-1.5 py-0.5 rounded font-bold">AI</span>
            </h1>
            <p className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Factory Voice Companion</p>
          </div>
        </div>

        <div className="flex items-center space-x-1 bg-slate-800 p-1 rounded-xl">
          <button
            onClick={() => setActiveTab("worker")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
              activeTab === "worker" ? "bg-amber-500 text-slate-900 shadow" : "text-slate-300 hover:text-white"
            }`}
          >
            <HardHat className="w-4 h-4" />
            <span className="hidden sm:inline">{t.workerTab}</span>
            <span className="sm:hidden">Worker</span>
          </button>
          <button
            onClick={() => setActiveTab("dashboard")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
              activeTab === "dashboard" ? "bg-amber-500 text-slate-900 shadow" : "text-slate-300 hover:text-white"
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            <span className="hidden sm:inline">{t.dashboardTab}</span>
            <span className="sm:hidden">Dashboard</span>
          </button>
          <button
            onClick={() => setActiveTab("whatsapp")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
              activeTab === "whatsapp" ? "bg-emerald-500 text-white shadow" : "text-slate-300 hover:text-white"
            }`}
          >
            <MessageSquare className="w-4 h-4" />
            <span>WhatsApp</span>
          </button>
        </div>

        <div className="flex items-center space-x-1 text-xs">
          <Globe className="w-4 h-4 text-slate-400 mr-1" />
          {["hi", "bn", "en"].map((l) => (
            <button
              key={l}
              onClick={() => setLang(l)}
              className={`px-2 py-1 rounded font-bold uppercase transition ${
                lang === l ? "bg-amber-400 text-slate-950 font-black" : "text-slate-300 hover:bg-slate-800"
              }`}
            >
              {l === "hi" ? "हिन्दी" : l === "bn" ? "বাংলা" : "ENG"}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
};
""",

    "shiftmitra/frontend/src/components/WorkerPortal/IconBadge.jsx": """import React from "react";
import { AlertTriangle, ShieldCheck, IndianRupee, ShieldAlert, ArrowDownCircle, Sparkles } from "lucide-react";

export const IconBadge = ({ iconType, className = "w-6 h-6" }) => {
  switch (iconType) {
    case "helmet":
      return <ShieldAlert className={`${className} text-amber-600`} />;
    case "money":
      return <IndianRupee className={`${className} text-emerald-600`} />;
    case "danger":
      return <AlertTriangle className={`${className} text-rose-600`} />;
    case "deduction":
      return <ArrowDownCircle className={`${className} text-amber-700`} />;
    case "bonus":
      return <Sparkles className={`${className} text-blue-600`} />;
    default:
      return <ShieldCheck className={`${className} text-sky-600`} />;
  }
};
""",

    "shiftmitra/frontend/src/components/WorkerPortal/DocumentCapture.jsx": """import React, { useRef, useState } from "react";
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
""",

    "shiftmitra/frontend/src/components/WorkerPortal/ExplanationCard.jsx": """import React, { useState, useEffect } from "react";
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
""",

    "shiftmitra/frontend/src/components/WorkerPortal/ExplainBackLoop.jsx": """import React, { useState } from "react";
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
""",

    "shiftmitra/frontend/src/components/WorkerPortal/WorkerPortal.jsx": """import React, { useState, useEffect } from "react";
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
""",

    "shiftmitra/frontend/src/components/ManagementDashboard/AnalyticsCharts.jsx": """import React from "react";

export const AnalyticsCharts = ({ data }) => {
  const docTypes = Object.entries(data.docTypeBreakdown || {});
  const languages = Object.entries(data.languageBreakdown || {});

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
        <h3 className="font-bold text-slate-800 text-sm mb-4">
          दस्तावेज़ प्रकार और भ्रम दर (Docs Processed vs Clarified)
        </h3>
        <div className="space-y-3">
          {docTypes.map(([type, total]) => {
            const confused = (data.docTypeConfusion && data.docTypeConfusion[type]) || 0;
            const pct = total > 0 ? Math.round((confused / total) * 100) : 0;
            return (
              <div key={type}>
                <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                  <span>{type}</span>
                  <span>{total} docs ({pct}% confused)</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden flex">
                  <div
                    className="bg-emerald-500 h-full"
                    style={{ width: `${100 - pct}%` }}
                    title="Understood"
                  />
                  <div
                    className="bg-rose-500 h-full"
                    style={{ width: `${pct}%` }}
                    title="Needed Clarification"
                  />
                </div>
              </div>
            );
          })}
        </div>
        <div className="flex gap-4 text-[11px] font-bold text-slate-500 mt-4">
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 bg-emerald-500 rounded-full"></span> Understood
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 bg-rose-500 rounded-full"></span> Needed Clarification
          </span>
        </div>
      </div>

      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
        <h3 className="font-bold text-slate-800 text-sm mb-4">
          भाषा उपयोग विश्लेषण (Worker Language Distribution)
        </h3>
        <div className="flex items-center justify-around h-36">
          {languages.map(([langCode, count]) => {
            const langLabel = langCode === "hi" ? "Hindi" : langCode === "bn" ? "Bengali" : "English";
            const color = langCode === "hi" ? "bg-amber-400 text-slate-900" : langCode === "bn" ? "bg-sky-500 text-white" : "bg-purple-500 text-white";
            return (
              <div key={langCode} className="text-center">
                <div className={`w-16 h-16 rounded-2xl mx-auto flex items-center justify-center font-black text-xl shadow-sm ${color}`}>
                  {count}
                </div>
                <span className="text-xs font-bold text-slate-700 block mt-2">{langLabel}</span>
                <span className="text-[10px] text-slate-400">workers queried</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
""",

    "shiftmitra/frontend/src/components/ManagementDashboard/MisunderstoodTopicsTable.jsx": """import React from "react";
import { AlertTriangle, Download } from "lucide-react";

export const MisunderstoodTopicsTable = ({ topics = [], recentEvents = [] }) => {
  const exportCsv = () => {
    let csvContent = "data:text/csv;charset=utf-8,ID,DocumentType,Language,ClarificationNeeded,MissedPoints,Timestamp\\n";
    recentEvents.forEach((ev) => {
      csvContent += `${ev.id},"${ev.documentType}",${ev.language},${ev.clarificationNeeded},"${(ev.missedPoints || []).join(";")}",${ev.timestamp}\\n`;
    });
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `shiftmitra_confusion_report_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-bold text-slate-900 text-base">Top Misunderstood Worker Topics</h3>
          <p className="text-xs text-slate-500">Aggregated from Explain-Back comprehension checks</p>
        </div>
        <button
          onClick={exportCsv}
          className="flex items-center gap-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold px-3 py-2 rounded-xl transition"
        >
          <Download className="w-4 h-4" />
          <span>Export CSV</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="border border-slate-200 rounded-xl overflow-hidden">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 font-bold uppercase text-[10px] border-b border-slate-200">
              <tr>
                <th className="p-3">Topic / Rule</th>
                <th className="p-3 text-right">Workers Confused</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {topics.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50">
                  <td className="p-3 font-semibold text-slate-800 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0" />
                    <span className="capitalize">{item.topic.replace("_", " ")}</span>
                  </td>
                  <td className="p-3 text-right font-bold text-rose-600">{item.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="border border-slate-200 rounded-xl overflow-hidden">
          <div className="bg-slate-50 p-2.5 text-[11px] font-bold uppercase text-slate-500 border-b border-slate-200">
            Recent Explain-Back Verifications
          </div>
          <div className="divide-y divide-slate-100 max-h-56 overflow-y-auto">
            {recentEvents.map((ev) => (
              <div key={ev.id} className="p-2.5 flex items-center justify-between text-xs">
                <div>
                  <span className="font-bold text-slate-800">{ev.documentType}</span>
                  <span className="ml-2 text-[10px] uppercase font-semibold text-slate-400">({ev.language})</span>
                </div>
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-black uppercase ${
                    ev.clarificationNeeded ? "bg-rose-100 text-rose-700" : "bg-emerald-100 text-emerald-700"
                  }`}
                >
                  {ev.clarificationNeeded ? "Clarified" : "Understood"}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
""",

    "shiftmitra/frontend/src/components/ManagementDashboard/Dashboard.jsx": """import React, { useEffect, useState, useMemo } from "react";
import { AlertOctagon, CheckCircle2, FileText, Users, RefreshCw, Filter } from "lucide-react";
import { AnalyticsCharts } from "./AnalyticsCharts";
import { MisunderstoodTopicsTable } from "./MisunderstoodTopicsTable";

export const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedLanguage, setSelectedLanguage] = useState("all");

  const fetchSummary = async () => {
    try {
      const res = await fetch("/api/analytics/summary");
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error("Dashboard Fetch Error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSummary();
    const interval = setInterval(fetchSummary, 6000);
    return () => clearInterval(interval);
  }, []);

  const filteredEvents = useMemo(() => {
    if (!data?.recentEvents) return [];
    return data.recentEvents.filter((ev) => {
      if (selectedLanguage !== "all" && ev.language !== selectedLanguage) return false;
      return true;
    });
  }, [data, selectedLanguage]);

  if (loading || !data) {
    return (
      <div className="p-16 text-center text-slate-500 flex flex-col items-center justify-center gap-3">
        <RefreshCw className="w-8 h-8 animate-spin text-amber-500" />
        <span className="font-bold text-sm text-slate-700">फैक्ट्री डेटा लोड हो रहा है...</span>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Live Factory Monitoring</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight mt-0.5">
            Confusion Logging Dashboard
          </h2>
          <p className="text-xs sm:text-sm text-slate-500">
            Real-time verified comprehension analytics across safety mandates, notices, and payslips
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center gap-1.5 bg-white border border-slate-300 rounded-xl px-2.5 py-1.5 shadow-2xs">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="text-xs font-bold text-slate-800 bg-transparent focus:outline-none cursor-pointer"
            >
              <option value="all">All Languages</option>
              <option value="hi">Hindi (हिन्दी)</option>
              <option value="bn">Bengali (বাংলা)</option>
              <option value="en">English</option>
            </select>
          </div>

          <button
            type="button"
            onClick={fetchSummary}
            className="flex items-center gap-1.5 text-xs font-bold bg-white border border-slate-300 px-3 py-2 rounded-xl shadow-2xs hover:bg-slate-50 text-slate-800 transition active:scale-95"
          >
            <RefreshCw className="w-3.5 h-3.5 text-slate-600" />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3.5 mb-6">
        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs">
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider">Total Scans</div>
          <div className="text-3xl font-black text-slate-900 mt-1.5 flex items-center justify-between">
            {data.totalProcessed}
            <div className="p-2 bg-amber-50 rounded-xl text-amber-600">
              <FileText className="w-5 h-5" />
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs">
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider">Confusion Rate</div>
          <div className="text-3xl font-black text-rose-600 mt-1.5 flex items-center justify-between">
            {data.confusionRate}%
            <div className="p-2 bg-rose-50 rounded-xl text-rose-600">
              <AlertOctagon className="w-5 h-5" />
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs">
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider">First-Time Pass</div>
          <div className="text-3xl font-black text-emerald-600 mt-1.5 flex items-center justify-between">
            {100 - data.confusionRate}%
            <div className="p-2 bg-emerald-50 rounded-xl text-emerald-600">
              <CheckCircle2 className="w-5 h-5" />
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs">
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider">Active Dialects</div>
          <div className="text-3xl font-black text-blue-600 mt-1.5 flex items-center justify-between">
            {Object.keys(data.languageBreakdown || {}).length}
            <div className="p-2 bg-blue-50 rounded-xl text-blue-600">
              <Users className="w-5 h-5" />
            </div>
          </div>
        </div>
      </div>

      <AnalyticsCharts data={data} />
      <MisunderstoodTopicsTable topics={data.topMisunderstoodTopics} recentEvents={filteredEvents} />
    </div>
  );
};
""",

    "shiftmitra/frontend/src/components/WhatsAppSimulator/WhatsAppSimulator.jsx": """import React, { useState, useRef, useEffect } from "react";
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
"""
}

def main():
    print("==================================================")
    print("   ShiftMitra – Creating Local Folder & ZIP File  ")
    print("==================================================")

    # 1. Write all files to disk
    created_count = 0
    for relative_path, content in FILES.items():
        folder = os.path.dirname(relative_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(relative_path, "w", encoding="utf-8") as f:
            f.write(content)
        created_count += 1
        print(f"  [+] Created: {relative_path}")

    # 2. Package everything into shiftmitra.zip
    zip_filename = "shiftmitra.zip"
    print(f"\nPackaging files into '{zip_filename}'...")
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("shiftmitra"):
            dirs[:] = [d for d in dirs if d not in ("node_modules", ".vite", "dist", "build", ".git")]
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, start=".")
                zipf.write(full_path, arcname)

    zip_size_kb = os.path.getsize(zip_filename) / 1024
    print(f"SUCCESS: Created '{zip_filename}' ({zip_size_kb:.1f} KB) with {created_count} files.")
    print("\nNext steps to run locally:")
    print("  1. cd shiftmitra")
    print("  2. npm run install:all")
    print("  3. npm run dev")
    print("  4. Open http://localhost:3000 in your browser.")
    print("==================================================")

if __name__ == "__main__":
    main()
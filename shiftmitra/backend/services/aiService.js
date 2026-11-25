export const generateExplanation = async ({ rawText, targetLang = "hi" }) => {
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

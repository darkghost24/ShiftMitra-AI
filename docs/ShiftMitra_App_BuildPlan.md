# ShiftMitra – Factory Worker’s AI Companion  
Detailed Build Plan for Hackathon Prototype

---

## 1. Problem Statement

Migrant and contract factory workers in India routinely receive important information (safety instructions, payslips, HR notices, policy updates) through printed posters, WhatsApp images, and formal documents that:

- Are written in complex language (often English / Hindi or local “official” style) that workers don’t fully understand.
- Assume workers can read fluently, even if many are semi-literate or literate only in their native language.
- Prioritize documentation and compliance rather than verified understanding.
- Provide no feedback loop to management about what workers are actually confused about.

As a result:

- Workers follow unsafe practices because they misunderstand or never fully grasp safety notices.
- Payslip disputes and mistrust increase when workers don’t understand deductions, overtime, and benefits.
- Factories think they have “communicated” (posters sent, trainings done) but have no accountability metric that proves workers really understood.

There is currently no simple, low-friction tool for workers to **capture any notice/payslip/poster** and get a **voice-first, language-appropriate explanation**, combined with an **“explain-back loop”** that confirms understanding and aggregates confusion for management.

---

## 2. Solution Overview

**ShiftMitra** is a voice-first mobile and WhatsApp assistant for factory workers.

Core idea:
- Workers **snap a photo** of a notice, payslip, or poster from the ShiftMitra app **or** **forward it via WhatsApp**.
- The app uses **OCR + translation + generative AI** to:
  - Extract the text,
  - Interpret it,
  - Explain it back in the worker’s **chosen language** using **audio, simple text, and icons**.
- After explaining, ShiftMitra asks the worker to **re-explain in their own words** (voice).
  - Speech-to-text + simple concept checks detect misunderstandings.
  - The worker immediately gets clarifications.
- An anonymized **Confusion Logging Dashboard** shows factories which topics and documents workers often misunderstand, enabling targeted retraining and better communication.

The solution is optimized for:

- **Low-power smartphones** and **low bandwidth**.
- **WhatsApp-native usage** for minimal learning curve.
- **Multiple Indian languages** and voice-based interactions for low literacy users.

---

## 3. Target Users

### Primary Users: Factory Workers (Migrant/Contract)

- Age: 18–45; often migrants from other states.
- Devices: Low-cost Android smartphones; heavy WhatsApp usage.
- Constraints:
  - Limited literacy and/or literacy only in native language.
  - Limited data packs, unstable network (factory areas, dorms).
  - Irregular shifts; use in short breaks.
- Needs:
  - To **understand** safety instructions, shift changes, company policies, payslips, and benefits clearly.
  - To **ask questions safely** without fear of retaliation.
  - To get explanations in **native language**, via **voice** and **visual cues**.

### Secondary Users: Factory Management / HR / Safety Officers

- Needs:
  - Evidence that safety and policy communications are **truly understood**, not just posted.
  - Insight into **which topics and documents workers find confusing**.
  - Tools to design better training and communication materials.
  - Simple, privacy-preserving, aggregate analytics (not surveillance of individuals).

---

## 4. Key Features

All features are planned for the hackathon MVP (even if some are v1/lightweight implementations).

1. **Multilingual Document Interpretation**
   - Snap/Upload/Forward a photo of:
     - Safety posters, HR notices, shift schedules.
     - Payslips / salary breakdowns.
     - Policy documents (leave, overtime, ESI, PF, etc.).
   - Use OCR to extract text and perform translation to user’s selected language.
   - Use generative AI to convert raw text into **simplified explanations** with:
     - Plain-language summary,
     - Step-by-step breakdown (e.g., of payslip components),
     - Example scenarios.
   - Output via:
     - **Audio narration** in user’s language.
     - **Short, simple text** and **supporting icons**.

2. **Voice-Based Comprehension Checks (Explain-Back Loop)**
   - After explanation:
     - Prompt user: “Tell me in your own words: what is this notice asking you to do?”
   - Use speech-to-text to capture user’s explanation.
   - Run a lightweight concept check:
     - Compare key concepts the AI expects vs. what user said.
     - If misunderstanding detected, respond with:
       - Follow-up simple clarification and examples.
       - Option to replay or get a “very simple mode” explanation.
   - Store concept-level results (not raw audio) for analytics.

3. **WhatsApp Integration**
   - Workers can:
     - Send any image of a document to the ShiftMitra **WhatsApp Business number**.
     - Receive:
       - A text summary,
       - A link or inline audio note explanation,
       - Icon-based visual summary (e.g., simple generated JPEG card).
   - Backend processes WhatsApp messages via webhook:
     - Download image → OCR → translation → explanation → send result.
   - Maintains **low-friction adoption** since workers already use WhatsApp heavily.

4. **Confusion Logging Dashboard (For Management)**
   - Web-based, mobile-responsive dashboard.
   - Aggregated, anonymized data only:
     - Most frequently interpreted document types (e.g., payslips, safety posters).
     - Topics with high confusion (e.g., “OT calculation”, “PPE rules”).
     - Typical misunderstanding patterns (e.g., “Workers think this is optional”).
   - Basic views:
     - Timeline view: confusion topics by week/month.
     - Document type breakdown.
     - Language breakdown (where available).
   - Exportable as CSV / simple PDF snapshot.

5. **Icon-Based Explanations**
   - Use a small, consistent icon set to visually represent:
     - Money/salary, overtime, deduction, bonus.
     - Safety gear (helmet, gloves, mask).
     - Actions: “must do”, “do not do”, “danger”, “report”.
   - Explanations combine:
     - Short text bullets (in simple language),
     - Icons next to each bullet,
     - Optional color coding (green = OK, red = not allowed).
   - For very low literacy users, icons plus audio should carry most of the meaning.

6. **Low-Power Mode**
   - App design optimized for:
     - Low-end Android phones.
     - Spotty, low-bandwidth connectivity.
   - Strategies:
     - Compress images before upload.
     - Allow **deferred processing**: if offline, queue upload; process when online.
     - Lightweight UI; minimal animations.
     - Ability to replay cached recent explanations without re-calling the AI.
   - For WhatsApp users, low-power effect is natural: they already use a low-data messaging interface.

---

## 5. User Flow

### 5.1 Worker Flow – Mobile App (Android PWA or lightweight native)

**Scenario**: Worker receives a printed shift change notice on a board.

1. **Onboarding**
   - Worker installs app via shared link/QR or visits PWA.
   - Selects preferred language (e.g., Hindi, Bengali, Tamil, Telugu).
   - Optional: selects factory from a dropdown or enters code (for mapping analytics).

2. **Capture Document**
   - Home screen: two main big buttons:
     - “Take Photo of Notice / Payslip”
     - “History”
   - User taps “Take Photo”.
   - Camera opens with guidance overlay: “Center the full paper; tap to capture”.
   - User captures the photo and confirms “Use this photo”.

3. **Processing**
   - Show simple loading screen (text + icon) with progress.
   - Backend:
     - Runs OCR.
     - Detects language.
     - Translates to user’s selected language.
     - Passes to LLM to generate:
       - Short summary,
       - Detailed simple explanation,
       - Key points list.
   - App receives structured explanation payload.

4. **Explanation Output**
   - Screen layout:
     - Title: “This document is about: [e.g., Overtime Payment Rules]”
     - Audio play button: “Listen in [Language]”.
     - Text sections like:
       - “Main Point” – 1–2 simple sentences.
       - “Important for You” – bullet list, each with icon.
       - “What You Must Do / Not Do” – action-oriented bullets.
   - Worker taps Play:
     - TTS reads explanation in their language.

5. **Voice-Based Comprehension Check**
   - After audio ends (or user scrolls down), show:
     - “Tell me in your words: What is this saying?” (with mic icon).
   - When user taps mic:
     - Simple instruction: “Speak now; you have 30 seconds.”
     - Capture audio → speech-to-text on backend.
   - Backend:
     - Extracts key points from original explanation (e.g., “You must wear helmet in this area”, “If not, fine of ₹500”).
     - Compares with user text using simple semantic similarity or keyword checks.
   - If understanding is **good enough**:
     - Show green tick + audio:
       - “You understood this correctly. Good job!”
   - If **misunderstanding**:
     - Show clarification message:
       - “It sounds like you may have missed an important point. Let me explain again very simply.”
     - Provide a simpler, shorter audio + icon explanation highlighting missed points.

6. **Optional Feedback**
   - Quick 1-tap feedback: “Was this clear?” [Yes / No]
   - Optional voice feedback: “Anything still confusing? (Speak)”
   - Store theme (not raw text) as confusion signal.

7. **History**
   - Worker can see last 10–20 documents:
     - Thumbnail image,
     - Topic label,
     - Date/time,
     - Re-play explanation.

---

### 5.2 Worker Flow – WhatsApp

**Scenario**: Worker receives a payslip screenshot on WhatsApp.

1. Worker **forwards image** to ShiftMitra WhatsApp number.
2. Backend receives message via WhatsApp Business API webhook.
3. Backend:
   - Downloads image → OCR → translation → LLM explanation.
   - Chooses response format:
     - Short text summary in same chat.
     - “Listen to explanation” as an audio file or TTS-generated audio note.
4. Bot replies:
   - Text: “This looks like your payslip. Main points: 1) Your basic pay is … 2) Overtime is … 3) Deductions are …”
   - Audio note: full explanation.
   - Optional quick ask:
     - “Please reply with a voice message: In your own words, what did you understand?”
5. Worker responds with voice message.
6. Backend performs same **comprehension check**.
7. Bot sends:
   - “Yes, you understood correctly.” or
   - “Let me explain again in a simpler way.” plus new audio.

---

### 5.3 Management Flow – Confusion Logging Dashboard

**Scenario**: Safety Manager wants to assess if workers understand recent PPE policy.

1. Manager logs into web dashboard using email + OTP or factory code.
2. Home screen shows:
   - “Most misunderstood topics this month”.
   - Simple stats:
     - Total documents processed (by type).
     - % of sessions where a clarification was needed.
3. Manager clicks “Safety Notices”.
   - Sees:
     - Top 5 confusion themes (e.g., “Consequences of not wearing PPE”, “When helmets are mandatory”).
     - Trend line of confusion over time.
4. Manager filters by **language** (e.g., Bengali workers show higher confusion).
5. Manager exports CSV/PDF to discuss with HR and plan training.

---

## 6. Technical Approach

### 6.1 Overall Architecture

- **Client**:
  - Android-friendly web app (PWA) or lightweight Android app (React Native or Flutter).
  - WhatsApp interface via WhatsApp Business API.
- **Backend**:
  - REST API server (e.g., Node.js/Express or Python/FastAPI).
  - OCR + text processing service.
  - AI service integrating:
    - OCR → language detection → translation → LLM-based explanation.
    - Speech-to-text → comprehension/semantic checks.
- **Database**:
  - Relational DB (PostgreSQL) or managed (Supabase/Firebase).
- **Dashboard**:
  - Web app using React/Vue + charting library (Chart.js/Recharts).

### 6.2 OCR & Translation

- For hackathon:
  - Use a managed OCR API (e.g., Google Cloud Vision, AWS Textract, or Tesseract via a wrapper).
  - Language detection: simple library (e.g., `franc` or inbuilt from translation API).
  - Translation: use provider like Google Translate API or Azure Translator.

**Flow:**
1. Image uploaded or received from WhatsApp.
2. OCR returns extracted text (and optionally layout).
3. Language detection to know source language.
4. Translate to the user’s target language if needed.
5. Send structured text to LLM for explanation.

### 6.3 Generative AI for Explanations

- Use an LLM via API (OpenAI / Anthropic / local model via hosted provider).
- Prompt pattern:
  - Provide:
    - Raw OCR text,
    - Detected document type hint (payslip, safety poster, etc.),
    - Target language,
    - Output schema (JSON).
  - Ask for:
    - `title`,
    - `short_summary`,
    - `detailed_explanation`,
    - `key_points` with `label`, `description`, `importance_level`, `icon_type`.
- Backend converts JSON output into:
  - Text for display,
  - Script for TTS.

### 6.4 Voice – TTS and STT

- **Speech-to-Text (STT)**:
  - Use Google Speech-to-Text, Azure Speech, or Whisper API.
  - Configure model for Indian languages (Hindi, Tamil, Telugu, Bengali, etc.).
- **Text-to-Speech (TTS)**:
  - Use Google Cloud Text-to-Speech or similar with natural voices.
  - Generate audio files from explanation text.

For hackathon:
- Focus on 2–3 major languages (e.g., Hindi, Bengali, Tamil) with clear config.

### 6.5 Comprehension Check Logic

Lightweight, hackathon-friendly approach:

1. From original LLM explanation, extract 3–5 “must understand” key points.
2. Convert each key point into a simple **keyword set** or short phrase in the user language.
3. From STT result (user’s re-explanation), run:
   - Fuzzy keyword matching (string contains/similarity).
   - Or use an LLM with a structured prompt:
     - “Here are the key points. Here is the user explanation. For each key point, say YES/NO whether user conveyed it.”
4. Aggregate:
   - If user hits ≥ X of key points (e.g., ≥ 60%), mark as “understood”.
   - Else mark as “needs clarification”.
5. For “needs clarification”:
   - Ask LLM to generate a **simple re-explanation** focusing on missed points.
6. Log:
   - Document ID/type.
   - Language.
   - Which key points were missed (for analytics).

### 6.6 WhatsApp Integration

- Register WhatsApp Business number.
- Use provider (e.g., Meta Cloud API, Twilio, Gupshup) for WhatsApp API.
- Implement webhook endpoint:
  - Receive inbound messages.
  - Distinguish text vs image.
  - For images:
    - Download file using media URL.
    - Pass through OCR and AI pipeline.
    - Respond with:
      - Text summary,
      - Audio file link/attachment.
  - For voice notes:
    - Download audio,
    - Run STT,
    - Run comprehension check pipeline.

### 6.7 Confusion Logging Dashboard

Backend:

- Store these fields (anonymized):
  - `session_id` (random),
  - `factory_id` (if set),
  - `document_type`,
  - `timestamp`,
  - `language`,
  - `needed_clarification` (bool),
  - `missed_key_points` (string array).
- Simple endpoints:
  - `/stats/summary?factory_id=...`
  - `/stats/topics?time_range=...`
  - `/stats/by-language?factory_id=...`

Frontend (React or similar):

- Components:
  - Stats cards: total docs, % confusion, top 3 topics.
  - Charts:
    - Line chart: confusion % over time.
    - Bar chart: confusion by document type.
    - Table: topics and confusion counts.

### 6.8 Icon-Based Explanations

- Prepare a small static icon set (SVG/PNG) mapped to `icon_type` keys:
  - `money`, `overtime`, `deduction`, `bonus`, `helmet`, `gloves`, `mask`, `danger`, `must_do`, `dont_do`, etc.
- LLM outputs `icon_type` for each key point.
- Frontend:
  - For each bullet, display associated icon + text.
- Ensure icons are:
  - High contrast.
  - Culturally intuitive where possible.

### 6.9 Low-Power Mode Considerations

- Client:
  - Implement as PWA or lightweight React Native app with:
    - Offline-first manifest where feasible.
    - Image compression via front-end library before upload (e.g., reduce to 1024px width, JPEG ~60–70% quality).
  - Avoid heavy libraries; basic CSS plus a minimal UI toolkit.
- Network:
  - Queue uploads and retries if network fails.
  - Limit repeated calls: store last N explanations locally (simple key-value).
- Backend:
  - Compress returned audio (e.g., MP3 @ 64 kbps).
  - Timeout settings and graceful fallback messages.

---

## 7. Success Metrics

To determine if ShiftMitra is working (especially in a pilot):

### 7.1 Worker-Level Metrics

- **Usage & Adoption**
  - # unique workers using app/WhatsApp bot per week.
  - # documents interpreted per worker per month.
- **Comprehension**
  - % of sessions where understanding is marked as “good enough” on first attempt vs after clarification.
  - Reduction in misunderstanding on second explanation (measure improvement).
- **Satisfaction**
  - Simple in-app feedback: % of sessions marked “Was this clear?” → “Yes”.
  - Qualitative: count/log of positive feedback vs confusion feedback.

### 7.2 Factory-Level Metrics

- **Communication Effectiveness**
  - Decrease in repeated questions about the same notice/policy (from HR/supervisors).
  - Reduction in reported incidents linked to misunderstanding (over time, for pilots).
- **Engagement with Dashboard**
  - # of logins by management per month.
  - # of actions taken (e.g., tagged topics, downloaded reports).
- **Confusion Trends**
  - Top confusion topics over time: are they changing/reducing after interventions?

### 7.3 Technical/Operational Metrics

- Average end-to-end response time:
  - From image upload to explanation delivered (target: < 15–20 seconds on 4G).
- Error rates:
  - OCR failure rate,
  - STT failure rate,
  - AI pipeline failure or fallback rate.
- Availability:
  - Uptime during pilot shifts.

---

## Hackathon Scope Recommendation

For the hackathon prototype, focus on:

1. **End-to-end happy path**:
   - Android web app: Take photo → OCR → explanation (text+audio) → basic voice comprehension check.
2. **WhatsApp integration (basic)**:
   - Forward image → get text summary back + basic audio (if feasible).
3. **Simple confusion logging**:
   - Store session metadata.
   - Simple dashboard with basic charts (confusion by document type).
4. **At least 2 Indian languages**:
   - Hindi + one more (e.g., Bengali or Tamil) to demonstrate multilingual capability.
5. **Icon framework**:
   - Hardcode icon mappings + show in explanations.

This will be enough to demo the core value:  
**Workers can snap or forward a document, hear a simple explanation in their language, validate their understanding via an explain-back loop, and management can see where communication fails.**
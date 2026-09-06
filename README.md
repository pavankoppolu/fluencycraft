# 🌟 FluencyCraft — Practical Everyday English Mastery Studio

Welcome to **FluencyCraft**! FluencyCraft is an automated, AI-driven daily English learning platform created to turn language practice into a **warm, empowering, and effortless 6–8 minute daily ritual**.

Rather than abstract textbook rules or software jargon, FluencyCraft grounds every lesson in **real-life daily living scenarios**—grocery shopping, clinic visits, commuting in autos/cabs, talking to neighbors, handling delivery calls, and family routines. 

Whether you are a student, working professional, homemaker, or job seeker, FluencyCraft gives you the practical tools and instant confidence to speak and write natural English every single day.

---

## 💡 Why FluencyCraft? (Core Vision & Benefits)

Language fluency is built through **consistent, real-world micro-practice**:

- 🎯 **Everyday Scenarios:** Learn phrases you use every day (e.g., *"Run errands"*, *"Drop me off near the bus stand"*, *"On an empty stomach"*, *"Out of stock"*).
- 🇮🇳 ➔ 🇬🇧 **Eliminate "Telugu-isms":** Real-time AI feedback correcting direct literal translations (e.g., changing *"To me headache is there"* into natural *"I have a slight headache"*).
- ⚡ **Instant Micro-Feedback:** Get immediate grammatical reasoning the exact second you select an answer.
- 🔒 **Answer Choice Locking:** Answers lock automatically upon selection to ensure focused learning.
- 🔊 **Native Auditory Speech Prompts:** Listen to real-world audio scenarios using browser-native Web Speech Synthesis (`SpeechSynthesisUtterance`).
- ⏰ **Automated Daily Pipeline:** Fresh 20-question HTML tests generated automatically every morning at **7:00 AM IST** powered by **Gemini AI** and **GitHub Actions**.

---

## 🔗 How to Access the Tests (With Direct Links & Examples)

FluencyCraft provides standalone interactive **HTML test pages** for every level. `latest.html` automatically points to the most recently generated test for that track.

### 🏠 Main Course Landing Page
- **Course Overview & Level Direct Links:** [https://fluencycraft.vercel.app](https://fluencycraft.vercel.app)

### 🎓 Interactive HTML Test Links

| Level / Track | Latest Test URL (`latest.html`) | Day 1 Test URL (`day-01.html`) |
| :--- | :--- | :--- |
| **Level 1: Everyday Essentials** (Beginner) | [tests/beginner/latest.html](https://fluencycraft.vercel.app/tests/beginner/latest.html) | [tests/beginner/day-01.html](https://fluencycraft.vercel.app/tests/beginner/day-01.html) |
| **Level 2: Workplace Communication** (Intermediate) | [tests/intermediate/latest.html](https://fluencycraft.vercel.app/tests/intermediate/latest.html) | [tests/intermediate/day-01.html](https://fluencycraft.vercel.app/tests/intermediate/day-01.html) |
| **Level 3: Executive Leadership** (Advanced) | [tests/advanced/latest.html](https://fluencycraft.vercel.app/tests/advanced/latest.html) | [tests/advanced/day-01.html](https://fluencycraft.vercel.app/tests/advanced/day-01.html) |

---

## 📁 Repository Directory Structure

```
fluencycraft/
├── tests/
│   ├── beginner/
│   │   ├── day-01.html
│   │   └── latest.html
│   ├── intermediate/
│   │   ├── day-01.html
│   │   └── latest.html
│   └── advanced/
│       ├── day-01.html
│       └── latest.html
├── api/
│   └── evaluate.js
├── scripts/
│   ├── curriculum.json
│   └── generate_daily_tests.py
├── .github/workflows/
│   └── daily_tests.yml
├── index.html
├── beginner.html
└── vercel.json
```

---

## 📋 The 5-Part Daily Living Flow (20 Questions per Day)

```
┌──────────────────────────────────────────────────────────────┐
│  🌟 Word of the Day & Everyday Phrase                        │
│  "Run errands" • Meaning, audio pronunciation, & usage       │
├──────────────────────────────────────────────────────────────┤
│  📘 Today's Concept Focus & Why It Is Important               │
│  Explains target grammar, phrasal verbs, & practical value   │
├──────────────────────────────────────────────────────────────┤
│  1. Daily Routine & Habits (4 MCQs)                          │
│     Real conversations at home, work, or outdoors            │
├──────────────────────────────────────────────────────────────┤
│  2. Everyday Vocabulary & Word Match (4 MCQs)                │
│     Practical terms ("Out of stock", "Running late", etc.)   │
├──────────────────────────────────────────────────────────────┤
│  3. Listening to Spoken English (4 Audio Clips)              │
│     Natural dialogues with 🔊 Listen audio buttons           │
├──────────────────────────────────────────────────────────────┤
│  4. Polite Social Expressions & Etiquette (4 MCQs)           │
│     How to request, say no politely, or ask directions     │
├──────────────────────────────────────────────────────────────┤
│  5. Real-Life Telugu ➔ English Translation (4 Scenarios)     │
│     Everyday Telugu sentences translated to natural English  │
│     with AI feedback on avoiding "Telugu-isms"               │
└──────────────────────────────────────────────────────────────┘
```

---

## 🗓️ 7-Day Universal Everyday Life Curriculum Roadmap

| Day & Theme | Everyday Scenario | Target Vocabulary | Telugu ➔ Natural English Context |
| :--- | :--- | :--- | :--- |
| **Day 1: Morning & Home Routines** | Waking up, tea, getting kids ready | Early riser, freshen up, tidy up | *"నేను సాధారణంగా ఉదయం 6 గంటలకే నిద్రలేచి..."* ➔ *"I usually wake up at 6:00 AM and have a cup of tea."* |
| **Day 2: Market & Grocery Shopping** | Supermarkets, vegetables, billing | Out of stock, ripe/fresh, receipt | *"ఈ టమాటాలు కేజీ ఎంత? కొంచెం తాజావి ఏరి ఇవ్వండి."* ➔ *"How much are these tomatoes per kilo? Please pick out fresh ones for me."* |
| **Day 3: Travel, Autos & Cabs** | Booking rides, fares, directions | Drop me off, take a right, fare | *"అన్నా, బస్టాండ్ దగ్గర డ్రాప్ చేయండి, ఎంత అవుతుంది?"* ➔ *"Please drop me off near the bus stand. How much is the fare?"* |
| **Day 4: Clinic & Health Visits** | Doctor symptoms, pharmacy | Sore throat, dizzy, prescription | *"రెండు రోజుల నుండి కొంచెం జ్వరంగా ఉంది..."* ➔ *"I've had a mild fever for two days. Which medication should I take?"* |
| **Day 5: Polite Social Manners** | Inviting neighbors, offering food | Drop by, lend a hand, I'd love to | *"సాయంత్రం మా ఇంటికి రండి..."* ➔ *"Please drop by our home this evening; we can all have tea together."* |
| **Day 6: Phone Calls & Deliveries** | Delivery agents, customer service | Pick up, parcel, check status | *"నా పార్సెల్ ఈ రోజు సాయంత్రానికి డెలివరీ అవుతుందా?"* ➔ *"Will my package be delivered by this evening?"* |
| **Day 7: Weekend Plans & Weather** | Movies, eating out, weather talk | Grab a bite, catch up, call it a day | *"ఈ వారాంతంలో మనం బయటకు వెళ్లి..."* ➔ *"Shall we go out and watch a movie this weekend?"* |

---

## ☕ Daily Routine Integration

1. ☀️ **Morning Tea Ritual (7:00 AM IST):** Open [FluencyCraft](https://fluencycraft.vercel.app) while enjoying morning tea.
2. 👤 **Set Learner Name:** Type your name (`e.g., Pavan`) in the header field.
3. 🌟 **Review Word of the Day & Concept Focus:** Absorb the daily phrase and understand why today's concept matters.
4. 🔊 **Listen & Answer:** Tap **🔊 Listen** on audio clips, answer questions, and absorb instant AI reasoning.
5. 🗣️ **Speak Out Loud:** Practice the polished natural English versions in Section 5 out loud.

---

## 🌐 Live Production Links

- 🌐 **Live Web Application:** **[https://fluencycraft.vercel.app](https://fluencycraft.vercel.app)**
- 🐙 **GitHub Repository:** [https://github.com/pavankoppolu/fluencycraft](https://github.com/pavankoppolu/fluencycraft)

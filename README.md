# 🌟 FluencyCraft — Apple Glass Practical English Mastery Studio

Welcome to **FluencyCraft**! FluencyCraft is an automated, AI-driven daily English learning platform created to turn language practice into an **Apple-inspired, high-aesthetic 6–8 minute daily ritual**.

Crafted with a sleek **Apple Glassmorphism UI** (frosted translucent glass cards, background glow meshes, and fluid micro-animations), FluencyCraft delivers 20 fresh, real-life daily scenario questions every morning at **7:00 AM IST**.

---

## 💡 Why FluencyCraft? (Core Vision)

Language fluency is built through consistent everyday micro-practice, not abstract textbook rules.

- 🎯 **Everyday Scenarios:** Learn natural expressions for grocery shopping, clinic visits, cab rides, phone calls, and family routines.
- 🇮🇳 ➔ 🇬🇧 **Eliminate "Telugu-isms":** Real-time AI feedback translating everyday Telugu thoughts into polished, natural English sentences.
- ⚡ **Instant Micro-Feedback:** Immediate grammatical reasoning the exact second you select an option.
- 🔒 **Option Choice Locking:** Answers lock automatically upon selection to ensure focused learning.
- ⏰ **Automated Daily Pipeline:** Powered by **Gemini AI** & **GitHub Actions** running daily at **7:00 AM IST**.

---

## 📁 Repository & Test File Structure

All daily test datasets are organized cleanly under the parent **`tests/`** directory:

```
fluencycraft/
├── tests/
│   ├── beginner/
│   │   ├── day-01.json
│   │   ├── day-02.json
│   │   └── latest.json
│   ├── intermediate/
│   │   ├── day-01.json
│   │   ├── day-02.json
│   │   └── latest.json
│   └── advanced/
│       ├── day-01.json
│       ├── day-02.json
│       └── latest.json
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

## 🔗 How to Access Tests (With Examples)

You can access FluencyCraft tests both interactively via the web UI and programmatically via direct JSON API endpoints.

### 1. Interactive Web Interface
- **Main Web Studio:** [https://fluencycraft.vercel.app](https://fluencycraft.vercel.app)
- **Beginner Studio Standalone:** [https://fluencycraft.vercel.app/beginner](https://fluencycraft.vercel.app/beginner)

### 2. Direct JSON Test Endpoints & API Examples

| Level / Track | Endpoint | Description |
| :--- | :--- | :--- |
| **Beginner (Latest)** | `https://fluencycraft.vercel.app/tests/beginner/latest.json` | Fetches today's latest 20-question test for beginner level |
| **Beginner (Day 1)** | `https://fluencycraft.vercel.app/tests/beginner/day-01.json` | Accesses specific Day 1 test dataset |
| **Intermediate (Latest)** | `https://fluencycraft.vercel.app/tests/intermediate/latest.json` | Fetches today's latest test for intermediate track |
| **Advanced (Latest)** | `https://fluencycraft.vercel.app/tests/advanced/latest.json` | Fetches today's latest test for advanced track |

#### 💻 cURL Example
```bash
# Fetch latest beginner test dataset
curl -s https://fluencycraft.vercel.app/tests/beginner/latest.json
```

#### 🌐 JavaScript Fetch Example
```javascript
// Fetch latest test programmatically in your frontend app
async function getTodayTest(level = 'beginner') {
  const response = await fetch(`https://fluencycraft.vercel.app/tests/${level}/latest.json`);
  const data = await response.json();
  console.log("Today's Title:", data.title);
  console.log("Word of the Day:", data.word_of_the_day.word);
  console.log("Questions Count:", data.questions.length);
}

getTodayTest('beginner');
```

---

## 📋 The 5-Part Daily Living Flow (20 Questions)

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
| **Day 1: Morning & Home Routines** | Waking up, tea, kids | Early riser, freshen up, tidy up | *"నేను సాధారణంగా ఉదయం 6 గంటలకే నిద్రలేచి..."* ➔ *"I usually wake up at 6:00 AM and have a cup of tea."* |
| **Day 2: Market & Grocery Shopping** | Supermarkets, vegetables, billing | Out of stock, ripe/fresh, receipt | *"ఈ టమాటాలు కేజీ ఎంత? కొంచెం తాజావి ఏరి ఇవ్వండి."* ➔ *"How much are these tomatoes per kilo? Please pick out fresh ones for me."* |
| **Day 3: Travel, Autos & Cabs** | Booking rides, fares, directions | Drop me off, take a right, fare | *"అన్నా, బస్టాండ్ దగ్గర డ్రాప్ చేయండి, ఎంత అవుతుంది?"* ➔ *"Please drop me off near the bus stand. How much is the fare?"* |
| **Day 4: Clinic & Health Visits** | Doctor symptoms, pharmacy | Sore throat, dizzy, prescription | *"రెండు రోజుల నుండి కొంచెం జ్వరంగా ఉంది..."* ➔ *"I've had a mild fever for two days. Which medication should I take?"* |
| **Day 5: Polite Social Manners** | Inviting neighbors, offering food | Drop by, lend a hand, I'd love to | *"సాయంత్రం మా ఇంటికి రండి..."* ➔ *"Please drop by our home this evening; we can all have tea together."* |
| **Day 6: Phone Calls & Deliveries** | Delivery agents, customer service | Pick up, parcel, check status | *"నా పార్సెల్ ఈ రోజు సాయంత్రానికి డెలివరీ అవుతుందా?"* ➔ *"Will my package be delivered by this evening?"* |
| **Day 7: Weekend Plans & Relaxation** | Movies, eating out, weather | Grab a bite, catch up, call it a day | *"ఈ వారాంతంలో మనం బయటకు వెళ్లి..."* ➔ *"Shall we go out and watch a movie this weekend?"* |

---

## ☕ Daily Routine Integration

1. ☀️ **Morning Tea Ritual (7:00 AM IST):** Open [FluencyCraft](https://fluencycraft.vercel.app) while enjoying morning tea.
2. 🌟 **Review Word of the Day & Concept Focus:** Absorb the daily phrase and understand why today's concept matters.
3. 🔊 **Listen & Answer:** Tap **🔊 Listen** on audio clips, answer questions, and absorb instant AI reasoning.
4. 🗣️ **Speak Out Loud:** Practice the polished natural English versions in Section 5 out loud.

---

## 🌐 Live Production Links

- 🌐 **Live Web Application:** **[https://fluencycraft.vercel.app](https://fluencycraft.vercel.app)**
- 🐙 **GitHub Repository:** [https://github.com/pavankoppolu/fluencycraft](https://github.com/pavankoppolu/fluencycraft)

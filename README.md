# 🚀 FluencyCraft — AI-Powered Daily English Mastery Studio

Welcome to **FluencyCraft**! FluencyCraft is an automated, AI-driven English practice platform designed to transform language learning into a seamless, high-impact daily habit. Powered by **Gemini AI**, **GitHub Actions**, and **Vercel**, FluencyCraft delivers fresh 20-question diagnostic and practice tests across three progressive skill tracks every morning at **7:00 AM IST**.

---

## 🎯 Project Goal

The primary goal of FluencyCraft is to bridge the gap between textbook English and real-world fluency. Whether you are building everyday conversational confidence, mastering workplace standup communication, or negotiating high-stakes executive decisions, FluencyCraft provides structured, daily micro-learning scenarios tailored to your level.

---

## 🌟 Key Benefits & Interactive Features

- ⚡ **Instant Real-Time Feedback:** Get score metrics and detailed grammatical explanations immediately upon submitting any question or full test.
- 🔊 **Native Auditory Speech Prompts:** Listen to real-world audio scenarios using browser-native Web Speech Synthesis (`SpeechSynthesisUtterance`).
- 🤖 **Automated Daily Refresh:** 20 fresh questions generated every single day at **7:00 AM IST** without manual intervention.
- 📈 **3 Progressive Skill Tracks:** Seamlessly transition from foundational everyday English to advanced executive diplomacy.
- 📱 **Clean & Responsive UI:** Designed with modern aesthetics, glassmorphism accents, and accessible touch-friendly controls.

---

## 🗺️ Learning Tracks & Where to Start

Choose your starting track on the landing page based on your current goal:

| Track | Target Audience | Key Skills Tested |
| :--- | :--- | :--- |
| **Level 1: Everyday Essentials** (Beginner) | Learners building daily confidence | Family routines, daily habits, polite requests, simple past tenses, basic listening prompts. |
| **Level 2: Workplace Communication** (Intermediate) | Professionals & team members | Standup sync updates, reporting completed actions, Slack/email etiquette, meeting phrasing. |
| **Level 3: Executive Leadership** (Advanced) | Team leads, managers & executives | Strategic stakeholder negotiation, passive/active syntax precision, tone nuance, diplomacy. |

👉 **Where to start:** Simply visit [FluencyCraft on Vercel](https://fluencycraft.vercel.app), choose your level tab, and start answering today's 20 questions!

---

## ⏰ How to Make FluencyCraft Part of Your Daily Routine

Building fluency requires consistent, low-friction daily practice. Here is how you can make FluencyCraft a daily habit:

1. ☕ **Morning Routine (7:00 AM IST):** Set a morning reminder to spend 5–10 minutes on today's test right after morning tea or breakfast.
2. 🔊 **Active Listening Practice:** Always click the **🔊 Listen** button on auditory scenario questions to train your auditory recognition and tone perception.
3. 📝 **Review Explanations:** Read the explanations for incorrect *and* correct answers to solidify grammar rules and professional context.
4. 🔁 **Track Your Score:** Aim to improve your percentage daily and progress to the next level track once you consistently score 90%+.

---

## 🛠️ Architecture & Tech Stack

- **Frontend:** HTML5, Modern CSS3 (Vanilla design tokens, CSS grid/flexbox, custom properties), JavaScript (ES6+).
- **Audio Engine:** Web Speech API (`window.speechSynthesis`).
- **AI Test Generator:** Python (`scripts/generate_daily_tests.py`) leveraging **Gemini API** (`GEMINI_API_KEY`).
- **Automation Pipeline:** GitHub Actions ([daily_tests.yml](.github/workflows/daily_tests.yml)) scheduled for `30 1 * * *` (7:00 AM IST).
- **Backend & Deployment:** Vercel Serverless Functions ([api/evaluate.js](api/evaluate.js)) & Vercel Web Hosting.

---

## 🚀 Local Development & Setup

If you want to run or contribute to FluencyCraft locally:

```bash
# 1. Clone the repository
git clone https://github.com/pavankoppolu/fluencycraft.git
cd fluencycraft

# 2. Set your Gemini API key (optional for local generation)
export GEMINI_API_KEY="your_api_key_here"

# 3. Generate daily test datasets locally
python scripts/generate_daily_tests.py

# 4. Serve the static site locally
python -m http.server 8000
```
Open `http://localhost:8000` in your browser to view the application!

---

## 📬 Live Links & Deployment

- 🌐 **Live Web Application:** [https://fluencycraft.vercel.app](https://fluencycraft.vercel.app)
- 🐙 **GitHub Repository:** [pavankoppolu/fluencycraft](https://github.com/pavankoppolu/fluencycraft)

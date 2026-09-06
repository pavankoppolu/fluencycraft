#!/usr/bin/env python3
import os
import sys
import json
import re
from datetime import datetime

CURRICULUM_PATH = os.path.join(os.path.dirname(__file__), "curriculum.json")

def load_curriculum():
    if os.path.exists(CURRICULUM_PATH):
        with open(CURRICULUM_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def generate_20_questions(level):
    curriculum = load_curriculum()
    roadmap = curriculum.get("curriculum_roadmap", [{}])
    words_of_day = curriculum.get("words_of_the_day", [{}])

    theme_info = roadmap[0] if roadmap else {
        "theme": "Morning & Home Routines",
        "scenario": "Waking up, making tea/breakfast, getting kids ready",
        "vocabulary": ["Early riser", "Freshen up", "Running late", "Tidy up"],
        "connecting_pillars": ["Short and sweet", "Bits and pieces", "Safe and sound", "Spick and span"],
        "concept_overview": "Day 1: Everyday Home Routines, Phrasal Verbs & Connecting Pillars",
        "why_important": "Mastering daily routine expressions and connecting pillars (like 'short and sweet') helps you express thoughts naturally without hesitation during everyday conversations.",
        "telugu_translation": {
            "telugu": "నేను సాధారణంగా ఉదయం 6 గంటలకే నిద్రలేచి, ఒక కప్పు టీ తాగుతాను.",
            "literal": "I generally in morning at 6 clock wake up and drink one cup tea.",
            "polished": "I usually wake up at 6:00 AM and have a cup of tea.",
            "feedback": "In English, say 'have a cup of tea' and specify time as '6:00 AM'."
        }
    }

    word_info = words_of_day[0] if words_of_day else {
        "word": "Run errands",
        "meaning": "Do short daily trips to accomplish chores",
        "usage": "I need to run a few errands at the market before dinner."
    }

    concept_overview = theme_info.get("concept_overview", "Day 1: Everyday Home Routines & Connecting Pillars")
    why_important = theme_info.get("why_important", "Developing automatic recall of everyday phrases and connecting pillars improves your speaking confidence in real-life situations.")
    telugu_data = theme_info.get("telugu_translation", {})
    vocab = theme_info.get("vocabulary", ["Run errands", "Freshen up", "Tidy up", "Out of stock"])
    pillars = theme_info.get("connecting_pillars", ["Short and sweet", "Bits and pieces", "Safe and sound", "Spick and span"])

    questions = [
        # SECTION 1: Daily Routine & Habits (4 MCQs)
        {
            "id": 1,
            "section": "1. Daily Routine & Habits",
            "question": f"When talking about your morning schedule, which sentence is grammatically correct?",
            "options": {
                "a": "I am usually wake up at 6 AM every morning.",
                "b": "I usually wake up at 6 AM every morning.",
                "c": "I usually wakes up at 6 AM every morning."
            },
            "answer": "b",
            "explanation": "<b>Correct: Option B</b><br>Habitual daily routines take the Simple Present tense (<i>I usually wake up</i>). Never pair 'am' directly with a base verb like 'am wake'.",
            "audio_prompt": ""
        },
        {
            "id": 2,
            "section": "1. Daily Routine & Habits",
            "question": "Which response is natural when someone asks what you are currently doing at home?",
            "options": {
                "a": "I am tidying up the living room right now.",
                "b": "I tidying up the living room right now.",
                "c": "I am tidy up the living room right now."
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>Ongoing actions right now require the Present Continuous form (<i>am/is/are + verb-ing</i>).",
            "audio_prompt": ""
        },
        {
            "id": 3,
            "section": "1. Daily Routine & Habits",
            "question": "Complete the sentence: 'My sister __________ a cup of warm tea every morning before breakfast.'",
            "options": {
                "a": "drink",
                "b": "drinks",
                "c": "is drink"
            },
            "answer": "b",
            "explanation": "<b>Correct: Option B</b><br>Singular third-person subjects ('My sister') require an <i>-s</i> ending on base verbs in the Simple Present (<i>drinks</i>).",
            "audio_prompt": ""
        },
        {
            "id": 4,
            "section": "1. Daily Routine & Habits",
            "question": "How do you correctly describe a past action finished yesterday morning?",
            "options": {
                "a": "Yesterday morning, I prepared breakfast for my family.",
                "b": "Yesterday morning, I have prepared breakfast for my family.",
                "c": "Yesterday morning, I am prepare breakfast for my family."
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>Definite past markers like 'Yesterday morning' mandate the Simple Past tense (<i>prepared</i>).",
            "audio_prompt": ""
        },

        # SECTION 2: Everyday Easy Vocabulary & Phrasal Verbs (4 MCQs)
        {
            "id": 5,
            "section": "2. Everyday Easy Vocabulary",
            "question": f"What is the easy daily meaning of the phrase '{word_info['word']}'?",
            "options": {
                "a": "To run fast in an athletic race.",
                "b": f"{word_info['meaning']}.",
                "c": "To cancel all daily plans."
            },
            "answer": "b",
            "explanation": f"<b>Correct: Option B</b><br>'{word_info['word']}' means: {word_info['meaning']}. Example: <i>\"{word_info['usage']}\"</i>",
            "audio_prompt": ""
        },
        {
            "id": 6,
            "section": "2. Everyday Easy Vocabulary",
            "question": "Choose the phrase that fits: 'I'm sorry for the delay, fresh milk was __________ at the grocery store.'",
            "options": {
                "a": "out of stock",
                "b": "running late",
                "c": "tidy up"
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>'Out of stock' means goods or products are temporarily unavailable for purchase.",
            "audio_prompt": ""
        },
        {
            "id": 7,
            "section": "2. Everyday Easy Vocabulary",
            "question": "What does the phrasal verb 'Freshen up' mean when returning home from work?",
            "options": {
                "a": "To cook a heavy meal.",
                "b": "To wash your hands/face and change into comfortable clothes.",
                "c": "To clean the whole house."
            },
            "answer": "b",
            "explanation": "<b>Correct: Option B</b><br>'Freshen up' means quickly washing and relaxing after returning home.",
            "audio_prompt": ""
        },
        {
            "id": 8,
            "section": "2. Everyday Easy Vocabulary",
            "question": "Select the correct term: 'Let's __________ for a quick cup of tea this evening.'",
            "options": {
                "a": "catch up",
                "b": "catch out",
                "c": "catch off"
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>'Catch up' means meeting someone to chat and share recent news.",
            "audio_prompt": ""
        },

        # SECTION 3: Connecting Pillars & Everyday Expressions (4 MCQs)
        {
            "id": 9,
            "section": "3. Connecting Pillars & Expressions",
            "question": "Complete the daily sentence: 'Keep the morning family update __________ so we aren't late for school.'",
            "options": {
                "a": "short and sweet",
                "b": "bits and pieces",
                "c": "bells and whistles"
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>'Short and sweet' is a connecting pillar meaning brief, pleasant, and direct without wasting time.",
            "audio_prompt": ""
        },
        {
            "id": 10,
            "section": "3. Connecting Pillars & Expressions",
            "question": "Which connecting pillar fits best: 'After cleaning the living room, the whole house is __________.'",
            "options": {
                "a": "spick and span",
                "b": "short and sweet",
                "c": "elephant in the room"
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>'Spick and span' is an everyday connecting pillar meaning completely neat, spotless, and tidy.",
            "audio_prompt": ""
        },
        {
            "id": 11,
            "section": "3. Connecting Pillars & Expressions",
            "question": "Choose the correct expression: 'I picked up a few __________ from the market for dinner.'",
            "options": {
                "a": "bits and pieces",
                "b": "touch and go",
                "c": "safe and sound"
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>'Bits and pieces' refers to small individual items or small household purchases.",
            "audio_prompt": ""
        },
        {
            "id": 12,
            "section": "3. Connecting Pillars & Expressions",
            "question": "Select the expression: 'Despite heavy evening traffic, my family arrived home __________.'",
            "options": {
                "a": "safe and sound",
                "b": "short and sweet",
                "c": "ups and downs"
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>'Safe and sound' means arriving safely without any harm or injury.",
            "audio_prompt": ""
        },

        # SECTION 4: Listening to Spoken English (4 Audio Clips)
        {
            "id": 13,
            "section": "4. Listening to Spoken English",
            "question": "Listen to Audio Clip 1. What is the speaker asking you to do?",
            "options": {
                "a": "Stop testing immediately.",
                "b": "Pick up a fresh packet of tea from the store on your way home.",
                "c": "Cancel tomorrow's grocery list."
            },
            "answer": "b",
            "explanation": "<b>Correct: Option B</b><br>The speaker says: <i>'Could you please pick up a fresh packet of tea from the store on your way home?'</i>",
            "audio_prompt": "Could you please pick up a fresh packet of tea from the store on your way home?"
        },
        {
            "id": 14,
            "section": "4. Listening to Spoken English",
            "question": "Listen to Audio Clip 2. What is the main instruction?",
            "options": {
                "a": "The speaker will drop by your home around 6:00 PM today.",
                "b": "The speaker wants to reschedule for next month.",
                "c": "The speaker is asking for directions to the airport."
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>The speaker says: <i>'Hey! I will drop by your place this evening around 6:00 PM for a quick chat.'</i>",
            "audio_prompt": "Hey! I will drop by your place this evening around 6:00 PM for a quick chat."
        },
        {
            "id": 15,
            "section": "4. Listening to Spoken English",
            "question": "Listen to Audio Clip 3. What does the phrase 'Let's call it a day' mean in this dialogue?",
            "options": {
                "a": "Check the date on the wall calendar.",
                "b": "Stop working on the task for today and rest.",
                "c": "Work late into the night."
            },
            "answer": "b",
            "explanation": "<b>Correct: Option B</b><br>'Let's call it a day' is an everyday idiom meaning we have finished work for today.",
            "audio_prompt": "We have made great progress on the chores! Let us call it a day and continue tomorrow morning."
        },
        {
            "id": 16,
            "section": "4. Listening to Spoken English",
            "question": "Listen to Audio Clip 4. What reminder is given?",
            "options": {
                "a": "Take an umbrella because dark clouds are gathering.",
                "b": "Stay indoors all weekend.",
                "c": "Buy a new raincoat online."
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>The speaker says: <i>'Don't forget your umbrella, it looks like rain this afternoon!'</i>",
            "audio_prompt": "Don't forget your umbrella when you step out, it looks like rain this afternoon!"
        },

        # SECTION 5: Real-Life Telugu ➔ English Translation & AI Feedback (4 Scenarios)
        {
            "id": 17,
            "section": "5. Real-Life Telugu ➔ English Translation",
            "question": f"Translate Scenario 1:<br><br><b>Telugu:</b> \"{telugu_data.get('telugu', '')}\"<br><i>(Literal attempt: \"{telugu_data.get('literal', '')}\")</i>",
            "options": {
                "a": f"{telugu_data.get('literal', '')}",
                "b": f"{telugu_data.get('polished', '')}",
                "c": "I morning wake up and tea drinking."
            },
            "answer": "b",
            "explanation": f"<b>Natural Phrasing & Guidance:</b><br>{telugu_data.get('feedback', '')}<br><br><b>Natural Version:</b> <i>\"{telugu_data.get('polished', '')}\"</i>",
            "audio_prompt": f"Natural English phrasing: {telugu_data.get('polished', '')}"
        },
        {
            "id": 18,
            "section": "5. Real-Life Telugu ➔ English Translation",
            "question": "Translate Scenario 2:<br><br><b>Telugu:</b> \"ఈ టమాటాలు కేజీ ఎంత? కొంచెం తాజావి ఏరి ఇవ్వండి.\"<br><i>(Literal attempt: \"These tomatoes kg how much? Pick and give fresh ones.\")</i>",
            "options": {
                "a": "These tomatoes kg how much? Pick and give fresh ones.",
                "b": "How much are these tomatoes per kilo? Please pick out some fresh ones for me.",
                "c": "What is price for tomatoes giving?"
            },
            "answer": "b",
            "explanation": "<b>Natural Phrasing & Guidance:</b><br>Avoid literal word-by-word translation. Use 'per kilo' for price by weight, and 'pick out' for selecting fresh produce.<br><br><b>Natural Version:</b> <i>\"How much are these tomatoes per kilo? Please pick out some fresh ones for me.\"</i>",
            "audio_prompt": "How much are these tomatoes per kilo? Please pick out some fresh ones for me."
        },
        {
            "id": 19,
            "section": "5. Real-Life Telugu ➔ English Translation",
            "question": "Translate Scenario 3:<br><br><b>Telugu:</b> \"అన్నా, బస్టాండ్ దగ్గర డ్రాప్ చేయండి, ఎంత అవుతుంది?\"<br><i>(Literal attempt: \"Brother, near bus stand drop me, how much will become?\")</i>",
            "options": {
                "a": "Brother, near bus stand drop me, how much will become?",
                "b": "Please drop me off near the bus stand. How much is the fare?",
                "c": "Drop bus stand how much cost becoming?"
            },
            "answer": "b",
            "explanation": "<b>Natural Phrasing & Guidance:</b><br>Avoid 'how much will become' (a common Telugu-ism). Use 'How much is the fare?' or 'What will it cost?'.<br><br><b>Natural Version:</b> <i>\"Please drop me off near the bus stand. How much is the fare?\"</i>",
            "audio_prompt": "Please drop me off near the bus stand. How much is the fare?"
        },
        {
            "id": 20,
            "section": "5. Real-Life Telugu ➔ English Translation",
            "question": "Translate Scenario 4:<br><br><b>Telugu:</b> \"నాకు కొంచెం తలనొప్పిగా ఉంది, ఒక గంట సేపు రెస్ట్ తీసుకుంటాను.\"<br><i>(Literal attempt: \"To me little headache is there, I will take rest one hour.\")</i>",
            "options": {
                "a": "To me little headache is there, I will take rest one hour.",
                "b": "I have a slight headache; I'm going to rest for an hour.",
                "c": "My head is hurting small, resting one hour."
            },
            "answer": "b",
            "explanation": "<b>Natural Phrasing & Guidance:</b><br>In English, say 'I have a slight headache' rather than 'to me headache is there'. Also say 'rest for an hour'.<br><br><b>Natural Version:</b> <i>\"I have a slight headache; I'm going to rest for an hour.\"</i>",
            "audio_prompt": "I have a slight headache; I'm going to rest for an hour."
        }
    ]

    return word_info, concept_overview, why_important, questions

def build_standalone_html(level, day_num, word_info, concept_overview, why_important, questions):
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    questions_js = json.dumps(questions, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FluencyCraft {level.capitalize()} - Day {day_num:02d} Practical Test</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #059669;
      --primary-dark: #047857;
      --surface: #ffffff;
      --background: #f8fafc;
      --text: #0f172a;
      --text-muted: #475569;
      --border: #e2e8f0;
      --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--background);
      color: var(--text);
      line-height: 1.6;
      padding: 24px 16px;
    }}
    .container {{ max-width: 860px; margin: 0 auto; }}

    .nav-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}
    .back-link {{
      color: var(--primary);
      text-decoration: none;
      font-weight: 700;
      font-size: 0.95rem;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .back-link:hover {{ text-decoration: underline; }}

    header {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 28px;
      margin-bottom: 20px;
      box-shadow: var(--card-shadow);
    }}
    .badge {{
      display: inline-block;
      background: #ecfdf5;
      color: #047857;
      font-weight: 800;
      font-size: 0.78rem;
      padding: 6px 14px;
      border-radius: 9999px;
      margin-bottom: 12px;
      border: 1px solid #a7f3d0;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    header h1 {{ font-size: 1.8rem; font-weight: 800; color: #064e3b; margin-bottom: 6px; }}
    header p {{ color: var(--text-muted); font-size: 0.98rem; }}

    /* Learner Name Field */
    .learner-name-wrap {{
      margin-top: 18px;
      padding-top: 16px;
      border-top: 1px dashed var(--border);
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .learner-name-wrap label {{ font-size: 0.9rem; font-weight: 700; color: var(--text); }}
    .learner-name-wrap input {{
      width: 100%;
      max-width: 380px;
      padding: 10px 14px;
      border-radius: 8px;
      border: 1px solid var(--border);
      font-size: 0.95rem;
      font-family: inherit;
    }}
    .learner-name-wrap input:focus {{ outline: none; border-color: var(--primary); }}

    /* Word of the Day Card */
    .wod-banner {{
      background: linear-gradient(135deg, #064e3b 0%, #059669 100%);
      color: white;
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: 0 6px 16px rgba(5, 150, 105, 0.15);
    }}
    .wod-header {{ font-size: 0.8rem; font-weight: 800; text-transform: uppercase; color: #a7f3d0; margin-bottom: 6px; }}
    .wod-title {{ font-size: 1.5rem; font-weight: 800; margin-bottom: 4px; }}
    .wod-meaning {{ font-size: 1.05rem; color: #ecfdf5; margin-bottom: 12px; }}
    .wod-usage {{
      font-size: 0.92rem;
      background: rgba(255, 255, 255, 0.15);
      padding: 10px 14px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}

    /* Concept & Importance Card */
    .concept-card {{
      background: #eff6ff;
      border-left: 5px solid #2563eb;
      border-radius: 14px;
      padding: 20px 24px;
      margin-bottom: 24px;
      border-top: 1px solid var(--border);
      border-right: 1px solid var(--border);
      border-bottom: 1px solid var(--border);
    }}
    .concept-title {{ font-size: 1.05rem; font-weight: 800; color: #1e40af; margin-bottom: 6px; }}
    .concept-body {{ font-size: 0.95rem; color: #1e293b; line-height: 1.5; }}
    .importance-box {{ margin-top: 10px; padding-top: 10px; border-top: 1px dashed #bfdbfe; font-size: 0.92rem; color: #334155; }}

    /* Quiz Cards */
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 22px;
      margin-bottom: 18px;
      box-shadow: var(--card-shadow);
    }}
    .card p.question {{ font-weight: 700; font-size: 1rem; margin-bottom: 16px; color: var(--text); }}

    .options {{ display: flex; flex-direction: column; gap: 10px; }}
    .option-label {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 14px;
      border-radius: 8px;
      background: #f8fafc;
      border: 1px solid var(--border);
      cursor: pointer;
      font-size: 0.95rem;
      transition: all 0.2s;
    }}
    .option-label:hover {{ background: #ecfdf5; border-color: #a7f3d0; }}
    .option-label.disabled {{ cursor: not-allowed; opacity: 0.85; }}
    .option-label.disabled:hover {{ background: #f8fafc; border-color: var(--border); }}
    .option-label input[type="radio"] {{ accent-color: var(--primary); width: 18px; height: 18px; }}

    .audio-btn {{
      background: #f1f5f9;
      color: #1e293b;
      border: 1px solid var(--border);
      padding: 8px 14px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.85rem;
      font-weight: 700;
      margin-bottom: 14px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .audio-btn:hover {{ background: #e2e8f0; }}

    /* Explanation Box */
    .explanation {{
      margin-top: 16px;
      padding: 14px;
      border-radius: 8px;
      font-size: 0.92rem;
      display: none;
      line-height: 1.5;
    }}
    .explanation.correct {{ background: #f0fdf4; border: 1px solid #bbf7d0; color: #14532d; }}
    .explanation.incorrect {{ background: #fef2f2; border: 1px solid #fecaca; color: #7f1d1d; }}

    .actions-bar {{ display: flex; gap: 12px; margin-top: 28px; }}
    button.submit-btn {{
      flex: 2;
      background: var(--primary);
      color: white;
      border: none;
      padding: 16px;
      border-radius: 10px;
      font-size: 1.05rem;
      font-weight: 800;
      cursor: pointer;
    }}
    button.submit-btn:hover {{ background: var(--primary-dark); }}
    button.reset-btn {{
      flex: 1;
      background: #f1f5f9;
      color: #334155;
      border: 1px solid var(--border);
      padding: 16px;
      border-radius: 10px;
      font-size: 1.05rem;
      font-weight: 700;
      cursor: pointer;
    }}

    #result-banner {{
      display: none;
      margin-top: 24px;
      padding: 24px;
      border-radius: 14px;
      text-align: center;
      background: var(--surface);
      border: 2px solid var(--primary);
    }}
    #result-title {{ font-size: 1.3rem; font-weight: 800; }}
    #result-score {{ font-size: 2.3rem; font-weight: 800; color: var(--primary); margin: 4px 0; }}
  </style>
</head>
<body>

<div class="container">

  <div class="nav-bar">
    <a href="../../index.html" class="back-link">← Back to Course Overview</a>
    <span style="font-size:0.88rem; font-weight:700; color:var(--text-muted);">Date: {today_str}</span>
  </div>

  <header>
    <span class="badge">Everyday Practical Studio • {level.capitalize()} Track</span>
    <h1>FluencyCraft {level.capitalize()} - Day {day_num:02d}</h1>
    <p>Practice 20 practical everyday questions covering routines, phrasal verbs, connecting pillars, auditory dialogues, polite social etiquette, and Telugu-to-English translation scenarios.</p>

    <div class="learner-name-wrap">
      <label for="learnerName">Learner's Name (Optional):</label>
      <input type="text" id="learnerName" placeholder="e.g., Pavan" oninput="saveNameState()">
      <span style="font-size:0.8rem; color:#059669; font-weight:600; margin-top:2px;">🔒 Note: All your answers and name are stored strictly in your local browser. No data is sent to external servers.</span>
    </div>
  </header>

  <!-- Word of the Day Banner -->
  <div class="wod-banner">
    <div class="wod-header">🌟 Word of the Day & Everyday Phrase</div>
    <div class="wod-title">{word_info.get('word', 'Run errands')}</div>
    <div class="wod-meaning">Meaning: {word_info.get('meaning', '')}</div>
    <div class="wod-usage">
      <span>Usage: "{word_info.get('usage', '')}"</span>
      <button type="button" class="audio-btn" style="margin:0; background:white; color:#047857;" onclick="playPrompt('{word_info.get('word', '')}. {word_info.get('usage', '')}')">🔊 Listen</button>
    </div>
  </div>

  <!-- Concept Covered Today & Why It Is Important -->
  <div class="concept-card">
    <div class="concept-title">📘 Today's Concept Focus: {concept_overview}</div>
    <div class="concept-body">Focusing on real-life daily living scenarios, connecting pillars (pair idioms), spoken audio recognition, and eliminating literal Telugu-isms.</div>
    <div class="importance-box">
      🎯 <b>Why this is important for your English skills:</b> {why_important}
    </div>
  </div>

  <form id="quizForm">
    <div id="questionsContainer"></div>

    <div class="actions-bar">
      <button type="button" class="submit-btn" onclick="evaluateFullQuiz()">Finish & View Final Score</button>
      <button type="button" class="reset-btn" onclick="resetQuiz()">Reset Test</button>
    </div>
  </form>

  <div id="result-banner">
    <div id="result-title">Test Result</div>
    <div id="result-score">0 / 20</div>
    <p style="color: var(--text-muted); font-size: 0.95rem;">Review your answers and detailed explanations above!</p>
  </div>

</div>

<script>
  const questionsData = {questions_js};
  const answerKeyMap = {{}};
  const userAnswersMap = {{}};
  const TEST_STORAGE_KEY = 'fluencycraft_saved_answers_' + window.location.pathname;

  window.addEventListener('DOMContentLoaded', () => {{
    loadNameState();
    renderQuestions(questionsData);
    restoreSavedAnswers();
  }});

  function saveNameState() {{
    const name = document.getElementById('learnerName').value.trim();
    localStorage.setItem('fluencycraft_learner_name', name);
  }}

  function loadNameState() {{
    const saved = localStorage.getItem('fluencycraft_learner_name');
    if (saved) document.getElementById('learnerName').value = saved;
  }}

  function restoreSavedAnswers() {{
    let savedMap = {{}};
    try {{
      savedMap = JSON.parse(localStorage.getItem(TEST_STORAGE_KEY) || '{{}}');
    }} catch(e) {{ savedMap = {{}}; }}

    for (let qKey in savedMap) {{
      const val = savedMap[qKey];
      const radio = document.querySelector(`input[name="${{qKey}}"][value="${{val}}"]`);
      if (radio) {{
        radio.checked = true;
        onAnswerSelected(qKey, val, false);
      }}
    }}
  }}

  function renderQuestions(questions) {{
    const container = document.getElementById('questionsContainer');
    container.innerHTML = '';

    questions.forEach((q, idx) => {{
      const qNum = idx + 1;
      answerKeyMap[`q${{qNum}}`] = {{ ans: q.answer, exp: q.explanation }};

      const card = document.createElement('div');
      card.className = 'card';

      let audioHtml = '';
      if (q.audio_prompt && q.audio_prompt.trim().length > 0) {{
        audioHtml = `<button type="button" class="audio-btn" onclick="playPrompt('${{q.audio_prompt.replace(/'/g, "\\'")}}')">🔊 Listen to Audio Clip</button>`;
      }}

      card.innerHTML = `
        <div style="font-size:0.8rem; font-weight:800; color:var(--primary); text-transform:uppercase; margin-bottom:6px;">${{q.section || ''}}</div>
        ${{audioHtml}}
        <p class="question">${{qNum}}. ${{q.question}}</p>
        <div class="options" id="optionsGroup_${{qNum}}">
          <label class="option-label" id="label_q${{qNum}}_a"><input type="radio" name="q${{qNum}}" value="a" onchange="onAnswerSelected('q${{qNum}}', 'a', true)"> A) ${{q.options.a}}</label>
          <label class="option-label" id="label_q${{qNum}}_b"><input type="radio" name="q${{qNum}}" value="b" onchange="onAnswerSelected('q${{qNum}}', 'b', true)"> B) ${{q.options.b}}</label>
          <label class="option-label" id="label_q${{qNum}}_c"><input type="radio" name="q${{qNum}}" value="c" onchange="onAnswerSelected('q${{qNum}}', 'c', true)"> C) ${{q.options.c}}</label>
        </div>
        <div class="explanation" id="exp${{qNum}}"></div>
      `;
      container.appendChild(card);
    }});
  }}

  function onAnswerSelected(qKey, selectedVal, isUserClick = true) {{
    userAnswersMap[qKey] = selectedVal;
    
    if (isUserClick) {{
      try {{
        localStorage.setItem(TEST_STORAGE_KEY, JSON.stringify(userAnswersMap));
      }} catch(e) {{}}
    }}

    const qNum = qKey.replace('q', '');
    const expDiv = document.getElementById(`exp${{qNum}}`);
    const keyData = answerKeyMap[qKey];
    const isCorrect = selectedVal === keyData.ans;

    expDiv.innerHTML = keyData.exp;
    expDiv.className = `explanation ${{isCorrect ? 'correct' : 'incorrect'}}`;
    expDiv.style.display = 'block';

    if (!isCorrect && isUserClick) {{
      logMistake(questionsData[parseInt(qNum) - 1], selectedVal);
    }}

    document.querySelectorAll(`input[name="${{qKey}}"]`).forEach(radio => radio.disabled = true);
    document.querySelectorAll(`#optionsGroup_${{qNum}} .option-label`).forEach(lbl => lbl.classList.add('disabled'));
  }}

  function logMistake(qObj, userChoiceVal) {{
    if (!qObj) return;
    let mistakes = [];
    try {{
      mistakes = JSON.parse(localStorage.getItem('fluencycraft_mistakes') || '[]');
    }} catch(e) {{ mistakes = []; }}

    const entry = {{
      id: qObj.id,
      section: qObj.section || 'General Practice',
      question: qObj.question,
      userChoice: userChoiceVal,
      correctAnswer: qObj.answer,
      explanation: qObj.explanation,
      date: new Date().toISOString().split('T')[0]
    }};

    if (!mistakes.some(m => m.question === entry.question)) {{
      mistakes.push(entry);
      localStorage.setItem('fluencycraft_mistakes', JSON.stringify(mistakes));
    }}
  }}

  function evaluateFullQuiz() {{
    let score = 0;
    const total = Object.keys(answerKeyMap).length;

    for (let key in answerKeyMap) {{
      if (userAnswersMap[key] === answerKeyMap[key].ans) score++;

      const qNum = key.replace('q', '');
      const expDiv = document.getElementById(`exp${{qNum}}`);
      expDiv.innerHTML = answerKeyMap[key].exp;
      expDiv.className = `explanation ${{userAnswersMap[key] === answerKeyMap[key].ans ? 'correct' : 'incorrect'}}`;
      expDiv.style.display = 'block';
    }}

    const name = document.getElementById('learnerName').value.trim();
    const banner = document.getElementById('result-banner');
    const title = document.getElementById('result-title');
    const scoreText = document.getElementById('result-score');

    title.innerText = name ? `Great job, ${{name}}!` : "Test Result";
    scoreText.innerText = `${{score}} / ${{total}} (${{Math.round((score / total) * 100)}}%)`;
    banner.style.display = 'block';
    banner.scrollIntoView({{ behavior: 'smooth' }});
  }}

  function playPrompt(text) {{
    if ('speechSynthesis' in window) {{
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.lang = 'en-US';
      window.speechSynthesis.speak(utterance);
    }}
  }}

  function resetQuiz() {{
    if (!confirm("Reset test? All selections will be cleared.")) return;
    document.getElementById('quizForm').reset();
    try {{ localStorage.removeItem(TEST_STORAGE_KEY); }} catch(e) {{}}
    document.querySelectorAll('.explanation').forEach(exp => {{ exp.style.display = 'none'; exp.innerHTML = ''; }});
    document.querySelectorAll('input[type="radio"]').forEach(r => r.disabled = false);
    document.querySelectorAll('.option-label').forEach(l => l.classList.remove('disabled'));
    document.getElementById('result-banner').style.display = 'none';
    for (let k in userAnswersMap) delete userAnswersMap[k];
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }}
</script>
</body>
</html>
"""
    return html_content

def build_weekend_test_html(level, questions):
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    default_questions_js = json.dumps(questions, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FluencyCraft {level.capitalize()} - Weekend Weak-Spot Adaptive Test</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #1e40af;
      --primary-dark: #1e3a8a;
      --surface: #ffffff;
      --background: #f8fafc;
      --text: #0f172a;
      --text-muted: #475569;
      --border: #cbd5e1;
      --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--background);
      color: var(--text);
      line-height: 1.6;
      padding: 24px 16px;
    }}
    .container {{ max-width: 860px; margin: 0 auto; }}

    .nav-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}
    .back-link {{
      color: var(--primary);
      text-decoration: none;
      font-weight: 700;
      font-size: 0.95rem;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .back-link:hover {{ text-decoration: underline; }}

    header {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 28px;
      margin-bottom: 20px;
      box-shadow: var(--card-shadow);
    }}
    .badge {{
      display: inline-block;
      background: #eff6ff;
      color: #1e40af;
      font-weight: 800;
      font-size: 0.78rem;
      padding: 6px 14px;
      border-radius: 9999px;
      margin-bottom: 12px;
      border: 1px solid #bfdbfe;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    header h1 {{ font-size: 1.8rem; font-weight: 800; color: #1e3a8a; margin-bottom: 6px; }}
    header p {{ color: var(--text-muted); font-size: 0.98rem; }}

    .learner-name-wrap {{
      margin-top: 18px;
      padding-top: 16px;
      border-top: 1px dashed var(--border);
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .learner-name-wrap label {{ font-size: 0.9rem; font-weight: 700; color: var(--text); }}
    .learner-name-wrap input {{
      width: 100%;
      max-width: 380px;
      padding: 10px 14px;
      border-radius: 8px;
      border: 1px solid var(--border);
      font-size: 0.95rem;
      font-family: inherit;
    }}

    /* Weak Spot Banner */
    .weakspot-banner {{
      background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
      color: white;
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: 0 6px 16px rgba(37, 99, 235, 0.15);
    }}
    .weakspot-header {{ font-size: 0.8rem; font-weight: 800; text-transform: uppercase; color: #bfdbfe; margin-bottom: 6px; }}
    .weakspot-title {{ font-size: 1.4rem; font-weight: 800; margin-bottom: 6px; }}
    .weakspot-desc {{ font-size: 0.98rem; color: #eff6ff; }}

    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 22px;
      margin-bottom: 18px;
      box-shadow: var(--card-shadow);
    }}
    .card p.question {{ font-weight: 700; font-size: 1rem; margin-bottom: 16px; color: var(--text); }}

    .options {{ display: flex; flex-direction: column; gap: 10px; }}
    .option-label {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 14px;
      border-radius: 8px;
      background: #f8fafc;
      border: 1px solid var(--border);
      cursor: pointer;
      font-size: 0.95rem;
      transition: all 0.2s;
    }}
    .option-label:hover {{ background: #eff6ff; border-color: #bfdbfe; }}
    .option-label.disabled {{ cursor: not-allowed; opacity: 0.85; }}
    .option-label.disabled:hover {{ background: #f8fafc; border-color: var(--border); }}
    .option-label input[type="radio"] {{ accent-color: var(--primary); width: 18px; height: 18px; }}

    .audio-btn {{
      background: #f1f5f9;
      color: #1e293b;
      border: 1px solid var(--border);
      padding: 8px 14px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.85rem;
      font-weight: 700;
      margin-bottom: 14px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .explanation {{
      margin-top: 16px;
      padding: 14px;
      border-radius: 8px;
      font-size: 0.92rem;
      display: none;
      line-height: 1.5;
    }}
    .explanation.correct {{ background: #f0fdf4; border: 1px solid #bbf7d0; color: #14532d; }}
    .explanation.incorrect {{ background: #fef2f2; border: 1px solid #fecaca; color: #7f1d1d; }}

    .actions-bar {{ display: flex; gap: 12px; margin-top: 28px; }}
    button.submit-btn {{
      flex: 2;
      background: var(--primary);
      color: white;
      border: none;
      padding: 16px;
      border-radius: 10px;
      font-size: 1.05rem;
      font-weight: 800;
      cursor: pointer;
    }}
    button.submit-btn:hover {{ background: var(--primary-dark); }}
    button.reset-btn {{
      flex: 1;
      background: #f1f5f9;
      color: #334155;
      border: 1px solid var(--border);
      padding: 16px;
      border-radius: 10px;
      font-size: 1.05rem;
      font-weight: 700;
      cursor: pointer;
    }}

    #result-banner {{
      display: none;
      margin-top: 24px;
      padding: 24px;
      border-radius: 14px;
      background: var(--surface);
      border: 2px solid var(--primary);
    }}
    #result-title {{ font-size: 1.3rem; font-weight: 800; text-align: center; }}
    #result-score {{ font-size: 2.3rem; font-weight: 800; color: var(--primary); margin: 4px 0; text-align: center; }}
    
    .feedback-box {{
      margin-top: 18px;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 12px;
      padding: 18px;
    }}
    .feedback-box h4 {{ font-size: 1.05rem; font-weight: 800; color: #1e3a8a; margin-bottom: 8px; }}
    .feedback-box ul {{ margin-left: 20px; color: #334155; font-size: 0.93rem; }}
  </style>
</head>
<body>

<div class="container">

  <div class="nav-bar">
    <a href="../../index.html" class="back-link">← Back to Course Overview</a>
    <span style="font-size:0.88rem; font-weight:700; color:var(--text-muted);">Weekend Test Date: {today_str}</span>
  </div>

  <header>
    <span class="badge">Weekend Adaptive Mastery Engine • {level.capitalize()} Track</span>
    <h1>FluencyCraft {level.capitalize()} - Weekend Weak-Spot Review</h1>
    <p>Targeted re-evaluation test built specifically from your recorded mistakes over the past 5 weekday practice sessions.</p>

    <div class="learner-name-wrap">
      <label for="learnerName">Learner's Name (Optional):</label>
      <input type="text" id="learnerName" placeholder="e.g., Pavan" oninput="saveNameState()">
      <span style="font-size:0.8rem; color:#1e40af; font-weight:600; margin-top:2px;">🔒 Note: All weak spots and answers are saved strictly inside your local browser.</span>
    </div>
  </header>

  <div class="weakspot-banner" id="weakspotBanner">
    <div class="weakspot-header">🎯 Adaptive Diagnosis Engine</div>
    <div class="weakspot-title" id="weakspotTitle">Analyzing Weekday Practice...</div>
    <div class="weakspot-desc" id="weakspotDesc">Checking your local mistake log from the past 5 days of practice.</div>
  </div>

  <form id="quizForm">
    <div id="questionsContainer"></div>

    <div class="actions-bar">
      <button type="button" class="submit-btn" onclick="evaluateFullQuiz()">Finish Weekend Test & Get Improvement Feedback</button>
      <button type="button" class="reset-btn" onclick="clearMistakesLog()">Clear Mistake History</button>
    </div>
  </form>

  <div id="result-banner">
    <div id="result-title">Weekend Test Result</div>
    <div id="result-score">0 / 0</div>

    <div class="feedback-box" id="feedbackBox">
      <h4>🎯 Weak Spot Improvement Feedback & Action Roadmap</h4>
      <div id="feedbackContent">Calculating personalized feedback based on your responses...</div>
    </div>
  </div>

</div>

<script>
  const defaultQuestions = {default_questions_js};
  let questionsData = [];
  const answerKeyMap = {{}};
  const userAnswersMap = {{}};

  window.addEventListener('DOMContentLoaded', () => {{
    loadNameState();
    loadAdaptiveQuestions();
  }});

  function saveNameState() {{
    const name = document.getElementById('learnerName').value.trim();
    localStorage.setItem('fluencycraft_learner_name', name);
  }}

  function loadNameState() {{
    const saved = localStorage.getItem('fluencycraft_learner_name');
    if (saved) document.getElementById('learnerName').value = saved;
  }}

  function loadAdaptiveQuestions() {{
    let mistakes = [];
    try {{
      mistakes = JSON.parse(localStorage.getItem('fluencycraft_mistakes') || '[]');
    }} catch(e) {{ mistakes = []; }}

    const bannerTitle = document.getElementById('weakspotTitle');
    const bannerDesc = document.getElementById('weakspotDesc');

    if (mistakes && mistakes.length > 0) {{
      bannerTitle.innerText = `🎯 ${{mistakes.length}} Weak Spot(s) Identified from Past 5 Days`;
      bannerDesc.innerText = "This weekend test is specially focused on concepts where you made errors during weekday practice. Overcome these weak spots to master everyday English!";

      questionsData = mistakes.map((m, idx) => {{
        return defaultQuestions.find(dq => dq.question === m.question) || {{
          id: idx + 1,
          section: m.section || "Targeted Weak Spot",
          question: m.question,
          options: defaultQuestions[idx % defaultQuestions.length].options,
          answer: defaultQuestions[idx % defaultQuestions.length].answer,
          explanation: m.explanation || "Review this target concept carefully.",
          audio_prompt: ""
        }};
      }});

      if (questionsData.length < 10) {{
        defaultQuestions.forEach(dq => {{
          if (questionsData.length < 10 && !questionsData.some(q => q.question === dq.question)) {{
            questionsData.push(dq);
          }}
        }});
      }}
    }} else {{
      bannerTitle.innerText = "✨ 5-Day Comprehensive Weekend Mastery Review";
      bannerDesc.innerText = "No weekday mistakes recorded yet! Here is a full 20-question review test spanning all 5 practical living modules.";
      questionsData = defaultQuestions;
    }}

    renderQuestions(questionsData);
    restoreSavedAnswers();
  }}

  function restoreSavedAnswers() {{
    const TEST_STORAGE_KEY = 'fluencycraft_saved_answers_' + window.location.pathname;
    let savedMap = {{}};
    try {{
      savedMap = JSON.parse(localStorage.getItem(TEST_STORAGE_KEY) || '{{}}');
    }} catch(e) {{ savedMap = {{}}; }}

    for (let qKey in savedMap) {{
      const val = savedMap[qKey];
      const radio = document.querySelector(`input[name="${{qKey}}"][value="${{val}}"]`);
      if (radio) {{
        radio.checked = true;
        onAnswerSelected(qKey, val, false);
      }}
    }}
  }}

  function renderQuestions(questions) {{
    const container = document.getElementById('questionsContainer');
    container.innerHTML = '';

    questions.forEach((q, idx) => {{
      const qNum = idx + 1;
      answerKeyMap[`q${{qNum}}`] = {{ ans: q.answer, exp: q.explanation }};

      const card = document.createElement('div');
      card.className = 'card';

      let audioHtml = '';
      if (q.audio_prompt && q.audio_prompt.trim().length > 0) {{
        audioHtml = `<button type="button" class="audio-btn" onclick="playPrompt('${{q.audio_prompt.replace(/'/g, "\\'")}}')">🔊 Listen to Audio Clip</button>`;
      }}

      card.innerHTML = `
        <div style="font-size:0.8rem; font-weight:800; color:var(--primary); text-transform:uppercase; margin-bottom:6px;">${{q.section || ''}}</div>
        ${{audioHtml}}
        <p class="question">${{qNum}}. ${{q.question}}</p>
        <div class="options" id="optionsGroup_${{qNum}}">
          <label class="option-label" id="label_q${{qNum}}_a"><input type="radio" name="q${{qNum}}" value="a" onchange="onAnswerSelected('q${{qNum}}', 'a', true)"> A) ${{q.options.a}}</label>
          <label class="option-label" id="label_q${{qNum}}_b"><input type="radio" name="q${{qNum}}" value="b" onchange="onAnswerSelected('q${{qNum}}', 'b', true)"> B) ${{q.options.b}}</label>
          <label class="option-label" id="label_q${{qNum}}_c"><input type="radio" name="q${{qNum}}" value="c" onchange="onAnswerSelected('q${{qNum}}', 'c', true)"> C) ${{q.options.c}}</label>
        </div>
        <div class="explanation" id="exp${{qNum}}"></div>
      `;
      container.appendChild(card);
    }});
  }}

  function onAnswerSelected(qKey, selectedVal, isUserClick = true) {{
    userAnswersMap[qKey] = selectedVal;
    
    if (isUserClick) {{
      const TEST_STORAGE_KEY = 'fluencycraft_saved_answers_' + window.location.pathname;
      try {{
        localStorage.setItem(TEST_STORAGE_KEY, JSON.stringify(userAnswersMap));
      }} catch(e) {{}}
    }}

    const qNum = qKey.replace('q', '');
    const expDiv = document.getElementById(`exp${{qNum}}`);
    const keyData = answerKeyMap[qKey];
    const isCorrect = selectedVal === keyData.ans;

    expDiv.innerHTML = keyData.exp;
    expDiv.className = `explanation ${{isCorrect ? 'correct' : 'incorrect'}}`;
    expDiv.style.display = 'block';

    document.querySelectorAll(`input[name="${{qKey}}"]`).forEach(radio => radio.disabled = true);
    document.querySelectorAll(`#optionsGroup_${{qNum}} .option-label`).forEach(lbl => lbl.classList.add('disabled'));
  }}

  function evaluateFullQuiz() {{
    let score = 0;
    const total = Object.keys(answerKeyMap).length;
    const missedSections = {{}};

    for (let key in answerKeyMap) {{
      const qNum = parseInt(key.replace('q', ''));
      const qObj = questionsData[qNum - 1];

      if (userAnswersMap[key] === answerKeyMap[key].ans) {{
        score++;
      }} else {{
        const sec = qObj ? qObj.section : 'General';
        missedSections[sec] = (missedSections[sec] || 0) + 1;
      }}

      const expDiv = document.getElementById(`exp${{qNum}}`);
      expDiv.innerHTML = answerKeyMap[key].exp;
      expDiv.className = `explanation ${{userAnswersMap[key] === answerKeyMap[key].ans ? 'correct' : 'incorrect'}}`;
      expDiv.style.display = 'block';
    }}

    const name = document.getElementById('learnerName').value.trim();
    const banner = document.getElementById('result-banner');
    const title = document.getElementById('result-title');
    const scoreText = document.getElementById('result-score');
    const feedbackContent = document.getElementById('feedbackContent');

    title.innerText = name ? `Weekend Mastery Result for ${{name}}!` : "Weekend Mastery Result";
    scoreText.innerText = `${{score}} / ${{total}} (${{Math.round((score / total) * 100)}}%)`;

    let feedbackHtml = `<ul>`;
    if (Object.keys(missedSections).length === 0) {{
      feedbackHtml += `<li style="color:#059669; font-weight:700;">🌟 Outstanding! You scored 100% on your weak spot review. All targeted concepts are now mastered!</li>`;
    }} else {{
      for (let sec in missedSections) {{
        feedbackHtml += `<li><b>${{sec}}</b>: ${{missedSections[sec]}} error(s) logged. <i>Action item:</i> Review the explanations for this section and practice these expressions in your daily conversations.</li>`;
      }}
    }}
    feedbackHtml += `</ul>`;
    feedbackContent.innerHTML = feedbackHtml;

    banner.style.display = 'block';
    banner.scrollIntoView({{ behavior: 'smooth' }});
  }}

  function clearMistakesLog() {{
    if (!confirm("Clear your weak spots history? This will reset your logged mistakes.")) return;
    localStorage.removeItem('fluencycraft_mistakes');
    alert("Mistake history cleared!");
    location.reload();
  }}

  function playPrompt(text) {{
    if ('speechSynthesis' in window) {{
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.lang = 'en-US';
      window.speechSynthesis.speak(utterance);
    }}
  }}
</script>
</body>
</html>
"""
    return html_content

def main():
    curriculum = load_curriculum()
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tests_root_dir = os.path.join(root_dir, "tests")

    for level in ["beginner", "intermediate", "advanced"]:
        level_dir = os.path.join(tests_root_dir, level)
        
        # Rule: Always stick with Day 1 (day-01.html) until perfected!
        day_num = 1

        word_info, concept_overview, why_important, questions = generate_20_questions(level)

        html_content = build_standalone_html(level, day_num, word_info, concept_overview, why_important, questions)
        weekend_content = build_weekend_test_html(level, questions)

        day_filename = f"day-{day_num:02d}.html"
        day_path = os.path.join(level_dir, day_filename)
        latest_path = os.path.join(level_dir, "latest.html")
        weekend_path = os.path.join(level_dir, "weekend-test.html")

        with open(day_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        with open(latest_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        with open(weekend_path, "w", encoding="utf-8") as f:
            f.write(weekend_content)

        print(f"[{level.upper()}] Successfully generated tests/{level}/{day_filename}, latest.html, and weekend-test.html")

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
import os
import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime

CURRICULUM_PATH = os.path.join(os.path.dirname(__file__), "curriculum.json")

def load_curriculum():
    if os.path.exists(CURRICULUM_PATH):
        with open(CURRICULUM_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_next_day_num(level_dir):
    os.makedirs(level_dir, exist_ok=True)
    existing_files = os.listdir(level_dir)
    day_nums = []
    for f in existing_files:
        match = re.match(r"day-(\d+)\.json", f)
        if match:
            day_nums.append(int(match.group(1)))
    if not day_nums:
        return 1
    return max(day_nums) + 1

def generate_test_for_day(level, day_num, curriculum):
    roadmap = curriculum.get("curriculum_roadmap", [])
    words_of_day = curriculum.get("words_of_the_day", [])

    theme_idx = (day_num - 1) % len(roadmap) if roadmap else 0
    theme_info = roadmap[theme_idx] if roadmap else {
        "theme": "Morning & Home Routines",
        "scenario": "Daily habits, home conversations",
        "vocabulary": ["Run errands", "Freshen up", "Tidy up"],
        "telugu_translation": {
            "telugu": "నేను సాధారణంగా ఉదయం 6 గంటలకే నిద్రలేచి, ఒక కప్పు టీ తాగుతాను.",
            "literal": "I generally in morning at 6 clock wake up and drink one cup tea.",
            "polished": "I usually wake up at 6:00 AM and have a cup of tea.",
            "feedback": "In English, say 'have a cup of tea' and specify time as '6:00 AM'."
        }
    }

    word_info = words_of_day[theme_idx] if words_of_day else {
        "word": "Run errands",
        "meaning": "Do short daily trips to accomplish chores",
        "usage": "I need to run a few errands before dinner."
    }

    telugu_data = theme_info.get("telugu_translation", {})

    # Generate 5-part interactive questions
    questions = [
        # Section 1: Daily Routine & Habits (2 MCQs)
        {
            "id": 1,
            "section": "1. Daily Routine & Habits",
            "question": f"In your daily routine ({theme_info['theme']}), which sentence is grammatically natural?",
            "options": {
                "a": f"I am usually {theme_info['vocabulary'][0].lower()} every morning.",
                "b": f"I usually {theme_info['vocabulary'][0].lower()} every morning.",
                "c": f"I usually {theme_info['vocabulary'][0].lower()}s every morning."
            },
            "answer": "b",
            "explanation": f"<b>Correct: Option B</b><br>Habitual daily actions take the Simple Present tense (<i>I usually {theme_info['vocabulary'][0].lower()}</i>). Never pair 'am' directly with a base action verb.",
            "audio_prompt": ""
        },
        {
            "id": 2,
            "section": "1. Daily Routine & Habits",
            "question": "When describing an action you are doing at home right now, select the correct response:",
            "options": {
                "a": "I am tidying up the living room right now.",
                "b": "I tidying up the living room right now.",
                "c": "I am tidy up the living room right now."
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>Actions in progress require the Present Continuous form (<i>am + verb-ing</i>).",
            "audio_prompt": ""
        },

        # Section 2: Everyday Vocabulary & Word Match (2 MCQs)
        {
            "id": 3,
            "section": "2. Everyday Vocabulary & Word Match",
            "question": f"What does the phrase '{word_info['word']}' mean in daily conversation?",
            "options": {
                "a": f"To run fast in a race.",
                "b": f"{word_info['meaning']}.",
                "c": "To cancel all daily plans."
            },
            "answer": "b",
            "explanation": f"<b>Correct: Option B</b><br>'{word_info['word']}' means: {word_info['meaning']}. Example: <i>\"{word_info['usage']}\"</i>",
            "audio_prompt": ""
        },
        {
            "id": 4,
            "section": "2. Everyday Vocabulary & Word Match",
            "question": f"Which term best fits: 'Sorry I'm late, fresh vegetables were __________ at the market.'",
            "options": {
                "a": "out of stock",
                "b": "run errands",
                "c": "drop by"
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>'Out of stock' means goods or produce are temporarily unavailable in store.",
            "audio_prompt": ""
        },

        # Section 3: Listening to Spoken English (2 Audio Clips)
        {
            "id": 5,
            "section": "3. Listening to Spoken English",
            "question": "Listen to the audio clip. What is the speaker requesting you to do?",
            "options": {
                "a": "Stop what you are doing and leave immediately.",
                "b": "Pick up a fresh packet of tea from the store on your way home.",
                "c": "Call a taxi for tomorrow morning."
            },
            "answer": "b",
            "explanation": "<b>Correct: Option B</b><br>The speaker asks: <i>'Could you please pick up a fresh packet of tea from the store on your way home?'</i>",
            "audio_prompt": "Could you please pick up a fresh packet of tea from the store on your way home?"
        },
        {
            "id": 6,
            "section": "3. Listening to Spoken English",
            "question": "Listen to the second audio clip. What is the core message?",
            "options": {
                "a": "The speaker wants to drop by your place this evening for a quick chat.",
                "b": "The speaker is cancelling all plans for the week.",
                "c": "The speaker is asking for directions to the bus station."
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>The speaker says: <i>'Hey! I'll drop by your place this evening around 6:00 PM for a quick chat.'</i>",
            "audio_prompt": "Hey! I will drop by your place this evening around 6:00 PM for a quick chat."
        },

        # Section 4: Polite Social Expressions (2 MCQs)
        {
            "id": 7,
            "section": "4. Polite Social Expressions",
            "question": "How should you politely ask a neighbor or colleague for assistance?",
            "options": {
                "a": "Give me help right now.",
                "b": "Could you please lend me a hand with this for a minute?",
                "c": "You must assist me."
            },
            "answer": "b",
            "explanation": "<b>Correct: Option B</b><br>'Lend a hand' is a courteous, friendly idiom for asking for assistance politely.",
            "audio_prompt": ""
        },
        {
            "id": 8,
            "section": "4. Polite Social Expressions",
            "question": "Choose the most polite way to decline an invitation when you are busy:",
            "options": {
                "a": "I would love to come, but I have a prior commitment.",
                "b": "No, I am not coming to your house.",
                "c": "Don't invite me today."
            },
            "answer": "a",
            "explanation": "<b>Correct: Option A</b><br>'I would love to come, but...' acknowledges the invitation warmly while declining politely.",
            "audio_prompt": ""
        },

        # Section 5: Real-Life Telugu ➔ English Translation (1 Interactive Scenario)
        {
            "id": 9,
            "section": "5. Real-Life Telugu ➔ English Translation",
            "question": f"Translate this Telugu daily scenario to natural conversational English:<br><br><b>Telugu:</b> \"{telugu_data.get('telugu', '')}\"<br><i>(Literal attempt: \"{telugu_data.get('literal', '')}\")</i>",
            "options": {
                "a": f"{telugu_data.get('literal', '')}",
                "b": f"{telugu_data.get('polished', '')}",
                "c": "I morning wake up and tea drinking."
            },
            "answer": "b",
            "explanation": f"<b>AI Feedback & Scoring (9/10):</b><br>{telugu_data.get('feedback', '')}<br><br><b>Natural Version:</b> <i>\"{telugu_data.get('polished', '')}\"</i>",
            "audio_prompt": f"Natural English phrasing: {telugu_data.get('polished', '')}"
        }
    ]

    return word_info, questions

def main():
    curriculum = load_curriculum()
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for level in ["beginner", "intermediate", "advanced"]:
        level_dir = os.path.join(root_dir, level)
        day_num = get_next_day_num(level_dir)

        word_info, questions = generate_test_for_day(level, day_num, curriculum)

        test_data = {
            "day": day_num,
            "date": today_str,
            "level": level,
            "title": f"FluencyCraft Everyday English - Day {day_num:02d}",
            "word_of_the_day": word_info,
            "total_questions": len(questions),
            "questions": questions
        }

        day_filename = f"day-{day_num:02d}.json"
        day_path = os.path.join(level_dir, day_filename)
        latest_path = os.path.join(level_dir, "latest.json")

        with open(day_path, "w", encoding="utf-8") as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)

        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)

        print(f"[{level.upper()}] Generated {day_filename} and updated latest.json ({len(questions)} questions)")

if __name__ == "__main__":
    main()

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
    return {
        "beginner": {"title": "Everyday Essentials", "sections": ["Daily Habits", "Past Memories", "Listening Prompts", "Everyday Reading"]},
        "intermediate": {"title": "Foundational Workplace Fluency", "sections": ["Daily Updates", "Completed Actions", "Workplace Listening", "Workplace Writing"]},
        "advanced": {"title": "Executive Communication", "sections": ["Strategic Negotiations", "Complex Syntax", "Executive Tone", "High-Stakes Writing"]}
    }

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

def call_gemini_api(prompt, api_key):
    models = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash"]
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "responseMimeType": "application/json"
        }
    }).encode("utf-8")

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text)
        except Exception as e:
            print(f"Warning: Model {model} failed ({e}), trying fallback...")
            continue
    raise RuntimeError("All Gemini API models failed.")

def generate_fallback_questions(level, day_num):
    questions = []
    level_titles = {
        "beginner": "Everyday Conversation & Routines",
        "intermediate": "Professional Workplace Communication",
        "advanced": "Executive Leadership & Diplomacy"
    }
    for i in range(1, 21):
        sec_num = ((i - 1) // 5) + 1
        questions.append({
            "id": i,
            "section": f"Section {sec_num}",
            "question": f"Sample question {i} for {level} level (Day {day_num:02d}). Select the correct grammatical option:",
            "options": {
                "a": "Option A - Grammatically incomplete phrasing.",
                "b": "Option B - Correct and standard English usage.",
                "c": "Option C - Unnatural sentence structure."
            },
            "answer": "b",
            "explanation": "<b>Correct: Option B</b><br>Option B represents standard English grammar and professional phrasing.",
            "audio_prompt": f"Listen carefully to scenario number {i} for {level} fluency."
        })
    return questions

def generate_test_for_level(level, info, day_num, api_key):
    prompt = f"""
You are an expert English Language Pedagogy AI creating a daily 20-question English test for Level: '{level.upper()}'.
Title: {info.get('title')}
Description: {info.get('description', '')}
Sections: {json.dumps(info.get('sections', []))}

Generate exactly 20 multiple-choice questions (5 questions per section across 4 sections).
Output MUST be a JSON object matching this schema:
{{
  "title": "{info.get('title')} - Day {day_num:02d}",
  "questions": [
    {{
      "id": 1,
      "section": "1. Section Name",
      "question": "Clear, contextual question or fill-in-the-blank prompt",
      "options": {{
        "a": "First choice",
        "b": "Second choice",
        "c": "Third choice"
      }},
      "answer": "a",
      "explanation": "<b>Correct: Explanation</b><br>Grammatical rule or workplace rationale.",
      "audio_prompt": "Short audio transcript for listening questions (if applicable, else empty string)"
    }}
  ]
}}

Ensure high quality, non-repetitive, real-world practical scenarios suited for {level} learners.
Return ONLY valid JSON.
"""

    if api_key:
        try:
            print(f"Calling Gemini API for {level} (Day {day_num:02d})...")
            data = call_gemini_api(prompt, api_key)
            if "questions" in data and len(data["questions"]) >= 20:
                return data["questions"][:20]
        except Exception as e:
            print(f"API call failed for {level}: {e}. Falling back to default generator.")
    
    return generate_fallback_questions(level, day_num)

def main():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("Notice: GEMINI_API_KEY environment variable not set. Generating fallback daily tests.")

    curriculum = load_curriculum()
    today_str = datetime.utcnow().strftime("%Y-%m-%d")

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for level in ["beginner", "intermediate", "advanced"]:
        level_info = curriculum.get(level, {})
        level_dir = os.path.join(root_dir, level)
        day_num = get_next_day_num(level_dir)

        questions = generate_test_for_level(level, level_info, day_num, api_key)

        test_data = {
            "day": day_num,
            "date": today_str,
            "level": level,
            "title": f"FluencyCraft {level.capitalize()} - Day {day_num:02d}",
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

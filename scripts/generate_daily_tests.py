#!/usr/bin/env python3
import os
import sys
import json
import re
import random
import urllib.request
import urllib.error
from datetime import datetime, timezone

def get_past_questions(level_dir):
    """
    Scans all existing day-XX.json files in the level directory
    and returns a set of all previously used question texts.
    """
    past_questions = set()
    if os.path.exists(level_dir):
        for fname in os.listdir(level_dir):
            if fname.startswith("day-") and fname.endswith(".json"):
                fpath = os.path.join(level_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        for q in data.get("questions", []):
                            if "question" in q:
                                clean_q = re.sub(r'<[^>]+>', '', q["question"]).strip().lower()
                                past_questions.add(clean_q)
                except Exception:
                    pass
    return past_questions

def get_day_concept_plan(level, day_num):
    """
    Returns planned daily living concept theme and focus for a given day and level.
    Supports 30+ distinct days per level.
    """
    level_str = level.lower()
    
    concepts_beginner = [
        {"theme": "Morning & Home Routines", "focus": "Everyday Home Routines & Basic Schedules", "why": "Expressing daily routines helps you speak without hesitation.", "word": "Run errands", "meaning": "Do short daily trips to accomplish chores", "usage": "I need to run errands before dinner."},
        {"theme": "Market & Grocery Shopping", "focus": "Market Shopping, Produce Selection & Pricing", "why": "Shopping for supplies requires asking about prices and weight politely.", "word": "Pick out", "meaning": "Carefully choose specific items from a group", "usage": "Help me pick out fresh tomatoes."},
        {"theme": "Travel, Autos & Cabs", "focus": "Neighborhood Travel & Commute Directions", "why": "Communicating ride directions and fares boosts independence.", "word": "Drop off", "meaning": "Take someone to a destination and leave them there", "usage": "Drop me off near the bus stand."},
        {"theme": "Clinic & Pharmacy Visits", "focus": "Doctor Symptoms & Medicine Dosage", "why": "Describing health conditions accurately ensures proper care.", "word": "On an empty stomach", "meaning": "Before eating food in the morning", "usage": "Take this tablet on an empty stomach."},
        {"theme": "Polite Social Manners", "focus": "Inviting Neighbors & Hospitality", "why": "Courteous invitations build friendly community relationships.", "word": "Drop by", "meaning": "Visit someone informally for a short time", "usage": "Please drop by our home for tea."},
        {"theme": "Phone Calls & Deliveries", "focus": "Delivery Tracking & Customer Support", "why": "Handling delivery calls smoothly prevents parcel delays.", "word": "Reach out to", "meaning": "Contact someone for help", "usage": "Reach out to support for parcel status."},
        {"theme": "Weekend Plans & Weather", "focus": "Outdoor Outings & Weather Forecasts", "why": "Discussing weekend plans makes casual chats enjoyable.", "word": "Grab a bite", "meaning": "Get a quick meal or snack", "usage": "Let's grab a bite after the movie."},
        {"theme": "Restaurant & Dining Out", "focus": "Ordering Food, Menu Items & Billing", "why": "Ordering food and asking for bills politely builds social confidence.", "word": "Order in", "meaning": "Request food delivered to your home", "usage": "Let us order in dinner tonight."},
        {"theme": "Bank & Financial Services", "focus": "Cash Withdrawals, UPI & Account Help", "why": "Managing banking interactions clearly protects your finances.", "word": "Fill out", "meaning": "Complete a official paper or online form", "usage": "Fill out this deposit slip at the counter."},
        {"theme": "Home Maintenance & Repairs", "focus": "Plumbing, Electrical & House Upkeep", "why": "Explaining home repair issues clearly helps technicians fix problems fast.", "word": "Fix up", "meaning": "Repair or renovate a damaged item", "usage": "We need to fix up the leaking tap."}
    ]

    concepts_intermediate = [
        {"theme": "Workplace Standups & Agendas", "focus": "Workplace Standups & Project Status Updates", "why": "Sharing clear status updates builds workplace credibility.", "word": "Circle back", "meaning": "Return to a topic later for follow-up", "usage": "Let us circle back to this item after lunch."},
        {"theme": "Client Communication & Updates", "focus": "Client Progress Reports & Expectations", "why": "Managing client expectations prevents project misunderstandings.", "word": "Touch base", "meaning": "Briefly connect with someone for info", "usage": "I will touch base with the team leader."},
        {"theme": "Team Collaboration & Workload", "focus": "Workload Balance & Deadline Extensions", "why": "Negotiating deadlines constructively maintains team trust.", "word": "Bottleneck", "meaning": "A congestion point delaying progress", "usage": "Testing is currently our main bottleneck."},
        {"theme": "Process Improvements & Feedback", "focus": "Workflow Streamlining & Problem Solving", "why": "Proposing fixes demonstrates professional initiative.", "word": "Streamline", "meaning": "Make a process more efficient", "usage": "We must streamline our code reviews."},
        {"theme": "Customer Escalations & Quality", "focus": "Resolving Complaints & Service Quality", "why": "De-escalating complaints diplomatically preserves accounts.", "word": "Iron out", "meaning": "Resolve minor details or discrepancies", "usage": "We will iron out contract terms today."},
        {"theme": "Technical Demos & Walkthroughs", "focus": "Feature Demos & Stakeholder Q&A", "why": "Explaining tech clearly helps non-technical partners decide.", "word": "Walk through", "meaning": "Demonstrate a process step by step", "usage": "Let me walk you through the new dashboard."},
        {"theme": "Performance Reviews & Goals", "focus": "Appraisals & Career Milestone Planning", "why": "Articulating achievements secures growth opportunities.", "word": "Step up", "meaning": "Take on extra responsibility when needed", "usage": "She stepped up to lead the sprint."}
    ]

    concepts_advanced = [
        {"theme": "Strategic Negotiation & Tone", "focus": "Diplomatic Refusals & Formal Negotiations", "why": "Executive communication requires modal diplomacy and syntax precision.", "word": "Iron out", "meaning": "Resolve minor details in an executive plan", "usage": "We need to iron out deal terms."},
        {"theme": "Stakeholder Alignment & Governance", "focus": "Fiscal Governance & Risk Hedging", "why": "Executive leadership demands financial syntax and risk hedging.", "word": "Hedge against", "meaning": "Protect an organization against loss", "usage": "Diversify to hedge against volatility."},
        {"theme": "Corporate Governance & Crisis", "focus": "Media Statements & Regulatory Compliance", "why": "Handling crisis communications protects company reputation.", "word": "Benchmark", "meaning": "Evaluate against industry standards", "usage": "We benchmark against international standards."},
        {"theme": "Strategic Pivots & Innovation", "focus": "Change Management & Enterprise Pivots", "why": "Framing major strategic shifts inspires investor confidence.", "word": "Pivot", "meaning": "Fundamentally shift business focus", "usage": "The company decided to pivot to cloud services."},
        {"theme": "Mergers & Acquisition Synergies", "focus": "M&A Integration & Financial Due Diligence", "why": "Articulating merger synergies requires precise corporate vocabulary.", "word": "Hinge on", "meaning": "Depend entirely on a single vital factor", "usage": "Success hinges on seamless integration."}
    ]

    if level_str == "beginner":
        plan_list = concepts_beginner
    elif level_str == "intermediate":
        plan_list = concepts_intermediate
    else:
        plan_list = concepts_advanced

    idx = (day_num - 1) % len(plan_list)
    item = plan_list[idx]
    
    cycle_num = (day_num - 1) // len(plan_list) + 1
    theme_title = f"{item['theme']}" + (f" (Phase {cycle_num})" if cycle_num > 1 else "")
    concept_overview = f"Day {day_num}: {item['focus']}"
    
    return {
        "theme": theme_title,
        "concept_overview": concept_overview,
        "why_important": item["why"],
        "word_info": {
            "word": item["word"],
            "meaning": item["meaning"],
            "usage": item["usage"]
        }
    }

def generate_via_gemini_api(level, day_num, plan_info, past_questions):
    """
    On-Demand Generation via Gemini AI.
    Prompts Gemini AI with the planned concept and instructions to generate
    20 unique questions that do NOT match any questions in past_questions.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    past_samples = list(past_questions)[:40]
    past_questions_str = json.dumps(past_samples, ensure_ascii=False) if past_samples else "[]"

    prompt = f"""
    You are an expert English language pedagogue designing a 20-question conceptual practical English test for FluencyCraft ({level.capitalize()} track, Day {day_num}).

    CONCEPTUAL MODULE FOCUS:
    - Planned Topic: {plan_info['theme']}
    - Targeted Concept: {plan_info['concept_overview']}
    - Pedagogical Purpose: {plan_info['why_important']}
    - Difficulty Level: {level.capitalize()} (Ensure vocabulary, tense complexity, and sentence structure strictly match the {level.capitalize()} difficulty tier).

    CONCEPTUAL ALIGNMENT MANDATE:
    This test MUST NOT contain random disconnected questions. ALL 20 questions MUST be systematically and conceptually tied to '{plan_info['theme']}':
    1. Section 1 (Q1-4): Test tenses and habits applied directly within '{plan_info['theme']}'.
    2. Section 2 (Q5-8): Test vocabulary and phrasal verbs relevant to '{plan_info['theme']}'.
    3. Section 3 (Q9-12): Test natural connecting pillars (pair idioms) in contexts related to '{plan_info['theme']}'.
    4. Section 4 (Q13-16): Auditory listening clips representing realistic spoken dialogues within '{plan_info['theme']}'.
    5. Section 5 (Q17-20): Real-life Telugu -> English translation scenarios expressing thoughts within '{plan_info['theme']}'.

    OPTION SHUFFLING & RIGOR MANDATE:
    - Every question MUST contain EXACTLY 4 options: "a", "b", "c", "d".
    - Answer keys MUST be evenly and randomly distributed across "a", "b", "c", and "d" (~5 questions per option key across the 20 questions). NEVER place the answer in option 'a' or 'b' for all questions.
    - Distractor choices ("a", "b", "c", "d" that are not the answer) MUST be realistic, subtle English learner errors or plausible alternatives (e.g. wrong preposition, subtle tense confusion, plausible misinterpretation). NEVER use repetitive dummy options.
    - The "explanation" field MUST always explicitly begin with "<b>Correct: Option X</b><br>" where X is the uppercase letter of the correct answer key ("A", "B", "C", or "D").

    Ensure NO questions overlap with these previously used questions: {past_questions_str}.

    Required JSON Schema:
    {{
      "word_info": {{
        "word": "{plan_info['word_info']['word']}",
        "meaning": "{plan_info['word_info']['meaning']}",
        "usage": "{plan_info['word_info']['usage']}"
      }},
      "concept_overview": "{plan_info['concept_overview']}",
      "why_important": "{plan_info['why_important']}",
      "questions": [
        // 20 objects with id 1..20 following the 5 sections above. Each question object must have options object with keys "a", "b", "c", "d", answer key ("a", "b", "c", or "d"), explanation ("<b>Correct: Option X</b>..."), and audio_prompt string.
      ]
    }}

    Return ONLY raw valid JSON without markdown wrapping or code blocks.
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4, "responseMimeType": "application/json"}
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            res_data = json.loads(resp.read().decode('utf-8'))
            text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
            text = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
            text = re.sub(r'```$', '', text, flags=re.MULTILINE).strip()
            parsed = json.loads(text)
            
            if "questions" in parsed and len(parsed["questions"]) == 20:
                print(f"[{level.upper()}] Successfully generated 20 questions on demand via Gemini AI for Day {day_num}!")
                return (
                    parsed.get("word_info", plan_info["word_info"]),
                    parsed.get("concept_overview", plan_info["concept_overview"]),
                    parsed.get("why_important", plan_info["why_important"]),
                    parsed["questions"]
                )
    except Exception as e:
        print(f"[{level.upper()}] Gemini API on-demand call skipped/failed ({e}). Using dynamic synthesis generator.")
    return None

def generate_on_demand_synthesis(level, day_num, plan_info, past_questions):
    """
    Dynamic Combinatorial Synthesizer with Strict De-duplication.
    Generates 20 unique questions on demand by dynamically parametrizing contexts,
    scenarios, options, and explanations. Filters out any question in past_questions.
    """
    rng = random.Random(f"{level}_{day_num}_{datetime.now(timezone.utc).strftime('%Y%m%d')}")

    word_info = plan_info["word_info"]
    concept_overview = plan_info["concept_overview"]
    why_important = plan_info["why_important"]

    # Parameter pools
    subjects = ["I", "My sister", "My colleague", "Our neighbor", "The delivery executive", "My manager", "The cab driver", "The store vendor"]
    times = ["every morning", "right now", "yesterday afternoon", "this evening", "by 5:00 PM", "twice a week", "on weekends"]

    actions_pool = [
        ("making morning tea", "I am having a fresh cup of tea before leaving.", "I am have fresh cup tea."),
        ("tidying up the room", "I am tidying up the room right now.", "I am tidy up room."),
        ("preparing breakfast for family", "I prepared breakfast for my family this morning.", "I am prepare breakfast family."),
        ("buying fresh produce at the market", "I picked out fresh tomatoes and spinach at the market.", "I buyed vegetables market."),
        ("booking an auto ride", "Please drop me off near gate 2 of the metro station.", "Drop me station gate."),
        ("inquiring about doctor appointment", "I need to consult a doctor regarding a mild fever.", "Doctor meeting wanted for fever."),
        ("inviting neighbors for tea", "Please drop by our place this evening for tea.", "Evening come my house tea."),
        ("tracking a package delivery", "Will my parcel be delivered by 5:00 PM today?", "My parcel delivery coming today?"),
        ("rescheduling a team sync", "Could we reschedule our sync meeting to 3:00 PM?", "Shift meeting 3 clock possible?"),
        ("declining an out-of-scope task", "While I understand the urgency, our current bandwidth is full.", "No cannot do this work."),
        ("checking grocery item stock", "Fresh milk packets were completely out of stock.", "Milk packet no stock having."),
        ("asking for item weight price", "How much are these organic apples per kilo?", "Apples kg how much cost?"),
        ("giving street directions", "Take a left turn after crossing the traffic signal.", "Signal crossing left turn take."),
        ("ordering food at a restaurant", "Could we please see the menu and order starters?", "Menu giving order doing."),
        ("withdrawing cash from ATM", "Is this card accepted at the cash withdrawal counter?", "Card cash withdrawal taking?")
    ]

    phrasal_verbs_pool = [
        ("run errands", "do short daily trips for chores", "I need to run errands at the market before dinner."),
        ("freshen up", "wash hands and face to relax after travel", "Let me freshen up after returning home."),
        ("pick out", "carefully choose specific items from a group", "Could you help me pick out the best mangos?"),
        ("drop off", "take someone to a destination and leave them there", "Please drop me off near the bus stand."),
        ("drop by", "visit someone informally for a short time", "Feel free to drop by our home this evening."),
        ("reach out to", "contact someone for help or information", "I will reach out to customer support tomorrow."),
        ("circle back", "return to a topic later for follow-up", "Let us circle back to the timeline discussion."),
        ("touch base", "briefly connect with someone to exchange news", "I will touch base with you after the review."),
        ("iron out", "resolve minor problems or details in a plan", "We need one final sync to iron out contract details."),
        ("hedge against", "protect against potential financial or operational loss", "We must diversify to hedge against market risk."),
        ("call off", "cancel a planned event or meeting", "They had to call off the afternoon presentation."),
        ("follow up", "check progress on a prior matter", "I will follow up with the team regarding the report."),
        ("order in", "request food delivered home", "Let us order in dinner tonight."),
        ("fill out", "complete an official form", "Please fill out this registration form.")
    ]

    pillars_pool = [
        ("short and sweet", "brief, pleasant, and direct", "Keep the morning family update short and sweet."),
        ("bits and pieces", "small miscellaneous items", "I picked up a few bits and pieces from the store."),
        ("safe and sound", "completely unharmed and intact after travel", "Our family arrived home safe and sound after the trip."),
        ("spick and span", "neat, spotless, and orderly", "After cleaning, the living room is spick and span."),
        ("touch and go", "precarious or uncertain outcome", "The negotiation was touch and go until midnight."),
        ("first and foremost", "most importantly or above all else", "First and foremost, data security is our top priority."),
        ("part and parcel", "an unavoidable essential component", "Audits are part and parcel of this industry."),
        ("by and large", "overall or generally speaking", "By and large, the project achieved all key milestones."),
        ("pros and cons", "advantages and disadvantages of a decision", "We carefully weighed all the pros and cons before deciding."),
        ("give and take", "mutual compromise and flexibility", "Team success requires a healthy amount of give and take.")
    ]

    telugu_pool = [
        ("నేను సాధారణంగా ఉదయం 6 గంటలకే నిద్రలేచి ఒక కప్పు టీ తాగుతాను.", "I generally in morning 6 clock wake up drink tea.", "I usually wake up at 6:00 AM and have a cup of tea.", "Use 'have a cup of tea' and specify time as '6:00 AM'."),
        ("ఈ టమాటాలు కేజీ ఎంత? కొంచెం తాజావి ఏరి ఇవ్వండి.", "These tomatoes kg how much? Pick give fresh.", "How much are these tomatoes per kilo? Please pick out fresh ones for me.", "Use 'per kilo' for price and 'pick out' for selection."),
        ("అన్నా, బస్టాండ్ దగ్గర డ్రాప్ చేయండి, ఎంత అవుతుంది?", "Brother bus stand drop me, how much will become?", "Please drop me off near the bus stand. How much is the fare?", "Avoid 'how much will become' and ask 'How much is the fare?'."),
        ("నాకు కొంచెం తలనొప్పిగా ఉంది, ఒక గంట సేపు రెస్ట్ తీసుకుంటాను.", "To me little headache is there, take rest one hour.", "I have a slight headache; I'm going to rest for an hour.", "Say 'I have a slight headache' instead of literal translations."),
        ("సాయంత్రం మా ఇంటికి రండి, టీ తాగుదాం.", "Evening my house come, tea drink.", "Please drop by our home this evening; we can have tea together.", "Use 'drop by our home' for informal invitations."),
        ("నా పార్సెల్ ఈ రోజు సాయంత్రానికి డెలివరీ అవుతుందా?", "My parcel today evening delivery becoming?", "Will my package be delivered by this evening?", "Use 'Will my package be delivered...' for delivery tracking."),
        ("రేపటి మీటింగ్ 3 గంటలకు రీషెడ్యూల్ చేయవచ్చా?", "Tomorrow meeting 3 clock reschedule possible?", "Could we reschedule tomorrow's meeting to 3:00 PM?", "Use 'Could we reschedule...' for polite professional requests."),
        ("ఈ ఒప్పందంలో కొన్ని మార్పులు చేస్తే బాగుంటుంది.", "In agreement some changes if do good.", "It would be advantageous to incorporate a few revisions into this agreement.", "Use executive diplomacy 'It would be advantageous to...'."),
        ("ముందుగా సమస్య యొక్క మూలకారణాన్ని కనుగొనాలి.", "First problem root cause finding wanted.", "First and foremost, we must identify the root cause of the issue.", "Use 'First and foremost' and 'identify the root cause'."),
        ("మీ ఆలోచన బాగుంది కానీ మన బడ్జెట్ దానికి అనుమతించదు.", "Your thought good but budget not allow.", "While your proposal is insightful, our current budget constraints prevent us from adopting it.", "Use diplomatic contrast 'While your proposal is insightful...'.")
    ]

    questions = []
    used_questions_clean = set(past_questions)

    def is_unique(q_str):
        clean = re.sub(r'<[^>]+>', '', q_str).strip().lower()
        if clean in used_questions_clean:
            return False
        used_questions_clean.add(clean)
        return True

    def create_shuffled_question(q_id, section, q_text, correct_choice, distractor1, distractor2, distractor3, exp_body, audio_prompt=""):
        choices = [
            (correct_choice, True),
            (distractor1, False),
            (distractor2, False),
            (distractor3, False)
        ]
        rng.shuffle(choices)
        
        keys = ["a", "b", "c", "d"]
        options = {}
        correct_key = "a"
        for i, (text_val, is_corr) in enumerate(choices):
            k = keys[i]
            options[k] = text_val
            if is_corr:
                correct_key = k
                
        explanation = f"<b>Correct: Option {correct_key.upper()}</b><br>{exp_body}"
        return {
            "id": q_id,
            "section": section,
            "question": q_text,
            "options": options,
            "answer": correct_key,
            "explanation": explanation,
            "audio_prompt": audio_prompt
        }

    # Section 1: Daily Routine & Habits (Q1-4)
    rng.shuffle(actions_pool)
    q_id = 1
    for act, correct_sent, wrong_sent in actions_pool:
        if q_id > 4:
            break
        subj = rng.choice(subjects)
        t_val = rng.choice(times)
        q_text = f"Day {day_num} Practice ({plan_info['theme']}): When talking about {act} ({t_val}), which sentence is grammatically correct for '{subj}'?"
        
        if not is_unique(q_text):
            q_text = f"Day {day_num} Scenario ({plan_info['theme']}): Select the natural English phrasing when {subj} is {act} {t_val}:"
            if not is_unique(q_text):
                continue
                
        d1 = wrong_sent
        d2 = wrong_sent.replace("am", "is").replace("I ", "He ") if "am" in wrong_sent else f"I am {act} right now."
        d3 = correct_sent.replace("am", "was") if "am" in correct_sent else wrong_sent + " yesterday"
        exp_body = f"Natural everyday English uses standard tense agreement: <i>\"{correct_sent}\"</i>."
        
        questions.append(create_shuffled_question(q_id, "1. Daily Routine & Habits", q_text, correct_sent, d1, d2, d3, exp_body))
        q_id += 1

    # Section 2: Vocabulary & Phrasal Verbs (Q5-8)
    rng.shuffle(phrasal_verbs_pool)
    q_id = 5
    for pv, meaning, example in phrasal_verbs_pool:
        if q_id > 8:
            break
        q_text = f"Day {day_num} Vocabulary ({plan_info['theme']}): What is the exact practical meaning of the phrase '{pv}'?"
        if not is_unique(q_text):
            q_text = f"Day {day_num} Terms ({plan_info['theme']}): Choose the correct definition for the phrasal verb '{pv}':"
            if not is_unique(q_text):
                continue

        correct_choice = f"{meaning.capitalize()}."
        d1 = "To postpone or cancel an activity indefinitely."
        d2 = "To perform a daily task hastily without preparation."
        d3 = "To clean or inspect a physical room thoroughly."
        exp_body = f"'{pv}' means: {meaning}. Example: <i>\"{example}\"</i>"

        questions.append(create_shuffled_question(q_id, "2. Everyday Vocabulary & Phrasal Verbs", q_text, correct_choice, d1, d2, d3, exp_body))
        q_id += 1

    # Section 3: Connecting Pillars (Q9-12)
    rng.shuffle(pillars_pool)
    q_id = 9
    for pil, pil_meaning, pil_ex in pillars_pool:
        if q_id > 12:
            break
        q_text = f"Day {day_num} Connecting Pillars ({plan_info['theme']}): Complete the sentence: '{pil_ex.replace(pil, '__________')}'"
        if not is_unique(q_text):
            q_text = f"Day {day_num} Pair Idioms ({plan_info['theme']}): Fill in the blank with the best connecting pillar: '{pil_ex.replace(pil, '__________')}'"
            if not is_unique(q_text):
                continue

        correct_choice = pil
        d1 = "touch and go" if pil != "touch and go" else "spick and span"
        d2 = "bits and pieces" if pil != "bits and pieces" else "short and sweet"
        d3 = "part and parcel" if pil != "part and parcel" else "first and foremost"
        exp_body = f"'{pil}' is a natural connecting pillar meaning: {pil_meaning}."

        questions.append(create_shuffled_question(q_id, "3. Connecting Pillars & Expressions", q_text, correct_choice, d1, d2, d3, exp_body))
        q_id += 1

    # Section 4: Listening (Q13-16)
    rng.shuffle(actions_pool)
    q_id = 13
    for act, correct_sent, wrong_sent in actions_pool:
        if q_id > 16:
            break
        q_text = f"Day {day_num} Auditory Clip {q_id - 12} ({plan_info['theme']}): Listen to the audio snippet. What instruction is given?"
        if not is_unique(q_text):
            q_text = f"Day {day_num} Spoken Clip {q_id - 12} ({plan_info['theme']}): Listen to the audio prompt. What message is shared?"
            if not is_unique(q_text):
                continue

        correct_choice = f"The speaker says: \"{correct_sent}\""
        d1 = f"The speaker says: \"{wrong_sent}\""
        d2 = "The speaker is requesting to cancel all scheduled meetings for today."
        d3 = "The speaker is asking for urgent driving directions to the station."
        exp_body = f"The speaker states: <i>\"{correct_sent}\"</i>"

        questions.append(create_shuffled_question(q_id, "4. Listening to Spoken English", q_text, correct_choice, d1, d2, d3, exp_body, audio_prompt=correct_sent))
        q_id += 1

    # Section 5: Telugu Translation (Q17-20)
    rng.shuffle(telugu_pool)
    q_id = 17
    for tel, lit, nat, exp in telugu_pool:
        if q_id > 20:
            break
        q_text = f"Day {day_num} Translation Scenario {q_id - 16} ({plan_info['theme']}):<br><br><b>Telugu:</b> \"{tel}\"<br><i>(Literal attempt: \"{lit}\")</i>"
        if not is_unique(q_text):
            q_text = f"Day {day_num} Telugu Scenario {q_id - 16} ({plan_info['theme']}):<br><br><b>Telugu:</b> \"{tel}\"<br><i>(Word-by-word: \"{lit}\")</i>"
            if not is_unique(q_text):
                continue

        clean_nat = nat.replace("'", "\\'")
        correct_choice = nat
        d1 = lit
        d2 = f"I am needing to {lit.lower()}" if len(lit) > 10 else "Word by word direct conversion"
        d3 = "Literal Indian English phrasing without modal polite verbs."
        exp_body = f"<b>Natural Version:</b> <i>\"{nat}\"</i><br><br>{exp}<br><button type=\"button\" class=\"audio-btn\" style=\"margin-top:10px; display:inline-flex; align-items:center; gap:6px;\" onclick=\"playPrompt('{clean_nat}')\">🔊 Listen to Polished Pronunciation</button>"

        questions.append(create_shuffled_question(q_id, "5. Real-Life Telugu ➔ English Translation", q_text, correct_choice, d1, d2, d3, exp_body))
        q_id += 1

    return word_info, concept_overview, why_important, questions

def generate_20_questions(level, day_num, level_dir):
    past_questions = get_past_questions(level_dir)
    plan_info = get_day_concept_plan(level, day_num)

    api_result = generate_via_gemini_api(level, day_num, plan_info, past_questions)
    if api_result:
        return api_result

    return generate_on_demand_synthesis(level, day_num, plan_info, past_questions)

def build_json_payload(level, day_num, word_info, concept_overview, why_important, questions):
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return {
        "day": day_num,
        "date": today_str,
        "level": level.lower(),
        "title": f"FluencyCraft {level.capitalize()} - Day {day_num:02d}",
        "concept_overview": concept_overview,
        "why_important": why_important,
        "word_of_the_day": word_info,
        "total_questions": len(questions),
        "questions": questions
    }

def build_standalone_html(level, day_num, word_info, concept_overview, why_important, questions):
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
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

  <div class="wod-banner">
    <div class="wod-header">🌟 Word of the Day & Everyday Phrase</div>
    <div class="wod-title">{word_info.get('word', 'Run errands')}</div>
    <div class="wod-meaning">Meaning: {word_info.get('meaning', '')}</div>
    <div class="wod-usage">
      <span>Usage: "{word_info.get('usage', '')}"</span>
      <button type="button" class="audio-btn" style="margin:0; background:white; color:#047857;" onclick="playPrompt('{word_info.get('word', '')}. {word_info.get('usage', '')}')">🔊 Listen</button>
    </div>
  </div>

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
  const CURRENT_LEVEL = "{level.lower()}";
  const CURRENT_DAY = {day_num};
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

  function markDayCompleted() {{
    let completed = [];
    try {{
      completed = JSON.parse(localStorage.getItem('fluencycraft_completed_days_' + CURRENT_LEVEL) || '[]');
    }} catch(e) {{ completed = []; }}
    if (!completed.includes(CURRENT_DAY)) {{
      completed.push(CURRENT_DAY);
      localStorage.setItem('fluencycraft_completed_days_' + CURRENT_LEVEL, JSON.stringify(completed));
    }}
  }}

  function restoreSavedAnswers() {{
    let savedMap = {{}};
    try {{
      savedMap = JSON.parse(localStorage.getItem(TEST_STORAGE_KEY) || '{{}}');
    }} catch(e) {{ savedMap = {{}}; }}

    for (let qKey in savedMap) {{
      const val = savedMap[qKey];
      const radio = document.querySelector(`input[name="${'{'}qKey{'}'}"][value="${'{'}val{'}'}"]`);
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
        const cleanAudio = q.audio_prompt.replace(/'/g, "\\'");
        audioHtml = `<button type="button" class="audio-btn" onclick="playPrompt('${{cleanAudio}}')">🔊 Listen to Audio Clip</button>`;
      }}

      let optionsHtml = '';
      const optKeys = Object.keys(q.options || {{}});
      optKeys.forEach(optKey => {{
        const keyUpper = optKey.toUpperCase();
        const valText = q.options[optKey];
        optionsHtml += `<label class="option-label" id="label_q${{qNum}}_${{optKey}}"><input type="radio" name="q${{qNum}}" value="${{optKey}}" onchange="onAnswerSelected('q${{qNum}}', '${{optKey}}', true)"> ${{keyUpper}}) ${{valText}}</label>`;
      }});

      card.innerHTML = `
        <div style="font-size:0.8rem; font-weight:800; color:var(--primary); text-transform:uppercase; margin-bottom:6px;">${{q.section || ''}}</div>
        ${{audioHtml}}
        <p class="question">${{qNum}}. ${{q.question}}</p>
        <div class="options" id="optionsGroup_${{qNum}}">
          ${{optionsHtml}}
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

    markDayCompleted();

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
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
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

    .locked-card {{
      background: #fef2f2;
      border: 2px dashed #ef4444;
      border-radius: 16px;
      padding: 32px 24px;
      text-align: center;
      margin-bottom: 24px;
    }}
    .locked-card h2 {{ color: #991b1b; font-size: 1.5rem; font-weight: 800; margin-bottom: 10px; }}
    .locked-card p {{ color: #7f1d1d; font-size: 1rem; max-width: 600px; margin: 0 auto 20px; }}

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

  <!-- Lock screen container for weekdays -->
  <div id="weekdayLockedContainer" style="display:none;">
    <div class="locked-card">
      <h2>🔒 Weekend Weak-Spot Test is Locked Today</h2>
      <p>This adaptive review test automatically unlocks on <b>Saturday</b> and <b>Sunday</b>. Complete your daily Monday through Friday practice sessions to log your weak spots!</p>
      <a href="../../index.html" class="audio-btn" style="background:#1e40af; color:white; padding:12px 24px; text-decoration:none; font-size:0.95rem;">Return to Daily Practice Dropdown</a>
    </div>
  </div>

  <div id="weekendActiveContainer">
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

</div>

<script>
  const defaultQuestions = {default_questions_js};
  let questionsData = [];
  const answerKeyMap = {{}};
  const userAnswersMap = {{}};

  window.addEventListener('DOMContentLoaded', () => {{
    loadNameState();
    checkWeekendAccess();
  }});

  function checkWeekendAccess() {{
    const dayOfWeek = new Date().getDay(); // 0 = Sunday, 6 = Saturday
    const isWeekend = (dayOfWeek === 0 || dayOfWeek === 6);

    // If URL has ?override=true or if it's weekend (Sat/Sun), unlock test
    const urlParams = new URLSearchParams(window.location.search);
    const forceUnlock = urlParams.get('override') === 'true';

    if (isWeekend || forceUnlock) {{
      document.getElementById('weekendActiveContainer').style.display = 'block';
      document.getElementById('weekdayLockedContainer').style.display = 'none';
      loadAdaptiveQuestions();
    }} else {{
      document.getElementById('weekendActiveContainer').style.display = 'none';
      document.getElementById('weekdayLockedContainer').style.display = 'block';
    }}
  }}

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

      let optionsHtml = '';
      const optKeys = Object.keys(q.options || {{}});
      optKeys.forEach(optKey => {{
        const keyUpper = optKey.toUpperCase();
        const valText = q.options[optKey];
        optionsHtml += `<label class="option-label" id="label_q${{qNum}}_${{optKey}}"><input type="radio" name="q${{qNum}}" value="${{optKey}}" onchange="onAnswerSelected('q${{qNum}}', '${{optKey}}', true)"> ${{keyUpper}}) ${{valText}}</label>`;
      }});

      card.innerHTML = `
        <div style="font-size:0.8rem; font-weight:800; color:var(--primary); text-transform:uppercase; margin-bottom:6px;">${{q.section || ''}}</div>
        ${{audioHtml}}
        <p class="question">${{qNum}}. ${{q.question}}</p>
        <div class="options" id="optionsGroup_${{qNum}}">
          ${{optionsHtml}}
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
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tests_root_dir = os.path.join(root_dir, "tests")

    increment_day = os.getenv("INCREMENT_DAY", "false").lower() in ["true", "1", "yes"]
    if "--increment" in sys.argv or "--new-day" in sys.argv:
        increment_day = True

    specified_day = None
    for arg in sys.argv[1:]:
        if arg.isdigit():
            specified_day = int(arg)

    today_weekday = datetime.now(timezone.utc).weekday() # 5 = Saturday, 6 = Sunday
    is_weekend = (today_weekday in [5, 6]) or ("--weekend" in sys.argv)
    
    if is_weekend and specified_day is None:
        print("[WEEKEND POLICY] Today is Weekend (Saturday/Sunday). Regular daily test generation is paused to focus strictly on Weekend Weak-Spot Review.")
        increment_day = False

    for level in ["beginner", "intermediate", "advanced"]:
        level_dir = os.path.join(tests_root_dir, level)
        os.makedirs(level_dir, exist_ok=True)

        existing_days = []
        if os.path.exists(level_dir):
            for fname in os.listdir(level_dir):
                match = re.match(r"^day-(\d+)\.html$", fname)
                if match:
                    existing_days.append(int(match.group(1)))

        if specified_day is not None:
            day_num = specified_day
        elif increment_day:
            day_num = (max(existing_days) + 1) if existing_days else 1
        else:
            day_num = max(existing_days) if existing_days else 1

        word_info, concept_overview, why_important, questions = generate_20_questions(level, day_num, level_dir)

        html_content = build_standalone_html(level, day_num, word_info, concept_overview, why_important, questions)
        weekend_content = build_weekend_test_html(level, questions)
        json_content = build_json_payload(level, day_num, word_info, concept_overview, why_important, questions)

        day_filename = f"day-{day_num:02d}.html"
        json_filename = f"day-{day_num:02d}.json"
        
        day_path = os.path.join(level_dir, day_filename)
        json_path = os.path.join(level_dir, json_filename)
        latest_html_path = os.path.join(level_dir, "latest.html")
        latest_json_path = os.path.join(level_dir, "latest.json")
        weekend_path = os.path.join(level_dir, "weekend-test.html")

        with open(day_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_content, f, indent=2, ensure_ascii=False)

        with open(latest_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        with open(latest_json_path, "w", encoding="utf-8") as f:
            json.dump(json_content, f, indent=2, ensure_ascii=False)

        with open(weekend_path, "w", encoding="utf-8") as f:
            f.write(weekend_content)

        print(f"[{level.upper()}] Generated tests/{level}/{day_filename}, {json_filename}, latest.html/json, and weekend-test.html (Day {day_num})")

    # Update AVAILABLE_DAYS in index.html dynamically
    index_path = os.path.join(root_dir, "index.html")
    if os.path.exists(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                idx_content = f.read()
            
            day_counts = {}
            for lvl in ["beginner", "intermediate", "advanced"]:
                lvl_dir = os.path.join(tests_root_dir, lvl)
                max_d = 1
                if os.path.exists(lvl_dir):
                    for fn in os.listdir(lvl_dir):
                        m = re.match(r"^day-(\d+)\.html$", fn)
                        if m:
                            max_d = max(max_d, int(m.group(1)))
                day_counts[lvl] = max_d
            
            new_days_block = f"const AVAILABLE_DAYS = {{\n      beginner: {day_counts['beginner']},\n      intermediate: {day_counts['intermediate']},\n      advanced: {day_counts['advanced']}\n    }};"
            updated_idx = re.sub(r'const AVAILABLE_DAYS = \{[^}]+\};', new_days_block, idx_content)
            
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(updated_idx)
            print(f"[INDEX.HTML] Updated AVAILABLE_DAYS: {day_counts}")
        except Exception as e:
            print(f"[INDEX.HTML] Could not update index.html AVAILABLE_DAYS: {e}")

if __name__ == "__main__":
    main()

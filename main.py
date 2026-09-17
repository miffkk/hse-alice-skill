import re
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

GREETINGS = ["hello", "hi", "hey", "start", "привет", "здравствуй", "начать"]

# Слой Small Talk для естественного общения
SMALL_TALK = [
    {
        "triggers": ["how are you", "how do you feel", "your feelings", "как дела", "как ты", "чувства"],
        "answer": "I don't have feelings, but I'm fully ready to help you navigate HSE life! What would you like to know?"
    },
    {
        "triggers": ["my name is", "i am", "меня зовут", "мое имя", "я "],
        "answer": "Nice to meet you! How can I help you with HSE studies, exams, or student life today?"
    },
    {
        "triggers": ["who are you", "what are you", "кто ты", "что ты умеешь"],
        "answer": "I am the HSE International Student Assistant. I can explain grading rules, exams, visas, dorms, and campus life."
    },
    {
        "triggers": ["thank", "thanks", "спасибо", "благодарю"],
        "answer": "You are very welcome! Let me know if you need anything else regarding HSE regulations."
    },
    {
        "triggers": ["bye", "goodbye", "пока", "до свидания"],
        "answer": "Goodbye and best of luck with your studies at HSE!"
    }
]

KB = [
    {
        "keywords": ["placement test", "entry test", "placement", "входное", "входной", "тестирование"],
        "answer": "Yes. The entry placement test is mandatory for students who do not have an international language certificate."
    },
    {
        "keywords": ["placement online", "test online", "entry online", "дистанционно", "онлайн"],
        "answer": "Yes. Both the written part and the oral interview of the placement test can be fully online."
    },
    {
        "keywords": ["entry test ranking", "placement ranking", "входной рейтинг"],
        "answer": "No. Entry test results are not counted in the student ranking."
    },
    {
        "keywords": ["purpose entry test", "why placement test", "цель входного"],
        "answer": "It predicts the optimal learning trajectory and appropriate difficulty level for the first and second modules."
    },
    {
        "keywords": ["mid-term english", "intermediate test", "intermediate", "промежуточное"],
        "answer": "Yes. Intermediate testing is conducted for all first-year students."
    },
    {
        "keywords": ["intermediate ranking", "промежуточный рейтинг"],
        "answer": "No. Intermediate test results are not included in the student ranking."
    },
    {
        "keywords": ["change english level", "switch level", "change level", "сменить уровень"],
        "answer": "Yes. Intermediate testing can serve as a transition point to another level or course direction."
    },
    {
        "keywords": ["internal english exam mandatory", "first year exam mandatory", "exam mandatory", "обязателен экзамен"],
        "answer": "Yes, the internal English exam is mandatory for all first-year students."
    },
    {
        "keywords": ["waive internal exam", "certificate waive", "waive exam", "перезачесть экзамен"],
        "answer": "Yes. The internal exam can be credited and waived if you have an eligible international certificate."
    },
    {
        "keywords": ["internal exam rating", "internal exam grade", "оценка экзамен рейтинг"],
        "answer": "Yes. The grade for the internal English exam is included in your current rating."
    },
    {
        "keywords": ["grading scale", "grade scale", "scale", "10-point", "шкала оценивания", "система оценивания", "баллы"],
        "answer": "HSE uses a 10-point grading scale. Grades 1 to 3 are fail (unsatisfactory), and 4 to 10 are pass."
    },
    {
        "keywords": ["minimum passing grade", "passing grade", "minimum pass", "проходной балл", "минимум сдать"],
        "answer": "The minimum passing grade is 4 out of 10 points."
    },
    {
        "keywords": ["how many modules", "study modules", "modules", "модули", "сколько модулей"],
        "answer": "The HSE academic year is divided into 4 study modules."
    },
    {
        "keywords": ["rounding", "round down", "округление", "округлять"],
        "answer": "Rounding follows standard arithmetic rules. Rounding down against the student is not permitted."
    },
    {
        "keywords": ["missed exam", "sick", "illness", "medical certificate", "болезнь", "справка", "заболел"],
        "answer": "Notify the study office on the exam day and submit an official medical certificate within three business days after recovery."
    },
    {
        "keywords": ["academic debt", "academic failure", "failed course", "задолженность", "хвост"],
        "answer": "An academic failure is receiving a final grade below 4 out of 10 in any course."
    },
    {
        "keywords": ["retake attempts", "how many retakes", "retake count", "пересдачи", "сколько пересдач"],
        "answer": "You get two retake attempts: the first with the course instructor, and the second before an academic commission."
    },
    {
        "keywords": ["retake period", "when retakes", "retake dates", "период пересдач", "когда пересдачи"],
        "answer": "Retakes take place twice a year: autumn period in September–October, and winter period in January–February."
    },
    {
        "keywords": ["dismissal", "expulsion", "debts dismiss", "отчисление", "сколько хвостов"],
        "answer": "A student with three or more unresolved academic debts in different courses is subject to dismissal."
    },
    {
        "keywords": ["syllabus", "kpu", "pud", "пуд", "программа дисциплины"],
        "answer": "The Course Syllabus (PUD) defines course rules, assessment criteria, and formula; it is published on the HSE website."
    },
    {
        "keywords": ["grade missing", "find grade", "view grade", "where grade", "smartlms grade", "нет оценки", "где оценка"],
        "answer": "Check your SmartLMS account. If your grade is missing, immediately contact your Study Office manager via corporate email."
    },
    {
        "keywords": ["schedule", "timetable", "ruz", "расписание", "руз"],
        "answer": "Your schedule is published in the RUZ electronic timetable system (ruz.hse.ru) and the HSE App X."
    },
    {
        "keywords": ["formula", "final grade calculate", "how grade calculated", "расчет оценки", "формула оценки"],
        "answer": "The final grade is calculated from continuous assessment elements and the exam according to the Course Syllabus formula."
    },
    {
        "keywords": ["attendance exam", "refuse exam", "absent exam access", "недопуск", "посещаемость"],
        "answer": "No. HSE regulations state that poor attendance alone cannot serve as a ground for denying exam access."
    },
    {
        "keywords": ["certificate of study", "enrolment certificate", "study certificate", "справка об обучении"],
        "answer": "You can order an enrollment certificate online via your Student Personal Account (ELK) or at your Study Office."
    },
    {
        "keywords": ["rating", "ranking", "рейтинг студента", "рейтинг"],
        "answer": "The student rating ranks academic performance; it is calculated twice a year (current and cumulative)."
    },
    {
        "keywords": ["cumulative rating", "кумулятивный рейтинг"],
        "answer": "The current rating covers one semester, while the cumulative rating takes into account all grades across the entire study period."
    },
    {
        "keywords": ["discount", "tuition discount", "lose discount", "лишение скидки", "скидка"],
        "answer": "Receiving an academic debt or a grade below 4 leads to the reduction or cancellation of tuition discounts."
    },
    {
        "keywords": ["plagiarism", "cheating", "плагиат", "списывание"],
        "answer": "Plagiarism leads to disciplinary sanctions ranging from failing the assignment (0 points) to expulsion."
    },
    {
        "keywords": ["appeal", "file appeal", "апелляция", "подать апелляцию"],
        "answer": "An appeal against procedural irregularities can be submitted within three business days after grade announcement."
    },
    {
        "keywords": ["appeal rejected", "отказ в апелляции"],
        "answer": "Appeals disputing grading criteria or task content rather than procedure violations are rejected without committee review."
    },
    {
        "keywords": ["visa extension", "prolong visa", "extend visa", "продление визы"],
        "answer": "Submit a visa extension request to the Visa and Registration Department at least 45 calendar days before your current visa expires."
    },
    {
        "keywords": ["migration card", "registration days", "миграционный учет"],
        "answer": "Foreign students must complete migration registration within 7 business days from the date of arrival."
    },
    {
        "keywords": ["vhi", "dms", "insurance", "страховка", "дмс"],
        "answer": "Yes. Voluntary health insurance (VHI/DMS) is mandatory for all foreign students throughout their study period in Russia."
    },
    {
        "keywords": ["fingerprinting", "274-fz", "medical check", "дактилоскопия", "медосвидетельствование"],
        "answer": "Under Federal Law 274-FZ, you must undergo state fingerprinting, photo registration, and medical checks within 90 days."
    },
    {
        "keywords": ["smartlms", "смарт лмс", "lms"],
        "answer": "SmartLMS is the university learning platform. Sign in using your corporate HSE email credentials."
    },
    {
        "keywords": ["academic leave", "gap year", "leave of absence", "академ", "академический отпуск"],
        "answer": "An academic leave of absence can be granted for medical, family, or exceptional reasons for up to two years."
    },
    {
        "keywords": ["not return leave", "fail return", "невыход из отпуска"],
        "answer": "Failure to resume studies by the deadline without valid grounds results in disciplinary expulsion."
    },
    {
        "keywords": ["dormitory", "check into dorm", "dorm", "заселение", "общежитие"],
        "answer": "Present your passport, migration card, accommodation voucher from ELK, and medical clearance certificates."
    },
    {
        "keywords": ["iup", "individual study plan", "иуп"],
        "answer": "Students who did not resolve debts during retakes may be offered to repeat courses via an Individual Study Plan (IUP)."
    },
    {
        "keywords": ["change address", "new address", "переезд", "смена адреса"],
        "answer": "Notify the Visa and Registration Department within 3 business days to update your migration records."
    },
    {
        "keywords": ["email domain", "student email", "корпоративная почта"],
        "answer": "All HSE students receive an official corporate email ending in @edu.hse.ru."
    },
    {
        "keywords": ["transfer credit", "credit transfer", "перезачет"],
        "answer": "Submit an application and official course transcripts to the Academic Supervisor of your degree program."
    },
    {
        "keywords": ["academic supervisor", "supervisor", "руководитель программы"],
        "answer": "The Academic Supervisor oversees the curriculum, resolves questions about individual study plans, and approves credit transfers."
    },
    {
        "keywords": ["appeal expulsion", "expulsion appeal", "обжаловать отчисление"],
        "answer": "A formal appeal against expulsion must be submitted to the University Appeals Committee within 10 calendar days."
    },
    {
        "keywords": ["buddy", "buddy program", "бадди"],
        "answer": "The HSE Buddy Program connects foreign students with local volunteers who assist with navigation and campus adaptation."
    },
    {
        "keywords": ["social card", "transport card", "student card", "социальная карта", "проездной"],
        "answer": "Verify your presence in the Moscow Student Register, then apply online via mos.ru for your student transport card."
    },
    {
        "keywords": ["exam sunday", "exam holiday", "holiday exam", "экзамен в праздник"],
        "answer": "No. Holding exams or interim assessments on Sundays and official state holidays is prohibited by HSE regulations."
    },
    {
        "keywords": ["application templates", "document templates", "templates", "шаблоны заявлений"],
        "answer": "Application templates are available in the LMS Student Archive and on the official website page of your study program."
    },
    {
        "keywords": ["unexcused absence", "absence 0", "miss exam zero", "неявка 0"],
        "answer": "Unexcused absence results in an automatic grade of 0 and an academic debt."
    }
]

def find_answer(query: str) -> str:
    raw_query = (query or "").lower().strip()
    cleaned = re.sub(r"[^\w\s]", " ", raw_query)
    words = set(cleaned.split())

    if not words or any(g in words for g in GREETINGS):
        return "Hello! I am your HSE International Assistant. Ask me anything about grading, visas, dorms, or exams!"

    # Проверка на Small Talk
    for talk in SMALL_TALK:
        for trig in talk["triggers"]:
            if trig in raw_query or trig in cleaned:
                return talk["answer"]

    # 1. Поиск по полному совпадению ключевой фразы
    for item in KB:
        for kw in item["keywords"]:
            if kw.lower() in cleaned:
                return item["answer"]

    # 2. Нестрогий поиск по пересечению слов
    best_match = None
    max_matches = 0

    for item in KB:
        for kw in item["keywords"]:
            kw_words = set(kw.lower().split())
            matches = len(words.intersection(kw_words))
            if matches > max_matches:
                max_matches = matches
                best_match = item["answer"]

    if max_matches > 0 and best_match:
        return best_match

    return "I am focused on HSE regulations. Try asking about grading, exams, dorms, or student visas!"

@app.post("/webhook")
async def alice_endpoint(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}

    session = data.get("session", {})
    req = data.get("request", {})

    is_new = session.get("new", False)
    user_text = req.get("command", "") or req.get("original_utterance", "")

    if is_new or not user_text.strip():
        response_text = "Hello! I am your HSE International Assistant. Ask me anything about grading, visas, dorms, or exams!"
    else:
        response_text = find_answer(user_text)

    return JSONResponse(content={
        "response": {
            "text": response_text,
            "end_session": False
        },
        "version": data.get("version", "1.0")
    })

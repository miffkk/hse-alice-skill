from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

KB = [
    {
        "keywords": ["placement test", "entry test", "placement", "входное", "входной", "тестирование"],
        "answer": "Yes. The entry placement test is mandatory for students who do not have an international language certificate."
    },
    {
        "keywords": ["placement online", "test online", "entry online", "дистанционно", "онлайн тест"],
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
        "keywords": ["mid-term english", "intermediate test", "промежуточное тестирование"],
        "answer": "Yes. Intermediate testing is conducted for all first-year students."
    },
    {
        "keywords": ["intermediate ranking", "промежуточный рейтинг"],
        "answer": "No. Intermediate test results are not included in the student ranking."
    },
    {
        "keywords": ["change english level", "switch level", "сменить уровень"],
        "answer": "Yes. Intermediate testing can serve as a transition point to another level or course direction."
    },
    {
        "keywords": ["internal english exam mandatory", "first year exam mandatory", "обязателен экзамен английский"],
        "answer": "Yes, the internal English exam is mandatory for all first-year students."
    },
    {
        "keywords": ["waive internal exam", "certificate waive", "перезачесть экзамен"],
        "answer": "Yes. The internal exam can be credited and waived if you have an eligible international certificate."
    },
    {
        "keywords": ["internal exam rating", "internal exam grade", "оценка экзамен рейтинг"],
        "answer": "Yes. The grade for the internal English exam is included in your current rating."
    },
    {
        "keywords": ["grading scale", "scale", "10-point", "шкала оценивания", "баллы"],
        "answer": "HSE uses a 10-point grading scale. Grades 1 to 3 are fail (unsatisfactory), and 4 to 10 are pass."
    },
    {
        "keywords": ["minimum passing grade", "passing grade", "проходной балл", "минимум сдать"],
        "answer": "The minimum passing grade is 4 out of 10 points."
    },
    {
        "keywords": ["how many modules", "modules", "модули", "сколько модулей"],
        "answer": "The HSE academic year is divided into 4 study modules."
    },
    {
        "keywords": ["rounding", "round down", "округление"],
        "answer": "Rounding follows standard arithmetic rules. Rounding down against the student is not permitted."
    },
    {
        "keywords": ["missed exam", "sick", "illness", "болезнь", "справка", "заболел"],
        "answer": "Notify the study office on the exam day and submit an official medical certificate within three business days after recovery."
    },
    {
        "keywords": ["academic debt", "academic failure", "задолженность", "хвост"],
        "answer": "An academic failure is receiving a final grade below 4 out of 10 in any course."
    },
    {
        "keywords": ["retake attempts", "how many retakes", "пересдачи", "сколько пересдач"],
        "answer": "You get two retake attempts: the first with the course instructor, and the second before an academic commission."
    },
    {
        "keywords": ["retake period", "when retakes", "период пересдач", "когда пересдачи"],
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
        "keywords": ["grade missing", "smartlms grade", "нет оценки"],
        "answer": "Immediately contact your Study Office manager via corporate email."
    },
    {
        "keywords": ["schedule", "timetable", "ruz", "расписание", "руз"],
        "answer": "Your schedule is published in the RUZ electronic timetable system (ruz.hse.ru) and the HSE App X."
    },
    {
        "keywords": ["formula", "final grade calculate", "расчет оценки", "формула оценки"],
        "answer": "The final grade is calculated from continuous assessment elements and the exam according to the Course Syllabus formula."
    },
    {
        "keywords": ["attendance exam", "refuse exam", "недопуск", "посещаемость"],
        "answer": "No. HSE regulations state that poor attendance alone cannot serve as a ground for denying exam access."
    },
    {
        "keywords": ["certificate of study", "enrolment certificate", "справка об обучении"],
        "answer": "You can order an enrollment certificate online via your Student Personal Account (ELK) or at your Study Office."
    },
    {
        "keywords": ["rating", "ranking", "рейтинг студента"],
        "answer": "The student rating ranks academic performance; it is calculated twice a year (current and cumulative)."
    },
    {
        "keywords": ["cumulative rating", "кумулятивный рейтинг"],
        "answer": "The current rating covers one semester, while the cumulative rating takes into account all grades across the entire study period."
    },
    {
        "keywords": ["discount", "tuition discount", "лишение скидки", "скидка"],
        "answer": "Receiving an academic debt or a grade below 4 leads to the reduction or cancellation of tuition discounts."
    },
    {
        "keywords": ["plagiarism", "cheating", "плагиат", "списывание"],
        "answer": "Plagiarism leads to disciplinary sanctions ranging from failing the assignment (0 points) to expulsion."
    },
    {
        "keywords": ["appeal", "апелляция", "подать апелляцию"],
        "answer": "An appeal against procedural irregularities can be submitted within three business days after grade announcement."
    },
    {
        "keywords": ["appeal rejected", "отказ в апелляции"],
        "answer": "Appeals disputing grading criteria or task content rather than procedure violations are rejected without committee review."
    },
    {
        "keywords": ["visa extension", "prolong visa", "продление визы"],
        "answer": "Submit a visa extension request to the Visa and Registration Department at least 45 calendar days before your current visa expires."
    },
    {
        "keywords": ["migration card", "registration days", "миграционный учет"],
        "answer": "Foreign students must complete migration registration within 7 business days from the date of arrival."
    },
    {
        "keywords": ["vhi", "dms", "страховка", "дмс"],
        "answer": "Yes. Voluntary health insurance (VHI/DMS) is mandatory for all foreign students throughout their study period in Russia."
    },
    {
        "keywords": ["fingerprinting", "274-fz", "дактилоскопия", "медосвидетельствование"],
        "answer": "Under Federal Law 274-FZ, you must undergo state fingerprinting, photo registration, and medical checks within 90 days."
    },
    {
        "keywords": ["smartlms", "смарт лмс", "lms"],
        "answer": "SmartLMS is the university learning platform. Sign in using your corporate HSE email credentials."
    },
    {
        "keywords": ["academic leave", "gap", "академ", "академический отпуск"],
        "answer": "An academic leave of absence can be granted for medical, family, or exceptional reasons for up to two years."
    },
    {
        "keywords": ["not return leave", "невыход из отпуска"],
        "answer": "Failure to resume studies by the deadline without valid grounds results in disciplinary expulsion."
    },
    {
        "keywords": ["dormitory", "check into dorm", "заселение", "общежитие"],
        "answer": "Present your passport, migration card, accommodation voucher from ELK, and medical clearance certificates."
    },
    {
        "keywords": ["iup", "individual study plan", "иуп"],
        "answer": "Students who did not resolve debts during retakes may be offered to repeat courses via an Individual Study Plan (IUP)."
    },
    {
        "keywords": ["change address", "переезд", "смена адреса"],
        "answer": "Notify the Visa and Registration Department within 3 business days to update your migration records."
    },
    {
        "keywords": ["email domain", "корпоративная почта"],
        "answer": "All HSE students receive an official corporate email ending in @edu.hse.ru."
    },
    {
        "keywords": ["transfer credit", "перезачет"],
        "answer": "Submit an application and official course transcripts to the Academic Supervisor of your degree program."
    },
    {
        "keywords": ["academic supervisor", "руководитель программы"],
        "answer": "The Academic Supervisor oversees the curriculum, resolves questions about individual study plans, and approves credit transfers."
    },
    {
        "keywords": ["appeal expulsion", "обжаловать отчисление"],
        "answer": "A formal appeal against expulsion must be submitted to the University Appeals Committee within 10 calendar days."
    },
    {
        "keywords": ["buddy", "бадди"],
        "answer": "The HSE Buddy Program connects foreign students with local volunteers who assist with navigation and campus adaptation."
    },
    {
        "keywords": ["social card", "transport card", "социальная карта", "проездной"],
        "answer": "Verify your presence in the Moscow Student Register, then apply online via mos.ru for your student transport card."
    },
    {
        "keywords": ["exam sunday", "exam holiday", "экзамен в праздник"],
        "answer": "No. Holding exams or interim assessments on Sundays and official state holidays is prohibited by HSE regulations."
    },
    {
        "keywords": ["application templates", "шаблоны заявлений"],
        "answer": "Application templates are available in the LMS Student Archive and on the official website page of your study program."
    },
    {
        "keywords": ["unexcused absence", "неявка 0"],
        "answer": "Unexcused absence results in an automatic grade of 0 and an academic debt."
    }
]

def find_answer(query: str) -> str:
    q = (query or "").lower().strip()
    for item in KB:
        for kw in item["keywords"]:
            if kw.lower() in q:
                return item["answer"]
    return "I couldn't find an exact match in the HSE regulations. Try asking about grading, exams, dorms, or visas."

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

    if is_new or not user_text:
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

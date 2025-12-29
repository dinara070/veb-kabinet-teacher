import json
from datetime import datetime

class TeacherCabinet:
    def __init__(self, teacher_name):
        # Особиста інформація викладача
        self.teacher_info = {
            "ПІБ": teacher_name,
            "Посада": "Доцент",
            "Ступінь": "Кандидат наук"
        }
        self.schedule = []  # Особистий розклад
        self.journals = {}   # Журнали поточної успішності
        self.exam_reports = [] # Екзаменаційні відомості

    # --- Робота з розкладом ---
    def add_lesson(self, time, subject, auditorium, group):
        lesson = {
            "Час": time,
            "Дисципліна": subject,
            "Аудиторія": auditorium,
            "Група": group
        }
        self.schedule.append(lesson)
        print(f"Заняття додано до розкладу: {subject} для групи {group}")

    # --- Журнал поточної успішності ---
    def create_journal(self, subject, group, students_list):
        self.journals[f"{subject}_{group}"] = {
            "students": {name: {"grades": [], "attendance": True} for name in students_list},
            "published": False
        }
        print(f"Створено журнал для дисципліни {subject} (Група: {group})")

    # --- Проставлення оцінок та автоматизація ---
    def set_grade(self, journal_key, student_name, grade_ects):
        if journal_key in self.journals and student_name in self.journals[journal_key]["students"]:
            # Автоматичне заповнення ідентичних полів/шкал
            national_grade = self._convert_to_national(grade_ects)
            
            grade_entry = {
                "ECTS": grade_ects,
                "National": national_grade,
                "Date": datetime.now().strftime("%Y-%m-%d")
            }
            self.journals[journal_key]["students"][student_name]["grades"].append(grade_entry)
            print(f"Оцінка {grade_ects} ({national_grade}) виставлена студенту {student_name}")

    def _convert_to_national(self, ects):
        # Логіка автоматичного проставлення національної оцінки
        mapping = {"A": "Відмінно", "B": "Добре", "C": "Добре", "D": "Задовільно", "E": "Задовільно"}
        return mapping.get(ects, "Незадовільно")

    # --- Екзаменаційні відомості ---
    def create_exam_report(self, report_id, subject, group, session_type):
        report = {
            "Номер відомості": report_id,
            "Дисципліна": subject,
            "Навчальна група": group,
            "Тип випробування": session_type, # Наприклад, "Іспит"
            "Editable": True
        }
        self.exam_reports.append(report)
        print(f"Створено екзаменаційну відомість №{report_id}")

    # --- Експорт в Excel (імітація) ---
    def export_to_excel(self, journal_key):
        if journal_key in self.journals:
            filename = f"journal_{journal_key}.json" # У прикладі експортуємо в JSON для демонстрації
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.journals[journal_key], f, ensure_ascii=False, indent=4)
            print(f"Журнал успішно вивантажено у файл {filename}")

# --- Демонстрація роботи системи ---

# 1. Авторизація викладача
cabinet = TeacherCabinet("Іванов Іван Іванович")

# 2. Формування розкладу
cabinet.add_lesson("08:30", "Вища математика", "Ауд. 302", "КН-21")

# 3. Робота з журналами
students = ["Петренко А.", "Сидоренко О.", "Ковальчук Д."]
cabinet.create_journal("Вища математика", "КН-21", students)

# 4. Проставлення оцінок (автоматичний розрахунок шкали)
cabinet.set_grade("Вища математика_КН-21", "Петренко А.", "A")
cabinet.set_grade("Вища математика_КН-21", "Сидоренко О.", "C")

# 5. Екзаменаційна сесія
cabinet.create_exam_report("В-405", "Вища математика", "КН-21", "Іспит")

# 6. Експорт даних для методиста
cabinet.export_to_excel("Вища математика_КН-21")

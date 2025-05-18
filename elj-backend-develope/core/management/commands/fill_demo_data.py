from django.core.management.base import BaseCommand
from core.models import (
    School, StudyYear, StudentClass, Subject, TeacherSubject, User,
    Student, Lesson, Day, Event
)
from django.db import transaction
from datetime import date, datetime

class Command(BaseCommand):
    help = "Полностью очищает базу и заполняет демонстрационными данными"

    def clear_data(self):
        # Очистка данных с правильным порядком!
        with transaction.atomic():
            try:
                from core.models import Mark
                Mark.objects.all().delete()
            except ImportError:
                pass
            Event.objects.all().delete()
            Day.objects.all().delete()
            Lesson.objects.all().delete()
            Student.objects.all().delete()
            StudentClass.objects.all().delete()
            StudyYear.objects.all().delete()
            Subject.objects.all().delete()
            TeacherSubject.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()
            School.objects.all().delete()

    def handle(self, *args, **options):
        self.stdout.write("Очищаем старые данные...")
        self.clear_data()

        # 1. Школа
        school, _ = School.objects.get_or_create(
            name="Школа №1",
            address="ул. Школьная, д.1",
            phone="+7 123 456-78-90"
        )

        # 2. Учебный год
        study_year, _ = StudyYear.objects.get_or_create(year=2024)

        # 3. Классы (1-11, A-D)
        all_classes = []
        for grade in range(1, 12):
            for letter in ['А', 'Б', 'В', 'Г', 'Д']:
                class_obj, _ = StudentClass.objects.get_or_create(
                    name=f"{grade}{letter}", study_year=study_year
                )
                all_classes.append(class_obj)

        # 4. Предметы (10)
        subjects_data = [
            "Математика", "Русский язык", "Литература", "Английский язык", "История",
            "География", "Биология", "Физика", "Химия", "Информатика"
        ]
        subject_objs = {}
        for subj_name in subjects_data:
            subject_objs[subj_name], _ = Subject.objects.get_or_create(
                name=subj_name, study_year=study_year
            )

        # 5. TeacherSubjects (10)
        teacher_subject_objs = {}
        for subj_name in subjects_data:
            ts, _ = TeacherSubject.objects.get_or_create(name=subj_name)
            teacher_subject_objs[subj_name] = ts
            ts.student_classes.add(*all_classes)

        # 6. Учителя (10)
        teachers_data = [
            ("teach1@school.ru", "Иван", "Иванов"),
            ("teach2@school.ru", "Екатерина", "Петрова"),
            ("teach3@school.ru", "Сергей", "Алексеев"),
            ("teach4@school.ru", "Мария", "Волкова"),
            ("teach5@school.ru", "Андрей", "Морозов"),
            ("teach6@school.ru", "Наталья", "Кузьмина"),
            ("teach7@school.ru", "Олег", "Смирнов"),
            ("teach8@school.ru", "Татьяна", "Котова"),
            ("teach9@school.ru", "Павел", "Дьяков"),
            ("teach10@school.ru", "Виктория", "Захарова"),
        ]
        teacher_objs = []
        for i, (email, name, surname) in enumerate(teachers_data):
            teacher = User.objects.filter(email=email).first()
            if not teacher:
                teacher = User.objects.create_user(
                    email=email, password="123456",
                    name=name, surname=surname
                )
            teacher_objs.append(teacher)
        # Связываем учителей с предметами
        for i, teacher in enumerate(teacher_objs):
            subj_name = subjects_data[i % len(subjects_data)]
            teacher.teaching_subjects.add(teacher_subject_objs[subj_name])

        # 7. Ученики (20 на каждый класс)
        names = ["Алексей", "Мария", "Дмитрий", "Елена", "Игорь", "Анна", "Сергей", "Наталья", "Евгений", "Ольга",
                 "Максим", "Татьяна", "Михаил", "София", "Роман", "Виктория", "Артур", "Юлия", "Василий", "Алиса"]
        surnames = ["Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов", "Васильев", "Захаров", "Орлов", "Павлов", "Семенов",
                    "Ковалев", "Григорьев", "Федоров", "Беляев", "Соловьев", "Воробьев", "Богданов", "Волков", "Карпов", "Борисов"]
        for class_obj in all_classes:
            for i in range(20):
                Student.objects.get_or_create(
                    name=names[i % len(names)],
                    surname=surnames[i % len(surnames)],
                    lastname=f"{names[(i+1)%len(names)]}ович",
                    birth_date=date(2011, 9, 1),  # Можно сделать разные года для разных классов
                    address=f"ул. Ученицкая, д.{i+1}",
                    phone=f"+7 987 22{i%10}-1{i:02d}-3{i:02d}",
                    student_class=class_obj
                )

        # 8. Расписание (уроки и дни) - пример для 1 класса А, понедельник
        lesson1, _ = Lesson.objects.get_or_create(
            subject_name="Математика", number=1, cabinet="101",
            time="8:00", class_name="1А", teacher=teacher_objs[0]
        )
        lesson2, _ = Lesson.objects.get_or_create(
            subject_name="Русский язык", number=2, cabinet="102",
            time="9:00", class_name="1А", teacher=teacher_objs[1]
        )
        lesson3, _ = Lesson.objects.get_or_create(
            subject_name="Литература", number=3, cabinet="103",
            time="10:00", class_name="1А", teacher=teacher_objs[2]
        )
        day_mon, _ = Day.objects.get_or_create(day_of_week="MON", teacher=teacher_objs[0])
        day_mon.lessons.add(lesson1, lesson2, lesson3)
        # Можно продублировать для других классов и дней

        # 9. События (10 штук)
        events_data = [
            ("День знаний", "Торжественная линейка ко Дню знаний", datetime(2024, 9, 1, 9, 0), teacher_objs[0]),
            ("Олимпиада по математике", "Школьный этап олимпиады", datetime(2024, 10, 10, 10, 0), teacher_objs[1]),
            ("День учителя", "Праздничный концерт", datetime(2024, 10, 5, 12, 0), teacher_objs[2]),
            ("Экскурсия в музей", "Посещение краеведческого музея", datetime(2024, 11, 20, 11, 0), teacher_objs[3]),
            ("Новогодний утренник", "Празднование Нового года", datetime(2024, 12, 28, 10, 0), teacher_objs[4]),
            ("День здоровья", "Спортивные соревнования", datetime(2025, 2, 10, 9, 0), teacher_objs[5]),
            ("Неделя науки", "Выставка научных проектов", datetime(2025, 3, 15, 13, 0), teacher_objs[6]),
            ("День космонавтики", "Классный час", datetime(2025, 4, 12, 12, 0), teacher_objs[7]),
            ("Последний звонок", "Праздник для выпускников", datetime(2025, 5, 25, 10, 0), teacher_objs[8]),
            ("Выпускной", "Торжественный бал", datetime(2025, 6, 30, 18, 0), teacher_objs[9]),
        ]
        for title, desc, date_ev, teacher in events_data:
            Event.objects.get_or_create(
                title=title,
                description=desc,
                date=date_ev,
                teacher=teacher
            )

        self.stdout.write(self.style.SUCCESS("Демо-данные успешно добавлены!"))

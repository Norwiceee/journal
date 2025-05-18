from django.core.management.base import BaseCommand
from core.models import (
    School, StudyYear, StudentClass, Subject, TeacherSubject, User,
    Student, Lesson, Day, Event
)
from datetime import date, datetime, timedelta


class Command(BaseCommand):
    help = "Заполняет базу демонстрационными данными"

    def handle(self, *args, **options):
        # 1. Школа
        school, _ = School.objects.get_or_create(
            name="Школа №1",
            address="ул. Школьная, д.1",
            phone="+7 123 456-78-90"
        )

        # 2. Учебный год
        study_year, _ = StudyYear.objects.get_or_create(year=2024)

        # 3. Классы
        class7a, _ = StudentClass.objects.get_or_create(
            name="7А", study_year=study_year
        )
        class7b, _ = StudentClass.objects.get_or_create(
            name="7Б", study_year=study_year
        )

        # 4. Предметы
        math, _ = Subject.objects.get_or_create(
            name="Математика", study_year=study_year
        )
        rus, _ = Subject.objects.get_or_create(
            name="Русский язык", study_year=study_year
        )
        eng, _ = Subject.objects.get_or_create(
            name="Английский язык", study_year=study_year
        )

        # 5. TeacherSubjects (для связи учителей и классов)
        math_teacher_subject, _ = TeacherSubject.objects.get_or_create(name="Математика")
        rus_teacher_subject, _ = TeacherSubject.objects.get_or_create(name="Русский язык")
        eng_teacher_subject, _ = TeacherSubject.objects.get_or_create(name="Английский язык")

        math_teacher_subject.student_classes.add(class7a, class7b)
        rus_teacher_subject.student_classes.add(class7a, class7b)
        eng_teacher_subject.student_classes.add(class7a, class7b)

        # 6. Учителя
        teacher1 = User.objects.filter(email="teach1@school.ru").first()
        if not teacher1:
            teacher1 = User.objects.create_user(
                email="teach1@school.ru", password="123456",
                name="Иван", surname="Иванов"
            )
        teacher2 = User.objects.filter(email="teach2@school.ru").first()
        if not teacher2:
            teacher2 = User.objects.create_user(
                email="teach2@school.ru", password="123456",
                name="Екатерина", surname="Петрова"
            )
        teacher3 = User.objects.filter(email="teach3@school.ru").first()
        if not teacher3:
            teacher3 = User.objects.create_user(
                email="teach3@school.ru", password="123456",
                name="Сергей", surname="Алексеев"
            )
        teacher1.teaching_subjects.add(math_teacher_subject)
        teacher2.teaching_subjects.add(rus_teacher_subject)
        teacher3.teaching_subjects.add(eng_teacher_subject)

        # 7. Ученики
        student1, _ = Student.objects.get_or_create(
            name="Павел", surname="Сидоров", lastname="Игоревич",
            birth_date=date(2011, 9, 10), address="ул. Молодёжная, д.10",
            phone="+7 987 222-11-33", student_class=class7a
        )
        student2, _ = Student.objects.get_or_create(
            name="Оля", surname="Кузнецова", lastname="Артёмовна",
            birth_date=date(2011, 7, 21), address="ул. Центральная, д.5",
            phone="+7 987 222-11-34", student_class=class7a
        )
        student3, _ = Student.objects.get_or_create(
            name="Василий", surname="Панов", lastname="Андреевич",
            birth_date=date(2011, 6, 4), address="ул. Советская, д.3",
            phone="+7 987 222-11-35", student_class=class7b
        )

        # 8. Расписание (уроки и дни)
        lesson1, _ = Lesson.objects.get_or_create(
            subject_name="Математика", number=1, cabinet="101",
            time="8:00", class_name="7А", teacher=teacher1
        )
        lesson2, _ = Lesson.objects.get_or_create(
            subject_name="Русский язык", number=2, cabinet="102",
            time="9:00", class_name="7А", teacher=teacher2
        )
        lesson3, _ = Lesson.objects.get_or_create(
            subject_name="Английский язык", number=3, cabinet="103",
            time="10:00", class_name="7А", teacher=teacher3
        )
        day_mon, _ = Day.objects.get_or_create(day_of_week="MON", teacher=teacher1)
        day_mon.lessons.add(lesson1, lesson2, lesson3)

        # 9. События
        event1, _ = Event.objects.get_or_create(
            title="День знаний",
            description="Торжественная линейка ко Дню знаний",
            date=datetime(2024, 9, 1, 9, 0),
            teacher=teacher1
        )
        event2, _ = Event.objects.get_or_create(
            title="Олимпиада по математике",
            description="Школьный этап олимпиады",
            date=datetime(2024, 10, 10, 10, 0),
            teacher=teacher1
        )

        self.stdout.write(self.style.SUCCESS("Демо-данные успешно добавлены!"))

import { notification } from "antd";

export const routeTranslator = routeName => {
  if (routeName === "journal") return "Журнал";
  if (routeName === "timetable") return "Расписание";
  if (routeName === "events") return "События";
  if (routeName === "account") return "Аккаунт";
  else return null;
};

export const pathDecoder = pathName => {
  let componentKey = null;
  if (pathName.includes("journal")) componentKey = "1";
  else if (pathName.includes("timetable")) componentKey = "2";
  else if (pathName.includes("events")) componentKey = "3";
  return componentKey;
};

export const dateTimeConverter = str => {
  const dateAndTime = str.split(" ");
  let convertedTime = str;
  if (dateAndTime.length === 2) {
    let datePart = dateAndTime[0].split("-");
    let timePart = dateAndTime[1];
    convertedTime = `${datePart[2]}-${datePart[1]}-${datePart[0]}T${timePart}:00Z`;
  }
  return convertedTime;
};

export const prettifyDjangoDateTime = str => {
  const dateAndTime = str.split("T");
  const date = dateAndTime[0].split("-");
  const time = dateAndTime[1].slice(0, dateAndTime[1].length - 4);
  return `${date[2]}.${date[1]}.${date[0]} ${time}`;
};

export const prettifyInitialDjangoDateTime = str => {
  return str.replace("-", ".");
};

export const openNotification = (msg, desc) => {
  notification.open({
    message: msg,
    description: desc
  });
};

export const dayOfWeekTranslator = str => {
  const tr_days = {
    MON: "Понедельник",
    TUE: "Вторник",
    WED: "Среда",
    THU: "Четверг",
    FRI: "Пятница",
    SAT: "Суббота"
  };
  return tr_days[str];
};

const studentFilterer = data => {
  const students = [];
  data.forEach(mark => {
    if (!students.find(student => student.id === mark.student.id)) {
      students.push(mark.student);
    }
  });
  return students;
};

const markFilterer = (students, marks) => {
  students.forEach(student => {
    if (!student["marks"]) student["marks"] = [];
    marks.forEach(mark => {
      if (mark.student.id === student.id) {
        student["marks"].push(mark);
      }
    });
    if (marks[0] && marks[0].subject) {
      student.subject_id = marks[0].subject.id;
    }
  });
  return students;
};

export const journalDataRearranger = data => {
  const students = studentFilterer(data);
  return markFilterer(students, data);
};

export const getWeekAsDateObjectsList = () => {
  let curr = new Date();
  let week = [];

  for (let i = 1; i <= 6; i++) {
    let first = curr.getDate() - curr.getDay() + i;
    let day_str = new Date(curr.setDate(first)).toISOString().slice(0, 10);
    week.push({
      [day_str]: {}
    });
  }
  return week;
};

export const getWeekAsDateStringsList = () => {
  let curr = new Date();
  let week = [];

  for (let i = 1; i <= 6; i++) {
    let first = curr.getDate() - curr.getDay() + i;
    let day_str = new Date(curr.setDate(first)).toISOString().slice(0, 10);
    week.push(day_str);
  }
  return week;
};

export const makeWeekJournalColumnsFromDateStringList = weekList => {
  let columns = [
    { title: "№", dataIndex: "id" },
    {
      title: "Фамилия",
      dataIndex: "surname",
      initialEditValue: "initial edit value"
    },
    { title: "Имя", dataIndex: "name" }
  ];
  weekList.forEach(date => {
    columns.push({
      title: date,
      dataIndex: `${date}.cellContent`
    });
  });
  return columns;
};

export const addMarkOptionsToEachStudent = (studentList, markOptions) => {
  studentList.forEach(student => {
    student.marks.forEach(mark => {
      mark["options"] = markOptions;
    });
  });
  return studentList;
};

export const addAbsentDatesToMarksOfStudentsList = (studentList, weekList) => {
  studentList.forEach(student => {
    let dates = [...weekList];
    student.marks.forEach(mark => {
      if (dates.includes(mark.date)) {
        dates.splice(dates.indexOf(mark.date), 1);
      }
    });
    dates.forEach(date => {
      student.marks.push({
        value: "PRE",
        date: date
      });
    });
  });
  return studentList;
};

export const markOptions = {
  PRE: "PRE",
  ABS: "ABS",
  FIV: "FIV",
  FOU: "FOU",
  THR: "THR",
  TWO: "TWO"
};

export const pullMarksToProperty = students => {
  students.forEach(student => {
    student.marks.forEach(mark => {
      student[mark.date] = mark;
    });
    delete student.marks;
  });
  return students;
};

export const addAbsentDatesToMarksOfStudentObjects = (
  studentList,
  weekList
) => {
  studentList.forEach(student => {
    let dates = [...weekList];
    dates.forEach(date => {
      if (typeof student[date] === "undefined") {
        student[date] = {
          value: "PRE",
          date: date,
          student_id: student.id,
          subject_id: student.subject_id
        };
      }
    });
  });
  return studentList;
};

export const pullStudentClassesFromHeader = (header, subjectName) => {
  let studentClasses = [];
  header.forEach(subject => {
    if (subject.name === subjectName) studentClasses = subject.student_classes;
  });
  return studentClasses;
};

export const compareSurnames = (a, b) => {
  if (a.surname > b.name) return 1;
  else if (a.surname < b.name) return -1;
  else return 0;
};

export const compareLessonNumbers = (a, b) => {
  if (a.number > b.number) return 1;
  else if (a.number < b.number) return -1;
  else return 0;
};

export const sortTimeTable = (timetable, sorterFunc) => {
  timetable.forEach(day => {
    day.lessons.sort(sorterFunc);
  });
  return timetable;
};

export const notificationConstants = {
  UNKNOWN_ERROR: [
    "Возникла ошибка!",
    "Обновите страницу и попробуйте заново. Если это не поможет, обратитесь к администратору."
  ],
  EVENT_FIELDS_REQUIRED: [
    "Не все поля заполнены!",
    "Пожалуйста заполните все поля и выберите дату со временем события."
  ],
  FORGOT_PASSWORD: [
    "Забыли пароль.",
    "Для восстановления пароля обратитесь к администратору."
  ]
};

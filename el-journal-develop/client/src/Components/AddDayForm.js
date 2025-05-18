// src/components/AddDayForm.js

import React, { useState } from "react";
import axios from "axios";

const AddDayForm = ({ lessons, teachers, onSuccess }) => {
    const [form, setForm] = useState({
        day_of_week: "",
        lessons: [],
        teacher: ""
    });
    const [error, setError] = useState("");

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleLessonsChange = (e) => {
        const options = e.target.options;
        const values = [];
        for (let i = 0, l = options.length; i < l; i++) {
            if (options[i].selected) {
                values.push(options[i].value);
            }
        }
        setForm({ ...form, lessons: values });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            await axios.post("/api/days/", {
                ...form,
                lessons: form.lessons.map(Number) // обязательно int id
            }, {
                headers: { Authorization: `Token ${localStorage.getItem("token")}` }
            });
            setForm({ day_of_week: "", lessons: [], teacher: "" });
            if (onSuccess) onSuccess();
            alert("День добавлен!");
        } catch (err) {
            setError("Ошибка при добавлении дня");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <select name="day_of_week" value={form.day_of_week} onChange={handleChange} required>
                <option value="">День недели</option>
                <option value="MON">Понедельник</option>
                <option value="TUE">Вторник</option>
                <option value="WED">Среда</option>
                <option value="THU">Четверг</option>
                <option value="FRI">Пятница</option>
                <option value="SAT">Суббота</option>
            </select>
            <select multiple name="lessons" value={form.lessons} onChange={handleLessonsChange} required>
                {lessons.map(lesson => (
                    <option key={lesson.id} value={lesson.id}>
                        {lesson.subject_name} ({lesson.class_name}, {lesson.time})
                    </option>
                ))}
            </select>
            <select name="teacher" value={form.teacher} onChange={handleChange} required>
                <option value="">Учитель</option>
                {teachers.map(t => (
                    <option key={t.id} value={t.id}>{t.surname} {t.name}</option>
                ))}
            </select>
            <button type="submit">Добавить день</button>
            {error && <div style={{ color: "red" }}>{error}</div>}
        </form>
    );
};

export default AddDayForm;

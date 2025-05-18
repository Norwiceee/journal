// src/components/AddLessonForm.js

import React, { useState } from "react";
import axios from "axios";

const AddLessonForm = ({ teachers, onSuccess }) => {
    const [form, setForm] = useState({
        subject_name: "",
        number: "",
        cabinet: "",
        time: "",
        class_name: "",
        teacher: ""
    });
    const [error, setError] = useState("");

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            await axios.post("/api/lessons/", form, {
                headers: { Authorization: `Token ${localStorage.getItem("token")}` }
            });
            setForm({ subject_name: "", number: "", cabinet: "", time: "", class_name: "", teacher: "" });
            if (onSuccess) onSuccess();
            alert("Урок добавлен!");
        } catch (err) {
            setError("Ошибка при добавлении урока");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input name="subject_name" placeholder="Название предмета" value={form.subject_name} onChange={handleChange} required />
            <input type="number" name="number" placeholder="Номер урока" value={form.number} onChange={handleChange} required />
            <input name="cabinet" placeholder="Кабинет" value={form.cabinet} onChange={handleChange} />
            <input name="time" placeholder="Время" value={form.time} onChange={handleChange} />
            <input name="class_name" placeholder="Класс (напр. 9А)" value={form.class_name} onChange={handleChange} />
            <select name="teacher" value={form.teacher} onChange={handleChange} required>
                <option value="">Выберите учителя</option>
                {teachers.map(t => (
                    <option key={t.id} value={t.id}>{t.surname} {t.name}</option>
                ))}
            </select>
            <button type="submit">Добавить урок</button>
            {error && <div style={{ color: "red" }}>{error}</div>}
        </form>
    );
};

export default AddLessonForm;

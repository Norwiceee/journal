// src/components/AddStudentForm.js

import React, { useState } from "react";
import axios from "axios";

const AddStudentForm = ({ studentClasses, onSuccess }) => {
    const [form, setForm] = useState({
        name: "",
        surname: "",
        lastname: "",
        birth_date: "",
        address: "",
        phone: "",
        student_class: "",
    });

    const [error, setError] = useState("");

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            await axios.post("/api/students/", form, {
                headers: { Authorization: `Token ${localStorage.getItem("token")}` }
            });
            setForm({ name: "", surname: "", lastname: "", birth_date: "", address: "", phone: "", student_class: "" });
            if (onSuccess) onSuccess();
            alert("Студент добавлен!");
        } catch (err) {
            setError("Ошибка при добавлении студента");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input name="surname" placeholder="Фамилия" value={form.surname} onChange={handleChange} required />
            <input name="name" placeholder="Имя" value={form.name} onChange={handleChange} required />
            <input name="lastname" placeholder="Отчество" value={form.lastname} onChange={handleChange} />
            <input type="date" name="birth_date" placeholder="Дата рождения" value={form.birth_date} onChange={handleChange} required />
            <input name="address" placeholder="Адрес" value={form.address} onChange={handleChange} />
            <input name="phone" placeholder="Телефон" value={form.phone} onChange={handleChange} />
            <select name="student_class" value={form.student_class} onChange={handleChange} required>
                <option value="">Выберите класс</option>
                {studentClasses.map(sc => (
                    <option key={sc.id} value={sc.id}>{sc.name}</option>
                ))}
            </select>
            <button type="submit">Добавить студента</button>
            {error && <div style={{ color: "red" }}>{error}</div>}
        </form>
    );
};

export default AddStudentForm;

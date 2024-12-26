import React, { useState } from "react";
import "./App.css"; // Стили (опционально)

const AddQuestionForm = () => {
  const [question, setQuestion] = useState(""); // Поле для вопроса
  const [answers, setAnswers] = useState(["", "", "", ""]); // Массив с вариантами ответа
  const [correctAnswer, setCorrectAnswer] = useState(""); // Верный ответ

  // Обновляем значение вопроса
  const handleQuestionChange = (e) => {
    setQuestion(e.target.value);
  };

  // Обновляем ответ по индексу
  const handleAnswerChange = (index, value) => {
    const updatedAnswers = [...answers];
    updatedAnswers[index] = value;
    setAnswers(updatedAnswers);
  };

  // Добавляем новый ответ
  const addAnswer = () => {
    if (answers.length == 5) {
      alert("У вопроса не может быть больше 5 ответов((")
      return
    }
    setAnswers([...answers, ""]);
  };

  // Удаляем ответ по индексу
  const removeAnswer = (index) => {
    const updatedAnswers = answers.filter((_, i) => i !== index);
    setAnswers(updatedAnswers);
  };

  // Обработка отправки формы
  const handleSubmit = async (e) => {
    const token = getAuthToken();
    if (!token) {
      alert("Какие-то проблемы и мы не можем понять, кто ты. Можешь перейти по ссылке в боте еще раз?");
      return;
    }
    console.log("Отправляем запрос с токеном: ", token)

    e.preventDefault();

    if (answers.length > 5 || answers.length < 2) {
      console.log("Некорректное число ответов: ", answers.length);
      alert("Количество ответов должно быть от 2 до 5")
      return
    }
    
    const payload = {
      question,
      answers,
      correctAnswer,
    };

    console.log("Отправляем данные:", payload);
    var uri = "api/question/suggest";
    console.log("uri: ", uri);

    try {
      const response = await fetch(uri, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        alert("Вопрос успешно добавлен!");
        setQuestion("");
        setAnswers(["", "", "", ""]);
        setCorrectAnswer("");
      } else {
        alert("Ошибка при добавлении вопроса.");
      }
    } catch (error) {
      console.error("Ошибка сети:", error);
      alert("Ошибка сети.");
    }
  };

  return (
    <div className="form-container">
      <h2>Добавить новый вопрос</h2>
      <form onSubmit={handleSubmit}>
        {/* Поле для вопроса */}
        <div>
          <label>Вопрос:</label>
          <input
            type="text"
            value={question}
            onChange={handleQuestionChange}
            placeholder="Введите ваш вопрос"
            required
          />
        </div>

        {/* Поля для ответов */}
        <div>
          <label>Варианты ответов:</label>
          {answers.map((answer, index) => (
            <div key={index} style={{ display: "flex", marginBottom: "5px" }}>
              <input
                type="text"
                value={answer}
                onChange={(e) => handleAnswerChange(index, e.target.value)}
                placeholder={`Ответ ${index + 1}`}
                required
              />
              <button
                type="button"
                onClick={() => removeAnswer(index)}
                style={{ marginLeft: "5px" }}
              >
                Удалить
              </button>
            </div>
          ))}
          <button type="button" onClick={addAnswer}>
            Добавить ответ
          </button>
        </div>

        {/* Выбор правильного ответа */}
        <div>
          <label>Верный ответ:</label>
          <select
            value={correctAnswer}
            onChange={(e) => setCorrectAnswer(e.target.value)}
            required
          >
            <option value="" disabled>
              Выберите верный ответ
            </option>
            {answers.map((answer, index) => (
              <option key={index} value={index}>
                {answer || `Ответ ${index + 1}`}
              </option>
            ))}
          </select>
        </div>

        {/* Кнопка отправки */}
        <button type="submit">Добавить вопрос</button>
      </form>
    </div>
  );
};

export default AddQuestionForm;

const getAuthToken = () => {
  const cookies = document.cookie.split("; ");
  const tokenCookie = cookies.find((cookie) => cookie.startsWith("auth_token="));
  if (tokenCookie) {
    console.log("Токен перед отправкой: ", decodeURIComponent(tokenCookie.split("=")[1]))
    return decodeURIComponent(tokenCookie.split("=")[1]); // Декодируем токен
  } else {
    return null;
  }
};

const saveTokenFromURL = () => {
  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");
  console.log("Токен перед сохранением: ", token)
  if (token) {
    document.cookie = `auth_token=${encodeURIComponent(token)}; Path=/; SameSite=Strict`;
  }
};

if (new URLSearchParams(window.location.search).has("token")) {
  saveTokenFromURL();
}
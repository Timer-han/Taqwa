import { React, useState } from "react";
import "../css/AddQuestion.css";
import { addQuestion } from "../services/api";

const AddQuestion = () => {
  const [question, setQuestion] = useState(""); // Поле для вопроса
  const [answers, setAnswers] = useState(["", "", "", ""]); // Массив с вариантами ответа
  const [correctAnswer, setCorrectAnswer] = useState(""); // Верный ответ
  const [description, setDescription] = useState("");
  const [difficulty, setDifficulty] = useState(null);

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
    if (answers.length === 5) {
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

  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  };

  const handleDifficultyChange = (e) => {
    if (e.target.value === "") {
      setDifficulty(null);
      return
    }

    setDifficulty(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    let currDifficulty
    try {
      currDifficulty = parseInt(difficulty);
      if (currDifficulty < 1 || currDifficulty > 100) {
        alert("Сложность должна быть от 1 до 100")
        return
      }
    } catch (error) {
      alert("Введите число")
      return
    }

    try {
      await addQuestion(question, answers, correctAnswer, description, currDifficulty);
    } catch (error) {
      console.log("Ошибка: ", error)
      alert("Ошибка, попробуйте снова:", error)
      return
    } finally {
      alert("Вопрос успешно добавлен!");
      setQuestion("");
      setAnswers(["", "", "", ""]);
      setCorrectAnswer("");
      setDescription("");
      setDifficulty(null);
    }
  };

  return (
    <div className="form-container">
      <h2 className="question-add">Добавить новый вопрос</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label className="question-label">Вопрос:</label>
          <input
            type="text"
            value={question}
            onChange={handleQuestionChange}
            placeholder="Введите ваш вопрос"
            required
            className="question-input"
          />
        </div>

        {/* Поля для ответов */}
        <div>
          <label className="answers-label">Варианты ответов:</label>
          {answers.map((answer, index) => (
            <div key={index} style={{ display: "flex", marginBottom: "5px" }}>
              <input
                type="text"
                value={answer}
                onChange={(e) => handleAnswerChange(index, e.target.value)}
                placeholder={`Ответ ${index + 1}`}
                required
                className="answers-input"
              />
              <button
                type="button"
                onClick={() => removeAnswer(index)}
                style={{ marginLeft: "5px" }}
                className="remove-button"
              >
                Удалить
              </button>
            </div>
          ))}
          <button type="button" onClick={addAnswer} className="add-button">
            Добавить ответ
          </button>
        </div>

        {/* Выбор правильного ответа */}
        <div>
          <label className="correct-label">Верный ответ:</label>
          <select
            value={correctAnswer}
            onChange={(e) => setCorrectAnswer(e.target.value)}
            required
            className="correct-select"
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

        {/* Описание */}
        <div>
          <label className="description-label">Описание:</label>
          <input 
            type="text"
            value={description}
            onChange={handleDescriptionChange}
            placeholder="Пояснение к вопросу, если пользователь ответит неверно"
            className="description-input"
          />
        </div>

        {/* Сложность */}
        <div>
          <label className="difficulty-label">Сложность:</label>
          <input 
            type="text"
            value={difficulty}
            onChange={handleDifficultyChange}
            placeholder="Сложность от 1 до 100"
            className="difficulty-input"
          />
        </div>

        {/* Кнопка отправки */}
        <button type="submit" className="send-button">Добавить вопрос</button>
      </form>
    </div>
  );
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

export default AddQuestion;
import React, { useState } from "react";
import "../css/Feedback.css"
import { sendFeedback } from "../services/api";

const Feedback = (uuid) => {
    const [feedbackType, setFeedbackType] = useState(null);
    const [comment, setComment] = useState("");

    const handleSubmitFeedback = async () => {
        try {
            await sendFeedback(feedbackType, uuid, comment);
        } catch (error) {
            console.log("Ошибка: ", error)
            alert("Ошибка, попробуйте снова:", error)
        } finally {
            alert("Ваш отзыв отправлен, спасибо)")
            setFeedbackType(null);
            setComment("");
        }
    }

    return <div className="feedback">
        <div className="feedback-buttons">
            <button
                onClick={() => {
                    setFeedbackType("good");
                    setComment("");
                    handleSubmitFeedback();
                }}
                className={`button-good ${feedbackType === "good" ? "selected" : ""}`}
            >Хороший вопрос</button>

            <button
                onClick={() => {
                    setFeedbackType("bad");
                    setComment("");
                }}
                className={`button-bad ${feedbackType === "bad" ? "selected" : ""}`}
            >Плохой вопрос</button>

            <button
                onClick={() => {
                    setFeedbackType("improve");
                    setComment(""); // Сбрасываем комментарий
                }}
                className={`button-improve ${feedbackType === "improve" ? "selected" : ""}`}
            >Я бы улучшил</button>
        </div>
        <div className="feedback-comment">
        {(feedbackType === "bad" || feedbackType === "improve") && (
            <div className="feedback-comment">
            <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Напишите свой комментарий..."
            />
            <button onClick={handleSubmitFeedback}>Отправить</button>
            </div>
        )}
        </div>
    </div>
};

export default Feedback;
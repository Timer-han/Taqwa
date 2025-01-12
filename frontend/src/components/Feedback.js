import React, { useState } from "react";
import "../css/Feedback.css"
import { sendFeedback } from "../services/api";

const Feedback = (uuid) => {
    const [feedbackType, setFeedbackType] = useState("");
    const [comment, setComment] = useState("");

    const handleSubmitFeedback = async (type, commentText = "") => {
        try {
            console.log("feedback and comment: ", type, commentText)
            await sendFeedback(type, uuid, commentText);
        } catch (error) {
            console.log("Ошибка: ", error)
            alert("Ошибка, попробуйте снова:", error)
        } finally {
            alert("Ваш отзыв отправлен, спасибо)")
            setFeedbackType("");
            setComment("");
        }
    }

    const handleFeedbackClick = (type) => {
        console.log("type:", type)
        setFeedbackType("good");
        if (type === "good") {
            handleSubmitFeedback(type);
        }
    };

    return <div className="feedback">
        <div className="feedback-buttons">
            <button
                onClick={() => handleFeedbackClick("good")}
                className={`button-good ${feedbackType === "good" ? "selected" : ""}`}
            >Хороший вопрос</button>

            <button
                onClick={() => handleFeedbackClick("bad")}
                className={`button-bad ${feedbackType === "bad" ? "selected" : ""}`}
            >Плохой вопрос</button>

            <button
                onClick={() => handleFeedbackClick("improve")}
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
            <button onClick={handleSubmitFeedback(feedbackType, comment)}>Отправить</button>
            </div>
        )}
        </div>
    </div>
};

export default Feedback;
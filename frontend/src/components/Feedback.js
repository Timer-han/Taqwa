import React, { useState } from "react";
import "../css/Feedback.css"
import { sendFeedback } from "../services/api";
import { replace, useNavigate } from "react-router-dom";

const Feedback = (uuid) => {
    const [feedbackType, setFeedbackType] = useState("");
    const [comment, setComment] = useState("");
    const navigate = useNavigate();

    const handleSubmitFeedback = async (type, commentText = "") => {
        try {
            await sendFeedback(type, uuid, commentText);
        } catch (error) {
            console.log("Ошибка: ", error)
            alert("Ошибка, попробуйте снова:", error)
        } finally {
            setFeedbackType("");
            setComment("");
            navigate("/", {replace: true} )
        }
    }

    const handleFeedbackClick = (type) => {
        setFeedbackType(type);
        if (type === "good" || type === "bad") {
            handleSubmitFeedback(type);
        }
    };

    return <div className="feedback">
        <div className="feedback-buttons">
            <button
                onClick={() => handleFeedbackClick("good")}
                className={`button-good ${feedbackType === "good" ? "selected" : ""}`}
            >Вопрос верный</button>

            <button
                onClick={() => handleFeedbackClick("bad")}
                className={`button-bad ${feedbackType === "bad" ? "selected" : ""}`}
            >Вопрос неверный</button>

            <button
                onClick={() => handleFeedbackClick("improve")}
                className={`button-improve ${feedbackType === "improve" ? "selected" : ""}`}
            >Есть идеи по улучшению</button>
        </div>

        <div className="feedback-comment">
        {(feedbackType === "improve") && (
            <div className="feedback-comment">
            <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Напишите свой комментарий..."
            />
            <button onClick={() => handleSubmitFeedback(feedbackType, comment)}>Отправить</button>
            </div>
        )}
        </div>
    </div>
};

export default Feedback;
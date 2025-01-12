import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getSuggest } from "../services/api";
import AnswerCard from "../components/AnswerCard";
import "../css/ReviewDetail.css"
import Feedback from "../components/Feedback";

const QuestionDetail = () => {
  const { uuid } = useParams();
  const [suggest, setSuggest] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchQuestion = async () => {
      try {
        const suggest = await getSuggest(uuid);
        setSuggest(suggest);
      } catch (error) {
        console.error("Ошибка при загрузке вопроса:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestion();
  }, [uuid]);

  if (loading) {
    return <div>Загрузка...</div>;
  }

  if (!suggest) {
    return <div>Вопрос не найден</div>;
  }

  return (
    <div className="review-detail">
      <h2 className="review-question">{suggest.question}</h2>
      <div className="answers-grid">
        {suggest.answers.map((answer, index) => (
          <AnswerCard suggest={suggest} answer={answer} index={index} />
        ))}
      </div>
      {suggest.description && <p><strong>Пояснение:</strong> {suggest.description}</p>}

      <div className="feedback-buttons">
        <Feedback uuid={uuid}/>
      </div>
    </div>
  );
};

export default QuestionDetail;

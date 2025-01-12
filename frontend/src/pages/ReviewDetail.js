import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getSuggest } from "../services/api";
import AnswerCard from "../components/AnswerCard";
import "../css/ReviewDetail.css"
import Feedback from "../components/Feedback";
import { parseAuthToken } from "../services/api";

const QuestionDetail = () => {
  const { uuid } = useParams();
  const [suggest, setSuggest] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isReviewed, setIsReviewed] = useState(false);

  useEffect(() => {
    const fetchQuestion = async () => {
      try {
        const suggest = await getSuggest(uuid);
        setSuggest(suggest);

        const telegram_id = parseAuthToken()
        const processedSuggest = {
          marked_as_correct: suggest.marked_as_correct.map((item) => String(item.telegram_id)),
          marked_as_erroneus: suggest.marked_as_erroneous.map((item) => String(item.telegram_id)),
          marked_as_improve: suggest.marked_as_improve.map((item) => String(item.telegram_id)),
        };

        let reviewed = false;
        if (processedSuggest.marked_as_correct.includes(telegram_id) ||
          processedSuggest.marked_as_erroneus.includes(telegram_id) ||
          processedSuggest.marked_as_improve.includes(telegram_id)) {
            reviewed = true;
          }

        setIsReviewed(reviewed);
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

      {(!isReviewed) && (
        <div className="feedback-buttons">
        <Feedback uuid={uuid}/>
      </div>
      )}
      {(isReviewed) && (
        <h4 className="review-done">Вопрос уже проверен</h4>
      )}
    </div>
  );
};

export default QuestionDetail;

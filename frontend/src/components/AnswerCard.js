import "../css/AnswerCard.css"

function AnswerCard({suggest, answer, index}) {
    return <div className="answer-card">
        {index === suggest.correct_id ? (
            <p className="answer-correct">{answer}</p>
        ) : (
            <p className="answer-wrong">{answer}</p>
        )}
    </div>
};

export default AnswerCard;
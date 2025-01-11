import "../css/SuggestCard.css"
import AnswerCard from "./AnswerCard";

function SuggestCard({suggest}) {
    return <div className="suggest-card">
        <div className="suggest-poster">
            <div className="suggest-overlay">
            </div>
        </div>
        <div className="suggest-info">
            <h3>{suggest.question}</h3>
            {suggest.answers.map((answer, index) => (
                <AnswerCard suggest={suggest} answer={answer} index={index} />
            ))}
        </div>
    </div>
}

export default SuggestCard;
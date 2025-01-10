import "../css/SuggestCard.css"
// import { useMovieContext } from "../contexts/MovieContext"

function SuggestCard({suggest}) {
    return <div className="suggest-card">
        <div className="suggest-poster">
            <div className="suggest-overlay">
            </div>
        </div>
        <div className="suggest-info">
            <h3>{suggest.question}</h3>
            {/* <p>{suggest.answers}</p> */}
            {suggest.answers.map((answer) => (
                <p>{answer}</p>
            ))}
        </div>
        {/* {suggests.map((suggest) => (
                      <SuggestCard suggest={suggest} key={suggest.uuid} />
                    ))} */}
    </div>
}

export default SuggestCard;
// import "../css/SuggestCard.css"
// import { useMovieContext } from "../contexts/MovieContext"

function SuggestCard({suggest}) {
    return <div className="suggest-card">
        <div className="suggest-poster">
            <div className="suggest-overlay">
            </div>
        </div>
        <div className="suggest-info">
            <h3>{suggest.title}</h3>
            <p>{suggest.release_date?.split("-")[0]}</p>
        </div>
    </div>
}

export default SuggestCard;
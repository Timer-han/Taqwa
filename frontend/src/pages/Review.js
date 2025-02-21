import { React, useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getNonReviewedSuggests, getReviewedCounts } from "../services/api";
import SuggestCard from "../components/SuggestCard";
import "../css/Review.css"

const Review = () => {
    const [suggests, setSuggests] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);
    const [reviewedCount, setReviewedCount] = useState(null);
    const [totalCount, setTotal] = useState(null);

    useEffect(() => {
        const loadSuggestedQuestions = async () => {
            try {
                const suggests = await getNonReviewedSuggests();
                setSuggests(suggests);
            } catch (err) {
                setError(`Ошибка: ${err.message}`)
            } finally {
                setLoading(false);
            }
        };

        const loadReviewedCounts = async () => {
            try {
                const data = await getReviewedCounts();
                setReviewedCount(data.reviewed_count);
                setTotal(data.total_count);                console.log(totalCount)
            } catch (err) {
                console.log(`Ошибка: ${err.message}`)
            } finally {
                setLoading(false);
            }
        };

        loadSuggestedQuestions();
        loadReviewedCounts();
    }, [])

    return (
        <div className="review">  
        {error && <div className="error-message">{error}</div>}
        {loading ? (
          <div className="loading">Loading...</div>
        ) : (
          <div className="suggests-grid">
            {suggests.map((suggest) => (
              <Link className="suggests-link" to={`/review/${suggest.uuid}`}>
                <SuggestCard suggest={suggest} key={suggest.uuid} />
              </Link>
            ))}
          </div>
        )}
        {totalCount && <div className="reviewed-counter">{reviewedCount}/{totalCount}</div>}
      </div>
    );
}

export default Review;
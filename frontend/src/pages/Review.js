import { React, useState, useEffect } from "react";

const Review = () => {
    const [suggests, setSuggests] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadSuggestedQuestions = async () => {
            try {
                const suggests = await getSuggests();
                setSuggests(suggests);
            } catch (err) {
                console.log(err);
                setError("Failed to find suggests...")
            } finally {
                setLoading(false);
            }
        };

        loadSuggestedQuestions();
    }, [])

    return (
        <div className="review">  
        {error && <div className="error-message">{error}</div>}
        {loading ? (
          <div className="loading">Loading...</div>
        ) : (
          <div className="suggests-grid">
            {suggests.map((suggest) => (
              <SuggestCard suggest={suggest} key={suggest.id} />
            ))}
          </div>
        )}
      </div>
    );
}

export default Review;
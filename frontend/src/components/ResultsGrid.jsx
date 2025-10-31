
export default function ResultsGrid({ results, isLoading }) {
  
    const getImageUrl = (imageId) => {
      // Our backend returns the image filename. We need to construct the full URL
      // that the browser can use to request it from our running backend server.
      // NOTE: This assumes we will serve static files from our backend later.
      // For now, it won't display anything, but the structure is correct.
      // We will fix the image display in the next step.
      return `http://localhost:8000/images/${imageId}`;
    }
  
    return (
      <div className="results-container">
        <h2>Results</h2>
        <div className="grid">
          {isLoading && <p>Loading...</p>}
          
          {!isLoading && results.length === 0 && (
            <p>Your search results will appear here.</p>
          )}
  
          {!isLoading && results.map((result, index) => (
            <div key={index} className="result-item">
              <img 
                // The id will look like 'images\\12345.jpg', we need to clean it up
                src={getImageUrl(result.id.split('\\').pop())} 
                alt={result.product_name} 
                onError={(e) => { e.target.style.display = 'none'; }} // Hide broken images
              />
              <p>{result.product_name}</p>
            </div>
          ))}
        </div>
      </div>
    );
  }
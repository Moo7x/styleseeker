// frontend/src/App.jsx

import { useState } from 'react'; 
import ImageUploader from './components/ImageUploader';
import ResultsGrid from './components/ResultsGrid';

function App() {
  // --- STATE MANAGEMENT ---
  const [selectedFile, setSelectedFile] = useState(null);
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // We will add the API call function here later

  return (
    <div className="app-container">
      <header>
        <h1>StyleSeeker</h1>
        <p>Find your next look by uploading an image.</p>
      </header>
      <main>
        {/* We will pass state down to our components as "props" */}
        <ImageUploader 
          setSelectedFile={setSelectedFile} 
          setIsLoading={setIsLoading}
          setResults={setResults}
        />
        <ResultsGrid 
          results={results} 
          isLoading={isLoading} 
        />
      </main>
    </div>
  )
}

export default App
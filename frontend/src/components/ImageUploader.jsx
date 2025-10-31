// frontend/src/components/ImageUploader.jsx

export default function ImageUploader({ setSelectedFile, setIsLoading, setResults }) {
  
    const handleFileChange = (event) => {
      // When a user selects a file, we update the state in the parent App component
      setSelectedFile(event.target.files[0]);
    };
  
    const handleSearch = async (event) => {
      event.preventDefault(); // Prevents the browser from reloading the page
      
      const fileInput = event.target.elements.fileInput;
      const file = fileInput.files[0];
  
      if (!file) {
        alert("Please select a file first!");
        return;
      }
  
      setIsLoading(true); // Tell the app we are starting to load
      setResults([]); // Clear previous results
  
      // --- THE API CALL ---
      const formData = new FormData();
      formData.append("file", file);
  
      try {
        const response = await fetch("http://localhost:8000/search/", {
          method: "POST",
          body: formData,
        });
  
        if (!response.ok) {
          throw new Error("Something went wrong with the search.");
        }
  
        const data = await response.json();
        setResults(data.results); // Update the results state in the parent
  
      } catch (error) {
        console.error("Search failed:", error);
        alert("Search failed. Please check the console for more details.");
      } finally {
        setIsLoading(false); // Tell the app we are done loading
      }
    };
  
    return (
      <div className="uploader-container">
        <h2>Upload an Image to Search</h2>
        <form onSubmit={handleSearch}>
          <input 
            type="file" 
            name="fileInput"
            accept="image/jpeg, image/png" 
            onChange={handleFileChange} 
          />
          <button type="submit">Search</button>
        </form>
      </div>
    );
  }
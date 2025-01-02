import React, { useState } from "react";
import PromptInput from "./components/promptInput";
import ResultsDisplay from "./components/displayResults";
import { testLLMs } from "./services/api";

function App() {
  const [results, setResults] = useState(null);

  const handleSubmission = async ({ prompt, selectedLLMs }) => {
    try {
      const data = {
        prompt,
        ground_truth: "Kuala Lumpur", // Replace with dynamic ground truth if needed
        selected_llms: selectedLLMs,
      };
      const response = await testLLMs(data);
      setResults(response.results);
    } catch (error) {
      console.error("Error fetching results:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>LLM Comparison Tool</h1>
      <PromptInput onSubmit={handleSubmission} />
      <ResultsDisplay results={results} />
    </div>
  );
}

export default App;

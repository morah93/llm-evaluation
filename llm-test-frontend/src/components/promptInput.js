import React from 'react';
import { useState } from 'react';


// Add your component code here
const PromptInput = ({ onSubmit }) => {
  const [prompt, setPrompt] = useState("")
  const [selectedLlm, setSelectedLlm] = useState([])

  const llmOptions = ["openai", "huggingface", "cohere", "anthropic", "llama"]

  const handleLlmSelection = (llm) => {
    setSelectedLlm((prev) =>
      prev.includes(llm) ? prev.filter((item) => item !== llm) : [...prev, llm]
    );
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt && selectedLlm.length > 0) {
      onSubmit({ prompt, selectedLlm });
    } else {
      alert("Please provide a prompt and select at least one LLM.");
    }
  };

  return (
    <div style={{ margin: "20px" }}>
      <h2>Test LLMs</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="prompt">Prompt:</label>
          <textarea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Enter your prompt here"
            style={{ width: "100%", height: "80px", margin: "10px 0" }}
          />
        </div>
        <div>
          <h4>Select LLM(s):</h4>
          {llmOptions.map((llm) => (
            <div key={llm}>
              <input
                type="checkbox"
                id={llm}
                value={llm}
                onChange={() => handleLlmSelection(llm)}
              />
              <label htmlFor={llm}>{llm}</label>
            </div>
          ))}
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default PromptInput;

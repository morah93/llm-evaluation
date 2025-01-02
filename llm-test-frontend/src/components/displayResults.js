import React from "react";

const ResultsDisplay = ({ results }) => {
  if (!results) {
    return null;
  }

  return (
    <div style={{ marginTop: "20px" }}>
      <h3>Results:</h3>
      {Object.entries(results).map(([llm, data]) => (
        <div key={llm} style={{ marginBottom: "20px" }}>
          <h4>{llm}</h4>
          <p><strong>Response:</strong> {data.response || "No response"}</p>
          <p><strong>Time:</strong> {data.time ? `${data.time.toFixed(2)}s` : "N/A"}</p>
          <p><strong>Accuracy:</strong> {data.accuracy ? `${data.accuracy.toFixed(2)}%` : "N/A"}</p>
          <p><strong>Score:</strong> {data.score ? `${data.score.toFixed(2)}` : "N/A"}</p>
        </div>
      ))}
    </div>
  );
};

export default ResultsDisplay;

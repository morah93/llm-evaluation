const API_URL = 'http://localhost:8000/api';  // Adjust this to match your backend URL

export const testLLMs = async (data) => {
  try {
    const response = await fetch(`${API_URL}/test-llms`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

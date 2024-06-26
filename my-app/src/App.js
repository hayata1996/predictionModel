import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [height, setHeight] = useState('');
  const [men, setMen] = useState(true);
  const [predictedWeight, setPredictedWeight] = useState(null);


  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/predict/', {
        men,
        height: parseFloat(height)
      });
      setPredictedWeight(response.data.weight);
    } catch (error) {
      console.error('There was an error predicting the weight!', error);
    }
  };

  return (
    <div className="App">
      <h1>Weight Prediction</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Height:
            <input
              type="number"
              value={height}
              onChange={(e) => {
                const value = parseFloat(e.target.value);
                if (value >= 0) {
                  setHeight(value);
                }
              }}
              required
            />
          </label>
        </div>
        <div>
          <label>
            Gender:
            <select
              value={men}
              onChange={(e) => setMen(e.target.value === 'true')}
              required
            >
              <option value={true}>Male</option>
              <option value={false}>Female</option>
            </select>
          </label>
        </div>
        <button type="submit">Predict Weight</button>
      </form>
      {predictedWeight !== null && (
        <div>
          <h2>Predicted Weight: {predictedWeight.toFixed(2)} kg</h2>
        </div>
      )}
    </div>
  );
}

export default App;

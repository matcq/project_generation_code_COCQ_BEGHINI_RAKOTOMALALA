import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [language, setLanguage] = useState("");
  const [concept, setConcept] = useState("");
  const [level, setLevel] = useState("");
  const [generatedCode, setGeneratedCode] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://127.0.0.1:5000/generate", {
        language,
        concept,
        level
      });

      // Affichez le code généré dans l'état
      setGeneratedCode(response.data.code);
    } catch (error) {
      console.error("Erreur lors de la génération :", error);
    }
  };

  return (
    <div className="app-container">
      <h1 className="title">Générateur de Code avec OpenAI</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>
            Langage :
            <input
              type="text"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              required
            />
          </label>

          <label>
            Concept :
            <input
              type="text"
              value={concept}
              onChange={(e) => setConcept(e.target.value)}
              required
            />
          </label>

          <label>
            Niveau :
            <input
              type="text"
              value={level}
              onChange={(e) => setLevel(e.target.value)}
              required
            />
          </label>
        </div>
        <button type="submit">Générer le code</button>
      </form>

      {generatedCode && (
        <div className="generated-code-container">
          <h2>Code généré :</h2>
          <pre>{generatedCode}</pre>
        </div>
      )}

    </div>
  );
}

export default App;

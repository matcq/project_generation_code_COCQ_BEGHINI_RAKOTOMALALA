import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // Assurez-vous que le CSS soit inclus

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
        level,
      });

      setGeneratedCode(response.data.code);
    } catch (error) {
      console.error("Erreur lors de la génération :", error);
    }
  };

  return (
    <div className="chatgpt-container">
      <header className="chatgpt-header">
        <h1>Générateur de Code</h1>
      </header>
      <main className="chatgpt-main">
        <form className="chatgpt-form" onSubmit={handleSubmit}>
          <div className="chatgpt-input-group">
            <label htmlFor="language">Langage :</label>
            <input
              id="language"
              type="text"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              placeholder="Exemple : Python, JavaScript"
              required
            />
          </div>
          <div className="chatgpt-input-group">
            <label htmlFor="concept">Concept :</label>
            <input
              id="concept"
              type="text"
              value={concept}
              onChange={(e) => setConcept(e.target.value)}
              placeholder="Exemple : Algorithme de tri"
              required
            />
          </div>
          <div className="chatgpt-input-group">
            <label htmlFor="level">Niveau :</label>
            <input
              id="level"
              type="text"
              value={level}
              onChange={(e) => setLevel(e.target.value)}
              placeholder="Exemple : Débutant, Avancé"
              required
            />
          </div>
          <button className="chatgpt-button" type="submit">
            Générer
          </button>
        </form>

        {generatedCode && (
          <div className="chatgpt-output">
            <h2>Code généré :</h2>
            <pre>{generatedCode}</pre>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from tavily import TavilyClient

# Charger les variables d'environnement
load_dotenv()

# Initialiser les clés API
openai_api_key = os.getenv("OPEN_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Initialisation des clients externes
client_tavily = TavilyClient(api_key=tavily_api_key)
ddg = DDGS()

# Initialisation du modèle LangChain
model = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    api_key=openai_api_key
)

# Créer une application Flask
app = Flask(__name__)
CORS(app)

# Fonction pour générer un code via LangChain
def generate_code(language, concept, level):
    prompt_template = PromptTemplate.from_template(
        f"\u00c9cris un exemple {level} en {language} sur {concept}, avec des commentaires détaillés expliquant le code."
    )
    prompt = prompt_template.format()

    try:
        chain = LLMChain(llm=model, prompt=prompt_template)
        response = chain.run(language=language, concept=concept, level=level)
        return response
    except Exception as e:
        return f"Erreur lors de la génération : {e}"

# Fonction pour exécuter une recherche d'informations
def perform_search(query, max_results=5):
    try:
        results = ddg.text(query, max_results=max_results)
        return [result["href"] for result in results]
    except Exception as e:
        return [f"Erreur lors de la recherche : {e}"]

# Fonction pour interroger Tavily
def ask_tavily(query):
    try:
        result = client_tavily.search(query, include_answer=True)
        return result.get("answer", "Pas de réponse trouvée.")
    except Exception as e:
        return f"Erreur avec Tavily : {e}"

# Route principale pour générer le code
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    language = data.get('language')
    concept = data.get('concept')
    level = data.get('level')

    # Appelle la fonction de génération
    response = generate_code(language, concept, level)
    return jsonify({'code': response})

# Route pour rechercher des informations
@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')
    max_results = data.get('max_results', 5)

    # Effectue une recherche
    results = perform_search(query, max_results)
    return jsonify({'results': results})

# Route pour utiliser Tavily
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('query')

    # Pose une question via Tavily
    response = ask_tavily(query)
    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run(debug=True)

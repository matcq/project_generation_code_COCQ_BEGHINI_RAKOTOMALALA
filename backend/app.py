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
def generate_code(language, concept, level, tavily_info):
    prompt_template = PromptTemplate.from_template(
        f"\u00c9cris un exemple {level} en {language} sur {concept}, avec des commentaires détaillés expliquant le code. Utilise ces informations supplémentaires : {tavily_info} et ajoute les urls consultés à la fin"
    )
    prompt = prompt_template.format()

    try:
        chain = LLMChain(llm=model, prompt=prompt_template)
        response = chain.run(language=language, concept=concept, level=level)
        return response
    except Exception as e:
        return f"Erreur lors de la génération : {e}"

# Fonction pour interroger Tavily
def ask_tavily(query):
    try:
        result = client_tavily.search(query, include_answer=True)

        urls = result.get("sources", [])

        # Formater les URLs en texte
        urls_text = "\n".join([f"Source: {url}" for url in urls])

        # Afficher la réponse brute de Tavily
        print("Réponse brute de Tavily:", result)

        # Récupérer la réponse ou renvoyer un message si rien n'est trouvé
        answer = result.get("answer", "Pas de réponse trouvée.")

        # Ajouter les URLs à la fin de la réponse
        full_answer = f"{answer}\n\n{urls_text}"

        return full_answer
    except Exception as e:
        return f"Erreur avec Tavily : {e}"

# Route principale pour générer le code
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    language = data.get('language')
    concept = data.get('concept')
    level = data.get('level')

    # Poser une question à Tavily avec les informations reçues du front-end
    query = f"Donne-moi des informations pour le langage {language}, concept {concept}, niveau {level}"
    tavily_info = ask_tavily(query)

    # Appelle la fonction de génération avec les informations de Tavily
    response = generate_code(language, concept, level, tavily_info)
    return jsonify({'code': response})

if __name__ == '__main__':
    app.run(debug=True)
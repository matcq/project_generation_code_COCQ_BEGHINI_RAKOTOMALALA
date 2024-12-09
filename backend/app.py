from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

# Créez l'instance de votre application Flask
app = Flask(__name__)
CORS(app)

# Récupération de la clé API OpenAI
openai_api_key = os.getenv("OPEN_API_KEY")

# Initialisation du modèle LangChain
model = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    api_key=openai_api_key
)

# Fonction pour générer du code
def generate_code(language, concept, level):
    # Création du prompt dynamique
    prompt_template = PromptTemplate.from_template(
        f"Écris un exemple {level} en {language} sur {concept}, avec des commentaires détaillés expliquant le code."
    )
    prompt = prompt_template.format()

    try:
        # Appel du modèle LangChain avec le prompt généré
        ai_response = model.invoke(prompt)
        return ai_response.content
    except Exception as e:
        return f"Erreur lors de la génération : {e}"

# Route principale pour générer le code
@app.route('/generate', methods=['POST'])
def generate():
      # Récupère les paramètres utilisateur
    data = request.json
    language = data.get('language')
    concept = data.get('concept')
    level = data.get('level')

    # Appelle la fonction de génération
    response = generate_code(language, concept, level)
    return jsonify({'code': response})

if __name__ == '__main__':
    app.run(debug=True)

# project_generation_code_COCQ_BEGHINI_RAKOTOMALALA

## Création d'un environnement virtuel

- Ouvrir un terminal et se mettre dans le dossier du projet
- Se mettre dans le dossier backend : cd backend
- Exécuter : python -m venv venv
- Exécuter : venv\Scripts\activate
- Exécuter : pip install -r requirements.txt
- Exécuter : deactivate
- pip install langchain-openai
- pip install langchain

## Ajout du fichier .env à la racine du projet

- Contenu du fichier .env :
OPENAI_API_KEY=
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_API_KEY=
TAVILY_API_KEY=
- Ajouter votre clé API OPENAI

## Lancement du projet

- Ouvrir un terminal et se mettre dans backend : cd backend
- Lancer la commande suivante : python app.py
- Ouvrir un deuxième terminal et se mettre dans frontend : cd frontend
- npm install
- Lancer la commande suivante : npm start

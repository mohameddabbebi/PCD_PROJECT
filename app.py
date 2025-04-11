from flask import Flask, render_template, request, jsonify
#import pickle
#import numpy as np
#import faiss
#from sentence_transformers import SentenceTransformer
#import ctransformers
from dataProcess import structure_data
from quiz import generate_quiz_from_data,generate_quiz_from_context,get_first_512_words
from Main import get_contextual_response,retrieve_relevant_texts
# Initialiser Flask
app = Flask(__name__)














@app.route('/')
def index():
    return render_template('index.html')

# Route de chat
@app.route('/chat', methods=['POST'])
def chat():
    # Récupérer l'entrée de l'utilisateur
    #print(request.json)  # Afficher la requête reçue pour déboguer
    #user_input = request.json.get("message")
    #if not user_input:
     #   return jsonify({"response": "Aucune entrée utilisateur fournie"}), 400
    user_input = request.json.get("message")
    context = retrieve_relevant_texts(user_input)
    response = get_contextual_response(context,user_input)
    #response="bla bla bla"
    
    # Retourner la réponse sous forme de JSON
    return jsonify({"response": response})

@app.route('/quiz',methods=['GET'])
def quiz():
    response=generate_quiz_from_data(structure_data('C:\\Users\\ramib\\Downloads\\chatbot_interface1\\chatbot_interface\\file1.txt'),2)
    return  jsonify({"response": response})
@app.route('/Resume',methods=['GET'])
def Resume():
    return"HELLO MY FRIEND"
    
    # Démarrer l'application Flask
if __name__ == '__main__':
    app.run(debug=False)

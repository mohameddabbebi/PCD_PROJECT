import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import ctransformers


def retrieve_relevant_texts(query, k=1):
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Charger les fichiers Pickle
    with open("C:\\Users\\ramib\\Downloads\\chatbot_interface1\\chatbot_interface\\texts.pkl", "rb") as f:
      texts = pickle.load(f)

    with open("C:\\Users\\ramib\\Downloads\\chatbot_interface1\\chatbot_interface\\metadata.pkl", "rb") as f:
      metadata = pickle.load(f)

    embeddings = np.load("C:\\Users\\ramib\\Downloads\\chatbot_interface1\\chatbot_interface\\embeddings.npy")
    index1 = faiss.read_index("C:\\Users\\ramib\\Downloads\\chatbot_interface1\\chatbot_interface\\faiss_index.index")
    # Convertir la requête en embedding
    query_embedding = embedding_model.encode([query])

    # Recherche dans l'index FAISS
    _, indices = index1.search(np.array(query_embedding, dtype=np.float32), k)  # Recherche dans l'index

    # Récupérer les textes pertinents en fonction des indices retournés
    retrieved_texts = [texts[i] for i in indices[0]]

    return retrieved_texts



def get_contextual_response(context,question):
    llm = ctransformers.AutoModelForCausalLM.from_pretrained(
    'C:\\Users\\ramib\\Downloads\\chatbot_interface1\\chatbot_interface\\llama-2-7b-chat.Q4_K_M.gguf',
    model_type='llama',
    max_new_tokens=512,
    temperature=0.5, #0.1 kenit
    gpu_layers=25,
    context_length=2048  
)
    # Construction stricte du prompt LLaMA 2
    prompt = f"""<s>[INST] <<SYS>>
    Répondez avec la langue française UNIQUEMENT en utilisant ce contexte :
    context:{context}
    <</SYS>>

    Question : {question} [/INST]"""
    try:
        # Génération contrôlée
        response = llm(
            prompt,
            max_new_tokens=512,
            temperature=0.5,  # Réduit les hallucinations
            top_p=0.95,        # Contrôle de la diversité
            stop=["</s>", "[INST]"]  # Tokens d'arrêt
        )

        # Nettoyage de la réponse
        response = response.split("[/INST]")[-1].strip()
        response = response.replace("<s>", "").replace("</s>", "").strip()

        return response

    except Exception as e:
        return f"Erreur de génération : {str(e)}"
    

# Exemple d'utilisation
question = "donner les etapes de l'algorithme CSMA/CD"
context = retrieve_relevant_texts(question)
response = get_contextual_response(context,question)
with open("reponse.txt", "w", encoding="utf-8") as f:
    f.write(response)
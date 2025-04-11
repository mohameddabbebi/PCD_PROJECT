import re
import random
from sentence_transformers import SentenceTransformer
import ctransformers 
from dataProcess import structure_data
def get_first_512_words(text):
    # Utilisation d'une expression régulière pour séparer les mots et ponctuations
    words = re.findall(r'\S+|[.,!?;]', text)  # \S+ capture les mots, et [.,!?;] capture les ponctuations
    return ' '.join(words[:512])  # Récupérer les 512 premiers mots (y compris ponctuation)

def generate_quiz_from_data(final_data,n):
    context=[]
    random_numbers = random.sample(range(len(final_data)), n)
    for i in range(n) :
      context.append(get_first_512_words(final_data[random_numbers[i]]['text']))  
      #context.append(final_data[random_numbers[i]]['text'])
    quiz=[]
    for i in range(n) :
      quiz.append(generate_quiz_from_context(context[i]))
    return quiz
    
def generate_quiz_from_context(context):
    llm = ctransformers.AutoModelForCausalLM.from_pretrained(
    'C:\\Users\\ramib\\Downloads\\chatbot_interface1\\chatbot_interface\\llama-2-7b-chat.Q4_K_M.gguf',
    model_type='llama',
    max_new_tokens=256,
    temperature=0.5, #0.1 kenit
    gpu_layers=25,
    context_length=2048  
)
    # Construction stricte du prompt LLaMA 2
    prompt = f"""<s>[INST] <<SYS>>
Tu es un générateur de quiz avec la langue française uniquement.
Règles :
-avec la langue française uniquement.
-avec la langue française uniquement.
-avec la langue française uniquement.
-avec la langue française uniquement.
-avec la langue française uniquement.
-avec la langue française uniquement.
-avec la langue française uniquement.
-avec la langue française uniquement.
- Génére exactement 2 questions à choix multiples (QCM) en français.
- Chaque question contient 4 propositions : A), B), C), D).
- Aucune phrase d’introduction ou de conclusion.
- Ne jamais utiliser l’anglais.
- Ne jamais dire "Voici", "Great", etc.
- Le résultat attendu est uniquement les questions et leurs réponses.
   Contexte :
   {context}
<</SYS>>
[/INST]"""

    try:
        # Génération contrôlée
        response = llm(
            prompt,
            max_new_tokens=256,
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
"""
final_data = structure_data('C:\\Users\\ramib\\Downloads\\chatbot_interface1\\chatbot_interface\\file1.txt')
#print(generate_quiz_from_data(final_data,2))
with open("quiz.txt", "w", encoding="utf-8") as f:
    for q in generate_quiz_from_data(final_data, 2):
        f.write(q + "\n\n")
"""
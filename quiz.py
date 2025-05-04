import re
import random
from sentence_transformers import SentenceTransformer
import ctransformers 
from dataProcess import structure_data
from transformers import MarianMTModel, MarianTokenizer
# Variables globales pour mémoriser les objets chargés
model = None
tokenizer = None

def trans(text):
    global model, tokenizer  # permet de modifier les variables globales

    if model is None or tokenizer is None:
        print("Chargement du modèle...")
        model_name = "Helsinki-NLP/opus-mt-en-fr"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def get_first_512_words(text):
    # Utilisation d'une expression régulière pour séparer les mots et ponctuations
    words = re.findall(r'\S+|[.,!?;]', text)  # \S+ capture les mots, et [.,!?;] capture les ponctuations
    return ' '.join(words[:512])  # Récupérer les 512 premiers mots (y compris ponctuation)

def generate_quiz_from_data1(final_data, n, level_of_quiz):
    context = []
    random_numbers = random.sample(range(len(final_data)), n)
    for i in range(n):
        context.append(get_first_512_words(final_data[random_numbers[i]]['text']))

    quiz = []
    for i in range(n):
        quiz.append(generate_quiz_from_context1(context[i], level_of_quiz,i))

    return quiz

def generate_quiz_from_context1(context, level_of_quiz,i):
    llm = ctransformers.AutoModelForCausalLM.from_pretrained(
        'C:\\Users\\ramib\\Downloads\\chatbot_interface1\\chatbot_interface\\llama-2-7b-chat.Q4_K_M.gguf',
        model_type='llama',
        max_new_tokens=256,
        temperature=0.5,
        gpu_layers=25,
        context_length=2048
    )

    # Choix du niveau de difficulté
    if level_of_quiz == 2:
        difficulty = "moyen"
    elif level_of_quiz > 2:
        difficulty = "difficile"
    else:
        difficulty = "facile"

    prompt = f"""<s>[INST] <<SYS>>
Vous êtes un générateur de quiz en anglais. Suivez ces instructions à la lettre :
1. Produisez exactement 2 questions à choix multiples.
2. Chaque question doit comporter 3 options libellées A), B) et C) .
3. Le quiz doit être de niveau **{difficulty}**.
4. Ne préfixez pas par une introduction ni ne terminez par une conclusion.
5. N’utilisez jamais un mot ou une expression anglaise (ex. “Here”, “Great”, etc.).
6. Fournissez uniquement les questions et leurs propositions de réponses, sans autre texte.

Contexte :
{context}
<</SYS>>
[/INST]"""

    try:
        response = llm(
            prompt,
            max_new_tokens=256,
            temperature=0.5,
            top_p=0.95,
            stop=["</s>", "[INST]"]
        )
        #zid dans le deuxieme appel de cette fonction il faut que Question 3,4 pas 1 et2.
        response = response.split("[/INST]")[-1].strip()
        response = response.replace("<s>", "").replace("</s>", "").strip()
        response=trans(response)
        #response = re.sub(r'questions?\s+au\s+niveau\s+\*\*(facile|moderne|difficile)\*\*\s*:?', '',response, flags=re.IGNORECASE)
        # 1. Supprimer tout avant le premier "Question"
        match = re.search(r'(Question\s*1\s*:?.*)',response, re.IGNORECASE | re.DOTALL)
        if match:
           response = match.group(1)
        response = re.sub(r'\s*(Question\s*\d*\s*:)', r'\n\1',response)
    # ➕ Ajouter un saut de ligne avant chaque A), B), C), D)
        response = re.sub(r'\s*([A-D]\))', r'\n\1', response)
        if (i==1):
            response= re.sub(r'Question\s*1\s*:', 'Question 3:',response)
            response= re.sub(r'Question\s*2\s*:', 'Question 4:',response)
        return response
    except Exception as e:
        return f"Erreur de génération : {str(e)}"
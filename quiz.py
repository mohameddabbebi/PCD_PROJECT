import random 

def generate_quiz_from_data(final_data,n):
    context=[]
    random_numbers = random.sample(range(len(final_data)), n)
    for i in range(n) :
      context.append(final_data[random_numbers[i]]['text'])
    quiz=[]
    for i in range(n) :
      quiz.append(generate_quiz_from_context(context[i]))
    return quiz
    
def generate_quiz_from_context(context):
    # Construction stricte du prompt LLaMA 2
    prompt = f"""<s>[INST] <<SYS>>
    Donner un quiz sur ce contexte :
    context:{context}
    <</SYS>>

    [/INST]"""

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

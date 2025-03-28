import re

def titelize_text(text, model_path='llama-2-7b-chat.Q2_K.gguf'):
    # Initialisation du modèle avec un contexte adapté (par exemple 2048 tokens)
    llm = Llama(model_path=model_path, n_ctx=2048)

    # Construction de l'invite pour le résumé
    prompt = f"Veuillez donner un titre pour  le texte suivant de manière concise et précise :\n\n{text}\n\nRésumé :"

    # Génération de la réponse
    response = llm(prompt, max_tokens=200, temperature=0.3)

    # Extraction et nettoyage du résumé généré
    summary = response['choices'][0]['text'].strip()
    return summary
def pre_of_the_preprocessing(final_data) :
  final_of_the_final_data =[]
  for x in final_data :
     subcontext = ""
     nbr_of_tokens = 0
     paragraphes = re.split(r'\. +\n', x)
     paragraphes1 = [] 
     for x in paragraphes :
      paragraphes1.append([count_tokens_nltk(x),x])
     for par in paragraphes1 :
       nbr_of_tokens  = nbr_of_tokens + par[0]
       if(nbr_of_tokens >512) :
         title = titelize_text(subcontext)
         final_of_the_final_data.append({'text':subcontext,'metadata':{'topic':title,'subtopic':x['metadata']['topic']}})
         subcontext=""
         nbr_of_tokens=0
       subcontext = subcontext + par[1]
       if(nbr_of_tokens == 0) :
        nbr_of_tokens  = nbr_of_tokens + par[0]
     title = titelize_text(subcontext)
     final_of_the_final_data.append({'text':subcontext,'metadata':{'topic':title,'subtopic':x['metadata']['topic']}})
  return final_of_the_final_data

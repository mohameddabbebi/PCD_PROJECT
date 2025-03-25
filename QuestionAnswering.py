
import torch
from transformers import AutoModelForQuestionAnswering , AutoTokenizer ,  pipeline
def QuestionAnswer_pipe(question,context) :
  model_name = 'deepset/roberta-base-squad2'
  model = AutoModelForQuestionAnswering.from_pretrained(model_name)
  tokenizer = AutoTokenizer.from_pretrained(model_name)
  input = tokenizer(question,context,return_tensors = "pt")
  output = model(**input)
  return tokenizer.decode(input.input_ids[0,torch.argmax(output.start_logits) : torch.argmax(output.end_logits) + 1])

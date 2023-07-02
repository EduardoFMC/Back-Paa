import os
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

os.chdir(os.path.dirname(__file__))


class DistilbertPokemon():
  def __init__(self):
    self.tokenizer = AutoTokenizer.from_pretrained("M4ycon/distilbert-base-uncased-finetuned-squad")
    self.model = AutoModelForQuestionAnswering.from_pretrained("M4ycon/distilbert-base-uncased-finetuned-squad")

  def answer_with_context(self, question: str, context: str):
    question_answerer = pipeline("question-answering", model=self.model, tokenizer=self.tokenizer)
    answer = question_answerer(question=question, context=context)['answer']
    return {"answer": answer}
  
  def answer_with_big_context(self, question: str):
    context = open('./data/big-context.txt', mode="r", encoding="utf-8").read()
    return self.answer_with_context(question, context)
  
distilbert_pokemon = DistilbertPokemon()

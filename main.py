import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import pipeline

from pretrained_model.distilbert_pokemon import distilbert_pokemon


os.chdir(os.path.dirname(__file__))


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionData(BaseModel):
    question: str

class QuestionWithContextData(BaseModel):
    question: str
    context: str

@app.get("/")
async def root():
    return {"message": "Up and running!"}

@app.post("/pokemon/untrained/question")
async def process_string(data: QuestionData):
    context = open('./pretrained_model/data/big-context.txt', mode="r", encoding="utf-8").read()

    # model_checkpoint = "distilbert-base-uncased-distilled-squad"
    model_checkpoint = "deepset/bert-base-uncased-squad2"
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    model = AutoModelForQuestionAnswering.from_pretrained(model_checkpoint)
    question_answerer = pipeline("question-answering", model=model, tokenizer=tokenizer)
    answer = question_answerer(question=data.question, context=context)['answer']

    return {"answer": answer}

@app.post("/pokemon/trained/question")
async def answer_with_big_context(data: QuestionData):
  return distilbert_pokemon.answer_with_big_context(data.question)

@app.post("/pokemon/trained/question-context")
async def answer_with_context(data: QuestionWithContextData):
  return distilbert_pokemon.answer_with_context(data.question, data.context)

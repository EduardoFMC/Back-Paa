from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Data(BaseModel):
    question: str

@app.post("/")
async def process_string(data: Data):
    with open('context.txt') as f:
        context = f.read()

    tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-uncased-squad2")
    model = AutoModelForQuestionAnswering.from_pretrained("deepset/bert-base-uncased-squad2")
    question_answerer = pipeline("question-answering", model=model, tokenizer=tokenizer)
    output_string = question_answerer(question=data.question, context=context)['answer']

    return {"output_string": output_string}


# 1. Library imports
import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
import random

class Application(BaseModel):
    id: int
    first_name: str
    last_name: str

class Decision(BaseModel):
    id: int
    first_name: str
    last_name: str
    probability: float
    acceptance: bool

app = FastAPI()

@app.post("/applications", response_model=Decision)
async def create_application(application: Application):
    first_name = application.first_name
    last_name = application.last_name
    proba = random.random()
    acceptance = proba > 0.5
    return Decision(id=application.id, first_name=first_name, last_name=last_name, probability=proba, acceptance=acceptance)


@app.get('/')
def index():
    return {'message': 'Hello, stranger'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from rag import RAG

app = FastAPI(title="RAG Document Search API")
rag = RAG(docs_path="documents")

INDEX_PATH = "storage/index"
DOCS_PATH = "documents"

if os.path.exists(INDEX_PATH + "index"):
    rag.index.load(INDEX_PATH)
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.post("/index")
async def build_index():
    try:
        os.makedirs(DOCS_PATH, exist_ok=True)
        os.makedirs("storage", exist_ok=True)
        rag.build(DOCS_PATH)
        rag.index.save(INDEX_PATH)
        return {"status": "ok", "message": "Индекс построен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/ask", response_model=AnswerResponse)
async def asl_question(request: QuestionRequest):
    if rag.index.index.ntotal == 0:
        raise HTTPException(status_code=400, detail="Индекс пуст. Сначало вызовите /index")
    answer = rag.ask(request.question)
    return(AnswerResponse(answer=answer, question = request.question))

@app.get("/status")
async def statis():
    return{
        "status": "ok",
        "chunks_indexed": rag.index.index.ntotal,
        "model": rag.model
    }
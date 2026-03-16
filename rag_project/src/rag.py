import os
import ollama
from embedder import Embedder
from index import FAISSIndex
from loader import load_directory
from chunker import chunk_text

ollama_host = os.getenv("OLLAMA_URL", "http://localhost:11434")
client = ollama.Client(host=ollama_host)

class RAG:
    def __init__(self, docs_path: str, model: str = "llama3.1:8b"):
        self.model = model
        self.embedder = Embedder()
        self.index = FAISSIndex()

    def build(self, docs_path: str):
        files = load_directory(docs_path)
        all_chunks = []

        for filename, text in files.items():
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            print(f"  {filename}: {len(chunks)} чанков")

        vectors = self.embedder.embed(all_chunks)
        self.index.add(all_chunks, vectors)
        print(f'Добавлено: {len(all_chunks)} чанков')

    def ask(self, question: str) -> str:
        vectorised_question = self.embedder.embed_one(question)
        chunks = self.index.search(vectorised_question)
        context = "\n---\n".join(chunks)
        prompt = f"""Ты HR-ассистент. Отвечай на русском языке от третьего лица.
        Ты анализируешь резюме кандидата и отвечаешь на вопросы О НЁМ.

        КОНТЕКСТ ИЗ РЕЗЮМЕ:
        {context}

        ВОПРОС: {question}

        Если информация есть в контексте — ответь кратко и точно.
        Если нет — напиши: "В резюме нет информации по этому вопросу."
        Ответ:"""
        response = client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.message.content
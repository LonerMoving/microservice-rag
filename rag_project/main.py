import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag import RAG

INDEX_PATH = "storage/index"
DOCS_PATH = "documents"

rag = RAG(docs_path=DOCS_PATH)

# Если индекс уже есть — загружаем, иначе строим
if os.path.exists(INDEX_PATH + ".index"):
    print("📂 Загружаю сохранённый индекс...")
    rag.index.load(INDEX_PATH)
    print("✓ Индекс загружен\n")
else:
    print("🔨 Строю индекс...")
    os.makedirs("storage", exist_ok=True)
    rag.build(DOCS_PATH)
    rag.index.save(INDEX_PATH)
    print("✓ Индекс сохранён\n")

print("RAG готов. Задавай вопросы (exit для выхода)\n")

while True:
    question = input("Вопрос: ").strip()
    if question.lower() == "exit":
        break
    if question:
        answer = rag.ask(question)
        print(f"\nОтвет: {answer}\n")
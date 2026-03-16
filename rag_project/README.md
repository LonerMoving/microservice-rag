# RAG Document Search

Система семантического поиска по документам с генерацией ответов на естественном языке.

## Архитектура
```
Документы (PDF/DOCX/TXT)
        ↓
    Chunker         — разбивка текста на куски с перекрытием
        ↓
    Embedder        — векторизация (paraphrase-multilingual-MiniLM-L12-v2)
        ↓
    FAISS Index     — хранение и поиск по векторам
        ↓
    LLM (Ollama)    — генерация ответа на основе найденных чанков
        ↓
    Ответ
```

## Стек

- `sentence-transformers` — мультиязычная векторизация текста
- `faiss-cpu` — векторное хранилище для семантического поиска
- `ollama` — локальный LLM (llama3.1:8b)
- `pymupdf` — парсинг PDF
- `python-docx` — парсинг DOCX

## Установка
```bash
# 1. Клонировать репозиторий
git clone https://github.com/YOUR_USERNAME/rag-document-search
cd rag-document-search

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Установить Ollama и скачать модель
# https://ollama.com/download
ollama pull llama3.1:8b
```

## Использование
```bash
# Положить документы в папку documents/
# Поддерживаются: .pdf, .docx, .txt

python main.py
```

Первый запуск — индекс строится и сохраняется. Последующие запуски — индекс загружается мгновенно.

## Структура проекта
```
rag_project/
├── documents/        — входные документы
├── storage/          — сохранённый FAISS индекс
├── src/
│   ├── loader.py     — загрузка и парсинг файлов
│   ├── chunker.py    — разбивка текста на чанки
│   ├── embedder.py   — векторизация текста
│   ├── index.py      — FAISS индекс
│   └── rag.py        — основная логика RAG
├── api.py            — FastAPI REST API
├── main.py
└── requirements.txt
```

## API

Запуск REST API:
```bash
uvicorn api:app --reload
```

Документация доступна на `http://127.0.0.1:8000/docs`

### Эндпоинты

| Метод | Путь | Описание |
|---|---|---|
| POST | /index | Построить индекс из документов в папке documents/ |
| POST | /ask | Задать вопрос по загруженным документам |
| GET | /status | Статус системы и количество проиндексированных чанков |

### Пример запроса
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Ваш вопрос"}'
```

### Пример ответа
```json
{
  "answer": "Ответ на основе документов",
  "question": "Ваш вопрос"
}
```
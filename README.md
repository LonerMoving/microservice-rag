# Microservice RAG

Микросервисная система семантического поиска по документам с генерацией ответов на естественном языке.

## Архитектура

```
Client (curl / HTTP)
        ↓
C# Gateway (ASP.NET Core)     :8090
        ↓  HTTP proxy
Python RAG Service (FastAPI)  :8000
        ↓              ↓
   FAISS Index      Ollama LLM (host)
        ↓
   Ответ пользователю
```

Два независимых сервиса в Docker-контейнерах:

- **gateway** — ASP.NET Core (.NET 9) принимает запросы и проксирует их в RAG сервис
- **rag** — Python FastAPI сервис реализует полный RAG пайплайн

## Стек

| Сервис | Технологии |
|---|---|
| Gateway | C#, ASP.NET Core (.NET 9), HttpClient, Docker |
| RAG Service | Python, FastAPI, FAISS, sentence-transformers, Ollama |
| Векторизация | paraphrase-multilingual-MiniLM-L12-v2 (50+ языков) |
| LLM | llama3.1:8b через Ollama (локально, без API ключей) |
| Оркестрация | Docker Compose |

## Быстрый старт

### Требования

- [Docker Desktop](https://docker.com/products/docker-desktop)
- [Ollama](https://ollama.com/download) с моделью llama3.1:8b

```bash
# Установить модель (один раз)
ollama pull llama3.1:8b
```

### Запуск

```bash
git clone https://github.com/LonerMoving/microservice-rag
cd microservice-rag

# Запустить оба сервиса одной командой
docker compose up --build
```

Система готова когда в логах появится:
```
rag-1     | INFO: Application startup complete.
gateway-1 | Now listening on: http://[::]:8080
```

### Остановка

```bash
docker compose down
```

## API

Все запросы идут через Gateway на порту **8090**.

### GET /status

Статус системы и количество проиндексированных чанков.

```bash
curl http://localhost:8090/status
```

```json
{
  "status": "ok",
  "chunks_indexed": 25,
  "model": "llama3.1:8b"
}
```

### POST /index

Построить индекс из документов в папке `rag_project/documents/`.
Поддерживаются: `.pdf`, `.docx`, `.txt`

```bash
curl -X POST http://localhost:8090/index
```

```json
{
  "status": "ok",
  "message": "Индекс построен"
}
```

### POST /ask

Задать вопрос по загруженным документам.

```bash
curl -X POST http://localhost:8090/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Ваш вопрос"}'
```

```json
{
  "answer": "Ответ на основе документов",
  "question": "Ваш вопрос"
}
```

## Структура проекта

```
microservice-rag/
├── docker-compose.yml          — оркестрация сервисов
├── gateway/                    — C# ASP.NET Core сервис
│   ├── Dockerfile
│   ├── Program.cs              — маршруты и HTTP proxy логика
│   └── gateway.csproj
└── rag_project/                — Python RAG сервис
    ├── Dockerfile
    ├── api.py                  — FastAPI эндпоинты
    ├── main.py                 — CLI интерфейс
    ├── requirements.txt
    └── src/
        ├── loader.py           — загрузка PDF/DOCX/TXT
        ├── chunker.py          — разбивка текста с overlap
        ├── embedder.py         — мультиязычная векторизация
        ├── index.py            — FAISS индекс + персистентность
        └── rag.py              — RAG пайплайн + Ollama
```

## Ключевые решения

- **Межсервисная коммуникация** — gateway обращается к rag по имени Docker сервиса (`http://rag:8000`), не по localhost
- **Ollama на хосте** — LLM запускается на хост-машине, контейнер обращается через `host.docker.internal:11434`
- **Мультиязычные embeddings** — `paraphrase-multilingual-MiniLM-L12-v2` корректно векторизует русский текст
- **Кэширование индекса** — FAISS индекс строится один раз и сохраняется через volume mount
- **Overlap между чанками** — контекст не теряется на границах кусков текста

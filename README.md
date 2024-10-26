#TODO: test.db is at root and inside app/app/, fix this

```bash
.
├── .venv
├── src/
│   ├── app
│   ├── api/
│   │   ├── v1/
│   │   │   ├── documents.py
│   │   │   ├── general_tasks.py
│   │   │   └── summaries.py
│   │   └── v2/
│   │       └── summaries.py
│   ├── database/
│   │   ├── scaffold/
│   │   │   └── test.db
│   │   └── database.py
│   ├── documents/
│   │   ├── document-1-357-1697.txt
│   │   └── ...
│   ├── logs/
│   │   ├── .gitkeep
│   │   └── celery.log
│   ├── models/
│   │   └── models.py
│   ├── schemas/
│   │   └── schemas.py
│   ├── services/
│   │   ├── v1/
│   │   │   └── summary_services.py
│   │   └── v2/
│   │       └── summary_services.py
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_tasks.py
│   ├── utils/
│   │   ├── v1/
│   │   │   └── utilities.py
│   │   └── websocket.py
│   ├── Dockerfile
│   ├── main.py
│   └── worker.py
├── .env
├── .gitignore
├── docker-compose.yml
├── READEME.md
└── requirements.txt
```
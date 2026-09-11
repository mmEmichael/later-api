# later-api

API for collecting and managing saved links from multiple services.

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- Docker (optional, for PostgreSQL / full stack)

## Setup

1. Copy env file and edit if needed:

```bash
cp .env.example .env
```

2. Install dependencies:

```bash
uv sync
```

3. Start PostgreSQL (example with Docker Compose database only):

```bash
docker compose up db -d
```

Make sure `DATABASE_URL` in `.env` points at that database
(for local runs outside Compose, use `localhost` instead of `db`).

4. Run the API:

```bash
uv run later-api
# or:
uv run uvicorn later_api.main:app --reload
```

API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Docker Compose (API + DB)

```bash
docker compose up --build
```

## Environment variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | SQLAlchemy URL, e.g. `postgresql+psycopg://user:pass@localhost:5432/db` |
| `CORS_ORIGINS` | Comma-separated allowed origins for the frontend |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` | Used by Compose Postgres |

## Tests

```bash
uv run pytest
```

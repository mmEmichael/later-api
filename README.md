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

For local runs (API and Alembic on your machine), use `localhost` in `DATABASE_URL`,
not `db` (that hostname only works inside Docker Compose).

2. Install dependencies:

```bash
uv sync
```

3. Start PostgreSQL (example with Docker Compose database only):

```bash
docker compose up db -d
```

4. Apply database migrations:

```bash
uv run alembic upgrade head
```

5. Run the API:

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

The API container runs `alembic upgrade head` before starting the server.

## Database migrations (Alembic)

Schema changes go through migrations, not `create_all`.

```bash
# apply all migrations
uv run alembic upgrade head

# show current revision
uv run alembic current

# after changing SQLModel tables, generate a new migration (review it!)
uv run alembic revision --autogenerate -m "describe change"
```

If the database already has tables from an older `create_all` setup and matches
the current models, mark it as up to date without re-running SQL:

```bash
uv run alembic stamp head
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
# or with details:
uv run pytest -v
```

Tests use in-memory SQLite (`create_all`) and do not need Postgres, Alembic, or the internet.

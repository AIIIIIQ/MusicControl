# Deployment

## Запуск
```bash
docker compose up --build
```

## Что делает backend entrypoint
1. `alembic upgrade head`
2. `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Переменные
- `DATABASE_URL`
- `MUSIC_DIR`, `COVERS_DIR`, `DOWNLOADS_DIR`
- `NODE_NAME`, `NODE_DESCRIPTION`
- `NODE_ACCESS_TOKEN`, `NODE_REQUIRE_TOKEN`

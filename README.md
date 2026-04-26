# MusicControl (single-owner mode)

MusicControl — локально разворачиваемый сайт для личного музыкального хранилища.

## Ключевая концепция
- Одна установка = один владелец хранилища.
- Локальный UI работает **без логина**.
- Backend автоматически создаёт технического владельца `local_owner`.
- Все сущности (tracks, playlists, share links, friend storages, settings) принадлежат `local_owner`.

## Быстрый старт
```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Swagger: http://localhost:8000/docs

При старте backend автоматически:
1. применяет миграции Alembic,
2. создаёт папки хранения,
3. создаёт `local_owner` и его settings (если отсутствуют).

## Node API защита
- `NODE_REQUIRE_TOKEN=false` — demo режим, node endpoints доступны без токена.
- `NODE_REQUIRE_TOKEN=true` — `/api/node/catalog` и `/api/node/tracks/*` требуют `Authorization: Bearer <NODE_ACCESS_TOKEN>`.
- `/api/node/ping` и `/api/node/info` всегда открыты.

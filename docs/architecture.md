# Архитектура

- Frontend: React + Vite + TypeScript (SPA без login flow).
- Backend: FastAPI + SQLAlchemy.
- DB: PostgreSQL + Alembic.
- Storage: локальные volumes (`music`, `covers`, `downloads`).

## Single-owner поток
1. Startup backend создаёт папки.
2. Проверяет DB connectivity.
3. Создаёт `local_owner` и settings при отсутствии.
4. Все локальные endpoint'ы получают пользователя через `get_local_owner`.

## Интеграции
- Friend nodes через `/api/node/*`.
- При `NODE_REQUIRE_TOKEN=true` защищены catalog/tracks endpoint'ы.

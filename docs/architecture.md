# Архитектура

- Backend: FastAPI (быстрая разработка REST + WebSocket + Swagger).
- Frontend: React + Vite + TypeScript (быстрый MVP с типами).
- DB: PostgreSQL + SQLAlchemy + Alembic (надёжное хранение и миграции).
- Deploy: Docker Compose (повторяемый локальный запуск).

## Компоненты
- `frontend`: SPA интерфейс.
- `backend`: API, auth, upload, stream, share, friend proxy.
- `postgres`: персистентное хранение метаданных.
- `data/*`: локальные volume-папки музыки/обложек/скачиваний.

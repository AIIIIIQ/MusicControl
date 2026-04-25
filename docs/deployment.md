# Deployment

## Команда
`docker compose up --build`

## Переменные окружения
- SECRET_KEY
- DATABASE_URL
- MUSIC_DIR
- COVERS_DIR
- DOWNLOADS_DIR
- NODE_NAME/NODE_DESCRIPTION

## Порты
- 5173 frontend
- 8000 backend
- 5432 postgres

## Volumes
- `pgdata` для БД
- `./data/music`
- `./data/covers`
- `./data/downloads`

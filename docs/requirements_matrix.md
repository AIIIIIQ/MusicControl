# Матрица требований

| ID | Тип | Описание | Приоритет | Компонент | Проверка |
|---|---|---|---|---|---|
| R1 | F | Первичная настройка админа | High | backend/auth + frontend/login | API + UI smoke |
| R2 | F | JWT login | High | backend/auth | POST /api/auth/login |
| R3 | F | Invite creation/use | High | backend/invites/auth | Swagger сценарий |
| R4 | F | Upload track | High | backend/tracks | POST /api/tracks/upload |
| R5 | F | Stream track with Range | High | backend/services/streaming | curl Range |
| R6 | F | Playlist CRUD | Medium | backend/playlists | API checks |
| R7 | F | Share links | High | backend/share-links | public URL test |
| R8 | F | Friend storage check/sync | High | backend/friend_storages | API checks |
| R9 | F | Node public API | High | backend/node_api | remote call |
| R10 | F | Sync-room WS | Medium | backend/sync_rooms | websocket smoke |
| N1 | NF | Docker Compose запуск | High | docker-compose | up --build |
| N2 | NF | Адаптивный UI и темы | Medium | frontend/css/settings | mobile viewport |

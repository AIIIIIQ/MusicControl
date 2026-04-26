# Требования (single-owner)

## Назначение
MusicControl хранит личную музыку владельца, даёт публичные ссылки и подключение каталогов друзей.

## Функциональные требования
1. Локальный интерфейс без авторизации.
2. Автосоздание `local_owner` на старте backend.
3. CRUD треков + stream/download + cover upload/show.
4. CRUD плейлистов + добавление/удаление треков.
5. Публичные share links для track/playlist с TTL и флагами stream/download.
6. Friend storages: check, sync catalog, stream remote, download remote.
7. Настройки владельца (theme).
8. Sync rooms для совместного состояния.
9. `/api/local/status` для дашборда.
10. Node API с опциональной токен-защитой.

## Нефункциональные
- Docker Compose запуск.
- Автоприменение миграций.
- PostgreSQL для метаданных.

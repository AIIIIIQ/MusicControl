# MusicControl MVP

Распределённая сеть личных музыкальных хранилищ (локально разворачиваемый MVP).

## Запуск
```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Swagger: http://localhost:8000/docs

## Быстрый сценарий
1. Откройте `http://localhost:5173`.
2. Нажмите **Первый запуск**, создайте администратора.
3. Загрузите трек на странице **Треки**.
4. Создайте share-link на странице **Ссылки**.
5. Добавьте friend storage на странице **Источники**.

## Seed/demo
- После входа админом можно вызвать `POST /api/dev/seed` в Swagger.
- Добавятся демо-пользователи и демонстрационный source.
- Для своих аудиофайлов положите треки в `./data/music` или загрузите через UI.


### Troubleshooting
- Если кнопка «Отправить» не работает, проверьте `docker compose logs backend` — backend должен быть в состоянии `running`.
- Ошибка `ModuleNotFoundError: No module named 'app'` исправлена в обновлённой версии проекта; пересоберите backend: `docker compose up --build backend`.

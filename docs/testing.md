# Тестирование

## Тест-кейсы (10+)
1. Первый setup создаёт admin.
2. Повторный setup отклоняется.
3. Login выдаёт JWT.
4. Invite создаётся админом.
5. Register-by-invite создаёт user.
6. Upload поддерживает mp3/flac/wav/ogg/m4a.
7. Stream трека с Range возвращает 206.
8. Share-link открывается публично.
9. Friend storage check меняет статус online/offline.
10. Sync catalog заполняет remote cache.
11. Создание sync-room и обновление state.
12. Смена темы через settings.

## Чек-лист
- API отвечает в Swagger.
- UI работает в desktop/mobile.
- Docker volumes сохраняют файлы.

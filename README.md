## Запуск
1. Установить Docker и Docker Compose.
2. Соберите и запустите сервис:
   ```bash
   docker-compose up --build
   ```

## Роуты
1. POST /rates/ - создать тарифы
2. POST /rates/file/ - создать тарифы из файла
3. GET /insurance/ - получить стоимость страхования по указанным фильтрам
4. GET /docs/ - свагер
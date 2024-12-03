## Запуск
1. Установить Docker и Docker Compose и Соберите и запустите сервис:
   ```bash
   docker-compose up --build
   ```
2. ИЛИ
   ```bash
   python -m uvicorn app.main:app --reload
   ```

## Роуты
1. POST /rates/ - создать тарифы
2. POST /rates/file/ - создать тарифы из файла
3. GET /insurance/ - получить стоимость страхования по указанным фильтрам
4. GET /docs/ - свагер
5. PUT /rates/ - изменение тарифа (указывается дата, тип, и изменяемая цена)
6. DELETE /rates/ - удаление тарифа (указывается дата и тип)
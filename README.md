# R4C - Robots for consumers

[Тестовое задание](description.md) по работе с `Django`. Написание `API endpoint`ов по введению в базу новых роботов, получению отчета в `excel`, отправке сообщений по оставленным заявкам.
1. Модели не изменялись
2. Чувствительные данные в `settings.py` не переносились в `.env`
3. Не использовался DRF
4. Валидация данных при помощи библиотеки  `pydentic`
5. Формирование `excel` файла при помощи `openpyxl`
6. Отслеживание новых роботов и отправка сообщений при помощи `django signals` и `django mail`

## Установка

- Развернуть виртуальную среду
- Установить библиотеки:
```bash
pip install -r requiremenets.txt
```
- Выполнить миграции
```bash
python3 manage.py makemigrations
```
- Создать `.env` файл с следующими переменными:
    1. EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
    2. EMAIL_HOST='Ваш SMTP server' `Например smtp.yandex.ru`
    3. EMAIL_PORT=465 `Порт сервера`
    4. EMAIL_USE_SSL=True `Использование порта SSL или TLS`
    5. EMAIL_USE_TLS=False
    6. EMAIL_HOST_USER='email@yandex.ru' `Ваша почта`
    7. EMAIL_HOST_PASSWORD='password' `Созданный сервисом пароль`

## Развертывание с помощью Docker
-убедитесь в наличии .env и requirements.txt в корне проекта, после выполните команду
```bash
docker-compose up --build
```
-Для создания суперпользователя выполните команду, где container_name это название вашего контейнера:
```bash
docker exec -it container_name python manage.py createsuperuser
```

 ## Запуск

 - Запустите приложение
 ```bash
 python3 manage.py runserver
 ```
 - Для проверки данных в `/admin` панеле создайте суперпользователя
```bash
 python3 manage.py createsuperuser
 ```
- При переходе в браузере по [адресу](http://127.0.0.1:8000/admin/) можно проверить данные

 ### Добавление робота в базу
 - POST запрос в `endpoint` `/robots/` (например http://127.0.0.1:8000/robots/).
    Необходимый формат данных: `{"model":"r8","version":"d8","created":"2023-09-25 23:59:59"}`

 ### Получение отчета в excel
  - GET запрос `endpoint` `/robots/report/` (например http://127.0.0.1:8000/robots/report/).
    При запросе начнется скачивание файла

### Оповещение по почте о появлении робота
- POST запрос в `endpoint` `/orders/` (например http://127.0.0.1:8000/orders/).
    Необходимый формат данных: `{"robot_serial": "r8-d8", "customer": "email@yandex.ru"}`
    После создания робота с моделью и версией `"model":"r8","version":"d8"`, аналогичными заявке, на указанную почту отправится письмо с оповещением о появлении робота.
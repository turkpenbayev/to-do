# Сервис "Список задач"

[![Build Status](https://github.com/turkpenbayev/to-do/actions/workflows/django.yml/badge.svg?branch=master)](https://github.com/turkpenbayev/to-do/actions/workflows/django.yml)

```sh
docker-compose up -d --build
```
## Дополнительные задания выполнение

- авторизация, выход, сброс пароля
- отправка email пользвателю при пометки задачи выполнено
- организовать тестирование написанного кода 
- обеспечить автоматическую сборку/тестирование с помощью GitHub CI 
- подготовить docker-compose для запуска всех сервисов проекта одной командой
- по адресу /docs/ страница со Swagger UI и в нём описаны разработанного API. Пример: [http://0.0.0.0:8000/docs/](http://0.0.0.0:8000/docs/)
- реализовать дополнительный сервис, который раз в сутки отправляет статистику по обработанным рассылкам на email
- логирование на всех этапах обработки запросов


**ТЕСТОВЫЕ ДАННЫЕ** 

    email="test@test.com"
    phone="77777777777"
    password="123456"
    token="b99b304a851cbe1ee69232e43cd5eeb55fe669ac"
    
    
**src/app/settings.py** поставте своии данны

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'EMAIL_HOST'
    EMAIL_PORT = 'EMAIL_PORT'
    EMAIL_HOST_USER = 'EMAIL_HOST_USER'
    EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'
    EMAIL_USE_SSL = 'EMAIL_USE_SSL'


**APIs**

![alt apis](https://raw.githubusercontent.com/turkpenbayev/to-do/master/assets/apis.png)


![alt apis](https://raw.githubusercontent.com/turkpenbayev/to-do/master/assets/login.png)


![alt apis](https://raw.githubusercontent.com/turkpenbayev/to-do/master/assets/list.png)


![alt apis](https://raw.githubusercontent.com/turkpenbayev/to-do/master/assets/create.png)

![alt apis](https://raw.githubusercontent.com/turkpenbayev/to-do/master/assets/token.png)


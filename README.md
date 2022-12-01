# Сервис уведомлений

[![Build Status](https://github.com/turkpenbayev/notifications/actions/workflows/django.yml/badge.svg?branch=master)](https://github.com/turkpenbayev/notifications/actions/workflows/django.yml)


```sh
docker-compose up -d --build
```

Документация по api [http://0.0.0.0:9000/docs/](http://0.0.0.0:9000/docs/)


## Дополнительные задания выполнение
1. организовать тестирование написанного кода 
2. обеспечить автоматическую сборку/тестирование с помощью GitLab CI 
3. подготовить docker-compose для запуска всех сервисов проекта одной командой
5. сделать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного API. Пример: [http://0.0.0.0:9000/docs/](http://0.0.0.0:9000/docs/)
6. реализовать администраторский Web UI для управления рассылками и получения статистики по отправленным сообщениям Пример: [http://0.0.0.0:9000/admin/notifications/mailing/](http://0.0.0.0:9000/admin/notifications/mailing/) login:admin, pass: admin
8. реализовать дополнительный сервис, который раз в сутки отправляет статистику по обработанным рассылкам на email notifications.task.notify_reporter
9. удаленный сервис может быть недоступен, долго отвечать на запросы или выдавать некорректные ответы. Необходимо организовать обработку ошибок и откладывание запросов при неуспехе для последующей повторной отправки. Задержки в работе внешнего сервиса никак не должны оказывать влияние на работу сервиса рассылок.
12. обеспечить подробное логирование на всех этапах обработки запросов, чтобы при эксплуатации была возможность найти в логах всю информацию по
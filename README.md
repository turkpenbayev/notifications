# Сервис уведомлений

## Обзор

Этот проект Dockerized, что облегчает его установку и развертывание. Он состоит из нескольких сервисов, включая основное приложение, воркер, а также сервис Redis для обработки фоновых задач.

## Предварительные требования

Убедитесь, что у вас установлен Docker на вашем компьютере. Если нет, вы можете загрузить его [здесь](https://www.docker.com/get-started).

## Начало работы

Следуйте этим шагам, чтобы запустить проект локально.

### 1. Клонирование репозитория

```bash
git clone https://github.com/ваш-юзернейм/ваш-проект.git
cd ваш-проект
```

### 2. Сборка Docker-образов
```bash
docker-compose build
```

### 3. Запуск Docker-контейнеров
```bash
docker-compose up
```
Это запустит сервисы, определенные в вашем файле docker-compose.yml, включая приложение, воркер и Redis.


### 4. Доступ к приложению

- Приложение должно быть доступно по адресу [http://localhost:8000](http://localhost:8000).
- админ [http://localhost:8000/admin](http://localhost:8000/admin).

## Дополнительная информация
- Файл docker-compose.yml определяет сервисы и их конфигурации.

- Файлы ./docker/app/Dockerfile и ./docker/worker/Dockerfile указывают, как строятся образы приложения и воркера.

- Директория ./src/ содержит исходный код вашего проекта.

- Redis используется в качестве зависимости как для приложения, так и для воркера. Убедитесь, что он доступен, прежде чем запускать другие сервисы.

## Настройка
Замените 'ваше_значение_токена' на нужное значение для переменной SERVICE_JWT_TOKEN, и укажите ваш часовой пояс в переменной TIME_ZONE (в данном случае, Asia/Almaty).
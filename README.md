# Тестовое задание на позицию Python Middle в Минздрав

_Почитайте README целиком, в нём много интересного ~~(или не очень)~~ :)_

---

## Задание 
Напишите два микросервиса на FastAPI:

1. Первый микросервис реализует создание и чтение юзеров.

2. Второй микросервис реализует добавление юзеров в друзья. Необходимо учесть момент, что нельзя добавить самого себя в друзья.

В качестве базы данных необходимо использовать PostgreSQL, для отправки запроса на микросервис библиотеку aiohttp. В качестве ORM нужно взять SQLAlchemy.

Микросервисы следует обернуть в Docker-контейнеры, которые должны запускаться командой docker-compose up

При написании микросервисов использовать паттерн Луковой архитектуры

Требуется предусмотреть логгирование методов эндпоинтов с помощью любого удобного инструмента

Все сомнительные моменты учесть на свое усмотрение, срок выполнения — один день.

---

## Запуск
Микросервисы обёрнуты в Docker контейнеры и запускаются через docker compose. 
1. Нужно выполнить команду `docker compose up`
<br/><br/>
2. После того как контейнеры запущены, нужно применить миграции\
`docker exec fastapi_friends_service alembic upgrade head`\
`docker exec fastapi_users_service alembic upgrade head`\
Это нужно делать только при первом запуске или после изменения таблиц в БД.
<br/><br/>
3. Теперь микросервисы работают и доступны на локальной машине\
Документация микросервиса пользователей: http://127.0.0.1:8001/api/docs \
Документация микросервиса друзей: http://127.0.0.1:8002/api/docs \
_Также доступен redoc_

---

## Описание
Проект состоит из двух микросервисов на FastAPI:
- `users_service` - Микросервис пользователей
- `friends_service` - Микросервис друзей

Для микросервисов написана документация, лучше всего её смотреть через redoc.

### Микросервис пользователей
В микросервисе пользователей можно создавать пользователей, получать всех пользователей, 
получать пользователя по его id и проверять существует ли пользователь по id

**Модель пользователя**
* `id` - уникальный id пользователя
* `username` - уникальный логин
* `first_name` - имя
* `second_name` - фамилия
* `birthday` - дата рождения
* `created_at` - дата и время создания

### Микросервис друзей
В микросервисе друзей можно создавать дружеские связи между пользователями, получать все 
дружеские связи пользователя и просматривать конкретную связь по её id.

Между двумя пользователями может быть только одна дружеская связь. А также нельзя 
создать дружескую связь с самим собой.

Микросервис друзей обращается к микросервису пользователей по протоколу http чтобы 
узнать существуют ли пользователи, с которыми проводятся операции 

**Модель дружеской связи**
* `id` - уникальный id дружбы
* `initiator_id` - id пользователя, который инициирует дружбу
* `target_id` - id пользователя, с котором создаётся дружба
* `tag` - тэг дружбы. Например: "Лучший друг", "Родственник" и т.д.
* `created_at` - дата и время создания дружбы

---

## Переменные среды

**! В рамках тестового задания все переменные среды прописаны сразу 
в `docker-compose.yml` чтобы было проще запустить проект !**

### Микросервис пользователей

* `POSTGRES_DB` - название БД
* `POSTGRES_USER` - пользователь БД
* `POSTGRES_PASSWORD` - пароль БД
* `POSTGRES_HOST` - хост БД (опционально)
* `POSTGRES_PORT` - порт БД (опционально)

### Микросервис друзей

* `POSTGRES_DB` - название БД
* `POSTGRES_USER` - пользователь БД
* `POSTGRES_PASSWORD` - пароль БД
* `POSTGRES_HOST` - хост БД (опционально)
* `POSTGRES_PORT` - порт БД (опционально)
* `USERS_SERVICE_URL` - ссылка на сервис пользователей

---

## Архитектура
Для реализации микросервисов использовалась луковая/слоистая архитектура.

### Описание
Доменная модель расположена в директории `core/entities`. 
Там лежат бизнес-модели, которые передаются между слоями.

Доменные сервисы расположены в `core/repositories`. 
Это интерфейсы для взаимодействия с бизнес-моделями и их реализации

Бизнес-логика расположена в `core/services`. 
В сервисы внедряются репозитории и уже через сервисы происходит работа со всеми данными, реализуется бизнес-логика

Инфраструктурный слой расположен в директории `api`. 
Там уже идут эндпоинты и схемы API. В каком-то роде эти схемы играют роль DTO

### Вывод
Таким образом мы получаем сервис разбитый на независимые слои и в случае необходимости любой слой можно заменить.
Такой сервис будет удобно расширять и поддерживать

P.S. Это мой первый опыт проектирования архитектуры с нуля самостоятельно, раньше доводилось работать только с 
готовыми архитектурами, и я не уверен, что всё сделал правильно. Но зато это был интересный и полезный опыт :)

---

## Логирование
Для логов сделал JSON логер, правда не хватило времени довести его до ума. 
По-хорошему в него надо добавить обработку ошибок и тела запроса и ответа.

В директории `utils` лежат 2 файла: `logger.py` и `logger_middleware.py`. 
В них соответственно кастомный JSON обработчик логов и Middleware, который оставляет лог на каждый запрос

Отключать стандартный логер FastAPI и писать логи в файл не стал.

С логированием у меня особо опыта не было, так что не уверен что и как надо логировать.
В логи вынес важную на мой взгляд информацию (_ещё должны были быть ошибки и тела, но не успелось_)

---

## Что ещё можно сделать

Не всё успелось за сутки, так что вот что я бы ещё сделал:

1. Тесты\
Я бы покрыл микросервисы тестами. Сейчас изучаю тестирование и уже прочувствовал всю прелесть тестов,
когда можно без боязни менять код и выкатывать обновление на прод
</br></br>
2. API Gateway с авторизацией\
Сервис без авторизации выглядит грустно, но, к сожалению, времени на это не хватило.
</br></br>
3. CI/CD\
Это можно считать как дополнение к тестам) CI/CD это всегда удобно и облегчает разработку

---

## Немного обо мне
Я выбрал задание для Middle, но пока не могу назвать себя разработчиком Middle уровня,
сейчас я оцениваю себя на Junior+. Так что претендую скорее на позицию Junior, а не Middle, и желательно чтобы
у меня был ментор/наставник

Взял задание посложнее, потому что это был для меня как некий вызов: справлюсь ли с такой задачей. 
И я считаю, что вышло вполне неплохо.

Спасибо за интересное тестовое задание. Ожидаю от Вас фидбек по получившемуся проекту и надеюсь, что мы в 
скором времени сможем поработать вместе :)

---

## Контакты

Telegram: @printeromg\
Почта: kitaev.gregory@gmail.com\
Телефон: +7 (993) 412-63-87

(Telegram предпочтительно)

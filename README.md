# BlogAPI

## О проекте
BlogAPI — это мощное решение для управления постами, комментариями и лайками в блоге. Проект разработан с использованием Django и предоставляет безопасную аутентификацию через JWT-токены.  

---

## Обзор
Данный проект представляет собой блог на основе Django, предоставляющий API для управления постами, комментариями, лайками и аутентификацией с использованием JWT-токенов.

---

## Технологии
- Python 3.12+
- Django 5.1.6+
- Django REST Framework
- Redis (для кеширования)
- drf-yasg (Swagger для документации API)

---

## Установка

### Требования
- Python 3.12+
- Django 5.1.6+
- Redis (для кеширования)

### Шаги по установке

1. Клонируйте репозиторий:
   ```bash
   git clone <repository_url>
   cd blog_project
   ```
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/MacOS
   .\venv\Scripts\activate  # Для Windows
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Примените миграции базы данных:
   ```bash
   python manage.py migrate
   ```
5. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```
6. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```
7. Откройте приложение по адресу [http://localhost:8000](http://localhost:8000)

---

## Основные зависимости
- asgiref==3.8.1
- colorama==0.4.6
- Django==5.1.6
- django-filter==25.1
- django-redis==5.4.0
- djangorestframework==3.15.2
- djangorestframework_simplejwt==5.4.0
- drf-yasg==1.21.10
- inflection==0.5.1
- iniconfig==2.0.0
- packaging==24.2
- pluggy==1.5.0
- PyJWT==2.10.1
- pytest==8.3.4
- pytest-django==4.10.0
- pytz==2025.1
- PyYAML==6.0.2
- redis==5.2.1
- sqlparse==0.5.3
- tzdata==2025.1
- uritemplate==4.1.1

---

## Конфигурация

### Переменные окружения
Создайте файл `.env` в корневой директории и добавьте следующие параметры:

```
SECRET_KEY=<your_django_secret_key>
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://127.0.0.1:6379/1
```

---

## Функциональность
- **CRUD-операции:** Создание, чтение, обновление и удаление постов и комментариев
- **Лайки/дизлайки:** Пользователи могут ставить лайки или дизлайки к постам
- **JWT-аутентификация:** Безопасная аутентификация для API
- **Пагинация:** Пагинация с размером страницы по умолчанию = 5
- **Кеширование:** Использование Redis для оптимизации производительности

---

## API Эндпоинты

### Посты
- **GET** `/api/posts/` — Список всех постов
- **POST** `/api/posts/` — Создать новый пост
- **GET** `/api/post/<int:pk>/` — Получить детали поста
- **PUT** `/api/post_edit/<int:pk>/` — Редактировать пост
- **DELETE** `/api/post_edit/<int:pk>/` — Удалить пост

### Комментарии
- **GET** `/api/post/<int:pk>/comments/` — Список комментариев к посту
- **POST** `/api/post/<int:pk>/comments/` — Добавить комментарий
- **PUT** `/api/post/<int:post_id>/comment_edit/<int:pk>/` — Редактировать комментарий
- **DELETE** `/api/post/<int:post_id>/comment_edit/<int:pk>/` — Удалить комментарий

### Лайки
- **POST** `/api/post/<int:pk>/like/` — Поставить или убрать лайк/дизлайк
- **GET** `/api/post/<int:pk>/likes_count/` — Получить количество лайков и дизлайков

### Аутентификация
- **POST** `/api/token/` — Получить JWT-токены
- **POST** `/api/token/refresh/` — Обновить JWT-токен

---

## Swagger Документация

Для просмотра документации API перейдите по ссылке:
```
http://localhost:8000/swagger/
```

---

## Админ-панель

Для доступа в админ-панель:
```
http://localhost:8000/admin/
```

---

## Запуск тестов

```bash
python manage.py test
```

---

## Проблемы с миграциями

Если возникли проблемы с миграциями:
```bash
python manage.py makemigrations
python manage.py migrate --fake
```

---

## Будущие улучшения
- Реализация детализированного логирования
- Добавление полного покрытия юнит-тестами и интеграционными тестами
- Оптимизация стратегий кеширования для популярных эндпоинтов

---

## Контакты
- GitHub: [Cinzanos](https://github.com/Cinzanos)
- Email: cinzanos123@gmail.com


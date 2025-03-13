from django.apps import AppConfig

class BlogConfig(AppConfig):
    """
    Конфигурация приложения Blog.

    Этот класс настраивает приложение blog в Django.
    В нем указывается название приложения и дефолтный тип авто-поля для моделей.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

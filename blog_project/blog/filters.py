import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    """
    Фильтрация постов по времени создания, категории и рейтингу.

    Этот фильтр позволяет фильтровать посты по следующим критериям:
    - time_create: фильтрация по времени создания (больше или равно заданной дате)
    - category: фильтрация по названию категории (с использованием подстрочного поиска)
    - rating: фильтрация по рейтингу
    """
    time_create = django_filters.DateFilter(field_name="time_create", lookup_expr="gte")
    category = django_filters.CharFilter(field_name="category__name", lookup_expr='icontains')
    rating = django_filters.NumberFilter(field_name="rating")

    class Meta:
        model = Post
        fields = ['time_create', 'category', 'rating']


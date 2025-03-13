from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import UserRateThrottle

from blog.filters import PostFilter
from blog.models import Post, Comment, Like
from blog.permissions import IsAuthorOrReadOnly
from blog.serializers import PostSerializer, CommentSerializer, LikeSerializer, PostLikeCountSerializer


class PostAPIList(generics.ListCreateAPIView):
    """
    Представление для списка постов и создания нового поста.

    Этот класс обрабатывает два основных действия:
    - Получение списка постов с фильтрацией, сортировкой и кешированием.
    - Создание нового поста с привязкой текущего пользователя как автора.
    """
    queryset = Post.objects.all().select_related('author', 'category').prefetch_related('likes').annotate(
        like_count=Count('likes', filter=Q(likes__is_like=True)),
        dislike_count=Count('likes', filter=Q(likes__is_like=False)),
        rating=F('like_count') - F('dislike_count')
    )
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'content']
    ordering_fields = ['time_create', 'title', 'rating']
    ordering = ['-time_create']

    def perform_create(self, serializer):
        """
        Сохраняет новый пост с автором, назначенным текущим пользователем.
        """
        serializer.save(author=self.request.user)

    @method_decorator(cache_page(60 * 10))  # Кешируем на 10 минут
    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запросы и возвращает список постов с кешированием.
        """
        return super().get(request, *args, **kwargs)


class PostAPIDetail(generics.RetrieveAPIView):
    """
    Представление для подробной информации о посте.

    Этот класс обрабатывает запросы для получения данных о конкретном посте.
    Используется кеширование для ускорения ответа на часто запрашиваемые посты.
    """
    queryset = Post.objects.all().select_related('author', 'category').prefetch_related('likes')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    throttle_classes = [UserRateThrottle]

    def retrieve(self, request, *args, **kwargs):
        """
        Возвращает подробную информацию о посте.
        Если данные уже в кеше, возвращает их из кеша.
        """
        post_id = kwargs['pk']
        cache_key = f'post_{post_id}'

        # Проверяем, есть ли пост в кеше
        post_data = cache.get(cache_key)
        if post_data:
            return Response(post_data)  # Если есть в кеше, сразу отдаем

        # Если нет в кеше, берем из БД
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=600)  # Кешируем на 10 минут

        return response


class PostAPIUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для обновления или удаления поста.

    Этот класс обрабатывает запросы на редактирование и удаление постов.
    После обновления или удаления поста соответствующие данные удаляются из кеша.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_update(self, serializer):
        """
        Удаляет кеш для измененного поста после обновления.
        """
        instance = serializer.save()
        cache.delete(f'post_{instance.id}')  # Удаляем кеш только для измененного поста

    def perform_destroy(self, instance):
        """
        Удаляет кеш для удаленного поста и сам пост из базы данных.
        """
        cache.delete(f'post_{instance.id}')  # Удаляем кеш только для удаленного поста
        instance.delete()


class CommentListCreate(generics.ListCreateAPIView):
    """
    Представление для списка комментариев и создания нового комментария.

    Этот класс обрабатывает запросы для получения комментариев к посту и создания новых комментариев.
    При создании комментария автором будет текущий авторизованный пользователь.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        """
        Возвращает комментарии для конкретного поста, проверяя его существование.
        """
        post_id = self.kwargs['pk']
        if not Post.objects.filter(id=post_id).exists():
            raise NotFound("Такого поста не существует.")
        return Comment.objects.filter(post_id=post_id).select_related('author').order_by('-created_at')

    def perform_create(self, serializer):
        """
        Сохраняет новый комментарий с текущим автором.
        """
        serializer.save(author=self.request.user)


class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления или удаления комментария.

    Этот класс обрабатывает запросы для работы с отдельными комментариями.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]  # Только автор может редактировать/удалять
    authentication_classes = [JWTAuthentication]


class LikeAPIView(generics.CreateAPIView):
    """
    Представление для добавления или обновления лайков на постах.

    Этот класс обрабатывает запросы для создания лайков или дизлайков.
    Пользователь может поставить лайк или дизлайк для поста.
    """
    queryset = Like.objects.all().select_related('user', 'post')  # Оптимизация
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        """
        Добавляет или обновляет лайк для указанного поста.
        """
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        user = self.request.user
        is_like = self.request.data.get('is_like')

        if is_like is None:
            return Response({"error": "Поле 'is_like' обязательно"}, status=status.HTTP_400_BAD_REQUEST)

        # Используем update_or_create для упрощения логики
        obj, created = Like.objects.update_or_create(
            user=user, post=post,
            defaults={"is_like": is_like}
        )
        return Response(
            {"message": "Лайк обновлен" if not created else "Лайк добавлен"},
            status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED
        )


class PostLikeCountAPIView(generics.RetrieveAPIView):
    """
    Представление для получения количества лайков и дизлайков для поста.

    Этот класс обрабатывает запросы на получение статистики лайков и дизлайков для конкретного поста.
    """
    queryset = Post.objects.all().annotate(
        like_count=Count('likes', filter=Q(likes__is_like=True)),
        dislike_count=Count('likes', filter=Q(likes__is_like=False)),
        rating=F('like_count') - F('dislike_count')
    )
    serializer_class = PostLikeCountSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

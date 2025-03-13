from rest_framework import serializers
from blog.models import *

class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.

    Этот сериализатор используется для отображения информации о категории.
    Он включает только поле "name", которое представляет собой название категории.
    """
    class Meta:
        model = Category
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.

    Этот сериализатор используется для отображения и создания постов.
    Включает такие поля как категория, автор, количество лайков и дизлайков, и рейтинг.
    Поля "views", "like_count", "dislike_count" и "rating" доступны только для чтения.
    """
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = serializers.StringRelatedField()
    like_count = serializers.IntegerField(read_only=True)
    dislike_count = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField(read_only=True)  # Для отображения рейтинга

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['views', 'like_count', 'dislike_count', 'rating']


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.

    Этот сериализатор используется для отображения информации о комментариях,
    включая имя автора, и другие поля комментария.
    """
    author = serializers.StringRelatedField(read_only=True)  # Отображаем имя автора

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Like.

    Этот сериализатор используется для отображения и создания лайков или дизлайков
    на постах. Пользователь и пост только для чтения.
    """
    is_like = serializers.ChoiceField(choices=[(True, "Like"), (False, "Dislike")])

    class Meta:
        model = Like
        fields = ['user', 'post', 'is_like']
        read_only_fields = ['user', 'post']


class PostLikeCountSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подсчета лайков и дизлайков на постах.

    Этот сериализатор используется для отображения количества лайков и дизлайков
    для каждого поста. Данные собираются динамически через фильтрацию лайков.
    """
    like_count = serializers.IntegerField(read_only=True)
    dislike_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'like_count', 'dislike_count']

    def to_representation(self, instance):
        """
        Переопределённый метод для сериализации данных.

        В этом методе добавляется подсчёт лайков и дизлайков для поста.
        Сначала вызывается стандартная сериализация объекта, затем добавляются два дополнительных поля:
        - `like_count`: количество лайков.
        - `dislike_count`: количество дизлайков.

        Аргументы:
        - instance: Экземпляр объекта модели, который будет сериализован.

        Возвращаемое значение:
        - Возвращает сериализованные данные объекта с дополнительной информацией о лайках и дизлайках.
        """
        representation = super().to_representation(instance)
        # Подсчитываем лайки и дизлайки
        representation['like_count'] = instance.likes.filter(is_like=True).count()
        representation['dislike_count'] = instance.likes.filter(is_like=False).count()
        return representation

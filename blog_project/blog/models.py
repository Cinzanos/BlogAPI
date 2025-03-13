from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    """
    Модель поста в блоге.

    Позволяет:
    - Хранить заголовок, контент, дату создания и обновления.
    - Отображать количество лайков и дизлайков.
    - Вычислять рейтинг на основе лайков и дизлайков.
    """
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=255, blank=True)
    time_create = models.DateField(auto_now_add=True)
    time_update = models.DateField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        """Возвращает заголовок поста."""
        return self.title

    def increase_views(self):
        """Увеличивает количество просмотров поста на 1."""
        self.views += 1
        self.save()

    def like_count(self):
        """Подсчитывает количество лайков поста."""
        return self.likes.filter(is_like=True).count()

    def dislike_count(self):
        """Подсчитывает количество дизлайков поста."""
        return self.likes.filter(is_like=False).count()

    def rating(self):
        """
        Вычисляет рейтинг поста как разницу между количеством лайков и дизлайков.
        """
        return self.like_count() - self.dislike_count()

class Category(models.Model):
    """
    Модель категории постов.

    Позволяет:
    - Хранить название категории.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """Возвращает название категории."""
        return self.name

class Comment(models.Model):
    """
    Модель комментария к посту.

    Позволяет:
    - Хранить текст комментария, автора и дату создания.
    """
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Возвращает строковое представление комментария."""
        return f"Comment by {self.author.username} on {self.post.title}"

class Like(models.Model):
    """
    Модель лайка/дизлайка для поста.

    Позволяет:
    - Хранить информацию о том, какой пользователь лайкнул/дизлайкнул пост.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    is_like = models.BooleanField()  # True - лайк, False - дизлайк

    class Meta:
        unique_together = ('user', 'post')  # Ограничиваем, чтобы пользователь не мог лайкать пост несколько раз

    def __str__(self):
        """Возвращает строковое представление лайка/дизлайка."""
        return f"{self.user} {'liked' if self.is_like else 'disliked'} {self.post.title}"

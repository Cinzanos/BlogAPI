from django.contrib import admin
from django import forms

from .models import Post, Category, Comment, Like

class PostAdmin(admin.ModelAdmin):
    """
    Управление постами в админке.

    Позволяет:
    - Просматривать, фильтровать, искать и редактировать посты.
    - Считывать и отображать количество лайков, дизлайков и рейтинг.
    """
    list_display = ('title', 'author', 'category', 'time_create', 'views', 'like_count', 'dislike_count', 'rating')
    list_filter = ('category', 'author')
    search_fields = ('title', 'content')
    ordering = ('-time_create',)

    def like_count(self, obj):
        """Подсчитывает количество лайков для поста."""
        return obj.like_count()

    def dislike_count(self, obj):
        """Подсчитывает количество дизлайков для поста."""
        return obj.dislike_count()

    def rating(self, obj):
        """Вычисляет рейтинг поста на основе лайков и дизлайков."""
        return obj.rating()

class CategoryAdmin(admin.ModelAdmin):
    """
    Управление категориями в админке.

    Позволяет:
    - Просматривать и редактировать категории.
    """
    list_display = ('name',)
    search_fields = ('name',)

class CommentAdmin(admin.ModelAdmin):
    """
    Управление комментариями к постам.

    Позволяет:
    - Просматривать, фильтровать и искать комментарии.
    """
    list_display = ('post', 'author', 'content', 'created_at')
    list_filter = ('post', 'author', 'created_at')
    search_fields = ('content',)

class LikeForm(forms.ModelForm):
    """Форма для лайков и дизлайков."""
    class Meta:
        model = Like
        fields = ['user', 'post', 'is_like']
        widgets = {
            'is_like': forms.RadioSelect(choices=[(True, 'Like'), (False, 'Dislike')])
        }

class LikeAdmin(admin.ModelAdmin):
    """
    Управление лайками и дизлайками в админке.

    Позволяет:
    - Управлять лайками пользователей.
    """
    form = LikeForm
    list_display = ('user', 'post', 'is_like')
    list_filter = ('is_like',)
    search_fields = ('user__username', 'post__title')
    list_editable = ['is_like']

# Регистрация моделей в админке
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)

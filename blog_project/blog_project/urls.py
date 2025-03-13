"""
URL configuration for blog_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from blog.views import *  # Импортируем представления из приложения blog


# Настройка схемы Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="API documentation for the blog project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myblogapi.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Разрешаем доступ к документации для всех
    authentication_classes=[JWTAuthentication],
)


# URL-пути для проекта
urlpatterns = [
    # Путь к административной панели Django
    path('admin/', admin.site.urls),

    # Путь для получения списка всех постов
    path('api/posts/', PostAPIList.as_view()),

    # Путь для редактирования и удаления поста по ID
    path('api/post_edit/<int:pk>/', PostAPIUpdateDelete.as_view()),

    # Путь для получения подробной информации о посте по ID
    path('api/post/<int:pk>/', PostAPIDetail.as_view()),

    # Путь для получения комментариев к посту и создания нового комментария
    path('api/post/<int:pk>/comments/', CommentListCreate.as_view()),

    # Путь для редактирования или удаления комментария по ID поста и ID комментария
    path('api/post/<int:post_id>/comment_edit/<int:pk>/', CommentRetrieveUpdateDestroy.as_view()),

    # Путь для постановки лайка или дизлайка на пост
    path('api/post/<int:pk>/like/', LikeAPIView.as_view()),

    # Путь для получения количества лайков и дизлайков у поста
    path('api/post/<int:pk>/likes_count/', PostLikeCountAPIView.as_view()),

    # Путь для получения токена (JWT) при аутентификации
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Путь для обновления токена (JWT)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Путь для документации Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

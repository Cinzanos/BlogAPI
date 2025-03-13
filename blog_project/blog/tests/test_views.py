import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from blog.models import Post, Comment, Like, Category


@pytest.fixture
def create_user():
    """
    Фикстура создания пользователя.

    Создает и возвращает нового пользователя с логином 'testuser' и паролем 'password'.
    Этот пользователь используется для аутентификации в тестах.
    """
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def create_category():
    """
    Фикстура создания категории.

    Создает и возвращает категорию с названием 'Test Category'.
    Эта категория используется при создании постов в тестах.
    """
    return Category.objects.create(name='Test Category')


@pytest.fixture
def create_post(create_user, create_category):
    """
    Фикстура создания поста.

    Создает и возвращает пост с заголовком 'Test Post', контентом 'Test content',
    автором, созданным через фикстуру create_user, и категорией, созданной через create_category.
    """
    return Post.objects.create(title='Test Post', content='Test content', author=create_user, category=create_category)


@pytest.fixture
def create_comment(create_user, create_post):
    """
    Фикстура создания комментария.

    Создает и возвращает комментарий с контентом 'Test comment', автором, созданным через фикстуру create_user,
    и привязанным к посту, созданному через фикстуру create_post.
    """
    return Comment.objects.create(post=create_post, author=create_user, content="Test comment")


@pytest.fixture
def auth_client(create_user):
    """
    Фикстура аутентифицированного клиента.

    Создает и возвращает экземпляр APIClient, аутентифицированный под пользователем, созданным через create_user.
    Этот клиент используется для выполнения запросов с авторизацией в тестах.
    """
    client = APIClient()
    client.force_authenticate(user=create_user)
    return client


@pytest.mark.django_db
def test_post_list(auth_client, create_post):
    """
    Тестирование списка постов.

    Проверяет, что запрос GET на список постов возвращает успешный ответ (200 OK),
    что в ответе присутствует ключ 'results' и что хотя бы один пост есть в списке.
    """
    response = auth_client.get('/api/posts/')
    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data
    assert len(response.data['results']) > 0  # Проверяем, что хотя бы 1 пост есть


@pytest.mark.django_db
def test_post_create(auth_client, create_category):
    """
    Тестирование создания поста.

    Проверяет, что POST-запрос на создание поста возвращает успешный ответ (201 Created),
    и что созданный пост имеет правильные данные.
    """
    data = {
        'title': 'New Post',
        'content': 'Content of the new post',
        'category': create_category.id
    }
    response = auth_client.post('/api/posts/', data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'New Post'


@pytest.mark.django_db
def test_post_detail(auth_client, create_post):
    """
    Тестирование получения детального поста.

    Проверяет, что запрос GET на детальную информацию о посте возвращает успешный ответ (200 OK),
    и что данные поста соответствуют ожидаемым.
    """
    response = auth_client.get(f'/api/post/{create_post.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Test Post'


@pytest.mark.django_db
def test_post_update(auth_client, create_post, create_category):
    """
    Тестирование обновления поста.

    Проверяет, что PUT-запрос на обновление поста возвращает успешный ответ (200 OK),
    и что обновленные данные соответствуют ожидаемым.
    """
    data = {
        'title': 'Updated Title',
        'content': 'Updated Content',
        'category': create_category.id
    }
    response = auth_client.put(f'/api/post_edit/{create_post.id}/', data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Updated Title'


@pytest.mark.django_db
def test_post_delete(auth_client, create_post):
    """
    Тестирование удаления поста.

    Проверяет, что DELETE-запрос на удаление поста возвращает успешный ответ (204 No Content),
    и что пост действительно удален из базы данных.
    """
    response = auth_client.delete(f'/api/post_edit/{create_post.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Post.objects.filter(id=create_post.id).count() == 0


@pytest.mark.django_db
def test_comment_create(auth_client, create_post, create_user):
    """
    Тестирование создания комментария.

    Проверяет, что POST-запрос на создание комментария возвращает успешный ответ (201 Created).
    """
    data = {"content": "Новый комментарий", "author": create_user.id, "post": create_post.id}
    response = auth_client.post(f'/api/post/{create_post.id}/comments/', data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_comment_list(auth_client, create_post):
    """
    Тестирование получения списка комментариев.

    Проверяет, что GET-запрос на получение списка комментариев возвращает успешный ответ (200 OK),
    что в ответе присутствует ключ 'results', и что количество комментариев равно 1.
    """
    Comment.objects.create(post=create_post, author=create_post.author, content="Тестовый комментарий")

    response = auth_client.get(f'/api/post/{create_post.id}/comments/')
    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data  # Проверяем, что данные возвращаются в виде пагинированного списка
    assert len(response.data['results']) == 1  # Ожидаем 1 комментарий


@pytest.mark.django_db
def test_comment_update(auth_client, create_comment):
    """
    Тестирование обновления комментария.

    Проверяет, что PUT-запрос на обновление комментария возвращает успешный ответ (200 OK).
    """
    data = {
        "content": "Обновленный комментарий",
        "post": create_comment.post.id  # ✅ Добавляем ID поста
    }
    response = auth_client.put(
        f'/api/post/{create_comment.post.id}/comment_edit/{create_comment.id}/',
        data, format='json'
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_comment_delete(auth_client, create_comment):
    """
    Тестирование удаления комментария.

    Проверяет, что DELETE-запрос на удаление комментария возвращает успешный ответ (204 No Content),
    и что комментарий действительно удален из базы данных.
    """
    response = auth_client.delete(
        f'/api/post/{create_comment.post.id}/comment_edit/{create_comment.id}/'
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Comment.objects.filter(id=create_comment.id).exists()  # Проверяем, что комментарий удалён


@pytest.mark.django_db
def test_like_post(auth_client, create_post):
    """
    Тестирование лайка поста.

    Проверяет, что POST-запрос на лайк поста возвращает успешный ответ (201 Created или 200 OK),
    и что лайк был успешно добавлен.
    """
    data = {'is_like': True}
    response = auth_client.post(f'/api/post/{create_post.id}/like/', data, format='json')
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK]
    assert Like.objects.filter(post=create_post).count() == 1


@pytest.mark.django_db
def test_dislike_post(auth_client, create_post):
    """
    Тестирование дизлайка поста.

    Проверяет, что POST-запрос на дизлайк поста возвращает успешный ответ (201 Created или 200 OK),
    и что дизлайк был успешно добавлен.
    """
    data = {'is_like': False}
    response = auth_client.post(f'/api/post/{create_post.id}/like/', data, format='json')
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK]
    assert Like.objects.filter(post=create_post).count() == 1


@pytest.mark.django_db
def test_post_like_count(auth_client, create_post, create_user):
    """
    Тестирование подсчета лайков.

    Проверяет, что GET-запрос на получение количества лайков для поста возвращает правильные значения
    для лайков и дизлайков.
    """
    Like.objects.create(user=create_user, post=create_post, is_like=True)
    response = auth_client.get(f'/api/post/{create_post.id}/likes_count/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['like_count'] == 1
    assert response.data['dislike_count'] == 0


@pytest.mark.django_db
def test_jwt_auth():
    """
    Тестирование получения JWT-токена.

    Проверяет, что POST-запрос на получение JWT-токена с правильными данными возвращает успешный ответ (200 OK),
    и что в ответе присутствуют токены 'access' и 'refresh'.
    """
    user = User.objects.create_user(username='jwtuser', password='password')
    client = APIClient()
    response = client.post('/api/token/', {'username': 'jwtuser', 'password': 'password'}, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data



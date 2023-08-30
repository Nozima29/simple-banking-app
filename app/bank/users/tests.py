import pytest
from users.models import AuthUser

# Create your tests here.


@pytest.fixture
def create_user(django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def create_auth_user():
    def make_user(user):
        return AuthUser.objects.create(user=user)
    return make_user


@pytest.mark.django_db
def test_user(create_user):
    user = create_user(username="test_user", password="123444")
    assert user.username == "test_user"


@pytest.mark.django_db
def test_auth_user(create_auth_user, create_user):
    user = create_user(username="test_user", password="123444")
    auth_user = create_auth_user(user)
    assert auth_user.user == user

import pytest

from tests.testapp.models import TestUser


@pytest.fixture
def user():
    user = TestUser.objects.create(
        test_email="billie@eilish.com",
        test_phone="1234567890",
    )
    yield user


@pytest.mark.django_db
def test_user(user):
    assert user.test_email == "billie@eilish.com"

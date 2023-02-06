from account.managers import UserManager
from django.contrib.auth import get_user_model
from pytest import fixture, mark, raises


@fixture
def user_manager() -> UserManager:
    user_manager = UserManager()
    user_manager.model = get_user_model()
    return user_manager


@mark.django_db
class TestUserManager:
    email = 'test@run.com'
    password = 'testrun321'

    def test_create_user_success(self, user_manager: UserManager):
        user = user_manager.create_user(
            email=self.email, password=self.password
        )

        assert user is not None

    def test_create_user_raise_value_error(self, user_manager):
        kwargs = {'email': '', 'password': self.password}
        with raises(ValueError):
            user_manager.create_user(**kwargs)

    def test_create_super_user_success(self, user_manager: UserManager):
        user = user_manager.create_superuser(
            email=self.email, password=self.password
        )

        assert user is not None

    @mark.parametrize(
        'extra_field',
        [{'is_active': False}, {'is_staff': False}, {'is_superuser': False}],
    )
    def test_create_super_user_raise_value_error(
        self, extra_field: dict, user_manager: UserManager
    ):
        kwargs = {
            'email': self.email,
            'password': self.password,
            **extra_field,
        }
        with raises(ValueError):
            user_manager.create_superuser(**kwargs)

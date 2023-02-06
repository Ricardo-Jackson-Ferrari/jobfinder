from django.contrib.auth import get_user_model
from model_bakery import baker
from pytest import fixture, mark


@fixture
def common_user(db):
    return baker.make(get_user_model())

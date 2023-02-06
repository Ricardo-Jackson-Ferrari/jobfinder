from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from model_bakery import baker
from pytest import fixture


@fixture
def common_user(db):
    return baker.make(get_user_model())


@fixture
def candidate_user(db):
    return baker.make(get_user_model(), is_candidate=True)


@fixture
def company_user(db):
    return baker.make(get_user_model(), is_company=True)


@fixture
def set_request_message():
    def setattribute(request):
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

    return setattribute

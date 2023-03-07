import shutil

from account.models import ProfileCandidate, ProfileCompany
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from model_bakery import baker
from pytest import fixture


@fixture(scope='session', autouse=True)
def media_root(tmpdir_factory):
    """
    Override Django media root with a temporary directory.
    """
    settings.MEDIA_ROOT = tmpdir_factory.mktemp('media', numbered=True)
    yield settings.MEDIA_ROOT
    shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)


@fixture
def common_user(db):
    return baker.make(get_user_model())


@fixture
def candidate_user(db):
    user = baker.make(get_user_model(), is_candidate=True)
    baker.make(ProfileCandidate, user=user, cv='cv.pdf')
    return user


@fixture
def company_user(db):
    user = baker.make(get_user_model(), is_company=True)
    baker.make(ProfileCompany, user=user)
    return user


@fixture
def set_request_message():
    def setattribute(request):
        setattr(request, 'session', 'session')
        setattr(request, '_messages', FallbackStorage(request))

    return setattribute

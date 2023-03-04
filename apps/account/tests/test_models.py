from unittest.mock import patch

from account.models import ProfileAbstract
from django.urls import reverse_lazy
from django.utils.text import slugify
from model_bakery import baker


class TestProfileAbstract:
    @patch('account.models.ProfileAbstract._meta.abstract', new=False)
    def test_profile_abstract_model_str(self):
        obj = baker.prepare(ProfileAbstract)

        assert str(obj) == obj.user.email


class TestProfileCompany:
    def test_get_absolute_url(self, db):
        profile = baker.make('ProfileCompany')
        url = reverse_lazy(
            'account:profile_company',
            kwargs={'title': slugify(profile.name), 'pk': profile.pk},
        )

        assert profile.get_absolute_url() == url

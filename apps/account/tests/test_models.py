from unittest.mock import patch

from account.models import ProfileAbstract
from model_bakery import baker


class TestProfileAbstract:
    @patch('account.models.ProfileAbstract._meta.abstract', new=False)
    def test_profile_abstract_model_str(self):
        obj = baker.prepare(ProfileAbstract)

        assert str(obj) == obj.user.email

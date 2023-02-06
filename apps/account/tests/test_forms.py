from account.forms import RecoveryForm
from django.utils.translation import gettext_lazy as _


class TestRecoveryForm:
    def test_valid_form(self, common_user):
        form = RecoveryForm({'email': common_user.email})
        assert form.is_valid()

    def test_invalid_form(self, common_user):
        form = RecoveryForm({'email': f'{common_user.email}0'})
        assert not form.is_valid()
        assert form.errors['email'] == [_('There is no user with this email.')]

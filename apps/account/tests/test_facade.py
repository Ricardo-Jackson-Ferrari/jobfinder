from unittest.mock import patch

from account.facade import send_recovery_email
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _
from model_bakery import baker
from pytest import mark, raises


@mark.django_db
class TestFacade:
    email = 'teste@email.com'

    def test_send_recovery_email_with_existing_user(self):
        baker.make(get_user_model(), email=self.email)

        with patch(
            'django.core.mail.EmailMultiAlternatives.send'
        ) as mock_send_email:
            mock_send_email.return_value = 1
            result = send_recovery_email(self.email)
            assert result == 1

    def test_send_recovery_email_with_nonexistent_user(self):
        with raises(ObjectDoesNotExist) as exception_info:
            send_recovery_email(f'{self.email}0')
        assert str(exception_info.value) == _(
            'There is no user with this email.'
        )

    @patch.object(EmailMultiAlternatives, 'send', side_effect=BadHeaderError)
    def test_send_recovery_email_raises_badheader_error(
        self, mock_send, common_user
    ):
        result = send_recovery_email(common_user.email)
        assert result == False

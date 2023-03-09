from unittest import mock

from common.views import ContactView
from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone
from model_bakery import baker


class TestContactView:
    @mock.patch('common.views.send_mail')
    def test_form_valid_sends_email(self, mock_send_mail):
        form = mock.Mock()
        form.cleaned_data = {
            'subject': 'Test Subject',
            'message': 'Test Message',
            'email': 'test@example.com',
            'name': 'Test Name',
        }

        view = ContactView()
        view.request = mock.MagicMock()
        view.form_valid(form)

        assert mock_send_mail.call_count == 1
        mock_send_mail.assert_called_once_with(
            'Test Name - Test Subject',
            'Test Message',
            'test@example.com',
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )


class TestIndexView:
    def test_get_context_data(self, db, client):
        baker.make('job.Job', posted_at=timezone.now(), _quantity=4)
        response = client.get(reverse_lazy('common:index'))
        assert response.status_code == 200
        assert len(response.context['jobs']) == 3

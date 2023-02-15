from unittest.mock import patch

from account.forms import ProfileCandidateForm, RegisterCandidateForm
from account.models import ProfileCandidate
from account.views import (
    LoginView,
    ProfileCompanyUpdateView,
    ProfileView,
    RecoveryForm,
    RecoveryView,
    RegisterBaseView,
)
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.db import DatabaseError
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from model_bakery import baker
from pytest import raises

ACCOUNT_RECOVERY_URL = reverse_lazy('account:recovery')
ACCOUNT_REGISTER_CANDIDATE_URL = reverse_lazy('account:candidate_signup')


class TestRecoveryView:
    def test_form_valid_with_success_send_recovery_mail(
        self, client, common_user
    ):
        response = client.post(
            ACCOUNT_RECOVERY_URL, {'email': common_user.email}
        )
        assert response.status_code == 302
        assert response.url == ACCOUNT_RECOVERY_URL
        assert response.has_header('location') is True

    def test_form_valid_with_send_recovery_email_returning_false(
        self, mocker, common_user, set_request_message
    ):
        factory = RequestFactory()
        request = factory.post(
            reverse('account:recovery'), {'email': common_user.email}
        )
        request.user = common_user
        set_request_message(request)
        form = RecoveryForm(request.POST)
        form.is_valid()

        # Patch the send_recovery_email function
        mocker.patch('account.views.send_recovery_email', return_value=False)

        # Run the test
        view = RecoveryView()
        view.request = request
        response = view.form_valid(form)

        # Check the response
        assert isinstance(response, HttpResponse)
        assert response.status_code == 200
        assert response.template_name == ['account/auth/recovery.html']

    def test_form_invalid(self, client, common_user):
        response = client.post(
            ACCOUNT_RECOVERY_URL, {'email': f'{common_user.email}0'}
        )
        assert response.status_code == 200
        assert (
            _('There is no user with this email.')
            in response.context['form'].errors['email']
        )


class TestRegisterBaseView:
    def test_register_base_view_post_request_with_valid_forms(
        self, client, db
    ):  # sourcery skip: class-extract-method
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test@example.com',
            'password1': 'testpassword1',
            'password2': 'testpassword1',
        }
        response = client.post(ACCOUNT_REGISTER_CANDIDATE_URL, data)
        assert response.status_code == 302
        assert get_user_model().objects.count() == 1

    def test_register_base_view_post_request_with_invalid_forms(
        self, client, db
    ):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test@example.com',
            'password2': 'testpassword1',
        }
        response = client.post(ACCOUNT_REGISTER_CANDIDATE_URL, data)
        assert response.status_code == 200
        assert get_user_model().objects.count() == 0

    def test_register_base_without_form_profile_class(self):
        class TestView(RegisterBaseView):
            form_class = RegisterCandidateForm

        request = RequestFactory().post('')
        with raises(ImproperlyConfigured):
            TestView.as_view()(request)

    def test_register_base_with_fields_and_form_profile_class(self):
        class TestView(RegisterBaseView):
            fields = ['cv']
            form_profile_class = ProfileCandidateForm
            model = ProfileCandidate

        request = RequestFactory().post('')
        with raises(ImproperlyConfigured):
            TestView.as_view()(request)

    def test_register_base_get_context_data_without_form_profile_in_kwargs(
        self,
    ):
        class TestView(RegisterBaseView):
            form_class = RegisterCandidateForm
            form_profile_class = ProfileCandidateForm
            request = RequestFactory().post('')
            object = None
            initial = {'form_profile': ProfileCandidateForm}

        assert TestView().get_context_data() != []

    def test_register_base_get_form_profile_with_form_profile_class_none(self):
        class TestView(RegisterBaseView):
            form_class = RegisterCandidateForm
            form_profile_class = ProfileCandidateForm
            request = RequestFactory().post('')

        with raises(TypeError):
            TestView().get_form_profile(form_profile_class=None)

    def test_register_base_get_form_profile_class_with_model_none(self):
        class TestView(RegisterBaseView):
            model = ProfileCandidate
            fields = ['cv']
            request = RequestFactory().post('')

        assert issubclass(TestView().get_form_profile_class(), BaseModelForm)

    def test_register_base_get_form_profile_class_with_object(self):
        class TestView(RegisterBaseView):
            object = ProfileCandidate()
            fields = ['cv']
            request = RequestFactory().post('')

        assert issubclass(TestView().get_form_profile_class(), BaseModelForm)

    def test_register_base_get_form_profile_class_without_fields_and_with_model(
        self,
    ):
        class TestView(RegisterBaseView):
            model = ProfileCandidate
            request = RequestFactory().post('')
            fields = ['cv']

        view = TestView()
        view.fields = None
        with raises(ImproperlyConfigured):
            view.get_form_profile_class()

    def test_get_error_message(self):
        assert (
            RegisterBaseView.error_message
            == RegisterBaseView().get_error_message()
        )

    def test_form_valid_without_message_success(self, db):
        class TestView(RegisterBaseView):
            success_message = ''
            form_class = RegisterCandidateForm
            form_profile_class = ProfileCandidateForm
            request = RequestFactory().post('')

        data_user = {
            'email': 'test@example.com',
            'password1': 'testpassword1',
            'password2': 'testpassword1',
        }
        data_profile = {
            'first_name': 'test',
            'last_name': 'user',
        }
        form = RegisterCandidateForm(data=data_user)
        form_profile = ProfileCandidateForm(data=data_profile)
        assert TestView().form_valid(form, form_profile).status_code == 302

    def test_form_valid_error(self, set_request_message):
        class TestView(RegisterBaseView):
            template_name = ''
            form_class = RegisterCandidateForm
            form_profile_class = ProfileCandidateForm
            request = RequestFactory().post('')
            object = None
            set_request_message(request)

        form = RegisterCandidateForm()
        form_profile = ProfileCandidateForm()

        with patch('account.views.atomic') as atomic_mock:

            def raise_exception(*args, **kwargs):
                raise DatabaseError

            atomic_mock.side_effect = raise_exception
            response = TestView().form_valid(form, form_profile)
        assert response.status_code == 200

    def test_form_valid_error_whitout_error_message(self, set_request_message):
        class TestView(RegisterBaseView):
            template_name = ''
            form_class = RegisterCandidateForm
            form_profile_class = ProfileCandidateForm
            request = RequestFactory().post('')
            object = None
            error_message = ''
            set_request_message(request)

        form = RegisterCandidateForm()
        form_profile = ProfileCandidateForm()

        with patch('account.views.atomic') as atomic_mock:

            def raise_exception(*args, **kwargs):
                raise DatabaseError

            atomic_mock.side_effect = raise_exception
            response = TestView().form_valid(form, form_profile)
        assert response.status_code == 200


class TestLoginView:
    def test_get_success_url(self):
        assert LoginView().get_success_url() == LoginView.success_url


class TestProfileView:
    def test_get_context_data_with_title(self, company_user):
        class TestView(ProfileView):
            object = company_user.profilecompany

        assert 'title' in TestView().get_context_data().keys()


class TestProfileCompanyUpdateView:
    def test_get_form(self, mocker, company_user, common_user):
        factory = RequestFactory()
        request = factory.get(reverse('account:profile_company_update'))
        request.user = company_user
        baker.make('Address', user=common_user)
        baker.make('Address', user=company_user)

        view = ProfileCompanyUpdateView()
        view.request = request
        form = view.get_form()

        assert form.fields['address'].queryset.count() == 1

    def test_get_form_without_form_class(
        self, mocker, company_user, common_user
    ):
        factory = RequestFactory()
        request = factory.get(reverse('account:profile_company_update'))
        request.user = company_user

        view = ProfileCompanyUpdateView()
        view.request = request
        form = view.get_form(form_class=view.form_class)

        assert form.fields['address'].queryset.count() == 0

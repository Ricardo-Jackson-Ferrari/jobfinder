from typing import Any, Dict, Optional, Type

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.db import DatabaseError
from django.db.transaction import atomic
from django.forms import BaseForm, BaseModelForm, models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    TemplateView,
    UpdateView,
)

from .facade import send_recovery_email
from .forms import (
    ProfileCandidateForm,
    ProfileCompanyForm,
    RecoveryForm,
    RegisterCandidateForm,
    RegisterCompanyForm,
)
from .mixins import CandidateUserMixin, CompanyUserMixin, OwnerProfileMixin
from .models import ProfileCandidate, ProfileCompany

ACCOUNT_LOGIN_URL = reverse_lazy('account:login')


class RegisterBaseView(SuccessMessageMixin, CreateView):
    form_profile_class: BaseModelForm = None
    success_url = ACCOUNT_LOGIN_URL
    success_message = _('Successfully registered!')
    error_message = _('Error when registering')
    user_group = ''

    def post(
        self, request: HttpRequest, *args: str, **kwargs: Any
    ) -> HttpResponse:
        self.object = None

        form = self.get_form()
        form_profile = self.get_form_profile()

        if form.is_valid() and form_profile.is_valid():
            return self.form_valid(form, form_profile)
        else:
            return self.form_invalid(form, form_profile)

    def form_valid(self, form: BaseModelForm, form_profile: BaseModelForm):
        # sourcery skip: extract-method
        try:
            with atomic():
                form.instance.__setattr__(self.user_group, True)
                self.object = form.save()
                form_profile.instance.user = self.object
                form_profile.save()
                if success_message := self.get_success_message(
                    form.cleaned_data
                ):
                    messages.success(self.request, success_message)
                return redirect(self.get_success_url())
        except DatabaseError:
            if error_message := self.get_error_message():
                messages.error(self.request, error_message)
            return self.form_invalid(form, form_profile)

    def get_error_message(self):
        return self.error_message

    def form_invalid(
        self, form: BaseModelForm, form_profile: BaseModelForm
    ) -> HttpResponse:
        return self.render_to_response(
            self.get_context_data(form=form, form_profile=form_profile)
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        if 'form_profile' not in kwargs:
            kwargs['form_profile'] = self.get_form_profile()
        return super().get_context_data(**kwargs)

    def get_form_profile(
        self, form_profile_class: Optional[Type[BaseModelForm]] = ...
    ) -> BaseModelForm:
        if form_profile_class is not None:
            form_profile_class = self.get_form_profile_class()
        return form_profile_class(**self.get_form_kwargs())

    def get_form_profile_class(self) -> Type[BaseModelForm]:
        if self.fields is not None and self.form_profile_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_profile_class' is not permitted."
            )
        if self.form_profile_class:
            return self.form_profile_class

        if self.model is not None:
            # If a model has been explicitly provided, use it
            model = self.model
        elif getattr(self, 'object', None) is not None:
            # If this view is operating on a single object, use
            # the class of that object
            model = self.object.__class__
        else:
            # Try to get a queryset and extract the model class
            # from that
            model = self.get_queryset().model

        if self.fields is None:
            raise ImproperlyConfigured(
                f"Using ModelFormMixin (base class of {self.__class__.__name__}) without the 'fields' attribute is prohibited."
            )

        return models.modelform_factory(model, fields=self.fields)


class RegisterCandidateView(RegisterBaseView):
    template_name = 'account/auth/candidate_register.html'
    form_class = RegisterCandidateForm
    form_profile_class = ProfileCandidateForm
    user_group = 'is_candidate'
    extra_context = {
        'title': 'Cadastro Candidato',
    }


class RegisterCompanyView(RegisterBaseView):
    template_name = 'account/auth/company_register.html'
    form_class = RegisterCompanyForm
    form_profile_class = ProfileCompanyForm
    user_group = 'is_company'
    extra_context = {
        'title': 'Cadastro Empresa',
    }


class RegisterView(TemplateView):
    template_name = 'account/auth/register.html'
    extra_context = {
        'title': 'Cadastro',
    }


class RecoveryView(SuccessMessageMixin, FormView):
    template_name = 'account/auth/recovery.html'
    form_class = RecoveryForm
    success_url = reverse_lazy('account:recovery')
    success_message = 'Solicitação realizada com sucesso!'
    extra_context = {
        'title': 'Recuperação de senha',
    }

    def form_valid(self, form: BaseForm) -> HttpResponse:
        if send_recovery_email(self.request.POST.get('email')):
            return super().form_valid(form)
        messages.error(self.request, _('Error sending email'))
        return self.form_invalid(form)


class LoginView(DjangoLoginView):
    template_name = 'account/auth/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('account:dashboard')
    extra_context = {
        'title': 'Acesso',
    }

    def get_success_url(self) -> str:
        return self.success_url or super().get_success_url()


class LogoutView(DjangoLogoutView):
    next_page = 'account:login'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'account/dashboard/dashboard.html'
    extra_context = {'title': 'Painel'}


class ProfileView(DetailView):
    template_name = 'account/profile.html'
    model = ProfileCompany
    context_object_name = 'company'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f'Profile | {self.object.name}'
        ctx['jobs'] = get_job_available().filter(company=self.object)
        return ctx


class ProfileCompanyUpdateView(
    CompanyUserMixin, OwnerProfileMixin, UpdateView
):
    template_name = 'account/dashboard/company/profile_company_update.html'
    model = ProfileCompany
    form_class = ProfileCompanyForm
    extra_context = {'title': _('Edit profile')}
    success_url = reverse_lazy('account:profile_company_update')

    def get_form(
        self, form_class: Optional[Type[BaseModelForm]] = None
    ) -> BaseModelForm:
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())


class ProfileCandidateUpdateView(
    CandidateUserMixin, OwnerProfileMixin, UpdateView
):
    template_name = 'account/dashboard/candidate/profile_candidate_update.html'
    model = ProfileCandidate
    form_class = ProfileCandidateForm
    extra_context = {'title': _('Edit profile')}
    success_url = reverse_lazy('account:profile_candidate_update')


class AddressManage(CompanyUserMixin, TemplateView):
    template_name = 'account/dashboard/company/address.html'
    extra_context = {'title': _('Address management')}


class PasswordResetView(
    SuccessMessageMixin, auth_views.PasswordResetConfirmView
):
    template_name = 'account/auth/password_reset.html'
    success_url = reverse_lazy('account:login')
    success_message = _('Password reset complete')


class SettingsView(
    SuccessMessageMixin, LoginRequiredMixin, auth_views.PasswordChangeView
):
    template_name = 'account/auth/settings.html'
    success_url = reverse_lazy('account:settings')
    success_message = _('Password change complete')
    extra_context = {'title': _('Settings')}

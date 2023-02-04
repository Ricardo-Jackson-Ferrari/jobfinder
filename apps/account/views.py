from typing import Any, Dict, Optional, Type

from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.db.transaction import atomic
from django.forms import BaseModelForm, models, BaseForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from .forms import (
    ProfileCandidateForm,
    ProfileCompanyForm,
    RecoveryForm,
    RegisterCandidateForm,
    RegisterCompanyForm,
)
from .facade import send_recovery_email

ACCOUNT_LOGIN_URL = reverse_lazy('account:login')


class RegisterBaseView(SuccessMessageMixin, CreateView):
    form_class: BaseModelForm = None
    form_profile_class: BaseModelForm = None
    success_url = ACCOUNT_LOGIN_URL
    success_message = 'Cadastro realizado com sucesso!'

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

    @atomic
    def form_valid(self, form: BaseModelForm, form_profile: BaseModelForm):
        self.object = form.save()
        form_profile.instance.user = self.object
        form_profile.save()
        return redirect(self.get_success_url())

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
        super().get_form_class()
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
    template_name = 'account/candidate_register.html'
    form_class = RegisterCandidateForm
    form_profile_class = ProfileCandidateForm
    extra_context = {
        'title': 'Cadastro Candidato',
    }


class RegisterCompanyView(RegisterBaseView):
    template_name = 'account/company_register.html'
    form_class = RegisterCompanyForm
    form_profile_class = ProfileCompanyForm
    extra_context = {
        'title': 'Cadastro Empresa',
    }


class RegisterView(TemplateView):
    template_name = 'account/register.html'
    extra_context = {
        'title': 'Cadastro',
    }


class RecoveryView(SuccessMessageMixin, FormView):
    template_name = 'account/recovery.html'
    form_class = RecoveryForm
    success_url = reverse_lazy('account:recovery')
    success_message = 'Solicitação realizada com sucesso!'
    extra_context = {
        'title': 'Recuperação de senha',
    }

    def form_valid(self, form: BaseForm) -> HttpResponse:
        send_recovery_email(self.request.POST.get('email'))
        return super().form_valid(form)


class LoginView(DjangoLoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True
    extra_context = {
        'title': 'Acesso',
    }


class LogoutView(DjangoLogoutView):
    next_page = 'account:login'

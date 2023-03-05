from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, TemplateView
from job.facade import get_job_available

from .forms import ContactForm


class IndexView(TemplateView):
    template_name = 'common/index.html'
    extra_context = {
        'title': _('Home'),
    }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['jobs'] = get_job_available().order_by('-posted_at')[:3]
        return ctx


class AboutView(TemplateView):
    template_name = 'common/about.html'
    extra_context = {
        'title': _('About Us'),
    }


class ContactView(SuccessMessageMixin, FormView):
    template_name = 'common/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('common:contact')
    success_message = _('Message sent successfully')
    extra_context = {
        'title': _('Contact'),
    }

    def form_valid(self, form) -> HttpResponse:
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')
        email = form.cleaned_data.get('email')
        name = form.cleaned_data.get('name')
        name_subject = f'{name} - {subject}'

        send_mail(
            name_subject,
            message,
            email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return super().form_valid(form)

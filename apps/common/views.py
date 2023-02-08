from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import ContactForm


class IndexView(TemplateView):
    template_name = 'common/index.html'
    extra_context = {
        'title': 'Início',
    }


class AboutView(TemplateView):
    template_name = 'common/about.html'
    extra_context = {
        'title': 'Sobre nós',
    }


class ContactView(FormView):
    template_name = 'common/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('common:contact')
    extra_context = {
        'title': 'Contato',
    }

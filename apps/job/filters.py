import datetime

import django_filters
from django import forms

from .choices import EXPERIENCIES, HIERARCHIES, MODALITIES, PERIOD_CHOICES
from .models import Job


class JobFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    modality = django_filters.MultipleChoiceFilter(
        choices=MODALITIES, widget=forms.CheckboxSelectMultiple
    )
    hierarchy = django_filters.MultipleChoiceFilter(
        choices=HIERARCHIES, widget=forms.CheckboxSelectMultiple
    )
    experience = django_filters.MultipleChoiceFilter(
        choices=EXPERIENCIES, widget=forms.CheckboxSelectMultiple
    )
    period = django_filters.ChoiceFilter(
        choices=PERIOD_CHOICES, method='filter_by_period'
    )

    def filter_by_period(self, queryset, name, value):
        today = datetime.date.today()

        if value == 'today':
            return queryset.filter(posted_at__date=today)
        elif value == 'last_3_days':
            three_days_ago = today - datetime.timedelta(days=3)
            return queryset.filter(posted_at__date__gte=three_days_ago)
        elif value == 'last_week':
            last_week = today - datetime.timedelta(days=7)
            return queryset.filter(posted_at__date__gte=last_week)
        elif value == 'last_2_weeks':
            two_weeks_ago = today - datetime.timedelta(days=14)
            return queryset.filter(posted_at__date__gte=two_weeks_ago)
        elif value == 'last_month':
            last_month = today - datetime.timedelta(days=30)
            return queryset.filter(posted_at__date__gte=last_month)

    class Meta:
        model = Job
        fields = {
            'category': ('exact',),
            'address__uf': ('exact',),
        }

from typing import Any, Dict

from account.mixins import CandidateUserMixin, CompanyUserMixin
from django.contrib import messages
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from tools.filters import CustomOrderFilter

from .facade import get_job_available, get_job_posted
from .filters import JobFilter
from .forms import JobApplicationForm
from .models import Job, JobApplication
from .serializers import (
    CandidateApplicationSerializer,
    JobApplicationPatchSerializer,
    JobApplicationSerializer,
    JobCreateSerializer,
    JobPatchSerializer,
    JobShowSerializer,
)


class JobListView(FilterView):
    filterset_class = JobFilter
    queryset = get_job_available()
    paginate_by = 10
    ordering = '-posted_at'
    template_name = 'job/job_listing.html'
    context_object_name = 'jobs'
    extra_context = {
        'title': 'Busca de vagas',
    }


class JobDetailView(FormMixin, DetailView):
    model = JobApplication
    form_class = JobApplicationForm
    queryset = get_job_posted().prefetch_related('sections__itens')
    template_name = 'job/job_details.html'

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            kwargs['instance'] = self.model(
                candidate=self.request.user.profilecandidate
            )
        return kwargs

    def get_success_url(self):
        return self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return (
            self.form_valid(form)
            if form.is_valid()
            else self.form_invalid(form)
        )

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Successful job application'))
        return super().form_valid(form)


class JobApiView(CompanyUserMixin, ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobShowSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        SearchFilter,
        CustomOrderFilter,
    ]
    search_fields = ('title',)
    ordering_fields = ('salary', 'posted_at', 'status')
    ordering = '-id'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobCreateSerializer
        elif self.request.method == 'PATCH':
            return JobPatchSerializer
        return super().get_serializer_class()

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(company=self.request.user.profilecompany)
        return qs

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.profilecompany)

    def partial_update(self, request, *args, **kwargs):
        request.data['status'] = False
        return super().partial_update(request, *args, **kwargs)


class CandidateApplicationListAPIView(CandidateUserMixin, ListAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = CandidateApplicationSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        SearchFilter,
        CustomOrderFilter,
    ]
    search_fields = ('job__title',)
    ordering_fields = (
        'created_at',
        'job__status',
    )
    ordering = '-id'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(candidate=self.request.user.profilecandidate)
        return qs


class JobApplicationListAPIView(CompanyUserMixin, ListAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        SearchFilter,
        CustomOrderFilter,
    ]
    search_fields = ('candidate__first_name',)
    ordering_fields = (
        'created_at',
        'status',
    )
    ordering = '-id'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(job__company=self.request.user.profilecompany)
        qs = qs.filter(job__id=self.kwargs.get('pk'))
        return qs


class JobApplicationPatchView(CompanyUserMixin, UpdateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationPatchSerializer

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(job__company=self.request.user.profilecompany)
        return qs

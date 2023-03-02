from typing import Any

from account.mixins import CompanyUserMixin
from django.db.models import QuerySet
from django.views.generic import DetailView
from django_filters.views import FilterView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from tools.filters import CustomOrderFilter

from .facade import get_job_available
from .filters import JobFilter
from .models import Job
from .serializers import (
    JobCreateSerializer,
    JobPatchSerializer,
    JobShowSerializer,
)


class JobListView(FilterView):
    filterset_class = JobFilter
    queryset = get_job_available()
    paginate_by = 2
    ordering = '-posted_at'
    template_name = 'job/job_listing.html'
    context_object_name = 'jobs'
    extra_context = {
        'title': 'Busca de vagas',
    }


class JobDetailView(DetailView):
    queryset = get_job_available().prefetch_related('sections__itens')
    template_name = 'job/job_details.html'


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

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from job.choices import EXPERIENCIES, HIERARCHIES, MODALITIES
from job.models import Job
from job.serializers import (
    CandidateApplicationSerializer,
    ItemListSerializer,
    ItemSerializer,
    JobApplicationSerializer,
    JobShowSerializer,
    SectionCreateSerializer,
    SectionListSerializer,
)
from model_bakery import baker
from pytest import raises
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient


class TestJobShowSerializer:
    def test_job_serializer_methods(self):
        job = baker.prepare(Job)
        job_serializer = JobShowSerializer(job)
        assert job_serializer.get_modality(job) == job.get_modality_display()
        assert job_serializer.get_hierarchy(job) == job.get_hierarchy_display()
        assert (
            job_serializer.get_experience(job) == job.get_experience_display()
        )


class TestJobCreateSerializer:
    def test_create_job_without_sections(self, db, company_user):
        client = APIClient()
        client.force_login(user=company_user)
        url = reverse_lazy('job:api_list')
        category = baker.make('job.Category')

        job_data = {
            'title': 'Test Job',
            'vacancies': 1,
            'modality': MODALITIES[0][0],
            'salary': 1000.00,
            'description': 'This is a test job.',
            'hierarchy': HIERARCHIES[0][0],
            'experience': EXPERIENCIES[0][0],
            'category': category.id,
        }

        response = client.post(url, job_data, format='json')

        assert response.status_code == 201
        assert Job.objects.count() == 1

        job = Job.objects.first()
        assert job.title == job_data['title']
        assert job.vacancies == job_data['vacancies']
        assert job.modality == job_data['modality']
        assert job.salary == job_data['salary']
        assert job.description == job_data['description']
        assert job.hierarchy == job_data['hierarchy']
        assert job.experience == job_data['experience']
        assert job.company == company_user.profilecompany

    def test_create_job_with_sections(self, db, company_user):
        client = APIClient()
        client.force_login(user=company_user)
        url = reverse_lazy('job:api_list')
        category = baker.make('job.Category')

        job_data = {
            'title': 'Test Job',
            'vacancies': 1,
            'modality': MODALITIES[0][0],
            'salary': 1000.00,
            'description': 'This is a test job.',
            'hierarchy': HIERARCHIES[0][0],
            'experience': EXPERIENCIES[0][0],
            'category': category.id,
            'sections': [
                {'title': 'Section Title', 'itens': [{'item': 'Item Text'}]}
            ],
        }

        response = client.post(url, job_data, format='json')

        assert response.status_code == 201
        assert Job.objects.count() == 1

        job = Job.objects.first()
        assert job.title == job_data['title']
        assert job.vacancies == job_data['vacancies']
        assert job.modality == job_data['modality']
        assert job.salary == job_data['salary']
        assert job.description == job_data['description']
        assert job.hierarchy == job_data['hierarchy']
        assert job.experience == job_data['experience']
        assert job.company == company_user.profilecompany


class TestCandidateApplicationSerializer:
    def test_candidate_application_serializer_methods(self, db):
        job = baker.make('job.Job')
        application = baker.prepare('job.JobApplication', job=job)
        application_serializer = CandidateApplicationSerializer(application)
        assert (
            application_serializer.get_status(application)
            == application.job.status
        )
        assert (
            application_serializer.get_url(application)
            == application.job.get_absolute_url()
        )


class TestJobApplicationSerializer:
    def test_job_application_serializer_methods(self, db):
        job = baker.make('job.Job')
        application = baker.prepare('job.JobApplication', job=job)
        application_serializer = JobApplicationSerializer(application)
        assert (
            application_serializer.get_evaluation(application)
            == application.get_evaluation_display()
        )
        assert (
            application_serializer.get_url(application)
            == application.job.get_absolute_url()
        )


class TestSectionListSerializer:
    def test_validate_with_valid_data(self):
        data = [{'title': 'Section 1', 'itens': [{'item': 'item 1'}]}]
        serializer = SectionListSerializer(
            child=SectionCreateSerializer(), data=data
        )
        assert serializer.is_valid() == True
        assert serializer.validated_data == data

    def test_validate_with_too_many_sections(self):
        data = [
            {'title': f'Section {i}', 'itens': [{'item': 'item 1'}]}
            for i in range(6)
        ]
        serializer = SectionListSerializer(
            child=SectionCreateSerializer(), data=data
        )
        with raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert str(excinfo.value.detail['non_field_errors'][0]) == _(
            'limit number of sections reached'
        )


class TestItemListSerializer:
    def test_validate_with_valid_data(self):
        data = [{'item': 'item i'}]
        serializer = ItemListSerializer(child=ItemSerializer(), data=data)
        assert serializer.is_valid() == True
        assert serializer.validated_data == data

    def test_validate_with_too_many_sections(self):
        data = [{'item': f'item {i}'} for i in range(6)]
        serializer = ItemListSerializer(child=ItemSerializer(), data=data)
        with raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert str(excinfo.value.detail['non_field_errors'][0]) == _(
            'limit number of items reached'
        )

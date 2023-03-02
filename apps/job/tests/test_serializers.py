from django.urls import reverse_lazy
from job.choices import EXPERIENCIES, HIERARCHIES, MODALITIES
from job.models import Job
from job.serializers import JobShowSerializer
from model_bakery import baker
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

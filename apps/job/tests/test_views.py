from django.urls import reverse_lazy
from job.models import Job
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

URL_JOB_API_LIST = reverse_lazy('job:api_list')


class TestJobApiView:
    def test_list_jobs(self, company_user):
        baker.make(Job, company=company_user.profilecompany)
        client = APIClient()
        client.force_login(user=company_user)
        response = client.get(URL_JOB_API_LIST)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    def test_partial_update_job(self, company_user):
        job = baker.make(Job, company=company_user.profilecompany)
        client = APIClient()
        client.force_login(user=company_user)
        response = client.patch(reverse_lazy('job:api_detail', args=[job.id]))
        assert response.status_code == status.HTTP_200_OK
        assert Job.objects.count() == 1
        job_update = Job.objects.get(id=job.id)
        assert job.status != job_update.status

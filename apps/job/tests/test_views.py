from django.contrib.messages import get_messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from job.models import Job
from model_bakery import baker
from pytest import fixture
from rest_framework import status
from rest_framework.test import APIClient

URL_JOB_API_LIST = reverse_lazy('job:api_list')


@fixture
def job_application(db, company_user):
    job = baker.make('job.Job', company=company_user.profilecompany)
    return baker.make('job.JobApplication', job=job)


@fixture
def api_client() -> APIClient:
    return APIClient()


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


class TestJobApplicationPatchView:
    def test_patch_job_application_success(self, job_application, api_client):
        url = reverse_lazy(
            'job:job_application_api_detail', kwargs={'pk': job_application.pk}
        )

        data = {'evaluation': 0}

        api_client.force_login(user=job_application.job.company.user)
        response = api_client.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK

        job_application.refresh_from_db()

        assert job_application.evaluation == 0

    def test_patch_job_application_with_wrong_company(
        self, job_application, api_client
    ):
        other_company = baker.make('account.ProfileCompany')
        url = reverse_lazy(
            'job:job_application_api_detail', kwargs={'pk': job_application.pk}
        )

        api_client.force_login(user=other_company.user)
        response = api_client.patch(url)

        assert response.status_code == status.HTTP_302_FOUND

        job_application.refresh_from_db()

        assert job_application.evaluation != 1


class TestJobApplicationListAPIView:
    def test_list_jobs(self, company_user):
        job = baker.make('job.Job', company=company_user.profilecompany)
        candidate_1 = baker.make('account.ProfileCandidate', cv='profile.pdf')
        candidate_2 = baker.make('account.ProfileCandidate', cv='profile.pdf')
        application_1 = baker.make(
            'job.JobApplication', job=job, candidate=candidate_1
        )
        application_2 = baker.make(
            'job.JobApplication', job=job, candidate=candidate_2
        )
        baker.make(Job, company=company_user.profilecompany)
        client = APIClient()
        client.force_login(user=company_user)
        url = reverse_lazy(
            'job:job_application_api_list', kwargs={'pk': job.pk}
        )
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['id'] == application_2.id
        assert response.data[1]['id'] == application_1.id


class TestCandidateApplicationListAPIView:
    def test_list_jobs(self, candidate_user):
        job_1 = baker.make('job.Job')
        job_2 = baker.make('job.Job')
        application_1 = baker.make(
            'job.JobApplication',
            job=job_1,
            candidate=candidate_user.profilecandidate,
        )
        application_2 = baker.make(
            'job.JobApplication',
            job=job_2,
            candidate=candidate_user.profilecandidate,
        )
        baker.make('job.JobApplication')
        client = APIClient()
        client.force_login(user=candidate_user)
        url = reverse_lazy('job:application_api_list')
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['id'] == application_2.id
        assert response.data[1]['id'] == application_1.id


class TestJobDetailView:
    def test_view_uses_correct_template(self, db):
        client = APIClient()
        job = baker.make('job.Job', posted_at=timezone.now())
        response = client.get(job.get_absolute_url())
        assert response.status_code == 200

    def test_view_redirects_on_successful_form_submission(
        self, candidate_user
    ):
        client = APIClient()
        client.force_login(user=candidate_user)
        job = baker.make('job.Job', posted_at=timezone.now())
        data = {
            'salary_claim': 1,
            'job': job.pk,
        }
        response = client.post(job.get_absolute_url(), data=data)

        messages = list(get_messages(response.wsgi_request))
        assert response.status_code == 302
        assert response.url == job.get_absolute_url()
        assert str(messages[0]) == _('Successful job application')

    def test_view_displays_errors_on_invalid_form_submission(
        self, candidate_user
    ):
        client = APIClient()
        client.force_login(user=candidate_user)
        job = baker.make('job.Job', posted_at=timezone.now())
        data = {
            'x': 1,
            'job': job.pk,
        }
        response = client.post(job.get_absolute_url(), data=data)
        assert response.status_code == 200

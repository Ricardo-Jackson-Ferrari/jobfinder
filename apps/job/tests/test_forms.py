import pytest
from django.forms.models import model_to_dict
from django.utils import timezone
from job.forms import JobApplicationForm
from job.models import Job, JobApplication
from mixer.backend.django import mixer
from model_bakery import baker


@pytest.fixture()
def job(db):
    return mixer.blend(Job, status=True, posted_at=timezone.now())


@pytest.fixture()
def job_application(db, job):
    return mixer.blend(JobApplication, job=job)


@pytest.mark.django_db
class TestJobApplicationForm:
    def test_clean_job_with_job_closed_should_raise_validation_error(
        self, job
    ):
        job.status = False
        job.save()

        form = JobApplicationForm({'job': job.pk})
        form.is_valid()

        assert 'job' in form.errors
        assert form.errors['job'][0] == 'job vacancy closed'

    def test_clean_job_with_unpublished_job_should_raise_validation_error(
        self, job
    ):
        job.posted_at = None
        job.save()

        form = JobApplicationForm({'job': job.pk})
        form.is_valid()

        assert 'job' in form.errors
        assert form.errors['job'][0] == 'unpublished job'

    def test_full_clean_with_already_applied_job_application(
        self, job, candidate_user
    ):
        application = baker.make(
            'job.JobApplication',
            job=job,
            candidate=candidate_user.profilecandidate,
            salary_claim=1,
        )
        application_data = model_to_dict(application)

        form = JobApplicationForm(
            instance=JobApplication(candidate=candidate_user.profilecandidate),
            data=application_data,
        )
        form.full_clean()

        assert '__all__' in form.errors.keys()
        assert form.errors['__all__'][0] == 'You already applied for this job'

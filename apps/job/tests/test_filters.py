from django.utils import timezone
from job.filters import JobFilter
from job.models import Job
from mixer.backend.django import mixer
from pytest import mark


class TestJobFilter:
    @mark.parametrize(
        'date_range, expected',
        [
            ('today', 1),
            ('last_3_days', 3),
            ('last_week', 4),
            ('last_2_weeks', 6),
            ('last_month', 7),
        ],
    )
    def test_job_filter_by_period(self, db, date_range, expected):
        qs = Job.objects.all()
        today = timezone.now()

        mixer.blend(Job, posted_at=today)
        mixer.blend(Job, posted_at=today - timezone.timedelta(days=1))
        mixer.blend(Job, posted_at=today - timezone.timedelta(days=2))
        mixer.blend(Job, posted_at=today - timezone.timedelta(days=5))
        mixer.blend(Job, posted_at=today - timezone.timedelta(days=8))
        mixer.blend(Job, posted_at=today - timezone.timedelta(days=12))
        mixer.blend(Job, posted_at=today - timezone.timedelta(days=15))

        filter_ = JobFilter()
        filtered_qs = filter_.filter_by_period(qs, 'period', date_range)

        assert len(filtered_qs) == expected

    def test_job_filter_by_period_no_match(self, db):
        qs = Job.objects.all()

        filter_ = JobFilter()
        filtered_qs = filter_.filter_by_period(qs, 'period', 'x')

        assert filtered_qs is None

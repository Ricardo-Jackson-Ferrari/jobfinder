from .models import Job


def get_job_available():
    return Job.objects.filter(
        status=True, posted_at__isnull=False
    ).select_related('address', 'category', 'company', 'company__address')


def get_job_posted():
    return Job.objects.filter(posted_at__isnull=False).select_related(
        'address', 'category', 'company', 'company__address'
    )

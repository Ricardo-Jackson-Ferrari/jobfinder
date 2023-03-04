from account.models import ProfileCandidate
from account.serializers import CandidateSerializer
from model_bakery import baker


class TestJobShowSerializer:
    def test_job_serializer_methods(self):
        candidate = baker.prepare(ProfileCandidate, cv='image.jpg')
        candidate_serializer = CandidateSerializer(candidate)
        assert candidate_serializer.get_cv(candidate) == candidate.cv.url

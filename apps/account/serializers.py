from rest_framework import serializers

from .models import ProfileCandidate


class CandidateSerializer(serializers.ModelSerializer):
    cv = serializers.SerializerMethodField()

    def get_cv(self, obj):
        return obj.cv.url

    class Meta:
        model = ProfileCandidate
        fields = (
            'first_name',
            'last_name',
            'cv',
        )

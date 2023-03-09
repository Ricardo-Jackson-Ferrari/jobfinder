from account.serializers import CandidateSerializer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Item, Job, JobApplication, Section


class ItemListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        if len(attrs) > 5:
            raise ValidationError(_('limit number of items reached'))
        return super().validate(attrs)


class ItemSerializer(serializers.ModelSerializer):
    section = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Item
        list_serializer_class = ItemListSerializer
        fields = ('item', 'section')


class SectionShowSerializer(serializers.ModelSerializer):
    itens = serializers.StringRelatedField(many=True)

    class Meta:
        model = Section
        fields = ('title', 'itens')


class SectionListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        if len(attrs) > 5:
            raise ValidationError(_('limit number of sections reached'))
        return super().validate(attrs)


class SectionCreateSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(read_only=True)
    itens = ItemSerializer(many=True)

    class Meta:
        model = Section
        list_serializer_class = SectionListSerializer
        fields = ('title', 'job', 'itens')


class JobShowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    address = serializers.StringRelatedField()
    sections = SectionShowSerializer(many=True)
    experience = serializers.SerializerMethodField()
    hierarchy = serializers.SerializerMethodField()
    modality = serializers.SerializerMethodField()
    subscribed = serializers.SerializerMethodField()
    company = serializers.StringRelatedField()

    def get_experience(self, obj):
        return obj.get_experience_display()

    def get_hierarchy(self, obj):
        return obj.get_hierarchy_display()

    def get_modality(self, obj):
        return obj.get_modality_display()

    def get_subscribed(self, obj):
        return obj.applications.count()

    class Meta:
        model = Job
        fields = (
            'id',
            'title',
            'company',
            'subscribed',
            'created_at',
            'posted_at',
            'vacancies',
            'modality',
            'address',
            'salary',
            'status',
            'description',
            'hierarchy',
            'category',
            'experience',
            'sections',
        )


class JobCreateSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    sections = SectionCreateSerializer(many=True, required=False)

    def create(self, validated_data):
        if 'sections' not in validated_data.keys():
            return super().create(validated_data)

        sections_data = validated_data.pop('sections')

        job_instance = Job.objects.create(**validated_data)
        for section_data in sections_data:
            itens_data = section_data.pop('itens')
            section_instance = Section.objects.create(
                job=job_instance, **section_data
            )
            for item_data in itens_data:
                Item.objects.create(section=section_instance, **item_data)
        return job_instance

    class Meta:
        model = Job
        fields = (
            'company',
            'title',
            'vacancies',
            'modality',
            'address',
            'salary',
            'status',
            'description',
            'hierarchy',
            'category',
            'experience',
            'sections',
        )


class JobPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('status',)


class CandidateApplicationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    job = serializers.StringRelatedField()
    status = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.job.status

    def get_url(self, obj):
        return obj.job.get_absolute_url()

    class Meta:
        model = JobApplication
        fields = (
            'id',
            'created_at',
            'job',
            'url',
            'status',
            'candidate',
            'salary_claim',
        )


class JobApplicationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    candidate = CandidateSerializer()
    evaluation = serializers.SerializerMethodField()

    def get_evaluation(self, obj):
        return obj.get_evaluation_display()

    def get_url(self, obj):
        return obj.job.get_absolute_url()

    class Meta:
        model = JobApplication
        fields = (
            'id',
            'created_at',
            'candidate',
            'salary_claim',
            'evaluation',
        )


class JobApplicationPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ('evaluation',)

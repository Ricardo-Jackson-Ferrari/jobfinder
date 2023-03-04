from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.utils.translation import gettext_lazy as _

from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    def clean_job(self):
        data = self.cleaned_data['job']
        if not data.status:
            raise ValidationError(_('job vacancy closed'))
        if not data.posted_at:
            raise ValidationError(_('unpublished job'))

        return data

    def full_clean(self):
        super().full_clean()
        try:
            self.instance.validate_unique()
        except forms.ValidationError as e:
            self._update_errors(e)

    class Meta:
        model = JobApplication
        exclude = (
            'candidate',
            'evaluation',
        )
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': _('You already applied for this job'),
            }
        }

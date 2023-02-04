from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import ProfileCandidate, ProfileCompany

EMAIL_HELP_TEXT = 'Enter a valid email address'


class RegisterCandidateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, help_text='Opcional')
    email = forms.EmailField(
        max_length=254, help_text=EMAIL_HELP_TEXT
    )

    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class RegisterCompanyForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(
        max_length=254, help_text=EMAIL_HELP_TEXT
    )

    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'email',
            'password1',
            'password2',
        ]


class ProfileCandidateForm(forms.ModelForm):
    class Meta:
        model = ProfileCandidate
        exclude = ('user',)


class ProfileCompanyForm(forms.ModelForm):
    class Meta:
        model = ProfileCompany
        exclude = ('user',)


class RecoveryForm(forms.Form):
    email = forms.EmailField(
        max_length=254, help_text='Enter a valid email address'
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = get_user_model().objects.filter(email=email)

        if not user.exists():
            raise ValidationError('email not registered')
        return email

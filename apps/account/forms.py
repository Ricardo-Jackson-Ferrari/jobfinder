from address.models import Address
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import ProfileCandidate, ProfileCompany

EMAIL_HELP_TEXT = _('Enter a valid email address')


class RegisterCandidateForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text=EMAIL_HELP_TEXT)

    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'password1',
            'password2',
        ]


class RegisterCompanyForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text=EMAIL_HELP_TEXT)

    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'password1',
            'password2',
        ]


class ProfileCandidateForm(forms.ModelForm):
    class Meta:
        model = ProfileCandidate
        exclude = ('user',)


class ProfileCompanyForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs) -> None:
        super(ProfileCompanyForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['address'].queryset = Address.objects.filter(user=user)

    class Meta:
        model = ProfileCompany
        exclude = ('user',)


class RecoveryForm(forms.Form):
    email = forms.EmailField(max_length=254, help_text=EMAIL_HELP_TEXT)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = get_user_model().objects.filter(email=email)

        if not user.exists():
            raise ValidationError(_('There is no user with this email.'))
        return email

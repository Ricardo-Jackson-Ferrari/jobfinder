from account.forms import ProfileCompanyForm, RecoveryForm
from django.utils.translation import gettext_lazy as _
from model_bakery import baker


class TestRecoveryForm:
    def test_valid_form(self, common_user):
        form = RecoveryForm({'email': common_user.email})
        assert form.is_valid()

    def test_invalid_form(self, common_user):
        form = RecoveryForm({'email': f'{common_user.email}0'})
        assert not form.is_valid()
        assert form.errors['email'] == [_('There is no user with this email.')]


class TestProfileCompanyForm:
    def test_user_filters_address(self, common_user, company_user):
        address = baker.make('Address', user=company_user)
        baker.make('Address', user=common_user)

        form = ProfileCompanyForm(user=company_user)
        assert form.fields['address'].queryset.count() == 1
        assert address in form.fields['address'].queryset.all()

        form = ProfileCompanyForm()
        assert form.fields['address'].queryset.count() == 2

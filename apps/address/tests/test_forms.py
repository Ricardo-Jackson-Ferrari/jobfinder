from address.forms import AddressForm
from address.models import Address
from django.utils.translation import gettext_lazy as _
from model_bakery import baker


class TestAddressForm:
    def test_address_form_validates_unique_data(self, company_user):
        form_data = {
            'title': 'title',
            'zipcode': '21760360',
            'street': 'Test Street',
            'number': '100',
            'district': 'Test Neighborhood',
            'city': 'Test City',
            'uf': 'RJ',
        }

        form = AddressForm(instance=company_user, data=form_data)
        form.full_clean()

        assert form.is_valid() is True

    def test_address_form_validates_unique_data_fail(self, db):
        form_data = {
            'title': 'Home',
            'zipcode': '12345678',
            'uf': 'AC',
            'city': 'Rio Branco',
            'district': 'Centro',
            'street': 'Rua dos Testes',
            'number': '123',
            'complement': 'Apto 201',
        }
        address = baker.make(Address, **form_data)

        form = AddressForm(instance=Address(user=address.user), data=form_data)
        form.full_clean()

        assert form.is_valid() is False

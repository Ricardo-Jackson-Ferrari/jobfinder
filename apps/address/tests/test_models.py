from address.models import Address
from django.core.exceptions import ValidationError
from model_bakery import baker
from pytest import raises


class TestAddressModel:
    def test_str_title(self):
        address = baker.prepare(Address)

        assert str(address) == address.title

    def test_clean(self, common_user):
        baker.make(Address, user=common_user, _quantity=5)
        address = baker.prepare(Address, user=common_user)

        with raises(ValidationError):
            address.clean()

from unittest.mock import Mock

import pytest
from address.models import Address
from address.serializers import AddressSerializer
from rest_framework.exceptions import ValidationError


class TestAddressSerializer:
    def test_address_serializer_validate_create(self, company_user):
        request = Mock()
        request.user = company_user
        context = {
            'request': request,
        }

        serializer = AddressSerializer(
            context=context,
            data={
                'title': 'Work',
                'zipcode': '12345678',
                'uf': 'SP',
                'city': 'São Paulo',
                'district': 'Centro',
                'street': 'Rua do Centro',
                'number': '123',
                'complement': 'Ap 1',
            },
        )

        assert serializer.is_valid()
        serializer.save(user=company_user)

        assert Address.objects.count() == 1
        address = Address.objects.first()
        assert address.title == 'Work'
        assert address.zipcode == '12345678'
        assert address.uf == 'SP'
        assert address.city == 'São Paulo'
        assert address.district == 'Centro'
        assert address.street == 'Rua do Centro'
        assert address.number == '123'
        assert address.complement == 'Ap 1'
        assert address.user == company_user

    def test_address_serializer_validate_create_except(self, company_user):
        request = Mock()
        request.user = company_user
        data = {
            'title': 'Home',
            'zipcode': '9876543210',
            'uf': 'XX',
            'city': 'Rio de Janeiro',
            'district': 'Copacabana',
            'street': 'Rua da Praia',
            'number': '456',
            'complement': 'Ap 2',
        }
        serializer = AddressSerializer(context={'request': request}, data=data)

        with pytest.raises(ValidationError):
            serializer.validate(data)

    def test_address_serializer_validate_update(self, company_user):
        address = Address.objects.create(
            user=company_user,
            title='Work',
            zipcode='12345678',
            uf='SP',
            city='São Paulo',
            district='Centro',
            street='Rua do Centro',
            number='123',
            complement='Ap 1',
        )
        request = Mock()
        request.user = company_user
        request.method = 'PATCH'
        data = {
            'title': 'Home',
            'zipcode': '87654321',
            'uf': 'RJ',
            'city': 'Rio de Janeiro',
            'district': 'Copacabana',
            'street': 'Rua da Praia',
            'number': '456',
            'complement': 'Ap 2',
        }
        serializer = AddressSerializer(
            context={'request': request}, instance=address, data=data
        )

        assert serializer.is_valid()
        serializer.save()

        assert Address.objects.count() == 1
        address.refresh_from_db()
        assert address.title == 'Home'
        assert address.zipcode == '87654321'
        assert address.uf == 'RJ'
        assert address.city == 'Rio de Janeiro'
        assert address.district == 'Copacabana'
        assert address.street == 'Rua da Praia'
        assert address.number == '456'
        assert address.complement == 'Ap 2'
        assert address.user == company_user

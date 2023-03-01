from address.models import Address
from django.urls import reverse_lazy
from model_bakery import baker
from rest_framework.test import APIClient

ADDRESS_API_URL = reverse_lazy('address:api_list')


class TestAddressApiView:
    def test_get_queryset(self, common_user, company_user):
        client = APIClient()
        client.force_login(user=company_user)

        baker.make(Address, user=common_user)
        address = baker.make(Address, user=company_user)

        response = client.get(ADDRESS_API_URL)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['id'] == address.id

    def test_perform_create(self, company_user):
        client = APIClient()
        client.force_login(company_user)
        data = {
            'title': 'Home',
            'zipcode': '123456789',
            'uf': 'SP',
            'city': 'São Paulo',
            'district': 'Centro',
            'street': 'Rua Direita',
            'number': '123',
            'complement': '',
        }

        response = client.post(ADDRESS_API_URL, data=data)
        assert response.status_code == 201

        address = Address.objects.get(id=response.data['id'])
        assert address.user == company_user

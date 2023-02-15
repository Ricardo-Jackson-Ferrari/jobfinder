from unittest import mock

from address.models import Address
from address.views import DeleteAddressView, ListAddressView
from django.test import RequestFactory
from model_bakery import baker


class TestListAddressView:
    def test_queryset(self, common_user, company_user):
        factory = RequestFactory()
        request = factory.get('/fake/url')
        request.user = company_user

        view = ListAddressView()
        view.request = request

        baker.make(Address, user=common_user)
        baker.make(Address, user=company_user)
        assert view.get_queryset().count() == 1


class TestDeleteAddressView:
    def test_form_valid(self):
        view = DeleteAddressView()
        view.request = mock.Mock()
        view.object = mock.Mock()

        response = view.form_valid(None)
        assert response.status_code == 200

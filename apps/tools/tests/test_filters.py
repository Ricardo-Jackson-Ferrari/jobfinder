import pytest
from address.models import Address
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory
from tools.filters import CustomOrderFilter

factory = APIRequestFactory()


@pytest.fixture
def my_model():
    return mixer.blend(Address)


def test_custom_order_filter(db, my_model):
    request = factory.get('/', {'sort': 'title', 'order': 'desc'})
    request.query_params = request.GET
    queryset = Address.objects.all()
    custom_filter = CustomOrderFilter()
    ordered_queryset = custom_filter.filter_queryset(
        request, queryset, Address
    )
    assert ordered_queryset[0] == my_model


def test_custom_order_filter_by_fields_bt(db, my_model):
    request = factory.get('/', {'sortName': 'title', 'sortOrder': 'desc'})
    request.query_params = request.GET
    queryset = Address.objects.all()
    custom_filter = CustomOrderFilter()
    ordered_queryset = custom_filter.filter_queryset(
        request, queryset, Address
    )
    assert ordered_queryset[0] == my_model


def test_return_get_default_ordering(db, my_model):
    request = factory.get('/')
    request.query_params = request.GET
    queryset = Address.objects.all()
    custom_filter = CustomOrderFilter()
    ordered_queryset = custom_filter.filter_queryset(
        request, queryset, Address
    )
    assert ordered_queryset[0] == my_model

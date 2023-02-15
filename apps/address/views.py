from account.mixins import CompanyUserMixin, OwnerUserMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from tools.mixins import (
    FormJsonResponseMixin,
    InstanceModelUserMixin,
    ListJsonResponseMixin,
)

from .forms import AddressForm
from .models import Address


class CreateAddressView(
    CompanyUserMixin, InstanceModelUserMixin, FormJsonResponseMixin, CreateView
):
    template_name = 'address/forms/create_address.html'
    model = Address
    form_class = AddressForm
    success_msg = _('Address created successfully')
    fail_msg = _('Failed to create address')


class ListAddressView(CompanyUserMixin, ListJsonResponseMixin, ListView):
    model = Address

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class UpdateAddressView(
    CompanyUserMixin, OwnerUserMixin, FormJsonResponseMixin, UpdateView
):
    model = Address
    form_class = AddressForm
    success_msg = _('Address updated successfully')
    fail_msg = _('Failed to update address, there is an error')


class DeleteAddressView(
    CompanyUserMixin, OwnerUserMixin, FormJsonResponseMixin, DeleteView
):
    model = Address

    def form_valid(self, form) -> JsonResponse:
        self.object.delete()
        return JsonResponse(status=200, data={})

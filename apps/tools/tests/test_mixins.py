import json
from unittest import mock

from address.models import Address
from django.forms import BaseModelForm
from django.http import Http404, HttpRequest, JsonResponse
from django.test import TestCase
from model_bakery import baker
from pytest import raises
from tools.mixins import (
    FormJsonResponseMixin,
    InstanceModelUserMixin,
    ListJsonResponseMixin,
)


class TestInstanceModelUserMixin:
    def test_get_form_kwargs(self, common_user):
        request = HttpRequest()
        request.user = common_user

        class TestView:
            def get_form_kwargs(self):
                return {}

        TempClass = type('TempClass', (InstanceModelUserMixin, TestView), {})
        view = TempClass()
        view.request = request
        view.model = Address

        kwargs = view.get_form_kwargs()

        assert kwargs['instance'].user == request.user
        assert isinstance(kwargs['instance'], view.model)


class TestFormJsonResponseMixin(TestCase):
    def test_form_valid(self):
        form = mock.Mock(BaseModelForm)
        form.save.return_value = 'object'
        view = FormJsonResponseMixin()
        view.success_msg = 'success'

        response = view.form_valid(form)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            json.loads(response.content.decode()),
            {
                'status_code': 201,
                'message': 'success',
            },
        )
        self.assertEqual(view.object, 'object')

    def test_form_invalid(self):
        form = mock.Mock(BaseModelForm)
        form.errors = 'errors'
        view = FormJsonResponseMixin()
        view.fail_msg = 'fail'

        response = view.form_invalid(form)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content.decode()),
            {
                'message': 'fail',
                'errors': 'errors',
                'status_code': 400,
            },
        )


class TestListJsonResponseMixin:
    def test_get(self, company_user):
        request = HttpRequest()

        class TestView:
            def get(self, request, *args, **kwargs):
                return None

        TempClass = type('TempClass', (ListJsonResponseMixin, TestView), {})
        baker.make(Address, user=company_user)
        qs = Address.objects.all()
        view = TempClass()
        view.request = request
        view.request.user = company_user
        view.get_queryset = mock.Mock(return_value=qs)
        view.get_allow_empty = mock.Mock(return_value=True)
        view.get_paginate_by = mock.Mock(return_value=None)
        view.get_context_data = mock.Mock(return_value={'address_list': qs})
        response = view.get(request)

        assert isinstance(response, JsonResponse)
        assert json.loads(response.content.decode()) == list(qs.values())
        assert view.object_list == qs
        view.get_allow_empty.assert_called_once_with()

    def test_get_with_allow_empty_false(self, company_user):
        request = HttpRequest()

        class TestView:
            def get(self, request, *args, **kwargs):
                return None

        TempClass = type('TempClass', (ListJsonResponseMixin, TestView), {})
        baker.make(Address, user=company_user)
        qs = Address.objects.all()
        view = TempClass()
        view.request = request
        view.request.user = company_user
        view.get_queryset = mock.Mock(return_value=qs)
        view.get_allow_empty = mock.Mock(return_value=False)
        view.get_paginate_by = mock.Mock(return_value=None)
        view.get_context_data = mock.Mock(return_value={'address_list': qs})
        response = view.get(request)

        assert isinstance(response, JsonResponse)
        assert json.loads(response.content.decode()) == list(qs.values())
        assert view.object_list == qs
        view.get_allow_empty.assert_called_once_with()

    def test_get_with_get_paginate_by(self, company_user):
        request = HttpRequest()

        class TestView:
            def get(self, request, *args, **kwargs):
                return None

        TempClass = type('TempClass', (ListJsonResponseMixin, TestView), {})
        baker.make(Address, user=company_user)
        qs = Address.objects.all()
        view = TempClass()
        view.request = request
        view.request.user = company_user
        view.get_queryset = mock.Mock(return_value=qs)
        view.get_allow_empty = mock.Mock(return_value=False)
        view.get_paginate_by = mock.Mock(return_value=2)
        view.get_context_data = mock.Mock(return_value={'address_list': qs})
        response = view.get(request)

        assert isinstance(response, JsonResponse)
        assert json.loads(response.content.decode()) == list(qs.values())
        assert view.object_list == qs
        view.get_allow_empty.assert_called_once_with()

    def test_get_raise_404(self, company_user):
        request = HttpRequest()

        class TestView:
            def get(self, request, *args, **kwargs):
                return None

        TempClass = type('TempClass', (ListJsonResponseMixin, TestView), {})
        baker.make(Address, user=company_user)
        qs = Address.objects.all()
        view = TempClass()
        view.request = request
        view.request.user = company_user
        view.get_queryset = mock.Mock(return_value=None)
        view.get_allow_empty = mock.Mock(return_value=False)
        view.get_paginate_by = mock.Mock(return_value=None)
        view.get_context_data = mock.Mock(return_value={'address_list': qs})

        with raises(Http404):
            response = view.get(request)

            assert isinstance(response, JsonResponse)
            assert json.loads(response.content.decode()) == list(qs.values())

        assert view.object_list is None
        view.get_allow_empty.assert_called_once_with()

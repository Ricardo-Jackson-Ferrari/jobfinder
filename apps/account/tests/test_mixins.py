from unittest.mock import MagicMock, patch

from account.mixins import (
    BaseUserMixin,
    CandidateUserMixin,
    CompanyUserMixin,
    OwnerUserMixin,
)
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse
from pytest import raises

User = get_user_model()


class TestBaseUserMixin:
    def test_base_user_mixin_handle_no_permission(
        self, common_user, set_request_message
    ):
        request = RequestFactory().get('/')
        request.user = common_user
        set_request_message(request)
        mixin = BaseUserMixin()
        mixin.request = request

        response = mixin.handle_no_permission()

        assert response.url == reverse('common:index')


class TestCandidateUserMixin:
    def test_candidate_user_mixin_test_func(self, candidate_user):
        request = RequestFactory().get('/')
        request.user = candidate_user
        mixin = CandidateUserMixin()
        mixin.request = request

        assert mixin.test_func() is True


class TestCompanyUserMixin:
    def test_candidate_user_mixin_test_func(self, company_user):
        request = RequestFactory().get('/')
        request.user = company_user
        mixin = CompanyUserMixin()
        mixin.request = request

        assert mixin.test_func() is True


class TestOwnerUserMixin:
    def test_dispatch_for_candidate(self, candidate_user):
        request = MagicMock()
        request.user = candidate_user
        mixin = OwnerUserMixin()
        mixin.kwargs = {}
        mixin.request = request
        with patch.object(mixin, 'handle_dispatch') as mock_handle_dispatch:
            mock_handle_dispatch.return_value = 'dispatched'
            response = mixin.dispatch(request)

        assert 'pk' in mixin.kwargs
        assert response == 'dispatched'
        assert mixin.kwargs['pk'] == candidate_user.profilecandidate.id
        mock_handle_dispatch.assert_called_once_with(request)

    def test_dispatch_for_company(self, company_user):
        request = MagicMock()
        request.user = company_user
        mixin = OwnerUserMixin()
        mixin.kwargs = {}
        mixin.request = request
        with patch.object(mixin, 'handle_dispatch') as mock_handle_dispatch:
            mock_handle_dispatch.return_value = 'dispatched'
            response = mixin.dispatch(request)

        assert 'pk' in mixin.kwargs
        assert response == 'dispatched'
        assert mixin.kwargs['pk'] == company_user.profilecompany.id
        mock_handle_dispatch.assert_called_once_with(request)

    def test_dispatch_for_another_user(self):
        request = MagicMock()
        mixin = OwnerUserMixin()
        mixin.kwargs = {}
        mixin.request = request
        with patch.object(mixin, 'handle_dispatch') as mock_handle_dispatch:
            mock_handle_dispatch.return_value = 'dispatched'
            response = mixin.dispatch(request)

        assert response == 'dispatched'
        mock_handle_dispatch.assert_called_once_with(request)

    def test_dispatch_def_handle_dispatch(self):
        request = MagicMock()
        mixin = OwnerUserMixin()
        mixin.kwargs = {}
        mixin.request = request
        with raises(AttributeError):
            mixin.dispatch(request)

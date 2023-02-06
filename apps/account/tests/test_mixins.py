from account.mixins import BaseUserMixin, CandidateUserMixin, CompanyUserMixin
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.urls import reverse

User = get_user_model()


class TestBaseUserMixin:
    def test_base_user_mixin_handle_no_permission(
        self, client, common_user, set_request_message
    ):
        request = RequestFactory().get('/')
        request.user = common_user
        set_request_message(request)
        mixin = BaseUserMixin()
        mixin.request = request

        response = mixin.handle_no_permission()

        assert response.url == reverse('common:index')


class TestCandidateUserMixin:
    def test_candidate_user_mixin_test_func(self, client, candidate_user):
        request = RequestFactory().get('/')
        request.user = candidate_user
        mixin = CandidateUserMixin()
        mixin.request = request

        assert mixin.test_func() is True


class TestCompanyUserMixin:
    def test_candidate_user_mixin_test_func(self, client, company_user):
        request = RequestFactory().get('/')
        request.user = company_user
        mixin = CompanyUserMixin()
        mixin.request = request

        assert mixin.test_func() is True

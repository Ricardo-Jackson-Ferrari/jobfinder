from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class BaseUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def handle_no_permission(self):
        messages.warning(
            self.request, _("You don't have permission to access that page")
        )
        return redirect('common:index')


class CandidateUserMixin(BaseUserMixin):
    def test_func(self):
        return self.request.user.is_candidate == True


class CompanyUserMixin(BaseUserMixin):
    def test_func(self):
        return self.request.user.is_company == True

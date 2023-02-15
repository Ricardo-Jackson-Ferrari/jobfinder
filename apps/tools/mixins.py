from typing import Any, Dict

from django.forms import BaseModelForm
from django.http import Http404, HttpRequest, JsonResponse
from django.utils.translation import gettext_lazy as _


class InstanceModelUserMixin:
    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.model(user=self.request.user)
        return kwargs


class FormJsonResponseMixin:
    def form_valid(self, form: BaseModelForm) -> JsonResponse:
        self.object = form.save()
        return JsonResponse(
            status=201,
            data={
                'status_code': 201,
                'message': self.success_msg,
            },
        )

    def form_invalid(self, form: BaseModelForm) -> JsonResponse:
        return JsonResponse(
            status=400,
            data={
                'message': self.fail_msg,
                'errors': form.errors,
                'status_code': 400,
            },
        )


class ListJsonResponseMixin:
    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        super().get(self, request, *args, **kwargs)
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, 'exists'
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _('Empty list and “%(class_name)s.allow_empty” is False.')
                    % {
                        'class_name': self.__class__.__name__,
                    }
                )
        ctx = self.get_context_data()
        data = list(ctx['address_list'].values())
        return JsonResponse(data, safe=False)

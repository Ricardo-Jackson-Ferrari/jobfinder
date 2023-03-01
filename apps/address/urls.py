from django.urls import path

from . import views

app_name = 'address'

urlpatterns = [
    path(
        'api/',
        views.AddressApiView.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
        name='api_list',
    ),
    path(
        'api/<int:pk>/',
        views.AddressApiView.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
        name='api_detail',
    ),
]

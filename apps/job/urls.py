from django.urls import path

from . import views

app_name = 'job'

urlpatterns = [
    path('search/', views.JobListView.as_view(), name='search'),
    path(
        'detail/<str:title>/<int:pk>/',
        views.JobDetailView.as_view(),
        name='detail',
    ),
    path(
        'api/',
        views.JobApiView.as_view(
            {
                'get': 'list',
                'post': 'create',
            }
        ),
        name='api_list',
    ),
    path(
        'api/<int:pk>/',
        views.JobApiView.as_view(
            {
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
        name='api_detail',
    ),
    path(
        'api/candidate/application/',
        views.CandidateApplicationListAPIView.as_view(),
        name='application_api_list',
    ),
    path(
        'api/<int:pk>/application/',
        views.JobApplicationListAPIView.as_view(),
        name='job_application_api_list',
    ),
    path(
        'api/application/<int:pk>/',
        views.JobApplicationPatchView.as_view(),
        name='job_application_api_detail',
    ),
]

from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path(
        'signup/',
        views.RegisterView.as_view(),
        name='signup',
    ),
    path(
        'signup/candidate/',
        views.RegisterCandidateView.as_view(),
        name='candidate_signup',
    ),
    path(
        'signup/company/',
        views.RegisterCompanyView.as_view(),
        name='company_signup',
    ),
    path(
        'recovery/',
        views.RecoveryView.as_view(),
        name='recovery',
    ),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

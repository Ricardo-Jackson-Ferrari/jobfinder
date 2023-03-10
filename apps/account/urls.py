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
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path(
        'recovery/',
        views.RecoveryView.as_view(),
        name='recovery',
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetView.as_view(),
        name='password_reset_confirm',
    ),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path(
        'company/profile_update/',
        views.ProfileCompanyUpdateView.as_view(),
        name='profile_company_update',
    ),
    path(
        'company/address/',
        views.AddressManageView.as_view(),
        name='company_address',
    ),
    path(
        'company/job/',
        views.JobManageView.as_view(),
        name='company_job',
    ),
    path(
        'candidate/profile_update/',
        views.ProfileCandidateUpdateView.as_view(),
        name='profile_candidate_update',
    ),
    path(
        'candidate/applications/',
        views.JobApplicationManageView.as_view(),
        name='candidate_application',
    ),
    path(
        'company/job/<int:pk>/',
        views.JobDetailView.as_view(),
        name='company_job_detail',
    ),
    path(
        'company/<str:title>/<int:pk>/',
        views.ProfileView.as_view(),
        name='profile_company',
    ),
]

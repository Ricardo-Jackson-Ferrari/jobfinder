from django.urls import path

from . import views

app_name = 'address'

urlpatterns = [
    path('create/', views.CreateAddressView.as_view(), name='create'),
    path('list/', views.ListAddressView.as_view(), name='list'),
    path('update/<int:pk>/', views.UpdateAddressView.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeleteAddressView.as_view(), name='delete'),
]

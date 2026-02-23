from django.urls import path
from . import views

app_name = 'referrals'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('referrals/', views.referrals, name='referrals'),
    path('settings/', views.settings, name='settings'),
]

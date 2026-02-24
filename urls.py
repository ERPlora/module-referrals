from django.urls import path
from . import views

app_name = 'referrals'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Referral
    path('referrals/', views.referrals_list, name='referrals_list'),
    path('referrals/add/', views.referral_add, name='referral_add'),
    path('referrals/<uuid:pk>/edit/', views.referral_edit, name='referral_edit'),
    path('referrals/<uuid:pk>/delete/', views.referral_delete, name='referral_delete'),
    path('referrals/bulk/', views.referrals_bulk_action, name='referrals_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]

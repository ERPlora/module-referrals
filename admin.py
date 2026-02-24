from django.contrib import admin

from .models import Referral

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer_name', 'referrer_email', 'referred_name', 'referred_email', 'referral_code', 'created_at']
    search_fields = ['referrer_name', 'referrer_email', 'referred_name', 'referred_email']
    readonly_fields = ['created_at', 'updated_at']


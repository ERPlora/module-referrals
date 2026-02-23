from django.contrib import admin

from .models import Referral

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer_name', 'referrer_email', 'referred_name', 'referred_email', 'referral_code']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


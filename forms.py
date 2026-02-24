from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Referral

class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referral
        fields = ['referrer_name', 'referrer_email', 'referred_name', 'referred_email', 'referral_code', 'status', 'reward_given', 'notes']
        widgets = {
            'referrer_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'referrer_email': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'email'}),
            'referred_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'referred_email': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'email'}),
            'referral_code': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'reward_given': forms.CheckboxInput(attrs={'class': 'toggle'}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
        }


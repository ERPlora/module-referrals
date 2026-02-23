from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

REF_STATUS = [
    ('pending', _('Pending')),
    ('converted', _('Converted')),
    ('rewarded', _('Rewarded')),
    ('expired', _('Expired')),
]

class Referral(HubBaseModel):
    referrer_name = models.CharField(max_length=255, verbose_name=_('Referrer Name'))
    referrer_email = models.EmailField(blank=True, verbose_name=_('Referrer Email'))
    referred_name = models.CharField(max_length=255, verbose_name=_('Referred Name'))
    referred_email = models.EmailField(blank=True, verbose_name=_('Referred Email'))
    referral_code = models.CharField(max_length=50, blank=True, verbose_name=_('Referral Code'))
    status = models.CharField(max_length=20, default='pending', choices=REF_STATUS, verbose_name=_('Status'))
    reward_given = models.BooleanField(default=False, verbose_name=_('Reward Given'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta(HubBaseModel.Meta):
        db_table = 'referrals_referral'

    def __str__(self):
        return str(self.id)


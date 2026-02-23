    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'referrals'
    MODULE_NAME = _('Referral Program')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'share-social-outline'
    MODULE_DESCRIPTION = _('Customer referral tracking and reward management')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'marketing'

    MENU = {
        'label': _('Referral Program'),
        'icon': 'share-social-outline',
        'order': 61,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Referrals'), 'icon': 'share-social-outline', 'id': 'referrals'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'referrals.view_referral',
'referrals.add_referral',
'referrals.change_referral',
'referrals.manage_settings',
    ]

"""
Referral Program Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('referrals', 'dashboard')
@htmx_view('referrals/pages/dashboard.html', 'referrals/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('referrals', 'referrals')
@htmx_view('referrals/pages/referrals.html', 'referrals/partials/referrals_content.html')
def referrals(request):
    """Referrals view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('referrals', 'settings')
@htmx_view('referrals/pages/settings.html', 'referrals/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}


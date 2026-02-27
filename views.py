"""
Referral Program Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import Referral

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('referrals', 'dashboard')
@htmx_view('referrals/pages/index.html', 'referrals/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_referrals': Referral.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# Referral
# ======================================================================

REFERRAL_SORT_FIELDS = {
    'status': 'status',
    'reward_given': 'reward_given',
    'referrer_name': 'referrer_name',
    'referrer_email': 'referrer_email',
    'referred_name': 'referred_name',
    'referred_email': 'referred_email',
    'created_at': 'created_at',
}

def _build_referrals_context(hub_id, per_page=10):
    qs = Referral.objects.filter(hub_id=hub_id, is_deleted=False).order_by('status')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'referrals': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'status',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_referrals_list(request, hub_id, per_page=10):
    ctx = _build_referrals_context(hub_id, per_page)
    return django_render(request, 'referrals/partials/referrals_list.html', ctx)

@login_required
@with_module_nav('referrals', 'referrals')
@htmx_view('referrals/pages/referrals.html', 'referrals/partials/referrals_content.html')
def referrals_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'status')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Referral.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(referrer_name__icontains=search_query) | Q(referrer_email__icontains=search_query) | Q(referred_name__icontains=search_query) | Q(referred_email__icontains=search_query))

    order_by = REFERRAL_SORT_FIELDS.get(sort_field, 'status')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['status', 'reward_given', 'referrer_name', 'referrer_email', 'referred_name', 'referred_email']
        headers = ['Status', 'Reward Given', 'Referrer Name', 'Referrer Email', 'Referred Name', 'Referred Email']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='referrals.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='referrals.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'referrals/partials/referrals_list.html', {
            'referrals': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'referrals': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def referral_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        referrer_name = request.POST.get('referrer_name', '').strip()
        referrer_email = request.POST.get('referrer_email', '').strip()
        referred_name = request.POST.get('referred_name', '').strip()
        referred_email = request.POST.get('referred_email', '').strip()
        referral_code = request.POST.get('referral_code', '').strip()
        status = request.POST.get('status', '').strip()
        reward_given = request.POST.get('reward_given') == 'on'
        notes = request.POST.get('notes', '').strip()
        obj = Referral(hub_id=hub_id)
        obj.referrer_name = referrer_name
        obj.referrer_email = referrer_email
        obj.referred_name = referred_name
        obj.referred_email = referred_email
        obj.referral_code = referral_code
        obj.status = status
        obj.reward_given = reward_given
        obj.notes = notes
        obj.save()
        return _render_referrals_list(request, hub_id)
    return django_render(request, 'referrals/partials/panel_referral_add.html', {})

@login_required
def referral_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Referral, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.referrer_name = request.POST.get('referrer_name', '').strip()
        obj.referrer_email = request.POST.get('referrer_email', '').strip()
        obj.referred_name = request.POST.get('referred_name', '').strip()
        obj.referred_email = request.POST.get('referred_email', '').strip()
        obj.referral_code = request.POST.get('referral_code', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.reward_given = request.POST.get('reward_given') == 'on'
        obj.notes = request.POST.get('notes', '').strip()
        obj.save()
        return _render_referrals_list(request, hub_id)
    return django_render(request, 'referrals/partials/panel_referral_edit.html', {'obj': obj})

@login_required
@require_POST
def referral_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Referral, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_referrals_list(request, hub_id)

@login_required
@require_POST
def referrals_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Referral.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_referrals_list(request, hub_id)


@login_required
@permission_required('referrals.manage_settings')
@with_module_nav('referrals', 'settings')
@htmx_view('referrals/pages/settings.html', 'referrals/partials/settings_content.html')
def settings_view(request):
    return {}


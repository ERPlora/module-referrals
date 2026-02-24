"""Tests for referrals views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('referrals:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('referrals:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('referrals:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestReferralViews:
    """Referral view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('referrals:referrals_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('referrals:referrals_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('referrals:referrals_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('referrals:referrals_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('referrals:referrals_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('referrals:referrals_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('referrals:referral_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('referrals:referral_add')
        data = {
            'referrer_name': 'New Referrer Name',
            'referrer_email': 'test@example.com',
            'referred_name': 'New Referred Name',
            'referred_email': 'test@example.com',
            'referral_code': 'New Referral Code',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, referral):
        """Test edit form loads."""
        url = reverse('referrals:referral_edit', args=[referral.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, referral):
        """Test editing via POST."""
        url = reverse('referrals:referral_edit', args=[referral.pk])
        data = {
            'referrer_name': 'Updated Referrer Name',
            'referrer_email': 'test@example.com',
            'referred_name': 'Updated Referred Name',
            'referred_email': 'test@example.com',
            'referral_code': 'Updated Referral Code',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, referral):
        """Test soft delete via POST."""
        url = reverse('referrals:referral_delete', args=[referral.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        referral.refresh_from_db()
        assert referral.is_deleted is True

    def test_bulk_delete(self, auth_client, referral):
        """Test bulk delete."""
        url = reverse('referrals:referrals_bulk_action')
        response = auth_client.post(url, {'ids': str(referral.pk), 'action': 'delete'})
        assert response.status_code == 200
        referral.refresh_from_db()
        assert referral.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('referrals:referrals_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('referrals:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('referrals:settings')
        response = client.get(url)
        assert response.status_code == 302


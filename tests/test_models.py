"""Tests for referrals models."""
import pytest
from django.utils import timezone

from referrals.models import Referral


@pytest.mark.django_db
class TestReferral:
    """Referral model tests."""

    def test_create(self, referral):
        """Test Referral creation."""
        assert referral.pk is not None
        assert referral.is_deleted is False

    def test_soft_delete(self, referral):
        """Test soft delete."""
        pk = referral.pk
        referral.is_deleted = True
        referral.deleted_at = timezone.now()
        referral.save()
        assert not Referral.objects.filter(pk=pk).exists()
        assert Referral.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, referral):
        """Test default queryset excludes deleted."""
        referral.is_deleted = True
        referral.deleted_at = timezone.now()
        referral.save()
        assert Referral.objects.filter(hub_id=hub_id).count() == 0



import secrets
from datetime import datetime, timezone as dt_timezone

from django.utils import timezone
from django.db import transaction
from rest_framework import authentication, exceptions
from rest_framework.exceptions import Throttled

from accounts.models import APIKey, UsageLog

DAILY_TAGGING_LIMIT = 15


def get_utc_midnight():
    """Get today's UTC midnight timestamp."""
    now = datetime.now(dt_timezone.utc)
    midnight = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=dt_timezone.utc)
    return midnight


def should_reset_daily_count(user_reset_at):
    """Check if daily count should be reset (UTC midnight has passed)."""
    if user_reset_at is None:
        return True
    today_midnight = get_utc_midnight()
    return user_reset_at < today_midnight


class APIKeyAuthentication(authentication.BaseAuthentication):
    """Authenticate using API Key (for API consumption only, not UI auth)."""
    header = "Api-Key"
    keyword = "Api-Key"

    def authenticate(self, request):
        raw_key = self._get_raw_key(request)

        api_key = self._get_api_key(raw_key)
        if api_key is None:
            raise exceptions.AuthenticationFailed("Invalid API key.")

        user = api_key.user
        if not user.is_active:
            raise exceptions.AuthenticationFailed("User inactive or deleted.")

        self._enforce_daily_limit(user)

        api_key.last_used_at = timezone.now()
        api_key.save(update_fields=["last_used_at"])

        return user, None

    def authenticate_header(self, request):
        return self.keyword

    def _get_raw_key(self, request) -> str:
        # Prefer Authorization: Api-Key <token> if provided
        auth_header = request.headers.get("Authorization") or request.META.get("HTTP_AUTHORIZATION")
        if auth_header:
            parts = auth_header.split(" ", 1)
            if len(parts) != 2 or parts[0] != self.keyword:
                raise exceptions.AuthenticationFailed("Invalid API key.")
            token = parts[1]
        else:
            token = request.headers.get(self.header) or request.META.get("HTTP_API_KEY")

        if token is None:
            raise exceptions.AuthenticationFailed("API key required.")

        token = token.strip()
        if not token:
            raise exceptions.AuthenticationFailed("API key required.")

        return token

    def _get_api_key(self, raw_key: str) -> APIKey | None:
        if not raw_key:
            return None

        prefix = raw_key[:16]
        try:
            stored = APIKey.objects.select_related("user").get(prefix=prefix)
        except APIKey.DoesNotExist:
            return None

        if not secrets.compare_digest(stored.key, self._hash_key(raw_key)):
            return None

        return stored

    def _hash_key(self, raw_key: str) -> str:
        from accounts.services.api_key import hash_key
        return hash_key(raw_key)

    def _enforce_daily_limit(self, user):
        """Enforce daily 15-request limit per user (UTC midnight reset)."""
        now = timezone.now()

        with transaction.atomic():
            locked_user = (
                type(user)
                .objects.select_for_update()
                .get(pk=user.pk)
            )

            # Check if we need to reset the daily count
            today_midnight = get_utc_midnight()
            if should_reset_daily_count(locked_user.daily_count_reset_at):
                locked_user.daily_tagging_count = 0
                locked_user.daily_count_reset_at = today_midnight
                locked_user.save(update_fields=["daily_tagging_count", "daily_count_reset_at"])

            # Check if limit would be exceeded
            if locked_user.daily_tagging_count >= DAILY_TAGGING_LIMIT:
                raise Throttled(detail="Daily tagging limit reached (15 requests per day).")

            # Increment count for this request
            locked_user.daily_tagging_count += 1
            locked_user.save(update_fields=["daily_tagging_count"])


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    """
    Session authentication without CSRF checks.
    Use this for API endpoints that need session auth but are called from SPA.
    """

    def enforce_csrf(self, request):
        # Skip CSRF check for session authentication
        return


class DailyLimitChecker:
    """Helper to check and enforce daily tagging limit for session-authenticated users."""

    @staticmethod
    def check_and_increment(user):
        """Check if user has remaining daily quota and increment count.
        
        Raises Throttled if limit exceeded.
        Returns the updated count.
        """
        with transaction.atomic():
            locked_user = (
                type(user)
                .objects.select_for_update()
                .get(pk=user.pk)
            )

            # Check if we need to reset the daily count
            today_midnight = get_utc_midnight()
            if should_reset_daily_count(locked_user.daily_count_reset_at):
                locked_user.daily_tagging_count = 0
                locked_user.daily_count_reset_at = today_midnight
                locked_user.save(update_fields=["daily_tagging_count", "daily_count_reset_at"])

            # Check if limit would be exceeded
            if locked_user.daily_tagging_count >= DAILY_TAGGING_LIMIT:
                raise Throttled(detail="Daily tagging limit reached (15 requests per day).")

            # Increment count for this request
            locked_user.daily_tagging_count += 1
            locked_user.save(update_fields=["daily_tagging_count"])

            return locked_user.daily_tagging_count

    @staticmethod
    def get_usage_info(user):
        """Get today's usage info for a user.
        
        Returns: {"used": int, "limit": int, "remaining": int}
        """
        with transaction.atomic():
            locked_user = (
                type(user)
                .objects.select_for_update()
                .get(pk=user.pk)
            )

            # Check if we need to reset the daily count
            today_midnight = get_utc_midnight()
            if should_reset_daily_count(locked_user.daily_count_reset_at):
                locked_user.daily_tagging_count = 0
                locked_user.daily_count_reset_at = today_midnight
                locked_user.save(update_fields=["daily_tagging_count", "daily_count_reset_at"])

            used = locked_user.daily_tagging_count
            return {
                "used": used,
                "limit": DAILY_TAGGING_LIMIT,
                "remaining": max(0, DAILY_TAGGING_LIMIT - used),
            }

import secrets
from datetime import timedelta

from django.utils import timezone
from rest_framework import authentication, exceptions

from accounts.models import APIKey, UsageLog


class APIKeyAuthentication(authentication.BaseAuthentication):
    header = "Api-Key"

    def authenticate(self, request):
        raw_key = request.headers.get(self.header) or request.META.get("HTTP_API_KEY")
        if not raw_key:
            return None

        api_key = self._get_api_key(raw_key.strip())
        if api_key is None:
            raise exceptions.AuthenticationFailed("Invalid API key.")

        user = api_key.user
        if not user.is_active:
            raise exceptions.AuthenticationFailed("User inactive or deleted.")

        self._enforce_quota(user)

        api_key.last_used_at = timezone.now()
        api_key.save(update_fields=["last_used_at"])

        return user, None

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

    def _enforce_quota(self, user):
        now = timezone.now()
        window_start = user.quota_reset_at or now - timedelta(days=7)

        if user.quota_reset_at is None or user.quota_reset_at <= now - timedelta(days=7):
            user.quota_reset_at = now
            user.save(update_fields=["quota_reset_at"])

        usage_count = UsageLog.objects.filter(user=user, used_at__gte=window_start).count()
        if usage_count >= user.weekly_quota:
            raise exceptions.AuthenticationFailed("API quota exceeded.")


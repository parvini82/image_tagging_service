import secrets
from datetime import timedelta

from django.utils import timezone
from django.db import transaction
from rest_framework import authentication, exceptions
from rest_framework.exceptions import Throttled

from accounts.models import APIKey, UsageLog


class APIKeyAuthentication(authentication.BaseAuthentication):
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

        self._enforce_quota(user)

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

    def _enforce_quota(self, user):
        now = timezone.now()
        seven_days_ago = now - timedelta(days=7)

        # Ensure quota checks and reset are atomic to avoid concurrent overrun.
        with transaction.atomic():
            locked_user = (
                type(user)
                .objects.select_for_update()
                .get(pk=user.pk)
            )

            reset_needed = locked_user.quota_reset_at is None or locked_user.quota_reset_at <= seven_days_ago
            if reset_needed:
                locked_user.quota_reset_at = now
                locked_user.save(update_fields=["quota_reset_at"])

            window_start = locked_user.quota_reset_at

            usage_count = UsageLog.objects.filter(user=locked_user, used_at__gte=window_start).count()

            # Enforce quota strictly before logging the request.
            if locked_user.weekly_quota == 0 or (usage_count + 1) > locked_user.weekly_quota:
                # Use DRF Throttled to return HTTP 429 while keeping auth semantics clean.
                raise Throttled(detail="API quota exceeded.")


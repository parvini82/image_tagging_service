from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from accounts.authentication import (
    APIKeyAuthentication,
    CsrfExemptSessionAuthentication,
    DailyLimitChecker,
)
from accounts.models import UsageLog
from .services.tagger import generate_tags


class ImageTagView(APIView):
    """Tag an image using the LangGraph pipeline.
    
    Supports two authentication methods:
    1. Session authentication (from UI/playground) - no API key needed
    2. API key authentication (from external API) - API key required
    """
    authentication_classes = [CsrfExemptSessionAuthentication, APIKeyAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = []  # Rate limiting via DailyLimitChecker

    def post(self, request):
        image_url = request.data.get("image_url")
        success = bool(image_url)

        if not image_url:
            self._log_usage(request.user, request.path, success=False)
            return Response(
                {"detail": "image_url is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check and enforce daily limit (only for successful requests)
        # This increments the count if limit not exceeded, otherwise raises Throttled
        try:
            DailyLimitChecker.check_and_increment(request.user)
        except Exception as e:
            # Log the failed attempt but don't count it
            self._log_usage(request.user, request.path, success=False)
            raise  # Re-raise the Throttled exception

        # Call the LangGraph tagging service
        tags = generate_tags(image_url)

        # Log successful usage
        self._log_usage(request.user, request.path, success=True)

        return Response(
            {"image_url": image_url, "tags": tags},
            status=status.HTTP_200_OK
        )

    def _log_usage(self, user, endpoint: str, success: bool):
        """Log usage for analytics."""
        UsageLog.objects.create(
            user=user,
            used_at=timezone.now(),
            endpoint=endpoint,
            success=success
        )

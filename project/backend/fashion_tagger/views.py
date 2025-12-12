from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import APIKeyAuthentication
from accounts.models import UsageLog


class ImageTagView(APIView):
    authentication_classes = [APIKeyAuthentication]
    throttle_classes = []  # DRF throttling disabled; quota enforced in APIKeyAuthentication

    def post(self, request):
        image_url = request.data.get("image_url")
        success = bool(image_url)

        self._log_usage(request.user, request.path, success)

        if not image_url:
            return Response({"detail": "image_url is required."}, status=status.HTTP_400_BAD_REQUEST)

        dummy_tags = {"category": "tshirt", "color": "red", "material": "cotton"}
        return Response({"image_url": image_url, "tags": dummy_tags}, status=status.HTTP_200_OK)

    def _log_usage(self, user, endpoint: str, success: bool):
        UsageLog.objects.create(user=user, used_at=timezone.now(), endpoint=endpoint, success=success)

from django.contrib.auth import login, logout
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, APIKey
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    MaskedAPIKeySerializer,
    APIKeyCreateSerializer,
)
from .services.api_key import generate_api_key


class RegisterView(APIView):
    """Register a new user."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Login user and set session cookie."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            login(request, user)
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Logout user and clear session."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK
        )


class MeView(APIView):
    """Get current authenticated user info."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class APIKeyViewSet(viewsets.ModelViewSet):
    """Manage API keys for the authenticated user."""
    serializer_class = MaskedAPIKeySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return APIKeyCreateSerializer
        return MaskedAPIKeySerializer

    def create(self, request, *args, **kwargs):
        """Generate a new API key for the user."""
        raw_key, api_key_obj = generate_api_key(request.user)
        
        # Store raw key temporarily for response
        api_key_obj._raw_key = raw_key
        
        serializer = self.get_serializer(api_key_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """Revoke (delete) an API key."""
        api_key = self.get_object()
        api_key.delete()
        return Response(
            {"detail": "API key revoked successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

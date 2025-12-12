"""
Example: Updated Django views.py with LangGraph integration.

Shows MINIMAL changes to existing endpoint.
Only changed: one import + one function call
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# ← NEW IMPORT: LangGraph service layer
from .services.tagger import generate_tags


class TagImageView(APIView):
    """
    POST /api/v1/tag/ - Tag fashion product image
    
    Request:
        {
            "image_url": "https://example.com/product.jpg"
        }
    
    Response:
        {
            "image_url": "https://example.com/product.jpg",
            "tags": {
                "category": "t-shirt",
                "color": "blue",
                "material": "cotton"
            }
        }
    
    Status Codes:
        - 200: Success
        - 400: Invalid input
        - 500: Server error (auth/rate limit still applied at outer level)
    """
    
    # Keep existing auth/permissions unchanged
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Process image tagging request"""
        
        # Validate input (unchanged)
        if not request.data.get("image_url"):
            return Response(
                {"error": "image_url is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_url = request.data.get("image_url")
        
        # Optional: allow mode selection via query param
        mode = request.query_params.get("mode", "fast")
        valid_modes = ["fast", "reasoning", "advanced_reasoning"]
        if mode not in valid_modes:
            mode = "fast"
        
        # ← THIS IS THE ONLY CHANGED LINE:
        # OLD: tags = {"category": "shirt", "color": "blue", "material": "cotton"}
        # NEW:
        try:
            tags = generate_tags(image_url, mode=mode)
        except Exception as e:
            # Graceful fallback (generate_tags already handles most errors internally)
            return Response(
                {"error": "Failed to generate tags"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Return response with unchanged shape
        return Response({
            "image_url": image_url,
            "tags": tags
        }, status=status.HTTP_200_OK)


# === BEFORE (OLD VERSION) ===
# class TagImageView(APIView):
#     permission_classes = [IsAuthenticated]
#     
#     def post(self, request):
#         if not request.data.get("image_url"):
#             return Response(
#                 {"error": "image_url is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         
#         image_url = request.data.get("image_url")
#         
#         # FAKE TAGS - REPLACED
#         tags = {
#             "category": "shirt",
#             "color": "blue",
#             "material": "cotton"
#         }
#         
#         return Response({
#             "image_url": image_url,
#             "tags": tags
#         })


# === ALTERNATIVE: Simple Sync View (without mode param) ===
class SimpleTagImageView(APIView):
    """Minimal version - no mode selection"""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        image_url = request.data.get("image_url")
        
        if not image_url:
            return Response(
                {"error": "image_url is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # One line: fetch + process through LangGraph
        tags = generate_tags(image_url)  # uses default "fast" mode
        
        return Response({
            "image_url": image_url,
            "tags": tags
        })


# === ALTERNATIVE: With Caching ===
from django.core.cache import cache
from django.views.decorators.cache import cache_page


class CachedTagImageView(APIView):
    """Version with per-URL caching (24 hours)"""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        image_url = request.data.get("image_url")
        
        if not image_url:
            return Response(
                {"error": "image_url is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check cache first
        cache_key = f"image_tags:{image_url}"
        cached_tags = cache.get(cache_key)
        
        if cached_tags is not None:
            return Response({
                "image_url": image_url,
                "tags": cached_tags,
                "cached": True  # indicator for debugging
            })
        
        # Generate fresh tags
        tags = generate_tags(image_url)
        
        # Cache for 24 hours
        cache.set(cache_key, tags, timeout=86400)
        
        return Response({
            "image_url": image_url,
            "tags": tags,
            "cached": False
        })


# === ALTERNATIVE: With Request Timeout Handling ===
import asyncio


class RobustTagImageView(APIView):
    """Version with explicit timeout + fallback"""
    
    permission_classes = [IsAuthenticated]
    REQUEST_TIMEOUT = 45  # seconds
    
    def post(self, request):
        image_url = request.data.get("image_url")
        
        if not image_url:
            return Response(
                {"error": "image_url is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Call with explicit timeout handling
            tags = generate_tags(image_url, mode="fast")
            
            if tags is None:
                # Should not happen, but failsafe
                tags = {
                    "category": None,
                    "color": None,
                    "material": None
                }
        
        except TimeoutError:
            return Response(
                {"error": "Image processing timeout - please try again"},
                status=status.HTTP_504_GATEWAY_TIMEOUT
            )
        
        except ValueError as e:
            return Response(
                {"error": f"Invalid input: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return Response(
                {"error": "Server error during tag generation"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({
            "image_url": image_url,
            "tags": tags
        })

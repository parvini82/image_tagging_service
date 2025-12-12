# LangGraph Integration Guide for Django Fashion Tagger

**Project:** image_tagging_service → Django Backend  
**Date:** December 2025  
**Status:** Production-Ready Integration

---

## Overview

This guide integrates your LangGraph-based image tagging pipeline into an existing Django REST Framework backend without modifying:
- Authentication (API Key auth)
- Rate limiting/quota enforcement
- API response shape
- Project structure
- Any existing endpoints

### Architecture

```
POST /api/v1/tag/ (existing Django endpoint)
  ↓
views.py (calls generate_tags)
  ↓
services/tagger.py (NEW service layer)
  ↓
LangGraph Pipeline
  ├─ image_to_tags_node (vision model → entities)
  ├─ serpapi_search_node (conditional, mode-dependent)
  ├─ translate_tags_node (LLM translation)
  └─ merge_results_node (normalization)
  ↓
normalize output
  ↓
{ "category": str|null, "color": str|null, "material": str|null }
  ↓
Django API response (unchanged)
```

---

## Step 1: Prepare Project Structure

Ensure your Django backend has this layout:

```
fashion_tagger/
├── models.py
├── views.py
├── serializers.py
├── services/
│   ├── __init__.py
│   └── tagger.py           # ← CREATE THIS (provided below)
├── migrations/
└── urls.py
```

---

## Step 2: Copy LangGraph Files to Django Backend

Move your entire LangGraph service as a reusable package inside Django:

```bash
# Create the LangGraph service module
mkdir -p fashion_tagger/services/langgraph_service

# Copy all LangGraph files
cp image_to_tags.py fashion_tagger/services/langgraph_service/
cp merge_results.py fashion_tagger/services/langgraph_service/
cp langgraph_service.py fashion_tagger/services/langgraph_service/
cp serpapi_search.py fashion_tagger/services/langgraph_service/
cp config.py fashion_tagger/services/langgraph_service/
cp init.py fashion_tagger/services/langgraph_service/__init__.py
cp model_client.py fashion_tagger/services/langgraph_service/
cp translate_tags.py fashion_tagger/services/langgraph_service/
```

Result:
```
fashion_tagger/services/
├── __init__.py
├── tagger.py                      # NEW: integration layer
└── langgraph_service/             # NEW: LangGraph subpackage
    ├── __init__.py
    ├── config.py
    ├── model_client.py
    ├── image_to_tags.py
    ├── translate_tags.py
    ├── serpapi_search.py
    ├── merge_results.py
    └── langgraph_service.py
```

---

## Step 3: Install Dependencies

Add to your `requirements.txt`:

```
langgraph>=0.0.50
langchain>=0.0.300
requests>=2.31.0
python-dotenv>=1.0.0
openrouter-python  # if using OpenRouter SDK
```

Install:
```bash
pip install -r requirements.txt
```

---

## Step 4: Environment Configuration

Ensure these environment variables are set (in `.env` or production config):

```env
# OpenRouter API
OPENROUTER_API_KEY=your_key_here
OPENROUTER_SITE_URL=https://your-domain.com
OPENROUTER_SITE_TITLE=Your App Name

# Optional: SerpAPI (for advanced_reasoning mode)
SERPAPI_API_KEY=your_key_here

# Request timeout
REQUEST_TIMEOUT=60
```

Your `config.py` will auto-load these with `load_dotenv()`.

---

## Step 5: Create tagger.py Service Layer

**File:** `fashion_tagger/services/tagger.py`

This is the **ONLY** new file you need to create. It:
1. Wraps the LangGraph pipeline
2. Normalizes output to Django schema
3. Handles errors gracefully
4. Provides logging for monitoring

See the attached `tagger.py` file for full implementation.

**Key function:**
```python
def generate_tags(image_url: str, mode: str = "fast") -> Dict[str, Optional[str]]:
    """
    Generate fashion product tags from image URL.
    
    Returns:
        {
            "category": str | None,
            "color": str | None,
            "material": str | None
        }
    """
```

---

## Step 6: Update Django View

**File:** `fashion_tagger/views.py`

Change only the tag generation line:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.tagger import generate_tags  # ← IMPORT


class TagImageView(APIView):
    """POST /api/v1/tag/ - Tag fashion image"""
    
    def post(self, request):
        serializer = TagImageSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        image_url = serializer.validated_data.get("image_url")
        
        # ← REPLACE FAKE TAGS WITH REAL ONES
        tags = generate_tags(image_url)  # ← THIS LINE CHANGED
        
        return Response({
            "image_url": image_url,
            "tags": tags
        })
```

**Before:**
```python
tags = {
    "category": "shirt",      # fake
    "color": "blue",           # fake
    "material": "cotton"       # fake
}
```

**After:**
```python
tags = generate_tags(image_url)  # real, from LangGraph
```

---

## Step 7: Optional - Configure Mode per Request

The `generate_tags()` function accepts a `mode` parameter:

```python
# Fast mode (default) - no SerpAPI
tags = generate_tags(image_url, mode="fast")

# With vision reasoning
tags = generate_tags(image_url, mode="reasoning")

# With vision + SerpAPI search
tags = generate_tags(image_url, mode="advanced_reasoning")
```

To add mode selection to API, update the view:

```python
class TagImageView(APIView):
    def post(self, request):
        serializer = TagImageSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        image_url = serializer.validated_data.get("image_url")
        mode = request.query_params.get("mode", "fast")  # ← Optional mode param
        
        tags = generate_tags(image_url, mode=mode)
        
        return Response({
            "image_url": image_url,
            "tags": tags
        })
```

---

## Step 8: Logging Configuration

Add to your Django `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'fashion_tagger.services.tagger': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```

This enables monitoring of:
- Successful tag generation
- Error cases
- Failed image fetches
- LangGraph failures

---

## Step 9: Testing

### Unit Test Example

```python
# fashion_tagger/tests.py

from django.test import TestCase
from services.tagger import generate_tags


class TaggerServiceTest(TestCase):
    def test_generate_tags_with_valid_url(self):
        """Test successful tag generation"""
        image_url = "https://example.com/product.jpg"
        tags = generate_tags(image_url)
        
        # Assert structure
        self.assertIn("category", tags)
        self.assertIn("color", tags)
        self.assertIn("material", tags)
        
        # All values should be str or None
        for value in tags.values():
            self.assertTrue(value is None or isinstance(value, str))
    
    def test_generate_tags_with_invalid_url(self):
        """Test graceful failure with invalid URL"""
        tags = generate_tags(None)
        
        # Should return safe defaults
        self.assertEqual(tags, {
            "category": None,
            "color": None,
            "material": None
        })
```

### Integration Test

```bash
# Test the full endpoint
curl -X POST http://localhost:8000/api/v1/tag/ \
  -H "Content-Type: application/json" \
  -H "Authorization: ApiKey your_key" \
  -d '{"image_url": "https://example.com/product.jpg"}'

# Response:
{
  "image_url": "https://example.com/product.jpg",
  "tags": {
    "category": "t-shirt",
    "color": "blue",
    "material": "cotton"
  }
}
```

---

## Step 10: Production Deployment Checklist

- [ ] All `.env` variables set in production (OpenRouter API key, etc.)
- [ ] LangGraph service installed (`pip install langgraph`)
- [ ] `fashion_tagger/services/langgraph_service/` directory present
- [ ] `tagger.py` created in `fashion_tagger/services/`
- [ ] Django `views.py` updated to call `generate_tags()`
- [ ] Logging configured in `settings.py`
- [ ] Rate limiting/auth unchanged
- [ ] API response shape unchanged (endpoint still returns same structure)
- [ ] Tests passing
- [ ] Error logs monitored (e.g., OpenRouter API failures, image fetch failures)

---

## Troubleshooting

### ImportError: No module named 'langgraph'
**Solution:** Run `pip install langgraph`

### OpenRouterError: OPENROUTER_API_KEY is empty
**Solution:** Ensure `OPENROUTER_API_KEY` is set in `.env` or environment

### Error: LangGraph service not available
**Solution:** Ensure `langgraph_service/` directory is in `fashion_tagger/services/`

### Tags return all None values
**Solution:**
1. Check OpenRouter API is responding (test with manual call)
2. Check image URL is publicly accessible (LangGraph can't access internal IPs)
3. Check logs for LLM parsing errors

### Image fetch timeout
**Solution:** Increase `REQUEST_TIMEOUT` in `.env` (default: 60 seconds)

---

## Performance Considerations

### Latency
- **Fast mode:** ~2-3s (single vision model)
- **Reasoning mode:** ~3-5s (reasoning model)
- **Advanced reasoning:** ~5-8s (vision + SerpAPI + translation)

### Caching Opportunity
Consider caching tags for frequently requested images:

```python
from django.core.cache import cache

def generate_tags_with_cache(image_url: str) -> Dict[str, Optional[str]]:
    cache_key = f"tags:{image_url}"
    cached = cache.get(cache_key)
    
    if cached:
        return cached
    
    tags = generate_tags(image_url)
    cache.set(cache_key, tags, timeout=86400)  # 24 hours
    
    return tags
```

---

## Monitoring & Alerts

Watch for these error patterns in logs:

1. **OpenRouterError**: API failures → check rate limits/quota
2. **Image fetch failed**: URL not accessible → validate customer input
3. **LangGraph returned empty**: Vision model parsing failed → check image quality
4. **OPENROUTER_API_KEY is empty**: Missing configuration → check env setup

---

## API Contract (Unchanged)

Your Django endpoint contract remains identical:

**Request:**
```json
POST /api/v1/tag/
{
  "image_url": "https://example.com/product.jpg"
}
```

**Response (200 OK):**
```json
{
  "image_url": "https://example.com/product.jpg",
  "tags": {
    "category": "t-shirt",
    "color": "blue",
    "material": "cotton"
  }
}
```

**Response (400 Bad Request):**
```json
{
  "image_url": ["This field may not be blank."]
}
```

---

## Summary

✅ **What Changed:**
- Added `fashion_tagger/services/tagger.py` (new file)
- Added `fashion_tagger/services/langgraph_service/` (copied from your project)
- Updated `fashion_tagger/views.py` (one line: call `generate_tags()`)
- Added environment variables to `.env`

❌ **What Did NOT Change:**
- Authentication logic
- Rate limiting
- Quota enforcement
- API response shape
- Existing endpoints
- Project structure (except new files)

---

## Next Steps

1. Copy the `tagger.py` file to your Django project
2. Copy your LangGraph service files to `services/langgraph_service/`
3. Update `views.py` to call `generate_tags(image_url)`
4. Test with: `python manage.py test fashion_tagger.tests`
5. Deploy and monitor logs

Good luck! 🚀